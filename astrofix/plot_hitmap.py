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

import os
import numpy as np

from astrofix import ASTROFIX_DATA
from astrofix import logger
from astrofix.analysis import Run
from astrofix.plt_ import plt, setup_gca

file_path = os.path.join(ASTROFIX_DATA,'noiseocc_thrscan',  '20241213-101137.csv')
noisy_ch_list =[(3,12), (10,11)]

run = Run(file_path)
logger.info("Run Trigger Threshold (mV) %.2f" % run.trigger_threshold())
logger.info("Run total time (min) %.2f" % run.running_time())

binning = (
            np.linspace(-0.5, run._NUM_COLS - 0.5, run._NUM_COLS + 1),
            np.linspace(-0.5, run._NUM_ROWS - 0.5, run._NUM_ROWS + 1)
            )
plt.figure('Hitmap_all')
data, _, _, _ = plt.hist2d(run.col, run.row, bins=binning)
logger.info(f'Pixel occupancy: \n %s' % str(data))
plt.xlabel('Column')
plt.ylabel('Row')
plt.gca().set_aspect('equal')

# masking noisy pixels
_mask = np.full(len(run), 1)
for (x,y) in noisy_ch_list:
    logger.info("Masking channel (%d, %d)" % (x,y))
    _cut = np.logical_or(run.col!=x, run.row!=y)
    _mask = np.logical_and(_mask, _cut)
logger.info("Trigger rate (w/ masked pixels) (Hz) %.2f" % (sum(_mask)/run.running_time()))
plt.figure('Hitmap')
data, _, _, _ = plt.hist2d(run.col[_mask], run.row[_mask], bins=binning)
plt.xlabel('Column')
plt.ylabel('Row')
plt.gca().set_aspect('equal')

plt.figure('TOT distribution')
plt.hist(run.tot, bins=np.linspace(0, 100, 100))
plt.xlabel(r'TOT [$\mu$s]')

        

plt.show()
