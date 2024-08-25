#main.py
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
import tkinter
from tkinter import messagebox, END, SUNKEN
from tkinter.constants import BOTTOM

import customtkinter
import CTkMenuBar
from CTkScrollableDropdown import *
from tkinter import ttk

import qth_editor


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_appearance_mode("dark")
        self.geometry("1024x768")
        self.title("FMRadioLog")
        self.frequencies = ["", ]
        self.fx_id = 0
        #TODO Create an icon

        #Menubar
        #TODO Add menu functions
        self.main_menubar = CTkMenuBar.CTkMenuBar(master=self)
        self.file_btn = self.main_menubar.add_cascade(text="File")

        #File Dropdown
        self.file_cascade = CTkMenuBar.CustomDropdownMenu(widget=self.file_btn)
        self.file_cascade.add_option(option="Export...", command=self.export_log)
        self.file_cascade.add_separator()
        self.file_cascade.add_option(option="Exit", command=self.close_app)


        #QTH Selection Block
        self.qth_lbl = customtkinter.CTkLabel(master=self, text="QTH Selection")
        self.qth_lbl.pack()
        self.qth_frame = customtkinter.CTkFrame(master=self)
        self.qth_frame.pack(fill="x", padx=5, pady=5)
        #---------------------------------------------------------------------------------------------------------------
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
        self.location_lbl = customtkinter.CTkLabel(master=self.qth_frame, text="Location:")
        self.location_lbl.grid(column=0, row=2, sticky="e", padx=5)
        self.location_entry = customtkinter.CTkEntry(master=self.qth_frame)
        self.location_entry.grid(column=1, row=2, sticky="ew", columnspan="5", padx=5, pady=5)
        self.edit_qth_btn = customtkinter.CTkButton(master=self.qth_frame, text="Edit QTH", command=self.edit_qth)
        self.edit_qth_btn.grid(column=6, row=1, sticky="ew", padx=5, pady=5)
        self.save_qth_btn = customtkinter.CTkButton(master=self.qth_frame, text="Save QTH", command=self.save_qth)
        self.save_qth_btn.grid(column=6, row=2, sticky="ew", padx=5, pady=5)

        # Master Block
        self.name_lbl = customtkinter.CTkLabel(master=self, text="Frequency data")
        self.name_lbl.pack()
        self.master_frame = customtkinter.CTkFrame(master=self)
        self.master_frame.pack(fill="x", padx=5, pady=5)
        #---------------------------------------------------------------------------------------------------------------
        self.frequency_lbl = customtkinter.CTkLabel(master=self.master_frame, text="Frequency:")
        self.frequency_lbl.grid(column=0, row=0, sticky="e", padx=5, pady=5)
        self.get_freqs()
        self.frequency_cbx = customtkinter.CTkComboBox(master=self.master_frame)
        self.frequency_cbx.grid(column=1, row=0, sticky="w")
        CTkScrollableDropdown(self.frequency_cbx, values=self.frequencies, justify="left")
        self.frequency_cbx.set("-")
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
        self.clear_btn = customtkinter.CTkButton(master=self.master_frame, text="Clear form", fg_color="#c24404",
                                                 hover_color="#de5009", command=self.clear_form)
        self.clear_btn.grid(column=1, row=5, sticky="ew", columnspan=2, pady=5)
        self.submit_btn = customtkinter.CTkButton(master=self.master_frame, text="Submit", fg_color="#00ac4e",
                                                  hover_color="#04c25A", command=self.insert_freq)
        self.submit_btn.grid(column=3, row=5, sticky="ew", columnspan=2)
        #TODO Add submit functions

        #Logger block
        self.logger_title_lbl = customtkinter.CTkLabel(master=self, text="Log table")
        self.logger_title_lbl.pack()
        self.logger_frame = customtkinter.CTkFrame(master=self)
        self.logger_frame.pack(fill="both", expand=True, padx=5, pady=5)
        #---------------------------------------------------------------------------------------------------------------
        #Treeview customisation
        bg_color = self._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"])
        text_color = self._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkLabel"]["text_color"])
        selected_color = self._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkButton"]["fg_color"])
        treestyle = ttk.Style()
        treestyle.theme_use('default')
        treestyle.configure("Treeview", background=bg_color, foreground=text_color, fieldbackground=bg_color,
                            borderwidth=0)
        treestyle.map('Treeview', background=[('selected', bg_color)], foreground=[('selected', selected_color)])
        self.bind("<<TreeviewSelect>>", lambda event: self.focus_set())
        self.logger_tv = ttk.Treeview(master=self.logger_frame, columns=("frequency", "rds", "rds?", "carrier", "pilot",
                                                                         "strength", "azimuth", "rt?", "rt"))
        self.logger_tv.grid(column=0, row=0, sticky="nsew", padx=5, pady=5)

        #Sets treeview headings
        self.logger_tv.heading("frequency", text="Frequency")
        self.logger_tv.heading("rds", text="PS")
        self.logger_tv.heading("rds?", text="RDS")
        self.logger_tv.heading("carrier", text="Carrier")
        self.logger_tv.heading("pilot", text="Stereo")
        self.logger_tv.heading("strength", text="Strength")
        self.logger_tv.heading("azimuth", text="Azimuth")
        self.logger_tv.heading("rt?", text="RadioText")
        self.logger_tv.heading("rt", text="RT Text")

        #Sets treeview column width
        self.logger_tv.column("#0", minwidth=0, width=0)
        self.logger_tv.column("frequency", minwidth=0, width=100)
        self.logger_tv.column("rds", minwidth=0, width=100)
        self.logger_tv.column("rds?", minwidth=0, width=20)
        self.logger_tv.column("carrier", minwidth=0, width=100)
        self.logger_tv.column("pilot", minwidth=0, width=20)
        self.logger_tv.column("strength", minwidth=0, width=100)
        self.logger_tv.column("azimuth", minwidth=0, width=100)
        self.logger_tv.column("rt?", minwidth=0, width=20)
        self.logger_tv.column("rt", minwidth=0, width=100)
        #Hides the first unused column
        self.logger_tv["show"] = "headings"

        #Status bar
        self.status_bar = tkinter.Label(master=self, text="Ready", bd=1, relief=SUNKEN, anchor="w",
                                        background="#333", foreground="#fff")
        self.status_bar.pack(side=BOTTOM, fill="x", ipadx=5)

        #Column configuration for QTH selection frame
        self.qth_frame.columnconfigure(index=1, weight=1)
        self.qth_frame.columnconfigure(index=3, weight=1)

        #Column configuration for Master frame
        self.master_frame.columnconfigure(index=1, weight=1)
        self.master_frame.columnconfigure(index=3, weight=1)

        #Column and row configuration for Logger frame
        self.logger_frame.columnconfigure(index=0, weight=1)
        self.logger_frame.rowconfigure(index=0, weight=1)

        self.tab_order()
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
        self.status_bar.configure(text="Saving...")
        if messagebox.askyesno(title="Are you sure?", message="Are you sure you want to update QTH data?"):
            latitude = self.latitude_entry.get()
            longitude = self.longitude_entry.get()
            altitude = self.altitude_entry.get()
            location = self.location_entry.get().replace(" ","_")
            qth_editor.QTHFileHandler(switch=0, qth=[latitude, longitude, altitude, location])
        else:
            pass
        self.on_load()
        self.latitude_entry.configure(state="readonly")
        self.longitude_entry.configure(state="readonly")
        self.altitude_entry.configure(state="readonly")
        self.save_qth_btn.configure(state="disabled")
        self.edit_qth_btn.configure(state="normal")
        self.status_bar.configure(text="Ready")


    def edit_qth(self):
        #Enables the QTH entries
        self.status_bar.configure(text="Editing QTH, waiting for Save command")
        self.latitude_entry.configure(state="normal")
        self.longitude_entry.configure(state="normal")
        self.altitude_entry.configure(state="normal")
        self.location_entry.configure(state="normal")
        self.save_qth_btn.configure(state="normal")
        self.edit_qth_btn.configure(state="disabled")

    def on_load(self):
        #Initializes the interface
        self.status_bar.configure(text="Loading...")
        self.latitude_entry.delete(0, END)
        self.longitude_entry.delete(0, END)
        self.altitude_entry.delete(0, END)
        self.location_entry.delete(0, END)
        qth = qth_editor.QTHFileHandler().read_qth_file().replace("'","").replace(" ","").replace("_"," ").split(",")
        self.latitude_entry.insert(0, qth[0])
        self.longitude_entry.insert(0, qth[1])
        self.altitude_entry.insert(0, qth[2])
        self.location_entry.insert(0, qth[3])
        self.latitude_entry.configure(state="readonly")
        self.longitude_entry.configure(state="readonly")
        self.altitude_entry.configure(state="readonly")
        self.save_qth_btn.configure(state="disabled")
        self.location_entry.configure(state="readonly")
        self.status_bar.configure(text="Ready")

    def insert_freq(self):
        self.status_bar.configure(text="Writing...")
        self.logger_tv.insert("", END, values=(self.frequency_cbx.get(),
                                               self.rds_entry.get(),self.rds_check.get(),
                                               self.carrier_entry.get(), self.stereo_check.get(),
                                               self.power_entry.get(), self.azimuth_entry.get(),
                                               self.radiotext_check.get(), self.radiotext_entry.get()))
        self.fx_id = self.fx_id + 1
        self.clear_form()
        self.status_bar.configure(text="Ready")

    def export_log(self):
        #TODO Complete export log function
        self.status_bar.configure(text="Exporting")
        for line in self.logger_tv.get_children():
            values = self.logger_tv.item(line)["values"]
            print(values)
        self.status_bar.configure(text="Ready")

    def clear_form(self):
        #Totally cleans the form
        self.frequency_cbx.set("-")
        self.rds_entry.delete(0, END)
        self.carrier_entry.delete(0, END)
        self.power_entry.delete(0, END)
        self.azimuth_entry.delete(0, END)
        self.radiotext_entry.delete(0, END)
        self.rds_check.deselect()
        self.stereo_check.deselect()
        self.radiotext_check.deselect()
        self.frequency_cbx.focus()

    def tab_order(self):
        #Sets the tab order for the frames
        self.frequency_cbx.focus()
        freq_widgets = [self.frequency_cbx, self.rds_entry, self.rds_check, self.carrier_entry, self.stereo_check,
                        self.power_entry, self.azimuth_entry, self.radiotext_check, self.radiotext_entry,
                        self.submit_btn]
        qth_widgets = [self.latitude_entry, self.longitude_entry, self.altitude_entry, self.location_entry,
                       self.save_qth_btn]

        for w in freq_widgets:
            w.lift()

        for w in qth_widgets:
            w.lift()

    def close_app(self):
        if messagebox.askyesno(title="Close the app?", message="Are you sure you want to exit the app?"):
            self.quit()


app = App()
app.mainloop()