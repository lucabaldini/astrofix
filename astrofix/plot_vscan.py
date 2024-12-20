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
from astrofix import logger
from astrofix.analysis import Run
from astrofix.plt_ import plt, setup_gca


#FOLDER_PATH = os.path.join(ASTROFIX_DATA, 'runsuite_vscan_20241219-114807')
# test run with a few pixels and a few v settings
#FOLDER_PATH = os.path.join(ASTROFIX_DATA, 'runsuite_vscan_20241219-124116')

# all pixel, one vinj and a few vthr
#FOLDER_PATH = os.path.join(ASTROFIX_DATA, 'runsuite_vscan_20241219-164745')

# one pixel, several vinj and a vthr
#FOLDER_PATH = os.path.join(ASTROFIX_DATA, 'runsuite_pixeldeepscan_20241220-085931') # [6,7]
#FOLDER_PATH = os.path.join(ASTROFIX_DATA, 'runsuite_pixeldeepscan_20241220-125418') # [9,8]
FOLDER_PATH = os.path.join(ASTROFIX_DATA, 'runsuite_pixeldeepscan_20241220-143616') # [7,6]

"""
data {'[row, col]': {vinj: ([vth], [tot], [tot_err], [frac good tot])}}
"""

def thrmodel(x, q, s):
    return q-x/s
    
def qsline(x, a):
    return a/x

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

# assuming one vinj only
Q = np.zeros(shape=(16, 13))
S = np.zeros(shape=(16, 13))
# assuming one pixel only
Vinj_pix = []
Q_pix    = []
S_pix    = []
SE_pix   = []

if len(data) ==1: # must be a deep pixel scan
    fig, (xx1, xx2, xx3) = plt.subplots(nrows=1, ncols=3, figsize=(15, 5), layout="constrained")
else:
    fig, (xx1) = plt.subplots(nrows=1, ncols=1, figsize=(5, 5), layout="constrained")
    xx1.set_title("All Pixels")
    
for pix_pair in data.keys():
    
    for vinj in data[pix_pair].keys():
        #xx1.set_title("Pixel %s" %pix_pair)
        #print(pix_pair, vth, data[pix_pair][vth][0], data[pix_pair][vth][1])
       
        xx1.errorbar(data[pix_pair][vinj][0], data[pix_pair][vinj][1], data[pix_pair][vinj][2], fmt='o', label="vinj %.0f" % vinj)
        try:
            fout, fcorr = curve_fit(thrmodel, data[pix_pair][vinj][0], data[pix_pair][vinj][1], p0=(100, 1))
            ferr = np.sqrt(fcorr.diagonal())
            print(pix_pair, vinj, fout, ferr)       
            xx1.plot(data[pix_pair][vinj][0], thrmodel(data[pix_pair][vinj][0], *fout))
            # one value (last) per pixels
            row, col = eval(pix_pair)
            Q[col][row] = fout[0]
            S[col][row] = fout[1]
            if len(data) ==1: # ok, there is one pixel, we can do fit out vs vinj
                Vinj_pix.append(vinj)
                Q_pix.append(fout[0])
                S_pix.append(fout[1])
                SE_pix.append(ferr[1])
        except:
            pass
        setup_gca(xlabel='Trigger threshold V [mV]', ylabel=r'Average TOT [$\mu$s]', 
        xmin=80, xmax=210, ymin=25, ymax=550)
        
#
# summarty plot
#   
if len(data) ==1: # ok, there is one pixel, we can do fit out vs vinj
    xx1.set_xlabel('Trigger threshold V [mV]')
    xx1.set_ylabel(r'Average TOT [$\mu$s]')
    xx1.set_xlim([80, 210])
    xx1.set_ylim([25, 300])
    xx1.legend(loc='upper right', fontsize ='x-small')
    
    xx2.plot(Vinj_pix, Q_pix, "o")
    xx2.set_xlabel(r"Injection Voltage [mV]")
    xx2.set_ylabel(r"ToT$_0$ [$\mu$s]")
    xx2.set_xlim([150, 1050])
    xx2.set_ylim([0.95*min(Q_pix),  1.05*max(Q_pix)])
    xx2.grid()
    
    xx3.errorbar(Vinj_pix, S_pix, SE_pix, fmt="o")
    xx3.set_xlabel(r"Injection Voltage [mV]")
    xx3.set_ylabel(r"S$_d$ [mV/$\mu$s]")
    xx3.set_xlim([150, 1050])
    xx3.set_ylim([0.98*min(S_pix), 1.02*max(S_pix)])
    xx3.grid()

if len(data)>1 : # muplible pixels, is worth a map
    fig, ((ax1, ax2, ax3), (bx1, bx2, bx3) ) = plt.subplots(nrows=2, ncols=3, figsize=(15, 9), layout="constrained")

    cbx1 = bx1.matshow(Q.T)
    bx1.set_title(r"ToT$_0$ [$\mu$s]")
    bx1.set_xlabel('Column')
    bx1.set_ylabel('Row')
    bx1.set_aspect('equal')
    fig.colorbar(cbx1)

    cbx2 = bx2.matshow(S.T)
    bx2.set_title(r"S$_d$ [mV/$\mu$s]")
    bx2.set_xlabel('Column')
    bx2.set_ylabel('Row')
    bx2.set_aspect('equal')
    fig.colorbar(cbx2)

    ax1.hist(Q.flatten(), bins=100)
    ax1.set_xlabel(r"ToT$_0$ [$\mu$s]")
    ax1.set_ylim([0, 13])
    logger.success('ToT$_0$ mu= %.1f sigma= %.1f' % (np.mean(Q.flatten()), np.std(Q.flatten(), ddof=1)))
    ax1.text(400, 8, r'$\mu$= %.1f $\sigma$= %.1f' % (np.mean(Q.flatten()), np.std(Q.flatten(), ddof=1)))

    ax2.hist(S.flatten(), bins=100)
    ax2.set_xlabel(r"S$_d$ [mV/$\mu$s]")
    ax2.set_ylim([0, 13])
    logger.success('S$_d$ mu= %.2f sigma= %.2f' % (np.mean(S.flatten()), np.std(S.flatten(), ddof=1)))
    ax2.text(0.2, 8, r'$\mu$= %.2f $\sigma$= %.2f' % (np.mean(S.flatten()), np.std(S.flatten(), ddof=1)))

    ax3.plot(S.flatten(), Q.flatten(), ".")
    ax3.set_xlabel(r"S$_d$ [mV/$\mu$s]")
    ax3.set_ylabel(r"ToT$_0$ [$\mu$s]")

    fout, fcorr = curve_fit(qsline, S.flatten(), Q.flatten())
    ferr = np.sqrt(fcorr.diagonal())
    logger.success("qsline %f +- %f" %( fout[0], ferr[0]))
    x = np.linspace(min(S.flatten()),max(S.flatten()),1000)
    ax3.plot(x, qsline(x, fout[0]), label="%.0f/x fit" % fout[0])
    ax3.legend()

    bx3.plot(S.flatten(), Q.flatten()/qsline(S.flatten(), fout[0]), ".")
    bx3.set_xlabel(r"S$_d$ [mV/$\mu$s]")
    bx3.set_ylabel(r"ToT$_0$/fit")

# finally show all
plt.show()
