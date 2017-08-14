#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Authors:    Marcus Grum, Karsten Tauchert, Norbert Gronau
    Copyright:  University of Potsdam
                Department of Business Informatics, esp. Processes and Systems
    Name:       printplotpdf.py
    Description:
    Creates a PDF file depending on the User-Account and its correlating projects hence plots.
    Returns the "pdf" formatted Project_User_Date.pdf.
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
from Tkinter import Toplevel, Label
from tkMessageBox import showinfo
from matplotlib.backends.backend_pdf import PdfPages
from ResourcePath import resource_path
from gui.calculation.MatrixCalculation import MatrixCalculation
from gui.calculation.RankingCalculation import RankingCalculation
from gui.calculation.BenchmarkCalculation import BenchmarkCalculation
from gui.calculation.Riskassessment import RiskAssessment
from gui.calculation.KooperationstypCalculation import FormProxy
from ListProjects import ListProjects
from TitlePagePDF import TitlePagePDF
from time import strftime
from os import name, remove, system
from PyPDF2 import PdfFileMerger, PdfFileReader
from subprocess import call



class PrintPDF:

    def __init__(self, sqlaccess, parent,  project, account):
        self.sqlacc = sqlaccess
        self.project = project
        self.account = account
        self.parent = parent
        self.proj_id = self.project.getprojid()

        self.signal = 0
        self.counter = 0

        self.pdf_figures = []
        self.options_dict = {}
        self.dimensions = ["Matrix", "Ranking", "Ranking ALLE"]
        self.pdf_plots = {}
        self.pdf_plots["plots"] = ["Matrix", "Ranking", "Benchmarking"]

        self.pdf_plots["dimension"] = ["Chancen", "Risiken", "Chancen und Risiken"]
        self.pdf_plots["measure"] = [u"Vor Maßnahmen", u"Nach Maßnahmen"]

    def generate_pdf(self):
        """
        Opens a toplevel window to inform about creating the pdf file and starts/calls the creation.
        :return: 
        """
        self.plotting_msg = Toplevel(self.parent)
        self.plotting_msg.title("Plotting...")
        message = Label(self.plotting_msg, text="Bitte haben Sie einen Moment Geduld!\n\nIhre PDF wird gerade generiert",
                           font="Helvetica 10 bold", wraplength=360, justify='center')
        message.pack(fill='both', side='top', expand=1)
        self.parent.after(100, self.create_pdf)

    def create_pdf(self):
        """
        The actual creation. Creates a filename based on account and project, builds all plots and merges them into
        one pdf file, uncluding a title page and an appendix with projectinformation.
        :return:
        """
        date = strftime("%Y_%m_%d")
        title = TitlePagePDF(self.project, self.account)
        title.generate_title()

        proj_list = ListProjects(self.sqlacc, self.project, self.account)
        proj_list.generate_pdf()

        project_name = self.project.getprojname().encode('utf-8')
        project_name = project_name.replace(' ', '_')
        account_name = self.account.getemail().encode('utf-8')
        file_name = project_name + "_" + account_name + "_" + date + ".pdf"
        path_filename = resource_path("gui/filingarea/" + str(file_name))
        print(path_filename)
        self.options_dict["Benchmarking"] = "Alle Projekte"

        # **** Risikoeinschätzung ****
        risiko_eval = RiskAssessment(self.account)
        self.pdf_figures.append(risiko_eval.calculate_plot(self.signal))

        # **** Kooperationistyp ****
        formprox_eval = FormProxy(self.account)
        self.pdf_figures.append(formprox_eval.calculate_plot(self.signal))

        # ****  Matrix Calculation  ****
        matrix = MatrixCalculation(self.sqlacc, self.options_dict, self.project)
        self.pdf_figures.append(matrix.generatepdfplots("Chancen"))
        self.pdf_figures.append(matrix.generatepdfplots("Risiken"))
        self.pdf_figures.append(matrix.generatepdfplots("Chancen und Risiken"))

        # **** Ranking Calculation ****
        ranking = RankingCalculation(self.sqlacc, self.options_dict, self.project, self.account)
        self.pdf_figures.append(ranking.calculate_pdfplot())

        # **** Benchmarking Calculation ****
        benchmarking = BenchmarkCalculation(self.sqlacc, self.options_dict, self.project, self.account)
        self.pdf_figures.append(benchmarking.generatepdfplots("Chancen"))
        self.pdf_figures.append(benchmarking.generatepdfplots("Risiken"))
        self.pdf_figures.append(benchmarking.generatepdfplots("Chancen und Risiken"))

        # **** Creating PDF with plots ****
        path_plots = resource_path("gui/filingarea/od_plots.pdf")
        with PdfPages(path_plots, 'wb') as pp:
            for i in range(len(self.pdf_figures)):
                self.counter += 1
                print "i: " + str(i) + "  type: " + str(type(self.pdf_figures[i]))
                pp.savefig(self.pdf_figures[i])

        # **** Merge Title-Page and Plots-PDF ****
        merger = PdfFileMerger()
        if name == 'posix':
            # linux
            print("linux")
            merger.append(PdfFileReader(resource_path("gui/filingarea/plot_title.pdf")), 'rb')
            merger.append(PdfFileReader(path_plots), 'rb')
            merger.append(PdfFileReader(resource_path("gui/filingarea/project_list.pdf")), 'rb')
            # titlepage = PdfFileReader(file("plot_title.pdf"), 'rb')
            # plotpages = PdfFileReader(file(path_plots), 'rb')
            # listpage = PdfFileReader(file("project_list.pdf"), 'rb')
            # merger.append(titlepage)
            # merger.append(plotpages)
            # merger.append(listpage)
        elif name == 'nt':
            print("win")
            merger.append(PdfFileReader(resource_path("gui/filingarea/plot_title.pdf")), 'rb')
            merger.append(PdfFileReader(path_plots), 'rb')
            merger.append(PdfFileReader(resource_path("gui/filingarea/project_list.pdf")), 'rb')
            # merger.append(PdfFileReader("C:/opendarkness/code/plot_title.pdf"), 'rb')
            # merger.append(PdfFileReader("C:/opendarkness/code/od_plots.pdf"), 'rb')
            # merger.append(PdfFileReader("C:/opendarkness/code/project_list.pdf"), 'rb')
        else:
            # mac
            print("mac")
            merger.append(PdfFileReader(resource_path("gui\\filingarea\\plot_title.pdf")), 'rb')
            merger.append(PdfFileReader(path_plots), 'rb')
            merger.append(PdfFileReader(resource_path("gui\\filingarea\\project_list.pdf")), 'rb')
            # titlepage = PdfFileReader(file("gui/filingarea/plot_title.pdf"), 'rb')
            # plotpages = PdfFileReader(file("gui/filingarea/od_plots.pdf"), 'rb')
            # listpage = PdfFileReader(file("gui/filingarea/project_list.pdf"), 'rb')
            # merger.append(titlepage)
            # merger.append(plotpages)
            # merger.append(listpage)

        # If path_filename allready exists remove and start writning again.
        try:
            print("Try")
            merger.write(path_filename)
        except Exception as e:
            print("Except")
            remove(path_filename)
            merger.write(file_name)

        #   Tries to remove the helper files. Just in case something would go wrong or  it
        #   woult be the first iteration of creating the pdf.
        try:
            remove(resource_path("gui/filingarea/plot_title.pdf"))
            remove(resource_path("gui/filingarea/project_list.pdf"))
        except:
            pass

        # **** PDF durch das Betriebssystem öffnen ****
        # manualpath = resource_path("gui/filingarea/Handbuch_OD_Tool.pdf")
        call(['open', path_filename])

        #open_cmd = "open " + str(path_filename)
        #system(open_cmd)

        # import webbrowser
        # webbrowser.open_new_tab(path_filename)
        # if name == 'nt':
        #     open_cmd = "start " + str(path_filename)
        #     system(open_cmd)
        # elif name == 'posix':
        #
        #
        #     open_cmd = "open " + str(path_filename)
        #     system(open_cmd)
        #     # subprocess.Popen(str(path_filename), shell=True)
        #     # open_cmd = "xdg-open " + str(path_filename)
        #     # system(open_cmd)
        # else:
        #     open_cmd = "open " + str(path_filename)
        #     system(open_cmd)
        #     # subprocess.Popen(str(path_filename), shell=True)
        #     # open_cmd = "open " + str(path_filename)
        #     # system(open_cmd)

        self.plotting_msg.destroy()
        showinfo("PDF erstellt", "Herzlichen Glückwunsch, Ihre PDF wurde erfolgreich erstellt.\n"
                                 "Sie können jetzt die PDF an einen Ort Ihrer Wahl speichern.")
