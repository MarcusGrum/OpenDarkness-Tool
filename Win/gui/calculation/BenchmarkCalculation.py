#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Authors:    Marcus Grum, Karsten Tauchert, Norbert Gronau
    Copyright:  University of Potsdam
                Department of Business Informatics, esp. Processes and Systems
    Name:       benchmark_calculation.py
    Description:
    Calculates the plots of the Project-Benchmarking from the OpenDarkness Tool.
    Returns the "figure" from matplotlib for Tkinter and pyplot. Depending on the signal sent.
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
from matplotlib.figure import Figure
from numpy import mean
from matplotlib.pyplot import figure, subplot2grid
from matplotlib import gridspec


class BenchmarkCalculation:

    def __init__(self, sqlaccess, options_dict, project, account):
        self.sqlacc = sqlaccess
        self.options_dict = options_dict
        self.project = project
        self.account = account

    def calculate_plot(self, signal):

        if signal == 1:
            f = Figure(figsize=(6, 6), dpi=75)
        else:
            f = figure(figsize=(8.27, 11.69), dpi=100)      # Din A4
            f.suptitle('Benchmarking')
        project_ids = self.account.getprojid()
        proj_names = {}
        for i in range(len(project_ids)):
            proj_names[project_ids[i]] = self.sqlacc.getprojname(project_ids[i])

        gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
        a = f.add_subplot(gs[0])
        # a = f.add_subplot(111)
        # a = subplot2grid((1, 3), (0, 0), colspan=2)
        a.set_xlabel(u'Ausmaß')
        a.set_ylabel(u'Wahrscheinlichkeit')

        a.set_ylim((0, 1))

        if self.options_dict["Dimension"] == "Chancen":
            a.set_xlim((0, 10))
            if self.options_dict["Measure"] == u"Vor Maßnahmen":
                """ Alle-Chancen-Vor"""
                x_mean = []
                y_mean = []
                for value in project_ids:
                    chance_eval = self.sqlacc.chance_eval(value)
                    eval = self.calculate(chance_eval)
                    x_mean.append(eval["x_mean"])
                    y_mean.append(eval["y_mean"])

                a.scatter(x_mean, y_mean, marker="*", color='green', s=700, label='Chancen-\nSchwerpunkte')
                title = u'Chancen\n' \
                        u'Vor Maßnahmen\n'

                for i, txt in enumerate(project_ids):
                    txt = str(txt)
                    x_new = x_mean[i] + 0.2
                    y_new = y_mean[i] + 0.05
                    a.annotate(txt, (x_new, y_new))
            else:
                """ Alle-Chancen-Nach"""
                x_mean = []
                y_mean = []

                for value in project_ids:
                    chance_eval = self.sqlacc.getmeasures_chance(value)
                    eval = self.calculate_measure(chance_eval)
                    x_mean.append(eval["x_mean"])
                    y_mean.append(eval["y_mean"])
                a.scatter(x_mean, y_mean, marker="*", color='green', s=700, label='Chancen-\nSchwerpunkte')
                title = u'Chancen\n' \
                        u'Nach Maßnahmen\n'
                for i, txt in enumerate(project_ids):
                    txt = str(txt)
                    x_new = x_mean[i] + 0.2
                    y_new = y_mean[i] + 0.05
                    a.annotate(txt, (x_new, y_new))
                
        elif self.options_dict["Dimension"] == "Risiken":
            a.set_xlim((-10, 0))
            if self.options_dict["Measure"] == u"Vor Maßnahmen":
                """ Alle-Risiken-Vor"""
                x_mean = []
                y_mean = []

                for value in project_ids:
                    risk_eval = self.sqlacc.risk_eval(value)
                    eval = self.calculate(risk_eval)
                    x_mean.append(eval["x_mean"] * (-1))
                    y_mean.append(eval["y_mean"])
                a.scatter(x_mean, y_mean, marker="*", color='red', s=700, label='Risiken-\nSchwerpunkte')
                title = u'Risiko\n' \
                        u'Vor Maßnahmen\n'
                for i, txt in enumerate(project_ids):
                    txt = str(txt)
                    x_new = x_mean[i] + 0.2
                    y_new = y_mean[i] + 0.05
                    a.annotate(txt, (x_new, y_new))
                
            else:
                """ Alle-Risiken-Nach"""
                x_mean = []
                y_mean = []

                for value in project_ids:
                    risk_eval = self.sqlacc.getmeasures_risk(value)
                    eval = self.calculate_measure(risk_eval)
                    x_mean.append(eval["x_mean"] * (-1))
                    y_mean.append(eval["y_mean"])
                a.scatter(x_mean, y_mean, marker="*", color='red', s=700, label='Risiken-\nSchwerpunkte')
                title = u'Risiko\n' \
                        u'Nach Maßnahmen\n'
                for i, txt in enumerate(project_ids):
                    txt = str(txt)
                    x_new = x_mean[i] + 0.2
                    y_new = y_mean[i] + 0.05
                    a.annotate(txt, (x_new, y_new))
                
        else:
            a.set_xlim((-10, 10))
            a.vlines(0, 0, 1, linestyles='dashed')
            if self.options_dict["Measure"] == u"Vor Maßnahmen":
                """ Alle-CuR-Vor"""

                x_mean_c = []
                y_mean_c = []
                for value in project_ids:
                    chance_eval = self.sqlacc.chance_eval(value)
                    eval = self.calculate(chance_eval)
                    x_mean_c.append(eval["x_mean"])
                    y_mean_c.append(eval["y_mean"])
                a.scatter(x_mean_c, y_mean_c, marker="*", color='limegreen', s=400, label='Chancen-\nSchwerpunkte')
                title =  u'Chancen\n' \
                         u'und Risiken\n' \
                         u'Vor Maßnahmen\n'
                for i, txt in enumerate(project_ids):
                    txt = str(txt)
                    x_new = x_mean_c[i] + 0.2
                    y_new = y_mean_c[i] + 0.05
                    a.annotate(txt, (x_new, y_new))

                x_mean_r = []
                y_mean_r = []
                for value in project_ids:
                    risk_eval = self.sqlacc.risk_eval(value)
                    eval = self.calculate(risk_eval)
                    x_mean_r.append(eval["x_mean"] * (-1))
                    y_mean_r.append(eval["y_mean"])
                a.scatter(x_mean_r, y_mean_r, marker="*", color='tomato', s=400, label='Risiken-\nSchwerpunkte')
                for i, txt in enumerate(project_ids):
                    txt = str(txt)
                    x_new = x_mean_r[i] + 0.2
                    y_new = y_mean_r[i] + 0.05
                    a.annotate(txt, (x_new, y_new))

                x_mean_bench = []
                y_mean_bench = []
                for i in range(len(x_mean_c)):
                    tmp_x = 0.5 * (x_mean_c[i] + x_mean_r[i])
                    tmp_y = 0.5 * (y_mean_c[i] + y_mean_r[i])
                    x_mean_bench.append(tmp_x)
                    y_mean_bench.append(tmp_y)
                a.scatter(x_mean_bench, y_mean_bench, marker='*', c='silver', s=1000, label='Schwerpunkt')
                for i, txt in enumerate(project_ids):
                    txt = str(txt)
                    x_new = x_mean_bench[i] + 0.3
                    y_new = y_mean_bench[i] + 0.05
                    a.annotate(txt, (x_new, y_new))
                
            else:
                """ Alle-CuR-Nach"""
                x_mean_c = []
                y_mean_c = []
                title = u'Chancen\n' \
                        u'und Risiken\n' \
                        u'Nach Maßnahmen\n'

                for value in project_ids:
                    chance_eval = self.sqlacc.getmeasures_chance(value)
                    eval = self.calculate_measure(chance_eval)
                    x_mean_c.append(eval["x_mean"])
                    y_mean_c.append(eval["y_mean"])
                a.scatter(x_mean_c, y_mean_c, marker="*", color='limegreen', s=400, label='Chancen-\nSchwerpunkte')

                for i, txt in enumerate(project_ids):
                    txt = str(txt)
                    x_new = x_mean_c[i] + 0.2
                    y_new = y_mean_c[i] + 0.05
                    a.annotate(txt, (x_new, y_new))

                x_mean_r = []
                y_mean_r = []
                for value in project_ids:
                    risk_eval = self.sqlacc.getmeasures_risk(value)
                    eval = self.calculate_measure(risk_eval)
                    x_mean_r.append(eval["x_mean"] * (-1))
                    y_mean_r.append(eval["y_mean"])
                a.scatter(x_mean_r, y_mean_r, marker="*", color='tomato', s=400, label='Risiken-\nSchwerpunkte')
                for i, txt in enumerate(project_ids):
                    txt = str(txt)
                    x_new = x_mean_r[i] + 0.2
                    y_new = y_mean_r[i] + 0.05
                    a.annotate(txt, (x_new, y_new))


                x_mean_bench = []
                y_mean_bench = []
                for i in range(len(x_mean_c)):
                    tmp_x = 0.5 * (x_mean_c[i] + x_mean_r[i])
                    tmp_y = 0.5 * (y_mean_c[i] + y_mean_r[i])
                    x_mean_bench.append(tmp_x)
                    y_mean_bench.append(tmp_y)

                a.scatter(x_mean_bench, y_mean_bench, marker='*', c='silver', s=1000, label='Schwerpunkte')
                for i, txt in enumerate(project_ids):
                    txt = str(txt)
                    x_new = x_mean_bench[i] + 0.3
                    y_new = y_mean_bench[i] + 0.02
                    a.annotate(txt, (x_new, y_new))

        a.legend(loc='upper right', bbox_to_anchor=(1.40, 1.02), scatterpoints=1,
                 title=title, fontsize=12, numpoints=1, markerscale=0.66,
                 fancybox=True, shadow=True, ncol=1)
        a.get_legend().get_title().set_color("orange")
        return f
                

    def calculate(self, eval):
        """

        :param eval:
        :return:
        """
        x_val = []
        y_val = []
        for row in eval:
            x_weighted = row["extent"] * row["weight"]

            x_val.append(x_weighted)
            y_val.append(row["probability"])

        x_mean = mean(x_val)
        y_mean = mean(y_val)

        calculation = {}
        calculation["x_val"] = x_val
        calculation["y_val"] = y_val
        calculation["x_mean"] = x_mean
        calculation["y_mean"] = y_mean

        return calculation

    def calculate_measure(self, eval):
        """

        :param eval:
        :return:
        """
        x_val = []
        y_val = []

        for row in eval:
            x_val.append(row["extent"])
            y_val.append(row["probability"])

        x_mean = mean(x_val)
        y_mean = mean(y_val)

        calculation = {}
        calculation["x_val"] = x_val
        calculation["y_val"] = y_val
        calculation["x_mean"] = x_mean
        calculation["y_mean"] = y_mean

        return calculation

    def calc_oneD_mean(self, valueOne, valueTwo):
        """
        Calculates the mean of two given arrays, lists. With equal length.
        :param valueOne: list float
        :param valueTwo: list float
        :return: list float
        """
        oneD_mean = []

        for i in range(len(valueOne)):
            oneD_mean.append(mean(valueOne[i], valueTwo[i]))

        return oneD_mean

    def generatepdfplots(self, dimension):

        project_ids = self.account.getprojid()
        f = figure(figsize=(8.27, 11.69), dpi=100)  # Din A4
        f.suptitle('Benchmarking')

        if dimension == u"Chancen":

            """ Alle-Chancen-Vor"""
            a = subplot2grid((2, 3), (0, 0), colspan=2)
            a.set_xlim((0, 10))
            a.set_ylim((0, 1))
            a.set_xlabel(u'Ausmaß')
            a.set_ylabel(u'Wahrscheinlichkeit')

            x_mean = []
            y_mean = []
            for value in project_ids:
                chance_eval = self.sqlacc.chance_eval(value)
                eval = self.calculate(chance_eval)
                x_mean.append(eval["x_mean"])
                y_mean.append(eval["y_mean"])
            a.scatter(x_mean, y_mean, marker="*", color='green', s=700, label='Chancen\nSchwerpunkte')
            a.set_title(u'Chancen - Benchmark - Vor Maßnahmen')
            for i, txt in enumerate(project_ids):
                txt = str(txt)
                x_new = x_mean[i] + 0.2
                y_new = y_mean[i] + 0.05
                a.annotate(txt, (x_new, y_new))
            a.legend(loc='upper right', bbox_to_anchor=(1.66, 1.05), scatterpoints=1, numpoints=1, markerscale=0.66,
                     fancybox=True, shadow=True, ncol=1)

            """ Alle-Chancen-Nach"""
            a = subplot2grid((2, 3), (1, 0), colspan=2)
            a.set_xlim((0, 10))
            a.set_ylim((0, 1))
            a.set_xlabel(u'Ausmaß')
            a.set_ylabel(u'Wahrscheinlichkeit')

            x_mean = []
            y_mean = []
            for value in project_ids:
                chance_eval = self.sqlacc.getmeasures_chance(value)
                eval = self.calculate_measure(chance_eval)
                x_mean.append(eval["x_mean"])
                y_mean.append(eval["y_mean"])
            a.scatter(x_mean, y_mean, marker="*", color='green', s=700, label='Chancen\nSchwerpunkte')
            a.set_title(u'Chancen - Benchmark - Nach Maßnahmen')
            for i, txt in enumerate(project_ids):
                txt = str(txt)
                x_new = x_mean[i] + 0.2
                y_new = y_mean[i] + 0.05
                a.annotate(txt, (x_new, y_new))
            a.legend(loc='upper right', bbox_to_anchor=(1.66, 1.05), scatterpoints=1, numpoints=1, markerscale=0.66,
                     fancybox=True, shadow=True, ncol=1)
            return f

        elif dimension == u"Risiken":

            """ Alle-Risiken-Vor"""
            a = subplot2grid((2, 3), (0, 0), colspan=2)
            a.set_xlim((-10, 0))
            a.set_ylim((0, 1))
            a.set_xlabel(u'Ausmaß')
            a.set_ylabel(u'Wahrscheinlichkeit')

            x_mean = []
            y_mean = []
            for value in project_ids:
                risk_eval = self.sqlacc.risk_eval(value)
                eval = self.calculate(risk_eval)
                x_mean.append(eval["x_mean"] * (-1))
                y_mean.append(eval["y_mean"])
            a.scatter(x_mean, y_mean, marker="*", color='red', s=700, label='Risiken\nSchwerpunkte')
            a.set_title(u'Risiko - Vor Maßnahmen')
            for i, txt in enumerate(project_ids):
                txt = str(txt)
                x_new = x_mean[i] + 0.2
                y_new = y_mean[i] + 0.05
                a.annotate(txt, (x_new, y_new))
            a.legend(loc='upper right', bbox_to_anchor=(1.66, 1.05), scatterpoints=1, numpoints=1, markerscale=0.66,
                     fancybox=True, shadow=True, ncol=1)

            """ Alle-Risiken-Nach"""
            a = subplot2grid((2, 3), (1, 0), colspan=2)
            a.set_xlim((-10, 0))
            a.set_ylim((0, 1))
            a.set_xlabel(u'Ausmaß')
            a.set_ylabel(u'Wahrscheinlichkeit')

            x_mean = []
            y_mean = []
            for value in project_ids:
                risk_eval = self.sqlacc.getmeasures_risk(value)
                eval = self.calculate_measure(risk_eval)
                x_mean.append(eval["x_mean"] * (-1))
                y_mean.append(eval["y_mean"])
            a.scatter(x_mean, y_mean, marker="*", color='red', s=700, label='Risiken\nSchwerpunkte')
            a.set_title(u'Risiko - Nach Maßnahmen')
            for i, txt in enumerate(project_ids):
                txt = str(txt)
                x_new = x_mean[i] + 0.2
                y_new = y_mean[i] + 0.05
                a.annotate(txt, (x_new, y_new))
            a.legend(loc='upper right', bbox_to_anchor=(1.66, 1.05), scatterpoints=1, numpoints=1, markerscale=0.66,
                     fancybox=True, shadow=True, ncol=1)
            return f

        else:
            """ Alle-CuR-Vor"""
            a = subplot2grid((2, 3), (0, 0), colspan=2)
            a.set_xlim((-10, 10))
            a.set_ylim((0, 1))
            a.set_xlabel(u'Ausmaß')
            a.set_ylabel(u'Wahrscheinlichkeit')
            a.vlines(0, 0, 1, linestyles='dashed')

            x_mean_c = []
            y_mean_c = []
            for value in project_ids:
                chance_eval = self.sqlacc.chance_eval(value)
                eval = self.calculate(chance_eval)
                x_mean_c.append(eval["x_mean"])
                y_mean_c.append(eval["y_mean"])
            a.scatter(x_mean_c, y_mean_c, marker="*", color='limegreen', s=400, label='Chancen\nSchwerpunkte')
            a.set_title(u'Chancen und Risiken - Vor Maßnahmen')
            for i, txt in enumerate(project_ids):
                txt = str(txt)
                x_new = x_mean_c[i] + 0.2
                y_new = y_mean_c[i] + 0.05
                a.annotate(txt, (x_new, y_new))

            x_mean_r = []
            y_mean_r = []
            for value in project_ids:
                risk_eval = self.sqlacc.risk_eval(value)
                eval = self.calculate(risk_eval)
                x_mean_r.append(eval["x_mean"] * (-1))
                y_mean_r.append(eval["y_mean"])
            a.scatter(x_mean_r, y_mean_r, marker="*", color='tomato', s=400, label='Risiken\nSchwerpunkte')
            for i, txt in enumerate(project_ids):
                txt = str(txt)
                x_new = x_mean_r[i] + 0.2
                y_new = y_mean_r[i] + 0.05
                a.annotate(txt, (x_new, y_new))

            x_mean_bench = []
            y_mean_bench = []
            for i in range(len(x_mean_c)):
                tmp_x = 0.5 * (x_mean_c[i] + x_mean_r[i])
                tmp_y = 0.5 * (y_mean_c[i] + y_mean_r[i])
                x_mean_bench.append(tmp_x)
                y_mean_bench.append(tmp_y)
            a.scatter(x_mean_bench, y_mean_bench, marker='*', c='silver', s=1000, label='Schwerpunkt')
            for i, txt in enumerate(project_ids):
                txt = str(txt)
                x_new = x_mean_bench[i] + 0.3
                y_new = y_mean_bench[i] + 0.05
                a.annotate(txt, (x_new, y_new))
            a.legend(loc='upper right', bbox_to_anchor=(1.66, 1.05), scatterpoints=1, numpoints=1, markerscale=0.66,
                     fancybox=True, shadow=True, ncol=1)

            """ Alle-CuR-Nach"""
            a = subplot2grid((2, 3), (1, 0), colspan=2)
            a.set_xlim((-10, 10))
            a.set_ylim((0, 1))
            a.set_xlabel(u'Ausmaß')
            a.set_ylabel(u'Wahrscheinlichkeit')
            a.vlines(0, 0, 1, linestyles='dashed')

            x_mean_c = []
            y_mean_c = []
            a.set_title(u'Chancen und Risiken -  Nach Maßnahmen')

            for value in project_ids:
                chance_eval = self.sqlacc.getmeasures_chance(value)
                eval = self.calculate_measure(chance_eval)
                x_mean_c.append(eval["x_mean"])
                y_mean_c.append(eval["y_mean"])
            a.scatter(x_mean_c, y_mean_c, marker="*", color='limegreen', s=400, label='Chancen\nSchwerpunkte')

            for i, txt in enumerate(project_ids):
                txt = str(txt)
                x_new = x_mean_c[i] + 0.2
                y_new = y_mean_c[i] + 0.05
                a.annotate(txt, (x_new, y_new))

            x_mean_r = []
            y_mean_r = []
            for value in project_ids:
                risk_eval = self.sqlacc.getmeasures_risk(value)
                eval = self.calculate_measure(risk_eval)
                x_mean_r.append(eval["x_mean"] * (-1))
                y_mean_r.append(eval["y_mean"])
            a.scatter(x_mean_r, y_mean_r, marker="*", color='tomato', s=400, label='Risiken\nSchwerpunkte')
            for i, txt in enumerate(project_ids):
                txt = str(txt)
                x_new = x_mean_r[i] + 0.2
                y_new = y_mean_r[i] + 0.05
                a.annotate(txt, (x_new, y_new))
            a.legend(loc='upper right', bbox_to_anchor=(1.66, 1.05), scatterpoints=1, numpoints=1, markerscale=0.66,
                     fancybox=True, shadow=True, ncol=1)
            return f