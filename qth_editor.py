#qth_editor.py
# ####################################################################### #
# This file is part of the FMRadioLog distribution.                       #
# Copyright (c) 2024 Augusto Burzo.                                       #
#                                                                         #
# This program is free software: you can redistribute it and/or modify    #
# it under the terms of the GNU General Public License as published by    #
# the Free Software Foundation, version 3.                                #
#                                                                         #
# This program is distributed in the hope that it will be useful, but     #
# WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU        #
# General Public License for more details.                                #
#                                                                         #
# You should have received a copy of the GNU General Public License       #
# along with this program. If not, see <http://www.gnu.org/licenses/>.    #
# ####################################################################### #

import base64


class QTHFileHandler:
    def __init__(self, qth=None, switch=None, **kwargs):
        if qth is None:
            qth = [0, 0, 0]
        self.qth = str(qth).encode("ascii")
        self.base64qth = base64.b64encode(self.qth)
        if switch == 0:
            self.write_qth_file()
        elif switch == 1:
            self.read_qth_file()

    def read_qth_file(self):
        with open("main.qth", "rb") as qth_file:
            self.qth = base64.b64decode(qth_file.read())
        self.qth = self.qth.decode("ascii")
        self.qth = self.qth.replace("[","").replace("]","").replace('"','')
        return self.qth

    def write_qth_file(self):
        with open("main.qth", "wb") as qth_file:
            qth_file.write(self.base64qth)
