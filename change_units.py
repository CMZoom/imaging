import radio_beam
from astropy.io import fits
import numpy as np
import os
import glob

corrected_hdus = []

for filename in glob.glob(os.path.expanduser("~/Dropbox/SMA_CMZ/CMZoom_Images/November17_continuum_fits/G*fits")):
    originalfits = fits.open(filename)
    originaldata = originalfits[0].data.squeeze()
    originalheader = originalfits[0].header
    beam = radio_beam.Beam.from_fits_header(originalheader)

    assert originalheader['BUNIT'] == 'Jy/beam'
    
    newdata = originaldata / beam.sr.value
    
    hdu = fits.PrimaryHDU(data=newdata, header=originalheader)

    corrected_hdus.append(hdu)

#outheader = ...
