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

import customtkinter
from tkinter import messagebox, END
import qth_editor

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_appearance_mode("dark")
        self.geometry("1024x768")
        self.title("FMRadioLog")
        self.frequencies = ["", ]
        #TODO Create an icon
        #TODO Add a menubar

        #QTH Selection Block
        self.qth_lbl = customtkinter.CTkLabel(master=self, text="QTH Selection")
        self.qth_lbl.pack(pady=1)
        self.qth_frame = customtkinter.CTkFrame(master=self)
        self.qth_frame.pack(pady=5, padx=5, fill="x")
        self.latitude_lbl = customtkinter.CTkLabel(master=self.qth_frame, text="Latitude:")
        self.latitude_lbl.grid(column=0, row=1, sticky="e", padx=5)
        self.latitude_entry = customtkinter.CTkEntry(master=self.qth_frame)
        self.latitude_entry.grid(column=1, row=1, sticky="ew", padx=5, pady=5)
        self.longitude_lbl = customtkinter.CTkLabel(master=self.qth_frame, text="Longitude:")
        self.longitude_lbl.grid(column=2, row=1, sticky="e", padx=5)
        self.longitude_entry = customtkinter.CTkEntry(master=self.qth_frame)
        self.longitude_entry.grid(column=3, row=1, sticky="ew", padx=5, pady=5)
        self.altitude_lbl= customtkinter.CTkLabel(master=self.qth_frame, text="Altitude:")
        self.altitude_lbl.grid(column=4, row=1, sticky="e", padx=5)
        self.altitude_entry = customtkinter.CTkEntry(master=self.qth_frame)
        self.altitude_entry.grid(column=5, row=1, sticky="ew")
        self.edit_qth_btn = customtkinter.CTkButton(master=self.qth_frame, text="Edit QTH", command=self.edit_qth)
        self.edit_qth_btn.grid(column=6, row=1, sticky="ew", padx=5, pady=5)
        self.save_qth_btn = customtkinter.CTkButton(master=self.qth_frame, text="Save QTH", command=self.save_qth)
        self.save_qth_btn.grid(column=6, row=2, sticky="ew", padx=5, pady=5)
        self.location_lbl = customtkinter.CTkLabel(master=self.qth_frame, text="Location:")
        self.location_lbl.grid(column=0, row=2, sticky="e", padx=5)
        self.location_entry = customtkinter.CTkEntry(master=self.qth_frame)
        self.location_entry.grid(column=1, row=2, sticky="ew", columnspan="5", padx=5, pady=5)

        # Master Block
        self.name_lbl = customtkinter.CTkLabel(master=self, text="Frequency data")
        self.name_lbl.pack(pady=1)
        self.master_frame = customtkinter.CTkFrame(master=self)
        self.master_frame.pack(pady=5, padx=5, fill="x")
        self.frequency_lbl = customtkinter.CTkLabel(master=self.master_frame, text="Frequency:")
        self.frequency_lbl.grid(column=0, row=0, sticky="e", padx=5, pady=5)
        self.get_freqs()
        self.frequency_cbx = customtkinter.CTkComboBox(master=self.master_frame, values=self.frequencies)
        self.frequency_cbx.grid(column=1, row=0, sticky="w")
        self.rds_lbl = customtkinter.CTkLabel(master=self.master_frame, text="RDS:")
        self.rds_lbl.grid(column=0, row=1, sticky="e", padx=5, pady=5)
        self.rds_entry = customtkinter.CTkEntry(master=self.master_frame)
        self.rds_entry.grid(column=1, row=1, sticky="ew", columnspan=3)
        self.rds_check = customtkinter.CTkCheckBox(master=self.master_frame, text="RDS?")
        self.rds_check.grid(column=4, row=1, padx=5)
        self.carrier_lbl = customtkinter.CTkLabel(master=self.master_frame, text="Carrier:")
        self.carrier_lbl.grid(column=0, row=2, sticky="e", padx=5, pady=5)
        self.carrier_entry = customtkinter.CTkEntry(master=self.master_frame)
        self.carrier_entry.grid(column=1, row=2, sticky="ew", columnspan=3)
        self.stereo_check = customtkinter.CTkCheckBox(master=self.master_frame, text="Stereo?")
        self.stereo_check.grid(column=4, row=2, padx=5)
        self.power_lbl = customtkinter.CTkLabel(master=self.master_frame, text="Strength (dBuV/m):")
        self.power_lbl.grid(column=0, row=3, sticky="e", padx=5, pady=5)
        self.power_entry = customtkinter.CTkEntry(master=self.master_frame)
        self.power_entry.grid(column=1, row=3, sticky="ew")
        self.azimuth_lbl = customtkinter.CTkLabel(master=self.master_frame, text="Azimuth (°):")
        self.azimuth_lbl.grid(column=2, row=3, sticky="e", padx=5)
        self.azimuth_entry = customtkinter.CTkEntry(master=self.master_frame)
        self.azimuth_entry.grid(column=3, row=3, sticky="ew")
        self.radiotext_check = customtkinter.CTkCheckBox(master=self.master_frame, text="RadioText?")
        self.radiotext_check.grid(column=4, row=3, padx=5)
        self.radiotext_lbl = customtkinter.CTkLabel(master=self.master_frame, text="Radio Text:")
        self.radiotext_lbl.grid(column=0, row=4, sticky="e", pady=5, padx=5)
        self.radiotext_entry = customtkinter.CTkEntry(master=self.master_frame)
        self.radiotext_entry.grid(column=1, row=4, sticky="ew", columnspan=4)
        self.clear_btn = customtkinter.CTkButton(master=self.master_frame, text="Clear form", fg_color="#ff6600",
                                                 hover_color="orange", text_color="black")
        self.clear_btn.grid(column=1, row=5, sticky="ew", columnspan=2, pady=5)
        #TODO Add a submit button
        #TODO Add a treeview to see the logged records

        #Column configuration for QTH selection frame
        self.qth_frame.columnconfigure(index=1, weight=1)
        self.qth_frame.columnconfigure(index=3, weight=1)

        #Column configuration for Master frame
        self.master_frame.columnconfigure(index=1, weight=1)
        self.master_frame.columnconfigure(index=3, weight=1)

        self.on_load()
    def get_freqs(self):
        #Generates a list of frequencies for the combobox
        low = 87.5
        self.frequencies = [str(low), ]
        while low < 107.9:
            low = low + 0.10
            ltp = (round(low, 2), )
            self.frequencies.append(str(ltp).replace("(", "").replace(",)",""))

    def save_qth(self):
        #Saves the QTH datas and resets the entries checking if the user wants to save data
        if messagebox.askyesno(title="Are you sure?", message="Are you sure you want to update QTH data?"):
            latitude = self.latitude_entry.get()
            longitude = self.longitude_entry.get()
            altitude = self.altitude_entry.get()
            qth_editor.QTHFileHandler(qth=[latitude, longitude, altitude])
        else:
            pass
        self.on_load()
        self.latitude_entry.configure(state="readonly")
        self.longitude_entry.configure(state="readonly")
        self.altitude_entry.configure(state="readonly")
        self.save_qth_btn.configure(state="disabled")
        self.edit_qth_btn.configure(state="normal")


    def edit_qth(self):
        #Enables the QTH entries
        self.latitude_entry.configure(state="normal")
        self.longitude_entry.configure(state="normal")
        self.altitude_entry.configure(state="normal")
        self.save_qth_btn.configure(state="normal")
        self.edit_qth_btn.configure(state="disabled")

    def on_load(self):
        #Initializes the interface
        self.latitude_entry.delete(0, END)
        self.longitude_entry.delete(0, END)
        self.altitude_entry.delete(0, END)
        qth = qth_editor.QTHFileHandler.read_qth_file(App).replace("'","").replace(" ","").split(",")
        self.latitude_entry.insert(0, qth[0])
        self.longitude_entry.insert(0, qth[1])
        self.altitude_entry.insert(0, qth[2])
        self.latitude_entry.configure(state="readonly")
        self.longitude_entry.configure(state="readonly")
        self.altitude_entry.configure(state="readonly")
        self.save_qth_btn.configure(state="disabled")
        #TODO Insert location function


app = App()
app.mainloop()