import logging
import os
from copy import deepcopy

import fitsio
from astropy.io import fits
from tqdm import tqdm

from . import PACKAGEDIR
from .cupy_numpy_imports import load_image, np, xp
from .designmatrix import (
    cartesian_design_matrix,
    radial_spline_design_matrix,
    restricted_strap_design_matrix,
    spline_design_matrix,
)
from .utils import (
    _align_with_tpf,
    _package_pca_comps,
    _validate_inputs,
    get_asteroid_mask,
    get_min_image_from_filenames,
    get_sat_mask,
    get_star_mask,
    identify_bad_frames,
)
from .version import __version__

log = logging.getLogger(__name__)


class ScatteredLightBackground(object):
    """Class for working with TESS data to fit and use scattered background models.

    ScatteredLightBackground will automatically set up a reasonable background model for you. If you
    want to tweak the model, check out the `design_matrix` API.
    """

    def __init__(
        self,
        sector,
        camera,
        ccd,
        column=None,
        row=None,
        sigma_f=None,
        nknots=50,
        cutout_size=2048,
        tstart=None,
        tstop=None,
        quality=None,
        verbose=False,
        njitter=10000,
        strap_npoly=2,
    ):
        """Initialize a `ScatteredLightBackground` object either for fitting or loading a model.

        Parameters
        ----------
        sector : int
            Sector number
        camera : int
            Camera number
        ccd : int
            CCD number
        column : None or xp.ndarray
            The column numbers to evaluate the design matrix at. If None, uses all pixels.
        row : None or xp.ndarray
            The column numbers to evaluate the design matrix at. If None, uses all pixels.
        sigma_f : xp.ndarray
            The weights for each pixel in the design matrix. Default is equal weights.
        nknots : int
                Number of knots to for spline matrix
        cutout_size : int
                Size of a "cutout" of images to use. Default is 2048. Use a smaller cut out to test functionality
        """
        log.debug("Initializing `ScatteredLightBackground` Object")
        self.sector = sector
        self.camera = camera
        self.ccd = ccd
        self.verbose = verbose
        self.njitter = njitter
        self.strap_npoly = strap_npoly
        self.A1 = radial_spline_design_matrix(
            column=column,
            row=row,
            ccd=ccd,
            sigma_f=sigma_f,
            prior_mu=2,
            prior_sigma=100,
            cutout_size=cutout_size,
        ) + cartesian_design_matrix(
            column=column,
            row=row,
            ccd=ccd,
            sigma_f=sigma_f,
            prior_mu=2,
            prior_sigma=100,
            cutout_size=cutout_size,
            npoly=4,
        )
        self.A2 = (
            spline_design_matrix(
                column=column,
                row=row,
                ccd=ccd,
                sigma_f=sigma_f,
                prior_sigma=200,
                nknots=nknots,
                cutout_size=cutout_size,
            )
            + radial_spline_design_matrix(
                column=column,
                row=row,
                ccd=ccd,
                sigma_f=sigma_f,
                prior_sigma=300,
                cutout_size=cutout_size,
            )
            + restricted_strap_design_matrix(
                column=column,
                row=row,
                ccd=ccd,
                sigma_f=sigma_f,
                prior_sigma=30,
                cutout_size=cutout_size,
                npoly=self.strap_npoly,
            )
        )
        self.cutout_size = cutout_size
        if row is None:
            self.column = np.arange(self.cutout_size)
        else:
            self.column = column
        if row is None:
            self.row = np.arange(self.cutout_size)
        else:
            self.row = row
        self.row, self.column = np.atleast_1d(self.row), np.atleast_1d(self.column)
        self.weights_basic = []
        self.weights_full = []
        self.jitter = []
        self.bkg = []
        # self._average_frame = xp.zeros(self.shape)
        # self._average_frame_count = 0
        self._average_frame = xp.zeros(self.shape)
        self.tstart = tstart
        self.tstop = tstop
        self.quality = quality
        log.debug("Initialized `ScatteredLightBackground` Object")

    def update_sigma_f(self, sigma_f):
        self.A1.update_sigma_f(sigma_f)
        self.A2.update_sigma_f(sigma_f)

    def clean(self):
        """Resets the weights and average frame"""
        self.weights_basic = []
        self.weights_full = []
        # self._average_frame = xp.zeros(self.shape)
        # self._average_frame_count = 0
        self._average_frame = xp.zeros(self.shape)
        self.jitter = []
        self.bkg = []

    def __repr__(self):
        return f"ScatteredLightBackground CCD:{self.ccd} ({len(self.weights_basic)} frames)"

    def __getitem__(self, key):
        """Set indexing"""
        if self.tstart is None:
            raise ValueError("Can not slice an object with no `tstart` array.")
        attrs = [
            item
            for item in self.__dir__()
            if not item.startswith("_")
            and isinstance(getattr(self, item), (xp.ndarray, list))
            and (xp.asarray(getattr(self, item)).shape[0] == len(self.tstart))
        ]
        copy = deepcopy(self)
        for attr in attrs:
            setattr(copy, attr, np.asarray(getattr(self, attr))[key])
            if isinstance(getattr(self, attr), list):
                setattr(copy, attr, list(getattr(copy, attr)))
        return copy

    def quality_mask(self, quality_bitmask=63):
        return (self.quality.astype(int) & (8192 | quality_bitmask)) == 0

    @property
    def path(self):
        return (
            f"{PACKAGEDIR}/data/sector{self.sector:03}/camera{self.camera:02}/ccd{self.ccd:02}/"
            f"tessbackdrop_sector{self.sector}_camera{self.camera}_ccd{self.ccd}.fits"
        )

    def _build_masks(self, frame):
        """Builds a set of pixel masks for the frame, which downweight saturated pixels or pixels with stars."""
        # if frame.shape != (2048, 2048):
        #     raise ValueError("Pass a frame that is (2048, 2048)")

        if not hasattr(self, "star_mask"):
            self.star_mask = get_star_mask(frame)

        if not hasattr(self, "sat_mask"):
            self.sat_mask = get_sat_mask(frame)
        if not hasattr(self, "jitter_mask"):
            if (~self.star_mask & self.sat_mask).sum() > self.njitter:
                s = np.random.choice(
                    (~self.star_mask & self.sat_mask).sum(),
                    size=self.njitter,
                    replace=False,
                )
                l = np.asarray(np.where(~self.star_mask & self.sat_mask))
                l = l[:, s]
                self.jitter_mask = np.zeros((self.cutout_size, self.cutout_size), bool)
                self.jitter_mask[l[0], l[1]] = True
            else:
                self.jitter_mask = (~self.star_mask & self.sat_mask).copy()

        if not hasattr(self, "bkg_mask"):
            if (self.star_mask & self.sat_mask).sum() > self.njitter:
                s = np.random.choice(
                    (self.star_mask & self.sat_mask).sum(),
                    size=self.njitter,
                    replace=False,
                )
                l = np.asarray(np.where(self.star_mask & self.sat_mask))
                l = l[:, s]
                self.bkg_mask = np.zeros((self.cutout_size, self.cutout_size), bool)
                self.bkg_mask[l[0], l[1]] = True
            else:
                self.bkg_mask = (self.star_mask & self.sat_mask).copy()

        sigma_f = xp.ones(frame.shape)
        sigma_f[~self.star_mask | ~self.sat_mask] = 1e6
        self.update_sigma_f(sigma_f)
        return

    @property
    def shape(self):
        if self.column is not None:
            return (self.row.shape[0], self.column.shape[0])
        else:
            return

    def _build_asteroid_mask(self, times):
        """Creates a mask for asteroids, and increases the flux errors in those
        pixels to reduce their contribution to the model

        Parameters
        ----------
        flux_cube: xp.ndarray or list of xp.ndarray
            3D flux cube of data. Be aware that this should be a short "batch"
            of flux data (e.g. 50 frames).
        """
        #        ast_mask = _asteroid_mask(flux_cube)
        ast_mask = get_asteroid_mask(
            sector=self.sector,
            camera=self.camera,
            ccd=self.ccd,
            cutout_size=self.cutout_size,
            times=times,
        )
        sigma_f = xp.ones((self.cutout_size, self.cutout_size))
        # More than the saturation limit
        sigma_f[~self.star_mask | ~self.sat_mask] = 1e6
        # Here we downweight asteroids and other variable pixels
        # The threshold is set very high, so we don't want these contributing at all
        sigma_f[ast_mask] = 1e6
        self.update_sigma_f(sigma_f)
        return ast_mask

    def _model_basic(self, tdx):
        """Model from the first design matrix"""
        return xp.power(10, self.A1.dot(self.weights_basic[tdx])).reshape(self.shape)

    def _model_full(self, tdx):
        """Model from the second design matrix"""
        return self.A2.dot(self.weights_full[tdx]).reshape(self.shape)

    def model(self, time_index=None):
        """Build a model for a frame with index `time_index`"""
        if time_index is None:
            time_index = np.arange(self.tstart.shape[0])
        single_frame = not hasattr(time_index, "__iter__")
        time_index = np.atleast_1d(time_index)
        if single_frame:
            return self._model_basic(time_index[0]) + self._model_full(time_index[0])
        return np.asarray(
            [self._model_basic(tdx) + self._model_full(tdx) for tdx in time_index]
        )

    def diagnose(self, fnames, ntimes=4):
        import matplotlib.pyplot as plt

        tdxs = np.linspace(0, self.weights_full.shape[0], ntimes + 2, dtype=int)[1:-1]
        fig, ax = plt.subplots(ntimes, 3, figsize=(4 * 3, 4 * ntimes))
        for jdx, tdx in enumerate(tdxs):
            while self.quality[tdx] != 0:
                tdx += 1
            dat = load_image(fnames[tdx])[self.row][:, self.column]
            v = np.nanpercentile(dat, (5, 95))
            ax[jdx, 0].imshow(dat, vmin=v[0], vmax=v[1])
            ax[jdx, 0].set_ylabel(f"{self.tstart[tdx]} BTJD")
            ax[jdx, 1].imshow(self.model(tdx), vmin=0, vmax=v[1] - v[0])
            ax[jdx, 2].imshow(dat - self.model(tdx), vmin=0, vmax=v[1] - v[0])
            for idx, title in enumerate(["Data", "Model", "Residuals"]):
                if jdx == 0:
                    ax[jdx, idx].set(title=title)
                ax[jdx, idx].set(xticks=[], yticks=[])
        plt.tight_layout()

    @property
    def average_frame(self):
        return (self._average_frame)[self.row, :][:, self.column]

    def _fit_basic_batch(self, flux):
        """Fit the first design matrix, in a batched mode"""
        # weights = list(self.A1.fit_batch(xp.log10(flux)))
        log.debug("Fitting basic DM batched")
        return self.A1.fit_batch(xp.log10(flux))

    def _fit_full_batch(self, flux):
        """Fit the second design matrix, in a batched mode"""
        #        weights = list(self.A2.fit_batch(flux))
        log.debug("Fitting full DM batched")
        return self.A2.fit_batch(flux)

    def _fit_batch(self, flux_cube, times=None, mask_asteroids=True):
        """Fit the both design matrices, in a batched mode"""
        log.debug(f"Fitting batch, mask_asteroids={mask_asteroids}")
        if mask_asteroids:
            if times is None:
                raise ValueError("Need times to mask asteroids")
            ast_mask = self._build_asteroid_mask(times)
        else:
            ast_mask = None
        weights_basic = self._fit_basic_batch(flux_cube)
        for tdx in range(len(weights_basic)):
            flux_cube[tdx] -= xp.power(10, self.A1.dot(weights_basic[tdx])).reshape(
                self.shape
            )
        weights_full = self._fit_full_batch(flux_cube)

        log.debug("Obtaining jitter cube")
        jitter, bkg = [], []
        for tdx in range(len(weights_full)):
            flux_cube[tdx] -= self.A2.dot(weights_full[tdx]).reshape(self.shape)
            jitter.append(flux_cube[tdx][self.jitter_mask])
            bkg.append(flux_cube[tdx][self.bkg_mask])
            # self._average_frame += flux_cube[tdx]
            # self._average_frame_count += 1
            flux_cube[tdx] += self.A2.dot(weights_full[tdx]).reshape(self.shape)

        for tdx in range(len(weights_basic)):
            flux_cube[tdx] += xp.power(10, self.A1.dot(weights_basic[tdx])).reshape(
                self.shape
            )
        log.debug("Batch done")
        return weights_basic, weights_full, jitter, bkg, ast_mask

    def _run_batches(self, input, tstart=None, batch_size=100, mask_asteroids=True):
        """
        Fit the model in batches, cutting the data into appropriate batch sizes.

        Parameters
        ----------
        input: list or np.ndarray
            list of filenames or 3D np.ndarray of flux values
        tstart: None or np.ndarray
            Array of tstart values, this is important for masking asteroids only
        batch_size: int
            Size to cut the data into in time
        mask_asteroids: bool
            Whether to mask out asteroids

        Returns
        -------
        weights_basic: np.ndarray
            The weights for the basic model. Has shape ntimes x nbasic weights
        weights_full: np.ndarray
            The weights for the basic model. Has shape ntimes x nfull weights
        jitter: np.ndarray
            The jitter components for the dataset, has size ntimes x njitter
        bkg: np.ndarray
            The background components for the dataset, has size ntimes x njitter
        asteroid_mask: np.ndarray
            A boolean mask showing where asteroids have been masked at some point
            in time. Has shape cutout_size x cutout_size.
        """
        if mask_asteroids and (tstart is None):
            raise ValueError("To mask asteroids, must pass `tstart` values.")

        nbatches = xp.ceil(len(input) / batch_size).astype(int)
        weights_basic, weights_full, jitter, bkg = [], [], [], []
        l = xp.arange(0, nbatches + 1, dtype=int) * batch_size
        if l[-1] > len(input):
            l[-1] = len(input)
        asteroid_mask = np.zeros((self.cutout_size, self.cutout_size), dtype=int)

        for l1, l2 in tqdm(
            zip(l[:-1], l[1:]),
            desc=f"{self.sector}, {self.camera}, {self.ccd} ",
            total=len(l) - 1,
            leave=True,
            position=0,
        ):
            log.debug(f"Running batch {l1}:{l2}")
            if isinstance(input, (np.ndarray, list)) & isinstance(input[0], str):
                flux_cube = np.asarray(
                    [
                        load_image(input[idx], cutout_size=self.cutout_size)
                        - self._average_frame
                        for idx in np.arange(l1, l2)
                    ]
                )
            elif isinstance(input, (np.ndarray, list)) & isinstance(
                input[0], np.ndarray
            ):
                flux_cube = np.asarray([i - self._average_frame for i in input[l1:l2]])
            else:
                raise ValueError("Can not parse input.")
            # Any values le 0 cause NaN's and infs...
            flux_cube[flux_cube <= 0] = 1e-5
            w1, w2, j, bk, ast_mask = self._fit_batch(
                flux_cube,
                times=[tstart[l1:l2] if mask_asteroids else None][0],
                mask_asteroids=mask_asteroids,
            )
            weights_basic.append(w1)
            weights_full.append(w2)
            jitter.append(j)
            bkg.append(bk)
            if mask_asteroids:
                asteroid_mask += ast_mask

        return (
            xp.vstack(weights_basic),
            xp.vstack(weights_full),
            xp.vstack(jitter),
            xp.vstack(bkg),
            asteroid_mask,
        )

    def fit_model(
        self,
        flux_cube,
        batch_size=100,
        mask_asteroids=False,
        cadence_mask=None,
    ):
        """Fit a model to a flux cube, fitting frames in batches of size `batch_size`.

        This will append to the list properties `self.weights_basic`, `self.weights_full`, `self.jitter`.

        Parameters
        ----------
        flux_cube : xp.ndarray
            3D array of frames.
        tstart: np.ndarray
            Times for each frame. Required if masking asteroids.
        batch_size : int
            Number of frames to fit at once.
        """
        if cadence_mask is None:
            cadence_mask = np.ones(len(flux_cube), bool)

        (w1, w2, j, bk, self.asteroid_mask) = self._run_batches(
            flux_cube[cadence_mask],
            tstart=[self.tstart[cadence_mask] if self.tstart is not None else None][0],
            batch_size=batch_size,
            mask_asteroids=mask_asteroids,
        )

        self.weights_basic = np.zeros((len(cadence_mask), w1.shape[1]))
        self.weights_basic[cadence_mask] = w1
        self.weights_basic[~cadence_mask] = np.nan
        self.weights_full = np.zeros((len(cadence_mask), w2.shape[1]))
        self.weights_full[cadence_mask] = w2
        self.weights_full[~cadence_mask] = np.nan
        self.jitter = np.zeros((len(cadence_mask), j.shape[1]))
        self.jitter[cadence_mask] = j
        self.jitter[~cadence_mask] = np.nan
        self.bkg = np.zeros((len(cadence_mask), bk.shape[1]))
        self.bkg[cadence_mask] = bk
        self.bkg[~cadence_mask] = np.nan

        _package_pca_comps(self)
        return

    def _package_weights_hdulist(self):
        hdu0 = self.hdu0
        s = np.argsort(self.tstart)
        cols = []
        for key in ["tstart", "tstop", "quality"]:
            if getattr(self, key) is not None:
                cols.append(
                    fits.Column(
                        name=key,
                        format="D",
                        unit="BJD - 2457000",
                        array=getattr(self, key)[s],
                    )
                )
        hdu1 = fits.BinTableHDU.from_columns(cols, name="TIME")
        hdu2 = fits.ImageHDU(np.asarray(self.weights_basic)[s], name="WEIGHTS1")
        hdu3 = fits.ImageHDU(np.asarray(self.weights_full)[s], name="WEIGHTS2")
        hdu4 = fits.ImageHDU(np.asarray(self.jitter_pack)[s], name="JITTER")
        hdu5 = fits.ImageHDU(np.asarray(self.bkg_pack)[s], name="BKG")
        hdu6 = fits.ImageHDU(np.asarray(self._average_frame), name="AVGFRAME")
        hdul = fits.HDUList([hdu0, hdu1, hdu2, hdu3, hdu4, hdu5, hdu6])
        return hdul

    def save(self, output_dir=None, overwrite=False):
        """Save a model fit to the scatterbrain data directory."""
        log.debug("Packaging data for save")

        if not hasattr(self, "weights_basic"):
            raise ValueError("There is no model to save")
        self.hdu0 = fits.PrimaryHDU()
        self.hdu0.header["ORIGIN"] = "scatterbrain"
        self.hdu0.header["AUTHOR"] = "christina.l.hedges@nasa.gov"
        self.hdu0.header["VERSION"] = __version__
        for key in ["sector", "camera", "ccd"]:
            self.hdu0.header[key] = getattr(self, key)
        self.hdu0.header["CUTSIZE"] = getattr(self, "cutout_size")
        self.hdu0.header["STRPPOLY"] = getattr(self, "strap_npoly")

        if output_dir is None:
            output_dir = f"{PACKAGEDIR}/data/sector{self.sector:03}/camera{self.camera:02}/ccd{self.ccd:02}/"
            if output_dir != "":
                if not os.path.isdir(output_dir):
                    os.makedirs(output_dir)

        hdul = self._package_weights_hdulist()
        fname = (
            f"tessbackdrop_sector{self.sector}_camera{self.camera}_ccd{self.ccd}.fits"
        )
        log.debug(f"Saving to {fname}")
        hdul.writeto(output_dir + fname, overwrite=overwrite)
        log.debug("Saved")

    @staticmethod
    def from_disk(sector, camera, ccd, row=None, column=None, dir=None):
        """
        Load a model fit to the tess-backrop data directory.

        Parameters
        ----------
        input: tuple or string
            Either pass a tuple with `(sector, camera, ccd)` or pass
            a file name in `dir` to load
        dir : str
            Optional tring with the directory name

        Returns
        -------
        self: `scatterbrain.SimpleScatteredLightBackground` object
        """

        fname = f"tessbackdrop_sector{sector}_camera{camera}_ccd{ccd}.fits"
        if dir is None:
            dir = f"{PACKAGEDIR}/data/sector{sector:03}/camera{camera:02}/ccd{ccd:02}/"
        elif dir != "":
            if not os.path.isdir(dir):
                raise ValueError("No solutions exist")
        if not os.path.isfile(dir + fname):
            if "sector" in locals():
                if os.path.isfile(
                    dir + f"sector{sector:03}/camera{camera:02}/ccd{ccd:02}/" + fname
                ):
                    dir = dir + f"sector{sector:03}/camera{camera:02}/ccd{ccd:02}/"
                else:
                    raise ValueError("No files exist")
            else:
                raise ValueError("No files exist")
        log.debug(f"Loading ScatteredLightBackground from {dir+fname}")
        return ScatteredLightBackground.from_path(dir + fname, row=row, column=column)

    @staticmethod
    def from_path(path, row=None, column=None):
        if row is None:
            row = np.asarray([1])
        if column is None:
            column = np.asarray([1])
        with fits.open(path, lazy_load_hdus=True) as hdu:
            sector, camera, ccd = [
                hdu[0].header[key]
                for key in [
                    "sector",
                    "camera",
                    "ccd",
                ]
            ]
        self = ScatteredLightBackground(
            sector=sector, camera=camera, ccd=ccd, row=row, column=column
        )
        with fits.open(path, lazy_load_hdus=True) as hdu:
            setattr(self, "cutout_size", hdu[0].header["CUTSIZE"])

            if "tstart" in hdu[1].data.names:
                self.tstart = hdu[1].data["tstart"]
            if "tstop" in hdu[1].data.names:
                self.tstop = hdu[1].data["tstop"]
            if "quality" in hdu[1].data.names:
                self.quality = hdu[1].data["QUALITY"]
            self.weights_basic = list(hdu[2].data)
            weights_full = hdu[3].data
            self.strap_npoly = hdu[0].header["STRPPOLY"]

            # We have to do some work to get out just the column pixels
            # we are interested in
            strap_locs = np.loadtxt(f"{PACKAGEDIR}/data/strap_locs.csv").astype(int) - 1
            strap_locs = np.unique([strap_locs - 1, strap_locs, strap_locs + 1])
            strap_weights = np.hstack(
                (
                    weights_full[:, -230 * self.strap_npoly :].reshape(
                        (weights_full.shape[0], self.strap_npoly, 230)
                    )[:, :, np.in1d(strap_locs, self.column)]
                ).transpose([1, 0, 2])
            )
            self.weights_full = np.hstack(
                [
                    weights_full[:, : -230 * self.strap_npoly],
                    strap_weights,
                ]
            )
            self.jitter_pack = hdu[4].data
            self.bkg_pack = hdu[5].data
            # self._average_frame = hdu[6].data
            # self._average_frame_count = 1
            self._average_frame = hdu[6].data
        return self

    @staticmethod
    def from_tpf(tpf, dir=None):
        backdrop = ScatteredLightBackground.from_disk(
            tpf.sector,
            tpf.camera,
            tpf.ccd,
            dir=dir,
            row=np.arange(tpf.shape[1]) + tpf.row - 1,
            column=np.arange(tpf.shape[2]) + tpf.column - 44 - 1,
        )
        idx, jdx = _align_with_tpf(backdrop, tpf)
        return backdrop[idx]

    @staticmethod
    def from_zenodo(tpf, dir=None):
        raise NotImplementedError

    def get_tpf_mask(self, tpf):
        idx, jdx = _align_with_tpf(self, tpf)
        return jdx

    @staticmethod
    def from_tess_images(
        fnames,
        mask_asteroids=True,
        batch_size=100,
        cutout_size=2048,
        sector=None,
        camera=None,
        ccd=None,
        verbose=False,
        quality_bitmask=63,
        njitter=5000,
    ):
        """Creates a ScatteredLightBackground model from filenames

        Parameters
        ----------
        fnames : list
            List of filenames to compute the background model for
        batch_size : int
            Number of files to process in a given batch

        Returns
        -------
        b : `scatterbrain.ScatteredLightBackground.ScatteredLightBackground`
            ScatteredLightBackground object
        """
        log.debug("Building `ScatteredLightBackground` from TESS images")

        fnames, sector, camera, ccd = _validate_inputs(fnames, sector, camera, ccd)
        self = ScatteredLightBackground(
            sector=sector,
            camera=camera,
            ccd=ccd,
            cutout_size=cutout_size,
            njitter=njitter,
            verbose=verbose,
        )
        self.tstart = np.asarray(
            [fitsio.read_header(fname, ext=0)["TSTART"] for fname in fnames]
        )
        s = np.argsort(self.tstart)
        self.tstart, fnames = self.tstart[s], np.asarray(fnames)[s]

        log.debug("Identifying bad frames")
        blown_out_frames = identify_bad_frames(fnames)

        # make a ScatteredLightBackground object
        self.tstop = np.asarray(
            [fitsio.read_header(fname, ext=0)["TSTOP"] for fname in fnames]
        )
        self.quality = np.asarray(
            [fitsio.read_header(fname, ext=1)["DQUALITY"] for fname in fnames]
        )
        self.quality[blown_out_frames] |= 8192
        # Step 1: find a good test frame
        log.debug("Building average frame")

        # We make an aggressive mask for the average image.
        cadence_mask = self.quality_mask(6911)
        if cadence_mask.sum() < 50:
            self._average_frame = np.zeros((self.cutout_size, self.cutout_size))
        else:
            self._average_frame = (
                get_min_image_from_filenames(
                    fnames[cadence_mask], cutout_size=self.cutout_size
                )
                - 1e-6
            )
        cadence_mask = self.quality_mask(quality_bitmask)
        log.debug("Building source masks")
        self._build_masks(self._average_frame)
        if self._average_frame.sum() != 0:
            m1 = self.A1.dot(self.A1.fit_frame(np.log10(self.average_frame))).reshape(
                (self.cutout_size, self.cutout_size)
            )
            m2 = self.A2.dot(self.A2.fit_frame((self.average_frame - m1))).reshape(
                (self.cutout_size, self.cutout_size)
            )
            self._average_frame = self._average_frame - np.nan_to_num(m1 + m2)

        log.debug("Running batches")

        self.fit_model(
            fnames,
            batch_size=batch_size,
            mask_asteroids=mask_asteroids,
            cadence_mask=cadence_mask,
        )

        return self
