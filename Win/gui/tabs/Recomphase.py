#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Authors:    Marcus Grum, Karsten Tauchert, Norbert Gronau
    Copyright:  University of Potsdam
                Department of Business Informatics, esp. Processes and Systems
    Name:       Recomphase.py
    Description:
    This is the Class that creates a window-frame for showing the the plots. The user is able
    to select by him/herself the desired plot.
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

import Tkinter as tk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
matplotlib.use("TkAgg")
from gui.calculation.MatrixCalculation import MatrixCalculation
from gui.calculation.RankingCalculation import RankingCalculation
from gui.calculation.BenchmarkCalculation import BenchmarkCalculation
from gui.calculation.Riskassessment import RiskAssessment
from gui.calculation.KooperationstypCalculation import FormProxy


class Recomphase:
    def __init__(self, sqlaccess, parent, account, project):
        # self.sqlacc = local_bind_p
        self.sqlacc = sqlaccess
        self.parent = parent
        self.account = account
        self.project_ids = self.account.getprojid()
        self.project = project
        self.status = 0
        self.graphicframe = tk.LabelFrame(self.parent, text='Grafik', width=800, height=450)
        self.graphicframe.pack(side='top', fill='both', expand=1)
        self.charisk_options = tk.LabelFrame(self.graphicframe, text='Optionen', width=800, height=50)
        self.charisk_options.pack(side='top', fill='both', expand=1)
        self.plotframe = tk.LabelFrame(self.graphicframe, text="Plot:", width=700, height=400)
        self.plotframe.pack(side='left', fill='x', expand=1)
        self.plotvar = tk.StringVar()
        self.legendframe = tk.LabelFrame(self.graphicframe, text='Legende:', width=100, height=400)
        self.legendframe.pack(side='right', fill='y', expand=1)
        self.measuresvar = tk.StringVar()
        self.benchmarkvar = tk.StringVar()
        self.dimensionvar = tk.StringVar()
        self.optionsframe()

    def showplot(self, f):

        # Fill plot
        canvas = FigureCanvasTkAgg(f, master=self.plotframe)
        canvas.show()
        canvas.get_tk_widget().pack(side="left", fill='both', expand=1)

        # Fill legend
        if self.plotvar.get() == "Benchmarking":
            tk.Label(self.legendframe, text='Alle Projekte',
                     font="Helvetica 14 bold").grid(row=0, column=0, pady=5, padx=5, sticky='w')
            names = tk.Label(self.legendframe, text='Projektnamen', font="Helvetica 12 bold")
            names.grid(row=1, column=1, pady=5, padx=5, sticky='w')
            numbers = tk.Label(self.legendframe, text='Id-Nummern', font="Helvetica 12 bold")
            numbers.grid(row=1, column=0, pady=5, padx=5, sticky='w')
            for i in range(len(self.project_ids)):
                r = i + 2
                tk.Label(self.legendframe, text=self.project_ids[i],
                         font="Helvetica 10").grid(row=r, column=0, pady=5, padx=5, sticky='w')
                tk.Label(self.legendframe, text=self.sqlacc.getprojname(self.project_ids[i]),
                         font="Helvetica 10").grid(row=r, column=1, pady=5, padx=5, sticky='w')
        elif self.plotvar.get() == u"Kooperationstyp":
            info = self.account.calculate_prox_form()
            tk.Label(self.legendframe, text="Kooperationstyp",
                     font="Helvetica 12 bold").grid(row=0, column=0, pady=5, padx=5, sticky='w')
            tk.Label(self.legendframe, text='Typ:',
                     font="Helvetica 10 bold").grid(row=1, column=0, pady=5, padx=5, sticky='w')
            tk.Label(self.legendframe, text=info["type"],
                     font="Helvetica 10").grid(row=2, column=0, pady=4, padx=5, sticky='w')
            tk.Label(self.legendframe, text='Erklärung:',
                     font="Helvetica 10 bold").grid(row=3, column=0, pady=5, padx=5, sticky='w')
            tk.Label(self.legendframe, text=info["text"], wraplength=190, justify='left',
                     font="Helvetica 10").grid(row=4, column=0, pady=4, padx=5, sticky='w')
        elif self.plotvar.get() == u"Risikoeinstellung":
            info = self.account.calculate_risk_ass()
            tk.Label(self.legendframe, text="Risikoeinstellung",
                     font="Helvetica 12 bold").grid(row=0, column=0, pady=5, padx=5, sticky='w')
            tk.Label(self.legendframe, text='Typ:',
                     font="Helvetica 10 bold").grid(row=1, column=0, pady=5, padx=5, sticky='w')
            tk.Label(self.legendframe, text=info["type"],
                     font="Helvetica 10").grid(row=2, column=0, pady=4, padx=5, sticky='w')
            tk.Label(self.legendframe, text='Erklärung:',
                     font="Helvetica 10 bold").grid(row=3, column=0, pady=5, padx=5, sticky='w')
            tk.Label(self.legendframe, text=info["text"], wraplength=190, justify='left',
                     font="Helvetica 10").grid(row=4, column=0, pady=4, padx=5, sticky='w')
        elif self.plotvar.get() == "Ranking aller Projekte":
            tk.Label(self.legendframe, text='Alle Projekte',
                     font="Helvetica 14 bold").grid(row=0, column=0, pady=5, padx=5, sticky='w')
            names = tk.Label(self.legendframe, text='Projektnamen', font="Helvetica 12 bold")
            names.grid(row=1, column=1, pady=5, padx=5, sticky='w')
            numbers = tk.Label(self.legendframe, text='Id-Nummern', font="Helvetica 12 bold")
            numbers.grid(row=1, column=0, pady=5, padx=5, sticky='w')
            for i in range(len(self.project_ids)):
                r = i + 2
                tk.Label(self.legendframe, text=self.project_ids[i],
                         font="Helvetica 10").grid(row=r, column=0, pady=5, padx=5, sticky='w')
                tk.Label(self.legendframe, text=self.sqlacc.getprojname(self.project_ids[i]),
                         font="Helvetica 10").grid(row=r, column=1, pady=5, padx=5, sticky='w')

        else:
            tk.Label(self.legendframe, text='Aktuelles Projekt').grid(row=0, column=0, pady=5,
                                                                      padx=5, sticky='w')
            names = tk.Label(self.legendframe, text='Projektnamen')
            names.grid(row=1, column=1, pady=5, padx=5, sticky='w')
            numbers = tk.Label(self.legendframe, text='Id-Nummern')
            numbers.grid(row=1, column=0, pady=5, padx=5, sticky='w')
            tk.Label(self.legendframe,
                     text=self.project.getprojid()).grid(row=2, column=0, pady=5,
                                                         padx=5, sticky='w')
            tk.Label(self.legendframe,
                     text=self.project.getprojname()).grid(row=2, column=1, pady=5,
                                                           padx=5, sticky='w')

    def optionsframe(self):

        self.plotvar.set("Matrix")
        self.measuresvar.set("Vor Maßnahmen")
        self.benchmarkvar.set("Aktuelles Projekt")
        self.dimensionvar.set("Chancen")

        # r=1
        tk.Label(self.charisk_options, text='Grafik:',
                 font="Helvetica 10 bold").grid(row=1, column=1, columnspan=2,
                                                pady=10, padx=5, sticky='w')
        tk.Label(self.charisk_options, text='Dimension:',
                 font="Helvetica 10 bold").grid(row=1, column=3, columnspan=2,
                                                pady=10, padx=5, sticky='w')
        tk.Label(self.charisk_options, text='Maßnahmen:',
                 font="Helvetica 10 bold").grid(row=1, column=5, columnspan=2,
                                                pady=10, padx=5, sticky='w')
        plotoptions = tk.OptionMenu(self.charisk_options, self.plotvar, "Matrix",
                                    "Benchmarking", "Ranking", "Ranking aller Projekte",
                                    "Risikoeinstellung", "Kooperationstyp")
        plotoptions.grid(row=2, column=1, columnspan=2, pady=10, padx=5, sticky='w')

        dimensions = tk.OptionMenu(self.charisk_options, self.dimensionvar,
                                   "Chancen", "Risiken", "Chancen und Risiken")
        dimensions.grid(row=2, column=3, columnspan=2, pady=10, padx=5, sticky='w')

        measuresoptions = tk.OptionMenu(self.charisk_options, self.measuresvar,
                                        "Vor Maßnahmen", "Nach Maßnahmen")
        measuresoptions.grid(row=2, column=5, columnspan=2, pady=10, padx=5, sticky='w')

        tk.Button(self.charisk_options, text='Zeige Plot',
                  font="Helvetica 12", command=self.updateplot).grid(row=1, column=9, rowspan=2,
                                                                     pady=10, sticky='news')

    def updateplot(self):
        """

        :return:
        """
        options_dict = {}
        options_dict["Dimension"] = str(self.dimensionvar.get())
        options_dict["Measure"] = self.measuresvar.get()
        signal = 1
        print "Grafik:", self.plotvar.get()

        if self.plotvar.get() == "Matrix":
            matrix = MatrixCalculation(self.sqlacc, options_dict, self.project)
            plot_figure = matrix.calculate_plot(signal)

        elif self.plotvar.get() == "Ranking":
            ranking = RankingCalculation(self.sqlacc, options_dict, self.project, self.account)
            plot_figure = ranking.calculate_plot()

        elif self.plotvar.get() == "Ranking aller Projekte":
            ranking = RankingCalculation(self.sqlacc, options_dict, self.project, self.account)
            plot_figure = ranking.calculate_all()
            print "Ich bin alle Projekte"

        elif self.plotvar.get() == "Benchmarking":
            benchmark = BenchmarkCalculation(self.sqlacc, options_dict, self.project, self.account)
            plot_figure = benchmark.calculate_plot(signal)

        elif self.plotvar.get() == "Risikoeinstellung":
            assessment = RiskAssessment(self.account)
            plot_figure = assessment.calculate_plot(signal)

        else:
            formproxy = FormProxy(self.account)
            plot_figure = formproxy.calculate_plot(signal)

        self.plotframe.destroy()
        self.legendframe.destroy()
        self.plotframe = tk.LabelFrame(self.graphicframe, text="Plot:", width=300, height=300)
        self.plotframe.pack(side='left', fill='both', expand=1)
        self.legendframe = tk.LabelFrame(self.graphicframe, text='Legende:', width=300, height=400)
        self.legendframe.pack(side='right', fill='both', expand=0)
        self.showplot(plot_figure)
