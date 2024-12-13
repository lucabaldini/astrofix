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

import glob

from astrofix import ASTROFIX_DATA
from astrofix.analysis import Run
from astrofix.plt_ import plt, setup_gca


FOLDER_PATH = ASTROFIX_DATA / 'noiseocc_thrscan'

threshold = []
rate = []
for file_path in glob.glob(f'{FOLDER_PATH}/*.csv'):
    run = Run(file_path)
    threshold.append(run.trigger_threshold())
    rate.append(len(run) / run.running_time())

plt.plot(threshold, rate, 'o')
setup_gca(xlabel='Trigger threshold [mV]', ylabel='Rate [Hz]', logx=True,
    logy=True, grids=True, xmin=0.75 * min(threshold), xmax=1.25 * max(threshold))
plt.show()
