#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 07:27:15 2017

@author: hph
"""

from astropy.io import fits
import numpy as np
import os
import glob


for filename in glob.glob(os.path.expanduser("~/Dropbox/SMA_CMZ/CMZoom_Images/November17_continuum_fits/G*fits")):
    originalfits = fits.open('/Users/hph/current_fits/'+filename)
    originaldata = originalfits[0].data[0,0,:,:]
    originalheader = originalfits[0].header
    bmaj = originalheader['BMAJ']
    bmin = originalheader['BMIN']
    beam_area_naive = np.pi*bmaj*bmin
    conversion_factor = (41253./(4*np.pi))*((2.35)**2)/beam_area_naive
    
    newdata = originaldata*conversion_factor
    
    newfits = originalfits
    newfits[0].data = newdata
    
    newfits.writeto('/Users/hph/current_fits/new_units/'+filename+'mod_Jy_per_Ster.fits',overwrite=True)

