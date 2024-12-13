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

import numpy as np

from astrofix import ASTROFIX_DATA
from astrofix.analysis import Run
from astrofix.plt_ import plt, setup_gca


FOLDER_PATH = ASTROFIX_DATA / 'ciscan'

vinj = []
tot = []
for file_path in glob.glob(f'{FOLDER_PATH}/*.csv'):
    run = Run(file_path)
    vinj.append(run.injection_voltage())
    tot.append(np.mean(run.tot))

plt.plot(vinj, tot, 'o')
setup_gca(xlabel='Injection voltage [mV]', ylabel='Average TOT [$\mu$s]', grids=True,
    xmin=min(vinj) - 10, xmax=max(vinj) + 10)

plt.show()
