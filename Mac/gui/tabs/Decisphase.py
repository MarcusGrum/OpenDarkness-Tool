#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Authors:    Marcus Grum, Karsten Tauchert, Norbert Gronau
    Copyright:  University of Potsdam
                Department of Business Informatics, esp. Processes and Systems
    Name:       recomphase.py
    Description:
    This is the Class that creates a window-frame for showing a final message and a proposal for printing out
    the plots as a pdf file. (csv soon!).
    The frame is embedded into the Notebook-Tabs of created by the OD_Tool_Class.py.
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
# import Tkinter as tk
from Tkinter import Frame, Label, Button, Toplevel
from gui.modules.PrintPDFPlot import PrintPDF
# from module.printplotpdf import PrintPDF
# import ttk
# import time
# import tkMessageBox as tkmb


class Decisphase():

    def __init__(self, sqlaccess, parent, account, project):
        # self.local_bind_p = local_bind_p
        self.sqlacc = sqlaccess
        self.parent = parent
        self.top_frame = Frame(self.parent, width=800, height=450)
        self.top_frame.pack(side='top', fill='both', expand=1)

        self.account = account
        self.project = project

        self.createframe()

    def createframe(self):

        text=("Wir bedanken uns für Ihre Eingabe und der Bearbeitung des Fragenkatalogs. "
              "Alle Ihre relevanten Informationen über das Projekt wurden verarbeitet.\n"
              "Sie haben jetzt die Wahl Ihre Plots als eine PDF-Datei speichern zu können, "
              "um sie komfortabel drucken und verschicken zu können")

        title = Label(self.top_frame, text="Vielen Dank!", fg="black", justify='left', font="Helvetica 16 bold")
        title.grid(row=1, column=1, pady=5, padx=5, sticky='w')

        message = Label(self.top_frame, text=text, wraplength=600, justify='left', fg="black", font="Helvetica 12")
        message.grid(row=2, column=1, pady=20, sticky='w')

        Button(self.top_frame, text='PDF generieren', font="Helvetica 12",
                  command=self.print_graphs).grid(row=3, column=1, pady=5, sticky='w')

    def print_graphs(self):

        self.pdf_plot = PrintPDF(self.sqlacc, self.parent, self.project, self.account)
        self.pdf_plot.generate_pdf()

    def create_progress(self):

        self.topwindow = Toplevel(self.parent)
        self.topwindow.title("PDF Generierung")
        message = Label(self.topwindow, text="PDF wird generiert, bitte haben Sie einen Moment Geduld",
                           font="Helvetica 12 italic", wraplength=300, justify='center')
        message.pack(side='top', fill='both', expand=1)

    def generate_pdf(self):

        self.pdf_plot = PrintPDF(self.sqlacc, self.parent, self.project, self.account)
        self.pdf_plot.generate_pdf()

    def check_status(self):
        if self.pdf_plot.status == False:
            self.topwindow.destroy()
            # print "Fuck off"
