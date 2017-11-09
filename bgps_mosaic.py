import numpy as np
import os
import reproject
from astropy.io import fits
import uvcombine


urls = [
    "http://irsa.ipac.caltech.edu/data/BOLOCAM_GPS/images/v2/INNER_GALAXY/maps/v2.1_ds2_l359_13pca_map20_crop.fits",
    "http://irsa.ipac.caltech.edu/data/BOLOCAM_GPS/images/v2/INNER_GALAXY/maps/v2.1_ds2_l000_13pca_map20_crop.fits",
    "http://irsa.ipac.caltech.edu/data/BOLOCAM_GPS/images/v2/INNER_GALAXY/maps/v2.1_ds2_l001_13pca_map20_crop.fits",
    "http://irsa.ipac.caltech.edu/data/BOLOCAM_GPS/images/v2/INNER_GALAXY/maps/v2.1_ds2_l004_13pca_map20_crop.fits",
    "http://irsa.ipac.caltech.edu/data/BOLOCAM_GPS/images/v2/INNER_GALAXY/maps/v2.1_ds2_l357_13pca_map20_crop.fits",
]

hdu1 = fits.open("http://irsa.ipac.caltech.edu/data/BOLOCAM_GPS/images/v2/INNER_GALAXY/maps/v2.1_ds2_l000_13pca_map20.fits",)

header = hdu1[0].header.copy()
header['NAXIS1'] = 2500
header['NAXIS2'] = 700
header['CRPIX1'] = 1250
header['CRVAL1'] = 0.0
header['CRVAL2'] = 0.0
header['CRPIX2'] = 350.0

totalimg, weightimg = np.zeros([header['NAXIS2'],header['NAXIS1']]), np.zeros([header['NAXIS2'],header['NAXIS1']])

for fn in urls:
    fh = fits.open(fn)
    reproj,weight = reproject.reproject_interp(fh, header)

    totalimg[weight.astype('bool')] += reproj[weight.astype('bool')]
    weightimg += weight

rslt = fits.PrimaryHDU(data=totalimg/weightimg, header=header)
rslt.writeto(os.path.expanduser('~/Dropbox/SMA_CMZ_FITS_files/BGPS_Mosaic.fits'), overwrite=True)


sma_mosaic = fits.open(os.path.expanduser('~/Dropbox/SMA_CMZ/CMZoom_Images/November17_continuum_fits/mosaic_JySr.fits'))
#sma_mosaic[0].header['BUNIT'] = 'Jy/sr'

comb = uvcombine.feather_simple(sma_mosaic[0], rslt)
