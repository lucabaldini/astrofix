# Copyright (C) 2024 the astrofix team.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import glob, os

import numpy as np
from scipy.optimize import curve_fit

from astrofix import ASTROFIX_DATA
from astrofix.analysis import Run
from astrofix.plt_ import plt, setup_gca


#FOLDER_PATH = os.path.join(ASTROFIX_DATA, 'runsuite_vscan_20241219-114807')
FOLDER_PATH = os.path.join(ASTROFIX_DATA, 'runsuite_vscan_20241219-124116')
"""
data {'[row, col]': {vinj: ([vth], [tot], [tot_err], [frac good tot])}}
"""

def thrmodel(x, q, s):
    return q-x/s

data = {}
for file_path in glob.glob(f'{FOLDER_PATH}/*.csv'):
    run = Run(file_path)
    
    nevt    = len(run)
    good_tot = run.filter_last_tot(1000)
    vinj    = run.injection_voltage()
    tot     = np.mean(good_tot)
    tot_err = np.std(good_tot, ddof=1)/np.sqrt(nevt)
    pix_str = str(run.inject_pixels())
    vthr    = run.trigger_threshold()
    
    if pix_str not in data.keys():
        data[pix_str] = {}
    if vinj not in data[pix_str].keys():
        data[pix_str][vinj] = ([], [], [], [])
    data[pix_str][vinj][0].append(vthr)
    data[pix_str][vinj][1].append(tot)
    data[pix_str][vinj][2].append(tot_err)



for pix_pair in data.keys():
    plt.figure()
    for vinj in data[pix_pair].keys():
        plt.title("Pixel %s" %pix_pair)
        #print(pix_pair, vth, data[pix_pair][vth][0], data[pix_pair][vth][1])
       
        plt.errorbar(data[pix_pair][vinj][0], data[pix_pair][vinj][1], data[pix_pair][vinj][2], fmt='o', label="vinj %.1f" % vinj)
        try:
            fout, fcorr = curve_fit(thrmodel, data[pix_pair][vinj][0], data[pix_pair][vinj][1], p0=(100, 1))
            ferr = np.sqrt(fcorr.diagonal())
            print(pix_pair, vinj, fout, ferr)       
            plt.plot(data[pix_pair][vinj][0], thrmodel(data[pix_pair][vinj][0], *fout))
        except:
            pass
        setup_gca(xlabel='Trigger threshold V [mV]', ylabel='Average TOT [$\mu$s]', grids=True, 
        legend = True, xmin=70, xmax=160, ymin=40, ymax=400)

        
plt.show()
