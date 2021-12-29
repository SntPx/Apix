#!/usr/bin/python3
#
# Copyright (c) 2021-2022 Christophe 'SntPx' RIVIERE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
""" Entrypoint for pxmgr

Entrypoint for pxmgr

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Christophe 'SntPx' RIVIERE"
__contact__ = "sntpx@meltdown.fr"
__copyright__ = "Copyright 2021, Christophe 'SntPx' RIVIERE"
__date__ = "2021/12/14"
__deprecated__ = False
__email__ = "meltdownfr@gmail.com"
__license__ = "GPLv3"
__maintainer__ = "Christophe 'SntPx' RIVIERE"
__status__ = "Production"
__version__ = "0.0.1"
import sys
from PyQt6 import QtWidgets
from gui.window import Ui
from edu.Domain import create_domains_skills



if __name__ == "__main__":
    create_domains_skills()
    app = QtWidgets.QApplication(sys.argv)
    win = Ui()
    sys.exit(app.exec())

