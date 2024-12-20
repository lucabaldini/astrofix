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

from astrofix import ASTROFIX_DATA
from astrofix.analysis import Run
from astrofix.plt_ import plt, setup_gca


#FOLDER_PATH = os.path.join(ASTROFIX_DATA, 'runsuite_vscan_20241219-114807')
FOLDER_PATH = os.path.join(ASTROFIX_DATA, 'runsuite_vscan_20241219-124116')
"""
data {'[row, col]': {vth: ([vinj], [tot], [tot_err], [frac good tot])}}
"""

data = {}
for file_path in glob.glob(f'{FOLDER_PATH}/*.csv'):
    run = Run(file_path)
    nevt    = len(run)
    good_tot = run.filter_last_tot()
    vinj    = run.injection_voltage()
    tot     = np.mean(good_tot)
    tot_err = np.std(good_tot, ddof=1)#/np.sqrt(nevt)
    pix_str = str(run.inject_pixels())
    vthr    = run.trigger_threshold()
    
        
    if pix_str not in data.keys():
        data[pix_str] = {}
    if vthr not in data[pix_str].keys():
        data[pix_str][vthr] = ([], [], [], [])
    data[pix_str][vthr][0].append(vinj)
    data[pix_str][vthr][1].append(tot)
    data[pix_str][vthr][2].append(tot_err)
    if nevt>0:
        data[pix_str][vthr][3].append(len(good_tot)/nevt)  
    else:
        data[pix_str][vthr][3].append(0)
for pix_pair in data.keys():
    plt.figure()
    for vth in data[pix_pair].keys():
        plt.title("Pixel %s" %pix_pair)
        #print(pix_pair, vth, data[pix_pair][vth][0], data[pix_pair][vth][1])
        plt.errorbar(data[pix_pair][vth][0], data[pix_pair][vth][1], data[pix_pair][vth][2], fmt='-o', label="vth %.1f" % vth)
        setup_gca(xlabel='Injection voltage [mV]', ylabel='Average TOT [$\mu$s]', grids=True, 
        legend = True, xmin=200, xmax=1100, ymin=40, ymax=400)

plt.figure()
for pix_pair in data.keys():
    for vth in data[pix_pair].keys():
        plt.errorbar(data[pix_pair][vth][0], data[pix_pair][vth][3], fmt='-o', label="%s vth %.1f" % (pix_pair, vth))
        setup_gca(xlabel='Injection voltage [mV]', ylabel='Fract Good TOT', grids=True, 
        xmin=200, xmax=1100, ymin=0, ymax=1.1)
        plt.legend(loc="lower left")
        
plt.show()
