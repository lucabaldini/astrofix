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

import numpy as np

from astrofix import ASTROFIX_DATA
from astrofix.plt_ import plt, setup_gca

FILE_PATH = ASTROFIX_DATA / '20241213_iv_scan.txt'
SIGMA_V = 1.


V, I = np.loadtxt(FILE_PATH, unpack=True)
plt.errorbar(V, I, SIGMA_V, fmt='o')
setup_gca(xlabel='$V_{bias}$ [V]', ylabel='I [nA]', grids=True, xmin=70, xmax=210)
plt.show()
