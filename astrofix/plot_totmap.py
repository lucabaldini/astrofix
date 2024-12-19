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

import glob, os, sys
import numpy as np

from astrofix import ASTROFIX_DATA
from astrofix import logger
from astrofix.analysis import Run
from astrofix.plt_ import plt, setup_gca


# this folter cointains one petting per pixel
# want to plot the map of average TOT
FOLDER_PATH = os.path.join(ASTROFIX_DATA, 'runsuite_vscan_20241219-143849')


data = np.zeros(shape=(16, 13))
for file_path in glob.glob(f'{FOLDER_PATH}/*.csv'):
    run = Run(file_path)
    #logger.info("Run Trigger Threshold (mV) %.1f and Injection Voltage (mV) %.1f" % 
    #(run.trigger_threshold(), run.injection_voltage()))
    
    nevt     = len(run)
    row, col = run.inject_pixels()
    good_tot = run.filter_last_tot(1000)
    all_tot  = run.tot
    tot      = np.mean(good_tot)
    tot_err  = np.std(good_tot, ddof=1)/np.sqrt(nevt)
    if len(all_tot) != nevt:
        logger.warning("Some bad TOT cases i this file")
    
    data[col][row] = tot
    logger.success("%d, %d, %f" % ( col, row, tot))

plt.matshow(data.T)
plt.xlabel('Column')
plt.ylabel('Row')
plt.gca().set_aspect('equal')

plt.figure('Average_Tot')
tots = data.flatten()
plt.hist(tots, bins=100, range=(100, 600))
logger.success('mu= %.1f sigma= %.1f' % (np.mean(tots), np.std(tots, ddof=1)))
plt.text(400, 10, r'$\mu$= %.1f $\sigma$= %.1f' % (np.mean(tots), np.std(tots, ddof=1)))
plt.xlabel("Average ToT [us]")

plt.show()
