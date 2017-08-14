#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

    Author:     Marcus Grum, Karsten Tauchert, Norbert Gronau
    Copyright:  University of Potsdam
                Department of Business Informatics, esp. Processes and Systems
    Name:       OpenDarkness.py
    Description:
    This is the starter for the OpenDarkness Tool.
"""
"""
OpenDarkness Tool, Support for making decisions for innovations by asking questions.
Copyright (C) 2016/2017 Marcus Grum, Karsten Tauchert, Norbert Gronau

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Contact:
M. Grum, K. Tauchert und N. Gronau
Lehrstuhl fuer Wirtschaftsinformatik, insbesondere Prozesse und Systeme
Universitaet Potsdam
August-Bebel-Straße 89
14482 Potsdam
Telefon: +49 331 977 3379
Fax: +49 331 977 3406
E-Mail: norbert.gronau@wi.uni-potsdam.de
E-Mail: marcus.grum@wi.uni-potsdam.de
E-Mail: karsten.tauchert@wi.uni-potsdam.de
"""
from Tkinter import Tk, Frame, Label
from ttk import Frame, Label

from PIL import Image, ImageTk
from os import path
import sys
from gui.modules.ResourcePath import resource_path
VERSION = "2.351"


class Main:

    def __init__(self, master):
        self.master = master
        self.master.title("OpenDarkness Tool "+VERSION)
        self.master.iconbitmap(resource_path("gui\\images\\OD_icon.ico"))
        self.windows = {}
        self.startinglogo()

    def startinglogo(self):
        """
        Just a logo to appear while loading the gui.
        :return:
        """
        self.windows["starter"] = Frame(self.master, width=330, height=260)
        self.windows["starter"].pack(expand=1, fill='both')
        logopath = resource_path("gui\\images\\OD_logo_long.png")
        load = Image.open(logopath)
        logo_od = ImageTk.PhotoImage(load)
        logopen = Label(self.windows["starter"], image=logo_od)
        logopen.image = logo_od
        logopen.grid(row=1, column=0, sticky='we')

        Label(self.windows["starter"], text="Version "+VERSION, font="Helvetica 8").grid(row=2, column=0, sticky='e')
        Label(self.windows["starter"], text="\n\nBitte haben Sie einen Moment Geduld!\nDas Tool wird geladen...\n",
              wraplength=320, font="Helvetica 12", justify='center').grid(row=3, column=0, sticky='we', padx=40)
        self.master.after(100, self.call_gui)

    def call_gui(self):
        """
        Starts the Gui itself.
        :return: 
        """
        import gui.ODGui as Gui
        self.windows["starter"].destroy()
        self.master.after(100)
        toolgui = Gui.ODGui(self.master)
        self.master.protocol("WM_DELETE_WINDOW", toolgui.exitapp)


if __name__ == "__main__":
    root = Tk()
    root.title("OpenDarkness Tool "+VERSION)
    root.geometry("+10+30")
    Main(root)
    root.mainloop()

