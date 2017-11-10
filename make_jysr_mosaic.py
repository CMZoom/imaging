import radio_beam
import reproject
from spectral_cube import wcs_utils
from astropy import wcs
from astropy.io import fits
from astropy.utils.console import ProgressBar
import numpy as np
import os
import glob

corrected_hdus = []

for filename in ProgressBar(glob.glob(os.path.expanduser("~/Dropbox/SMA_CMZ/CMZoom_Images/November17_continuum_fits/G*fits"))):
    originalfits = fits.open(filename)
    originaldata = originalfits[0].data.squeeze()
    originalheader = originalfits[0].header
    beam = radio_beam.Beam.from_fits_header(originalheader)

    assert originalheader['BUNIT'] == 'Jy/beam'
    
    newdata = originaldata / beam.sr.value
    newheader = wcs_utils.strip_wcs_from_header(originalheader)
    newheader.update(wcs.WCS(originalheader).celestial.to_header())
    
    hdu = fits.PrimaryHDU(data=newdata, header=newheader)

    corrected_hdus.append(hdu)

outheader = fits.getheader(os.path.expanduser('~/Dropbox/SMA_CMZ_FITS_files/BGPS_Mosaic.fits'))
outheader['NAXIS1'] = 20000
outheader['NAXIS2'] = 4000
outheader['CRVAL1'] = 0.435
outheader['CRVAL2'] = -0.167
outheader['CRPIX1'] = 10000
outheader['CRPIX2'] = 2000
outheader['CDELT1'] = -0.00013888888888
outheader['CDELT2'] = 0.00013888888888
del outheader['CD1_1']
del outheader['CD1_2']
del outheader['CD2_1']
del outheader['CD2_2']

newdata = np.zeros([outheader['NAXIS2'], outheader['NAXIS1']])
newweight = np.zeros([outheader['NAXIS2'], outheader['NAXIS1']])

for hdu in ProgressBar(corrected_hdus):

    reproj,weight = reproject.reproject_interp(hdu, outheader)

    newdata[weight.astype('bool')] += reproj[weight.astype('bool')]
    newweight += weight

outheader['BUNIT'] = 'Jy/sr'

final_hdu = fits.PrimaryHDU(data=newdata/newweight, header=outheader)
final_hdu.writeto(os.path.expanduser('~/Dropbox/SMA_CMZ/CMZoom_Images/November17_continuum_fits/mosaic_JySr.fits'))