#file_editor.py
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

from tkinter import filedialog as fd, messagebox as mb
import json


class FileHandler:
    def __init__(self, mode=None, file=None):
        self.file = file
        if mode == "read":
            self.read_file()
        elif mode == "write":
            self.write_file()
        elif mode == "export_csv":
            self.write_csv()
        else:
            raise ValueError("File handler selection unknown")

    @staticmethod
    def read_file(file):
        if file is None:
            file_name = fd.askopenfilename(defaultextension=".swl", filetypes=(("FMRL File", "*.swl"),
                                                                               ("FMRL Bin File", "*.fml")))
            with open(file_name, "r", encoding="utf-8") as f:
                data = json.loads(f.read())
                return data
        else:
            with open(file, "r", encoding="utf-8") as f:
                data = json.loads(f.read())
                return data

    def write_file(self):
        #Saves the bandscan file in plain file or bin file
        file_name = fd.asksaveasfilename(defaultextension=".swl", filetypes=(("FMRL File", "*.swl"),
                                                                             ("FMRL Bin File", "*.fml")))
        if file_name.endswith(".swl"):

                with open(file_name, "w", encoding="utf-8") as f:
                    json.dump(self.file, f, ensure_ascii=False, indent=4)
                return True

        elif file_name.endswith(".fml"):
            #TODO Add the BIN file section
            mb.showwarning(title="Function unavailable", message="The function is not yet available")

        else:
            pass

    def write_csv(self):
        file_name = fd.asksaveasfilename(defaultextension=".csv", filetypes=(("Comma separated values", "*.csv"),))
        try:
            with open(file_name, "w") as f:
                f.write(self.file)

        except FileNotFoundError:
            mb.showinfo(title="File not saved", message="The file was not saved")
