#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Authors:    Marcus Grum, Karsten Tauchert, Norbert Gronau
    Copyright:  University of Potsdam
                Department of Business Informatics, esp. Processes and Systems
    Name:       matrix_calculation.py
    Description:
    Calculates the plots of the Project-Matrix from the OpenDarkness Tool.
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
from matplotlib.pyplot import figure, show, subplot2grid
from matplotlib import gridspec
from numpy import mean, negative


class MatrixCalculation:
    """
    Initializing the calculation object and when asked returns the 'figure' for plotting.
    """
    def __init__(self, sqlaccess, options_dict, project):
        self.sqlacc = sqlaccess
        self.option_dict = options_dict
        self.project = project
        self.proj_id = self.project.getprojid()

    def calculate_plot(self, signal):
        """
        The calculation and creation of the figures for the plots.
        :param signal: int
        :return f: figure
        """
        if signal == 1:
            f = Figure(figsize=(6, 6), dpi=75)
        else:
            f = figure(figsize=(8.27, 11.69), dpi=100)      #Din A4
            f.suptitle('Matrix')
        gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
        a = f.add_subplot(gs[0])

        # a = subplot2grid((1, 3), (0, 0), colspan=2)
        a.set_xlabel(u'Ausmaß')
        a.set_ylabel(u'Wahrscheinlichkeit')
        a.set_ylim((0, 1))
        rightboarder = 0
        entry = self.option_dict

        if entry["Dimension"] == "Chancen":
            a.set_xlim((0, 10))
            if entry["Measure"] == u"Vor Maßnahmen":
                chance_eval = self.sqlacc.chance_eval(self.proj_id)
                eval = self.calculate(chance_eval)
                a.scatter(eval["x_val"], eval["y_val"], label='Datenpunkte', color='limegreen')
                a.scatter(eval["x_mean"], eval["y_mean"], marker="*", color='green', s=400, label='Schwerpunkt')
                # a.set_title(u'Chancen - Vor Maßnahmen')
                title = u"Chance\n" \
                        u"Vor Maßnahmen\n"

            else:
                chance_eval = self.sqlacc.getmeasures_chance(self.proj_id)
                eval = self.calculate_measure(chance_eval)
                a.scatter(eval["x_val"], eval["y_val"], label='Datenpunkte', color='limegreen')
                a.scatter(eval["x_mean"], eval["y_mean"], marker="*", color='green', s=400, label='Schwerpunkt')
                # a.set_title(u'Chancen - Nach Maßnahmen')
                title = u"Chance\n" \
                        u"Nach Maßnahmen\n"
            rightboarder = 10

        elif entry["Dimension"] == "Risiken":
            a.set_xlim((-10, 0))
            if entry["Measure"] == u"Vor Maßnahmen":
                risk_eval = self.sqlacc.risk_eval(self.proj_id)
                eval = self.calculate(risk_eval)
                a.scatter(negative(eval["x_val"]), eval["y_val"],
                          label='Datenpunkte', color='tomato')
                a.scatter(eval["x_mean"] * (-1), eval["y_mean"],
                       marker="*", color='red', s=400, label='Schwerpunkt')
                a.yaxis.tick_right()
                a.yaxis.set_label_position("right")
                # a.set_title(u'Risiko - Vor Maßnahmen')
                title = u"Risiko\n" \
                        u"Vor Maßnahmen\n"

            else:
                risk_eval = self.sqlacc.getmeasures_risk(self.proj_id)
                eval = self.calculate_measure(risk_eval)
                a.scatter(negative(eval["x_val"]), eval["y_val"],
                          label='Datenpunkte', color='tomato')
                a.scatter(eval["x_mean"] * (-1), eval["y_mean"],
                       marker="*", color='red', s=400, label='Schwerpunkt')
                a.yaxis.tick_right()
                a.yaxis.set_label_position("right")
                # a.set_title(u'Risiko - Nach Maßnahmen')
                title = u"Risiko\n" \
                        u"Nach Maßnahmen\n"
            rightboarder = 0
        else:
            a.set_xlim((-10, 10))
            a.vlines(0, 0, 1, linestyles='dashed')
            if entry["Measure"] == u"Vor Maßnahmen":
                chance_eval = self.sqlacc.chance_eval(self.proj_id)
                eval_c = self.calculate(chance_eval)
                risk_eval = self.sqlacc.risk_eval(self.proj_id)
                eval_r = self.calculate(risk_eval)

                a.scatter(eval_c["x_val"], eval_c["y_val"],
                          label='Datenpunkte', color='palegreen')
                a.scatter(eval_c["x_mean"], eval_c["y_mean"],
                       marker="*", color='limegreen', s=400, label='Chance')
                a.scatter(negative(eval_r["x_val"]), eval_r["y_val"],
                          label='Datenpunkte', color='tomato')
                a.scatter(eval_r["x_mean"] * (-1), eval_r["y_mean"],
                       marker="*", color='red', s=400, label='Risiko')
                a.scatter(mean([eval_c["x_mean"], negative(eval_r["x_mean"])]),
                       mean([eval_c["y_mean"], eval_r["y_mean"]]),
                       marker='*', color='grey', s=1000, label='Schwerpunkt')
                # a.set_title(u'Chancen & Risiken - Vor Maßnahmen')
                title = u"Chance\n" \
                        u"und Risiko\n" \
                        u"Vor Maßnahmen\n"
            else:
                chance_eval = self.sqlacc.getmeasures_chance(self.proj_id)
                eval_c = self.calculate_measure(chance_eval)
                risk_eval = self.sqlacc.getmeasures_risk(self.proj_id)
                eval_r = self.calculate_measure(risk_eval)

                a.scatter(eval_c["x_val"], eval_c["y_val"],
                          label='Datenpunkte', color='palegreen')
                a.scatter(eval_c["x_mean"], eval_c["y_mean"],
                       marker="*", color='limegreen', s=400, label='Chance')
                a.scatter(negative(eval_r["x_val"]), eval_r["y_val"],
                          label='Datenpunkte', color='tomato')
                a.scatter(eval_r["x_mean"] * (-1), eval_r["y_mean"],
                       marker="*", color='red', s=400, label='Risiko')
                a.scatter(mean([eval_c["x_mean"], negative(eval_r["x_mean"])]),
                       mean([eval_c["y_mean"], eval_r["y_mean"]]),
                       marker='*', color='grey', s=1000, label='Schwerpunkt')
                # a.set_title(u'Chancen & Risiken - Nach Maßnahmen')
                title = u"Chance\n" \
                        u"und Risiko\n" \
                        u"Nach Maßnahmen\n"
            rightboarder = 10
        a.legend(loc='upper right', bbox_to_anchor=(1.33, 1.02), scatterpoints=1,
                 title=title, fontsize= 12, numpoints=1, markerscale=0.66,
                 fancybox=True, shadow=True, ncol=1)
        a.get_legend().get_title().set_color("orange")
        return f
    # print "Matrix berechnet!"

    def calculate(self, eval):
        """
        The calculation of the array which holds the points and the mean of the plot.
        :param eval: float dict
        :return: float dict
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
        Same as above, just another database. Measures.
        :param eval: float dict
        :return: float dict
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

    def generatepdfplots(self, dimension):
        """
        Same as calculate_plot, but for the pdf print out.
        Little changes in designn.
        :return:
        """
        f = figure(figsize=(8.27, 11.69), dpi=100)  # Din A4
        f.suptitle('Matrix')
        if dimension == "Chancen":
            # Matrix - Chancen - Vor Maßnahmen
            a = subplot2grid((2,3),(0,0), colspan=2)
            # a = f.add_subplot(311)
            a.set_xlim((0, 10))
            a.set_ylim((0, 1))
            chance_eval = self.sqlacc.chance_eval(self.proj_id)
            eval = self.calculate(chance_eval)
            a.scatter(eval["x_val"], eval["y_val"], label='Datenpunkte', color='limegreen')
            a.scatter(eval["x_mean"], eval["y_mean"], marker="*", color='green', s=400, label='Schwerpunkt')
            a.set_title(u'Chancen - Vor Maßnahmen')
            a.legend(loc='upper right', bbox_to_anchor=(1.66, 1.02), scatterpoints=1, numpoints=1, markerscale=0.66,
                     fancybox=True, shadow=True, ncol=1)

            a = subplot2grid((2, 3), (1,0), colspan=2)
            # a = f.add_subplot(312)
            a.set_xlim((0, 10))
            chance_eval = self.sqlacc.getmeasures_chance(self.proj_id)
            eval = self.calculate_measure(chance_eval)
            a.scatter(eval["x_val"], eval["y_val"], label='Datenpunkte', color='limegreen')
            a.scatter(eval["x_mean"], eval["y_mean"], marker="*", color='green', s=400, label='Schwerpunkt')
            a.set_title(u'Chancen - Nach Maßnahmen')
            a.legend(loc='upper right', bbox_to_anchor=(1.66, 1.02), scatterpoints=1, numpoints=1, markerscale=0.66,
                     fancybox=True, shadow=True, ncol=1)
            return f
        elif dimension == "Risiken":
            a = subplot2grid((2, 3), (0, 0), colspan=2)
            # a = f.add_subplot(211)
            a.set_xlim((-10, 0))
            a.set_ylim((0, 1))

            risk_eval = self.sqlacc.risk_eval(self.proj_id)
            eval = self.calculate(risk_eval)
            a.scatter(negative(eval["x_val"]), eval["y_val"],
                      label='Datenpunkte', color='tomato')
            a.scatter(eval["x_mean"] * (-1), eval["y_mean"],
                   marker="*", color='red', s=400, label='Schwerpunkt')
            a.yaxis.tick_right()
            a.yaxis.set_label_position("right")
            a.legend(loc='upper right', bbox_to_anchor=(1.66, 1.02), scatterpoints=1, numpoints=1, markerscale=0.66,
                     fancybox=True, shadow=True, ncol=1)
            a.set_title(u'Risiko - Vor Maßnahmen')

            # a = f.add_subplot(212)
            a = subplot2grid((2, 3), (1, 0), colspan=2)
            a.set_xlim((-10, 0))
            a.set_ylim((0, 1))
            risk_eval = self.sqlacc.getmeasures_risk(self.proj_id)
            eval = self.calculate_measure(risk_eval)
            a.scatter(negative(eval["x_val"]), eval["y_val"],
                      label='Datenpunkte', color='tomato')
            a.scatter(eval["x_mean"] * (-1), eval["y_mean"],
                   marker="*", color='red', s=400, label='Schwerpunkt')
            a.yaxis.tick_right()
            a.yaxis.set_label_position("right")
            a.set_title(u'Risiko - Nach Maßnahmen')
            a.legend(loc='upper right', bbox_to_anchor=(1.66, 1.02), scatterpoints=1, numpoints=1, markerscale=0.66,
                     fancybox=True, shadow=True, ncol=1)
            # print "Matrix Risiken plot"
            return f
        else:
            a = subplot2grid((2, 3), (0, 0), colspan=2)
            # a = f.add_subplot(211)
            a.set_xlim((-10, 10))
            a.set_ylim((0, 1))
            a.vlines(0, 0, 1, linestyles='dashed')
            chance_eval = self.sqlacc.chance_eval(self.proj_id)
            eval_c = self.calculate(chance_eval)
            risk_eval = self.sqlacc.risk_eval(self.proj_id)
            eval_r = self.calculate(risk_eval)
            a.scatter(eval_c["x_val"], eval_c["y_val"],
                      label='Datenpunkte', color='palegreen')
            a.scatter(eval_c["x_mean"], eval_c["y_mean"],
                   marker="*", color='limegreen', s=400, label='Chance')
            a.scatter(negative(eval_r["x_val"]), eval_r["y_val"],
                      label='Datenpunkte', color='tomato')
            a.scatter(eval_r["x_mean"] * (-1), eval_r["y_mean"],
                   marker="*", color='red', s=400, label='Risiko')
            a.scatter(mean([eval_c["x_mean"], negative(eval_r["x_mean"])]),
                   mean([eval_c["y_mean"], eval_r["y_mean"]]),
                   marker='*', color='grey', s=1000, label='Schwerpunkt')
            a.legend(loc='upper right', bbox_to_anchor=(1.66, 1.02), scatterpoints=1, numpoints=1, markerscale=0.66,
                     fancybox=True, shadow=True, ncol=1)
            a.set_title(u'Chancen & Risiken - Vor Maßnahmen')

            a = subplot2grid((2, 3), (1, 0), colspan=2)
            # a = f.add_subplot(212)
            a.set_xlim((-10, 10))
            a.set_ylim((0, 1))
            a.vlines(0, 0, 1, linestyles='dashed')
            chance_eval = self.sqlacc.getmeasures_chance(self.proj_id)
            eval_c = self.calculate_measure(chance_eval)
            risk_eval = self.sqlacc.getmeasures_risk(self.proj_id)
            eval_r = self.calculate_measure(risk_eval)
            a.scatter(eval_c["x_val"], eval_c["y_val"],
                      label='Datenpunkte', color='palegreen')
            a.scatter(eval_c["x_mean"], eval_c["y_mean"],
                   marker="*", color='limegreen', s=400, label='Chance')
            a.scatter(negative(eval_r["x_val"]), eval_r["y_val"],
                      label='Datenpunkte', color='tomato')
            a.scatter(eval_r["x_mean"] * (-1), eval_r["y_mean"],
                   marker="*", color='red', s=400, label='Risiko')
            a.scatter(mean([eval_c["x_mean"], negative(eval_r["x_mean"])]),
                   mean([eval_c["y_mean"], eval_r["y_mean"]]),
                   marker='*', color='grey', s=1000, label='Schwerpunkt')
            a.set_title(u'Chancen & Risiken - Nach Maßnahmen')
            a.legend(loc='upper right', bbox_to_anchor=(1.66, 1.05), scatterpoints=1, numpoints=1, markerscale=0.66,
                     fancybox=True, shadow=True, ncol=1)
            # print "MAtrix Chancen und Risiken plot"
            return f