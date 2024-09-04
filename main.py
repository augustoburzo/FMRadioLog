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
import locale
import sys
import tkinter as tk

import ttkbootstrap as ttk
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from tkinter import messagebox, END, SUNKEN, font
from tkinter.constants import BOTTOM, NORMAL, DISABLED

import qth_editor
from constants import *
from file_editor import FileHandler

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        locale.setlocale(locale.LC_ALL, '')
        Style("litera")
        self.overrideredirect(False)
        self.geometry("1024x768+20+20")
        self.title("FMRadioLog")

        self.iconbitmap("icon.ico")

        self.frequencies = ["",]
        self.fx_id = None

        #Menu bar
        self.menuframe = ttk.Frame(self)
        self.menubar = ttk.Menu(self.menuframe)

        #File menu
        self.filemenu = ttk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(menu=self.filemenu, label="File")
        self.filemenu.add_command(
            label="Load Bandscan...",
            accelerator="Ctrl+L",
            command=self.load_bandscan
        )
        self.filemenu.add_command(
            label="Save Bandscan...",
            accelerator="Ctrl+S",
            command=self.save_bandscan
        )
        self.filemenu.add_separator()
        self.filemenu.add_command(
            label="Export Bandscan...",
            accelerator="Ctrl+E",
            command=self.export_log
        )
        self.filemenu.add_separator()
        self.filemenu.add_command(
            label="Exit",
            accelerator="Alt+F4",
            command=self.destroy
        )

        self.config(menu=self.menubar)
        #TODO Create an icon


        #QTH Selection Block
        self.qth_lbl = ttk.Label(master=self, text="QTH Selection")
        self.qth_lbl.pack()
        self.qth_frame = ttk.Frame(master=self)
        self.qth_frame.pack(fill="x", padx=5, pady=5)
        #---------------------------------------------------------------------------------------------------------------
        self.latitude_lbl = ttk.Label(master=self.qth_frame, text="Latitude:")
        self.latitude_lbl.grid(column=0, row=1, sticky="e", padx=5)
        self.latitude_entry = ttk.Entry(master=self.qth_frame)
        self.latitude_entry.grid(column=1, row=1, sticky="ew", pady=5)
        self.longitude_lbl = ttk.Label(master=self.qth_frame, text="Longitude:")
        self.longitude_lbl.grid(column=2, row=1, sticky="e", padx=5)
        self.longitude_entry = ttk.Entry(master=self.qth_frame)
        self.longitude_entry.grid(column=3, row=1, sticky="ew", padx=5, pady=5)
        self.altitude_lbl= ttk.Label(master=self.qth_frame, text="Altitude:")
        self.altitude_lbl.grid(column=4, row=1, sticky="e", padx=5)
        self.altitude_entry = ttk.Entry(master=self.qth_frame)
        self.altitude_entry.grid(column=5, row=1, sticky="ew")
        self.location_lbl = ttk.Label(master=self.qth_frame, text="Location:")
        self.location_lbl.grid(column=0, row=2, sticky="e", padx=5)
        self.location_entry = ttk.Entry(master=self.qth_frame)
        self.location_entry.grid(column=1, row=2, sticky="ew", columnspan=5, pady=5)
        self.edit_qth_btn = ttk.Button(master=self.qth_frame, text="Edit QTH", command=self.edit_qth, style=WARNING)
        self.edit_qth_btn.grid(column=6, row=1, sticky="ew", padx=5, pady=5)
        self.save_qth_btn = ttk.Button(master=self.qth_frame, text="Save QTH", command=self.save_qth, style=DANGER)
        self.save_qth_btn.grid(column=6, row=2, sticky="ew", padx=5, pady=5)

        # Master Block
        self.name_lbl = ttk.Label(master=self, text="Frequency data")
        self.name_lbl.pack()
        self.master_frame = ttk.Frame(master=self)
        self.master_frame.pack(fill="x", padx=5, pady=5)
        #---------------------------------------------------------------------------------------------------------------
        self.frequency_lbl = ttk.Label(master=self.master_frame, text="Frequency:")
        self.frequency_lbl.grid(column=0, row=0, sticky="e", padx=5, pady=5)
        self.get_freqs()
        self.frequency_cbx = ttk.Combobox(master=self.master_frame, values=self.frequencies)
        self.frequency_cbx.set(value=87.5)
        self.frequency_cbx.config(state=READONLY)
        self.frequency_cbx.grid(column=1, row=0, sticky="w", pady=5)
        self.rds_lbl = ttk.Label(master=self.master_frame, text="RDS:")
        self.rds_lbl.grid(column=0, row=1, sticky="e", padx=5, pady=5)
        self.rds_entry = ttk.Entry(master=self.master_frame)
        self.rds_entry.grid(column=1, row=1, sticky="ew", columnspan=3, pady=5)
        self.rds_value = tk.BooleanVar()
        self.rds_check = ttk.Checkbutton(master=self.master_frame, text="RDS?", variable=self.rds_value)
        self.rds_check.grid(column=4, row=1, padx=5, sticky="ew", ipady=5)
        self.carrier_lbl = ttk.Label(master=self.master_frame, text="Carrier:")
        self.carrier_lbl.grid(column=0, row=2, sticky="e", padx=5, pady=5)
        self.carrier_entry = ttk.Entry(master=self.master_frame)
        self.carrier_entry.grid(column=1, row=2, sticky="ew", columnspan=3, pady=5)
        self.stereo_value = tk.BooleanVar()
        self.stereo_check = ttk.Checkbutton(master=self.master_frame, text="Stereo?", variable=self.stereo_value)
        self.stereo_check.grid(column=4, row=2, padx=5, sticky="ew", ipady=5)
        self.power_lbl = ttk.Label(master=self.master_frame, text="Strength (dBuV/m):")
        self.power_lbl.grid(column=0, row=3, sticky="e", padx=5, pady=5)
        self.power_entry = ttk.Entry(master=self.master_frame)
        self.power_entry.grid(column=1, row=3, sticky="ew", pady=5)
        self.azimuth_lbl = ttk.Label(master=self.master_frame, text="Azimuth (°):")
        self.azimuth_lbl.grid(column=2, row=3, sticky="e", padx=5)
        self.azimuth_entry = ttk.Entry(master=self.master_frame)
        self.azimuth_entry.grid(column=3, row=3, sticky="ew", pady=5)
        self.radiotext_value = tk.BooleanVar()
        self.radiotext_check = ttk.Checkbutton(master=self.master_frame, text="RadioText?",
                                               variable=self.radiotext_value)
        self.radiotext_check.grid(column=4, row=3, padx=5, sticky="ew", ipady=5)
        self.radiotext_lbl = ttk.Label(master=self.master_frame, text="Radio Text:")
        self.radiotext_lbl.grid(column=0, row=4, sticky="e", pady=5, padx=5)
        self.radiotext_entry = ttk.Entry(master=self.master_frame)
        self.radiotext_entry.grid(column=1, row=4, sticky="ew", columnspan=4, pady=5)
        self.clear_btn = ttk.Button(master=self.master_frame, text="Clear form", command=self.clear_form,
                                    style=WARNING)
        self.clear_btn.grid(column=1, row=5, sticky="ew", columnspan=2, pady=5)
        self.submit_btn = ttk.Button(master=self.master_frame, text="Submit", command=self.insert_freq,
                                     style=SUCCESS)
        self.submit_btn.grid(column=3, row=5, sticky="ew", columnspan=2, pady=5)
        self.delete_row_btn = ttk.Button(master=self.master_frame, text="Delete record", command=self.delete_row,
                                         style=DANGER)
        self.delete_row_btn.grid(column=1, row=6, sticky="ew", columnspan=4, pady=5)
        self.delete_row_btn.configure(state=DISABLED)

        #Logger block
        self.logger_title_lbl = ttk.Label(master=self, text="Log table")
        self.logger_title_lbl.pack()
        self.logger_frame = ttk.Frame(master=self)
        self.logger_frame.pack(fill="both", expand=True, padx=5, pady=5)
        #---------------------------------------------------------------------------------------------------------------
        #Treeview customisation
        #TODO Add edit function to single line
        self.logger_tv = ttk.Treeview(master=self.logger_frame, columns=("frequency", "rds", "rds?", "carrier", "pilot",
                                                                         "strength", "azimuth", "rt?", "rt"))
        self.logger_tv.grid(column=0, row=0, sticky="nsew", padx=5, pady=5)

        #Sets treeview headings
        self.logger_tv.heading(FREQUENCY, text="Frequency")
        self.logger_tv.heading(RDS, text="PS")
        self.logger_tv.heading(RDS_CHECK, text="RDS")
        self.logger_tv.heading(CARRIER, text="Carrier")
        self.logger_tv.heading(PILOT_CHECK, text="Stereo")
        self.logger_tv.heading(STRENGTH, text="Strength")
        self.logger_tv.heading(AZIMUTH, text="Azimuth")
        self.logger_tv.heading(RADIOTEXT_CHECK, text="RadioText")
        self.logger_tv.heading(RADIOTEXT, text="RT Text")

        #Sets treeview column width
        self.logger_tv.column("#0", minwidth=0, width=0)
        self.logger_tv.column(FREQUENCY, minwidth=0, width=100)
        self.logger_tv.column(RDS, minwidth=0, width=100)
        self.logger_tv.column(RDS_CHECK, minwidth=0, width=20)
        self.logger_tv.column(CARRIER, minwidth=0, width=100)
        self.logger_tv.column(PILOT_CHECK, minwidth=0, width=20)
        self.logger_tv.column(STRENGTH, minwidth=0, width=100)
        self.logger_tv.column(AZIMUTH, minwidth=0, width=100)
        self.logger_tv.column(RADIOTEXT_CHECK, minwidth=0, width=20)
        self.logger_tv.column(RADIOTEXT, minwidth=0, width=100)
        #Hides the first unused column
        self.logger_tv["show"] = "headings"
        self.logger_tv.bind("<Double-1>", self.on_treeview_click)

        #Status bar
        self.status_bar = ttk.Label(master=self, text="Ready", relief=SUNKEN, anchor="w")
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

        self.protocol("WM_DELETE_WINDOW", self.close_app)
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
        self.status_bar.configure(text=STATUS_WRITE)
        if messagebox.askyesno(title="Are you sure?", message="Are you sure you want to update QTH data?"):
            latitude = self.latitude_entry.get()
            longitude = self.longitude_entry.get()
            altitude = self.altitude_entry.get()
            location = self.location_entry.get().replace(" ","_")
            qth_editor.QTHFileHandler(switch=0, qth=[latitude, longitude, altitude, location])
        else:
            pass
        self.on_load()
        self.latitude_entry.configure(state=READONLY)
        self.longitude_entry.configure(state=READONLY)
        self.altitude_entry.configure(state=READONLY)
        self.save_qth_btn.configure(state=DISABLED)
        self.edit_qth_btn.configure(state=NORMAL)
        self.status_bar.configure(text=STATUS_READY)


    def edit_qth(self):
        #Enables the QTH entries
        self.status_bar.configure(text=STATUS_EDIT)
        self.latitude_entry.configure(state=NORMAL)
        self.longitude_entry.configure(state=NORMAL)
        self.altitude_entry.configure(state=NORMAL)
        self.location_entry.configure(state=NORMAL)
        self.save_qth_btn.configure(state=NORMAL)
        self.edit_qth_btn.configure(state=DISABLED)

    def on_load(self):
        #Initializes the interface
        self.status_bar.configure(text=STATUS_LOAD)
        self.latitude_entry.delete(0, END)
        self.longitude_entry.delete(0, END)
        self.altitude_entry.delete(0, END)
        self.location_entry.delete(0, END)
        qth = qth_editor.QTHFileHandler().read_qth_file().replace("'","").replace(" ","").replace("_"," ").split(",")
        self.latitude_entry.insert(0, qth[0])
        self.longitude_entry.insert(0, qth[1])
        self.altitude_entry.insert(0, qth[2])
        self.location_entry.insert(0, qth[3])
        self.latitude_entry.configure(state=READONLY)
        self.longitude_entry.configure(state=READONLY)
        self.altitude_entry.configure(state=READONLY)
        self.save_qth_btn.configure(state=DISABLED)
        self.location_entry.configure(state=READONLY)
        self.delete_row_btn.configure(state=DISABLED)
        self.status_bar.configure(text=STATUS_READY)

    def insert_freq(self):
        #Adds a record to the log treeview
        if self.fx_id is None and self.carrier_entry.get() != "":
            self.status_bar.configure(text=STATUS_WRITE)
            self.logger_tv.insert("", END, values=(self.frequency_cbx.get(),
                                                   self.rds_entry.get(),self.rds_value.get(),
                                                   self.carrier_entry.get(), self.stereo_value.get(),
                                                   self.power_entry.get(), self.azimuth_entry.get(),
                                                   self.radiotext_value.get(), self.radiotext_entry.get()))
        elif self.fx_id is not None and self.carrier_entry.get() != "":
            self.status_bar.configure(text=STATUS_WRITE)
            self.logger_tv.item(self.fx_id, values=(self.frequency_cbx.get(),
                                                   self.rds_entry.get(),self.rds_value.get(),
                                                   self.carrier_entry.get(), self.stereo_value.get(),
                                                   self.power_entry.get(), self.azimuth_entry.get(),
                                                   self.radiotext_value.get(), self.radiotext_entry.get()))
        else: messagebox.showerror(title="No data", message="Too few data to submit")

        self.clear_form()
        self.sort_treeview()
        self.delete_row_btn.configure(state=DISABLED)
        self.status_bar.configure(text=STATUS_READY)

    def export_log(self):
        #Exports a csv file with all the records
        #TODO Add JSON function
        self.status_bar.configure(text=STATUS_EXPORT)
        file = (f"LATITUDE:;{self.latitude_entry.get()};LONGITUDE:;{self.longitude_entry.get()};"
                f"ALTITUDE:;{self.altitude_entry.get()};LOCATION:;{self.location_entry.get()}\n\n"
                f"FREQUENCY;RDS;RDS?;CARRIER;STEREO?;INDEX;AZIMUTH;RADIOTEXT?;RADIOTEXT\n")
        for line in self.logger_tv.get_children():
            values = self.logger_tv.item(line)["values"]
            print(values)
            for value in values:
                file = file + f"{value};"
            file = file + "\n"

        FileHandler(mode="export_csv", file=file)
        self.status_bar.configure(text=STATUS_READY)

    def load_bandscan(self, file=None):
        self.status_bar.configure(text=STATUS_LOAD)
        #Loads bandscan file data and inserts data in the GUI
        file = FileHandler.read_file(file)
        count = 0
        #Enables location entries
        self.latitude_entry.configure(state=NORMAL)
        self.longitude_entry.configure(state=NORMAL)
        self.altitude_entry.configure(state=NORMAL)
        self.location_entry.configure(state=NORMAL)
        #Initializes entries
        self.latitude_entry.delete(0, END)
        self.longitude_entry.delete(0, END)
        self.altitude_entry.delete(0, END)
        self.location_entry.delete(0, END)
        #Inserts the retrieved data
        self.latitude_entry.insert(0, file[0][LATITUDE])
        self.longitude_entry.insert(0, file[0][LONGITUDE])
        self.altitude_entry.insert(0, file[0][ALTITUDE])
        self.location_entry.insert(0, file[0][LOCATION])
        del file[0]
        self.logger_tv.delete(*self.logger_tv.get_children())
        for record in file:
            self.logger_tv.insert('', END, iid=count, text="", values=(record[FREQUENCY], record[RDS],
                                                                       record[RDS_CHECK],record[CARRIER],
                                                                       record[PILOT_CHECK], record[STRENGTH],
                                                                       record[AZIMUTH], record[RADIOTEXT_CHECK],
                                                                       record[RADIOTEXT]))
            count = count + 1
        self.sort_treeview()
        self.status_bar.configure(text=STATUS_READY)

    def save_bandscan(self):
        #Saves the bandscan file using the FileHandler() function
        self.status_bar.configure(text=STATUS_WRITE)
        location = {LATITUDE:self.latitude_entry.get(), LONGITUDE:self.longitude_entry.get(),
                ALTITUDE:self.altitude_entry.get(), LOCATION:self.location_entry.get()}
        values = [location]
        for x in self.logger_tv.get_children():
            value_dict = {}

            for col, item in zip(self.logger_tv["columns"], self.logger_tv.item(x)["values"]):
                value_dict[col] = item

            values.append(value_dict)

        FileHandler(mode="write", file=values)
        self.status_bar.configure(text=STATUS_READY)

    def clear_form(self):
        #Totally cleans the form
        self.frequency_cbx.set("87.5")
        self.rds_entry.delete(0, END)
        self.carrier_entry.delete(0, END)
        self.power_entry.delete(0, END)
        self.azimuth_entry.delete(0, END)
        self.radiotext_entry.delete(0, END)
        self.rds_check.selection_clear()
        self.stereo_check.selection_clear()
        self.radiotext_check.selection_clear()
        self.frequency_cbx.focus()
        self.delete_row_btn.configure(state=DISABLED)


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
            self.destroy()
            self.quit()

    def sort_treeview(self):
        #Sorts the treeview based on the records frequency
        rows = [(float(self.logger_tv.set(item, "frequency").lower()), item)
                for item in self.logger_tv.get_children("")]
        rows = sorted(rows)
        for index, (values, item) in enumerate(rows):
            self.logger_tv.move(item, "", index)

    def on_treeview_click(self, event=None):
        #Enables the treeview click to populate the form and edit the selected record
        item = self.logger_tv.identify('row', event.x, event.y)
        self.clear_form()
        self.fx_id = self.logger_tv.selection()[0]
        self.frequency_cbx.set(self.logger_tv.item(item, "values")[0])
        self.rds_entry.insert(0, self.logger_tv.item(item, "values")[1])
        self.rds_value.set(self.logger_tv.item(item, "values")[2])
        self.carrier_entry.insert(0, self.logger_tv.item(item, "values")[3])
        self.stereo_value.set(self.logger_tv.item(item, "values")[4])
        self.power_entry.insert(0, self.logger_tv.item(item, "values")[5])
        self.azimuth_entry.insert(0, self.logger_tv.item(item, "values")[6])
        self.radiotext_value.set(self.logger_tv.item(item, "values")[7])
        self.radiotext_entry.insert(0, self.logger_tv.item(item, "values")[8])
        self.delete_row_btn.configure(state=NORMAL)

    def delete_row(self):
        self.logger_tv.delete(self.fx_id)
        self.clear_form()



app = App()
app.mainloop()