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


FOLDER_PATH = os.path.join(ASTROFIX_DATA, 'noiseocc_thrscan')
noisy_ch_list =[(3,12), (10,11)]

threshold = []
rate = []
rate_masked = []
for file_path in glob.glob(f'{FOLDER_PATH}/*.csv'):
    run = Run(file_path)
    threshold.append(run.trigger_threshold())
    rate.append(len(run) / run.running_time())
    mask = np.full(len(run), 1)
    for (x,y) in noisy_ch_list:
        #logger.info("Masking channel (%d, %d)" % (x,y))
        _cut = np.logical_or(run.col!=x, run.row!=y)
        mask = np.logical_and(mask, _cut)
    rate_masked.append(sum(mask) / run.running_time())

plt.plot(threshold, rate, 'o', label="all enabled")
plt.plot(threshold, rate_masked, 'd', label="%d masked pixels" %len(noisy_ch_list))
setup_gca(xlabel='Trigger threshold [mV]', ylabel='Rate [Hz]', logx=False,
    logy=True, grids=True, xmin=0.75 * min(threshold), xmax=1.25 * max(threshold))
plt.legend()
plt.show()
