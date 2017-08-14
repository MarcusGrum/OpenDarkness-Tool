#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Authors:    Marcus Grum, Karsten Tauchert, Norbert Gronau
    Copyright:  University of Potsdam
                Department of Business Informatics, esp. Processes and Systems
    Name:       ranking_calculation.py
    Description:
    Calculates the plots of the Project(s)-Ranking from the OpenDarkness Tool.
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
from numpy import shape, ones, mean
from matplotlib.pyplot import figure
from matplotlib import gridspec

class RankingCalculation:

    def __init__(self, sqlaccess, options_dict, project, account):
        self.sqlacc = sqlaccess
        self.options_dict = options_dict
        self.project = project
        self.account = account
        self.project_ids = self.account.getprojid()
        self.proj_id = self.project.getprojid()
        self.proj_name = self.project.getprojname()

    def calculate_plot(self):

        f = Figure(figsize=(6, 6), dpi=75)
        # a = f.add_subplot(111)
        gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
        a = f.add_subplot(gs[0])
        entry = self.options_dict
    
        if entry["Dimension"] == "Chancen":

            xes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            a.hlines(1, 0, 10)  # Draw a horizontal line
            a.set_xlim(-1, 11)
            a.set_ylim(0.5, 1.5)
            a.annotate(u"Wahrscheinliches Ausmaß", xy=(0, 1), xytext=(4, 0.75))
            y = ones(shape(xes))  # Make all y values the same
            a.plot(xes, y, '|', c='black', ms=10)
            a.plot(0, 1, '|', c='black', ms=30)
            a.plot(10, 1, ">", c='grey', ms=20)

            for i, txt in enumerate(xes):
                x = i - 0.1
                a.annotate(str(txt), xy=(x, 0.85), xytext=(x, 0.85))
            a.axis('off')

            if entry["Measure"] == u"Vor Maßnahmen":
                chance_eval = self.sqlacc.chance_eval(self.proj_id)
                eval = self.calculate(chance_eval)
                ranking = self.calc_schwerp_rank(eval["x_mean"], eval["y_mean"])
                a.scatter(ranking, 1, c='green', marker='*', s=700, label="Chancen-\nSchwerpunkt")
                # a.set_title(u"Chancen - Vor Maßnahmen")
                # a.annotate(self.proj_name, xy=(ranking, 1), xytext=(ranking, 1.2))
                title = u"Chancen\nVor Maßnahmen\n"
            else:
                chance_eval = self.sqlacc.getmeasures_chance(self.proj_id)
                eval = self.calculate_measure(chance_eval)
                ranking = self.calc_schwerp_rank(eval["x_mean"], eval["y_mean"])
                a.scatter(ranking, 1, s=700, c='green', marker='*', label="Chancen-\nSchwerpunkt")
                # a.set_title(u"Chancen - Nach Maßnahmen")
                title = u"Chancen\nNach Maßnahmen\n"

        elif entry["Dimension"] == "Risiken":

            xes = [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0]
            a.hlines(1, -10, 0)  # Draw a horizontal line
            a.set_xlim(-11, 1)
            a.set_ylim(0.5, 1.5)
            a.annotate(u"Wahrscheinliches Ausmaß", xy=(-10, 1), xytext=(-6, 0.75))
            y = ones(shape(xes))  # Make all y values the same
            a.plot(xes, y, '|', c='black', ms=10)
            a.plot(-10, 1, '|', c='black', ms=30)
            a.plot(0, 1, ">", c='grey', ms=20)

            for i, txt in enumerate(xes):
                x = txt - 0.3
                a.annotate(str(txt), xy=(x, 0.85), xytext=(x, 0.85))
            a.axis('off')
            if entry["Measure"] == u"Vor Maßnahmen":
                risk_eval = self.sqlacc.risk_eval(self.proj_id)
                eval = self.calculate(risk_eval)
                ranking = self.calc_schwerp_rank(eval["x_mean"], eval["y_mean"]) * (-1)
                a.scatter(ranking, 1, s=700, marker='*', color='red', label="Risiken-\nSchwerpunkt")
                # a.set_title(u"Risiken - Vor Maßnahmen")
                title = u"Risiken\nVor Maßnahmen\n"
            else:
                risk_eval = self.sqlacc.getmeasures_risk(self.proj_id)
                eval = self.calculate_measure(risk_eval)
                ranking = self.calc_schwerp_rank(eval["x_mean"], eval["y_mean"]) * (-1)
                a.scatter(ranking, 1, marker='*', s=700, color='red', label="Risiken-\nSchwerpunkt")
                # a.set_title(u"Risiken - Nach Maßnahmen")
                title = u"Risiken\nNach Maßnahmen\n"
        else:
            x_coords = [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

            a.hlines(1, -10, 10)  # Draw a horizontal line
            a.set_xlim(-11, 11)
            a.set_ylim(0.5, 1.5)
            a.annotate(u"Wahrscheinliches Ausmaß", xy=(-10, 1), xytext=(-6, 0.75))
            y_coords = ones(shape(x_coords))
            a.plot(x_coords, y_coords, '|', c='black', ms=10)
            a.plot([-10, 0], [1, 1], '|', c='black', ms=25)
            a.plot(10, 1, '>', c='grey', ms=20)

            for i, txt in enumerate(x_coords):
                if i % 2 == 0:
                    x = txt
                    a.annotate(str(txt), xy=(x - 0.2, 1), xytext=(x - 0.2, 0.90))
            a.axis('off')

            if entry["Measure"] == u"Vor Maßnahmen":
                chance_eval = self.sqlacc.chance_eval(self.proj_id)
                eval = self.calculate(chance_eval)
                ranking_c = self.calc_schwerp_rank(eval["x_mean"], eval["y_mean"])
                a.scatter(ranking_c, 1, marker='*', c='green', s=400, label="Chancen-\nSchwerpunkt")
                # a.set_title(u" Chancen und Risiken - Vor Maßnahmen")
                risk_eval = self.sqlacc.risk_eval(self.proj_id)
                eval = self.calculate(risk_eval)
                ranking_r = self.calc_schwerp_rank(eval["x_mean"], eval["y_mean"]) * (-1)
                a.scatter(ranking_r, 1, marker='*', c='red', s=400, label="Risiko-\nSchwerpunkt")
                a.scatter(mean([ranking_c, ranking_r]), 1, marker='*', c='grey', s=1200, label='Schwerpunkt')
                title = u"Chancen\nund Risiken\nVor Maßnahmen\n"
            else:
                chance_eval = self.sqlacc.getmeasures_chance(self.proj_id)
                eval = self.calculate_measure(chance_eval)
                ranking_c = self.calc_schwerp_rank(eval["x_mean"], eval["y_mean"])
                a.scatter(ranking_c, 1, marker='*', c='green', s=400, label="Chancen-\nSchwerpunkt")
                # a.set_title(u"Chancen und Risiken - Nach Maßnahmen")
                risk_eval = self.sqlacc.getmeasures_risk(self.proj_id)
                eval = self.calculate_measure(risk_eval)
                ranking_r = self.calc_schwerp_rank(eval["x_mean"], eval["y_mean"]) * (-1)
                a.scatter(ranking_r, 1, marker='*', c='red', s=400, label="Risiken-\nSchwerpunkt")
                a.scatter(mean([ranking_c, ranking_r]), 1, marker='*', c='grey', s=1200, label='Schwerpunkt')
                title = u"Chancen\nund Risiken\nNach Maßnahmen\n"
        a.legend(loc='upper right', bbox_to_anchor=(1.40, 1.02), scatterpoints=1,
                 title=title, fontsize=12, numpoints=1, markerscale=0.66,
                 fancybox=True, shadow=True, ncol=1)
        a.get_legend().get_title().set_color("orange")
        return f

    def calculate_all(self):
        """

        :return:
        """
        f = Figure(figsize=(6, 6), dpi=75)
        a = f.add_subplot(111)

        x_coords = [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        a.hlines(1, -10, 10)  # Draw a horizontal line
        a.set_xlim(-11, 11)
        a.set_ylim(0.5, 1.5)
        a.annotate(u"Wahrscheinliches Ausmaß", xy=(-10, 1), xytext=(-6, 0.75))
        y_coords = ones(shape(x_coords))
        a.plot(x_coords, y_coords, '|', c='black', ms=10)
        a.plot([-10, 0], [1, 1], '|', c='black', ms=25)
        a.plot(10, 1, '>', c='grey', ms=20)

        for i, txt in enumerate(x_coords):
            if i % 2 == 0:
                x = txt
                a.annotate(str(txt), xy=(x - 0.2, 1), xytext=(x - 0.2, 0.90))
        a.axis('off')

        project_ids = self.account.getprojid()
        proj_names = {}
        for i in range(len(project_ids)):
            proj_names[project_ids[i]] = self.sqlacc.getprojname(project_ids[i])

        if self.options_dict["Measure"] == u"Vor Maßnahmen":
            x_mean_c = []
            y_mean_c = []
            for value in project_ids:
                chance_eval = self.sqlacc.chance_eval(value)
                eval = self.calculate(chance_eval)
                x_mean_c.append(eval["x_mean"])
                y_mean_c.append(eval["y_mean"])

            x_mean_r = []
            y_mean_r = []
            for value in project_ids:
                risk_eval = self.sqlacc.risk_eval(value)
                eval = self.calculate(risk_eval)
                x_mean_r.append(eval["x_mean"] * (-1))
                y_mean_r.append(eval["y_mean"])

            x_mean_bench = []
            y_mean_bench = []
            for i in range(len(x_mean_c)):
                tmp_x = 0.5 * (x_mean_c[i] + x_mean_r[i])
                tmp_y = 0.5 * (y_mean_c[i] + y_mean_r[i])
                x_mean_bench.append(tmp_x)
                y_mean_bench.append(tmp_y)

            ranking_all = []
            for i in range(len(x_mean_bench)):
                ranking_all.append(self.calc_schwerp_rank(x_mean_bench[i], y_mean_bench[i]))

            y_ones = ones(shape(ranking_all))

            a.scatter(ranking_all, y_ones, marker='*', c='grey', s=1200)

            for i, txt in enumerate(project_ids):
                txt = str(txt)
                x_new = ranking_all[i] + 0.2
                y_new = y_ones[i] + 0.07 + i * 0.05
                a.annotate(txt, (x_new, y_new))

            return f

        else:

            x_mean_c = []
            y_mean_c =[]
            for value in project_ids:
                chance_eval = self.sqlacc.getmeasures_chance(value)
                eval = self.calculate_measure(chance_eval)
                x_mean_c.append(eval["x_mean"])
                y_mean_c.append(eval["y_mean"])

            x_mean_r = []
            y_mean_r = []
            for value in project_ids:
                risk_eval = self.sqlacc.getmeasures_risk(value)
                eval = self.calculate_measure(risk_eval)
                x_mean_r.append(eval["x_mean"] * (-1))
                y_mean_r.append(eval["y_mean"])

            x_mean_bench = []
            y_mean_bench = []
            for i in range(len(x_mean_c)):
                tmp_x = 0.5 * (x_mean_c[i] + x_mean_r[i])
                tmp_y = 0.5 * (y_mean_c[i] + y_mean_r[i])
                x_mean_bench.append(tmp_x)
                y_mean_bench.append(tmp_y)

            ranking_all = []
            for i in range(len(x_mean_bench)):
                ranking_all.append(self.calc_schwerp_rank(x_mean_bench[i], y_mean_bench[i]))

            y_ones = ones(shape(ranking_all))

            a.scatter(ranking_all, y_ones, marker='*', c='grey', s=1200)

            for i, txt in enumerate(project_ids):
                txt = str(txt)
                x_new = ranking_all[i] + 0.2
                y_new = y_ones[i] + 0.07 + i * 0.05
                a.annotate(txt, (x_new, y_new))

            return f



    def calculate(self, eval):
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

        x_val = []
        y_val = []

        for row in eval:
            # x_weighted = row["extent"] * row["weight"]
            # x_val.append(x_weighted)
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

    def calc_schwerp_rank(self, x_coords, y_coords):

        schwerpunkt = 1.0 / 101.0 * (10.0 * y_coords + 100.0 * x_coords)

        return schwerpunkt

    """ Bis mir was besseres einfällt :( """
    """ FIX FIX --> oben verändert, also hier auch noch ändern :("""
    def calculate_pdfplot(self):

        f = figure(figsize=(8.27, 11.69), dpi=100)  #Din A4

        f.suptitle('Ranking')

        """ Chance
            Vor Maßnahmen
        """
        a = f.add_subplot(321)
        xes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        y = ones(shape(xes))  # Make all y values the same
        a.annotate(u"Wahrscheinliches Ausmaß", xy=(0, 1), xytext=(0, 0.75))
        a.hlines(1, 0, 10)  # Draw a horizontal line
        a.set_xlim(-1, 11)
        a.set_ylim(0.5, 1.5)
        a.plot(xes, y, '|', c='black', ms=10)
        a.plot(0, 1, '|', c='black', ms=20)
        a.plot(10.3, 1, ">", c='grey', ms=15)
        for i, txt in enumerate(xes):
            x = i - 0.1
            a.annotate(str(txt), xy=(x, 0.85), xytext=(x, 0.85))
        a.axis('off')
        chance_eval = self.sqlacc.chance_eval(self.proj_id)
        eval = self.calculate(chance_eval)
        ranking = self.calc_schwerp_rank(eval["x_mean"], eval["y_mean"])
        a.scatter(ranking, 1, c='green', marker='*', s=700, label="Chancen")
        a.set_title(u"Chancen - Vor Maßnahmen")
        # a.annotate(self.proj_name, xy=(ranking, 1), xytext=(ranking, 1.2))
        """ Chance
            Nach Maßnahme
        """
        a = f.add_subplot(322)
        a.hlines(1, 0, 10)  # Draw a horizontal line
        a.set_xlim(-1, 11)
        a.set_ylim(0.5, 1.5)
        a.plot(xes, y, '|', c='black', ms=10)
        a.plot(0, 1, '|', c='black', ms=20)
        a.plot(10.3, 1, ">", c='grey', ms=15)
        a.annotate(u"Wahrscheinliches Ausmaß", xy=(0, 1), xytext=(0, 0.75))
        for i, txt in enumerate(xes):
            x = i - 0.1
            a.annotate(str(txt), xy=(x, 0.85), xytext=(x, 0.85))
        a.axis('off')
        chance_eval = self.sqlacc.getmeasures_chance(self.proj_id)
        eval = self.calculate_measure(chance_eval)
        ranking = self.calc_schwerp_rank(eval["x_mean"], eval["y_mean"])
        a.scatter(ranking, 1, s=700, c='green', marker='*', label="Chancen")
        a.set_title(u"Chancen - Nach Maßnahmen")

        """ Risk
            Vor Maßnahmen
        """
        a = f.add_subplot(323)
        xes = [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0]
        a.hlines(1, -10, 0)  # Draw a horizontal line
        a.set_xlim(-11, 1)
        a.set_ylim(0.5, 1.5)
        a.annotate(u"Wahrscheinliches Ausmaß", xy=(-10, 1), xytext=(-10, 0.75))
        y = ones(shape(xes))  # Make all y values the same
        a.plot(xes, y, '|', c='black', ms=10)
        a.plot(-10, 1, '|', c='black', ms=30)
        a.plot(0.3, 1, ">", c='grey', ms=20)

        for i, txt in enumerate(xes):
            x = txt - 0.2
            a.annotate(str(txt), xy=(x, 0.85), xytext=(x, 0.85))
        a.axis('off')
        risk_eval = self.sqlacc.risk_eval(self.proj_id)
        eval = self.calculate(risk_eval)
        ranking = self.calc_schwerp_rank(eval["x_mean"], eval["y_mean"]) * (-1)
        a.scatter(ranking, 1, s=700, marker='*', c='red', label="Schwerpunkt")
        a.set_title(u"Risiken - Vor Maßnahmen")

        """ Risiko
            Nach Maßnahme
        """
        a = f.add_subplot(324)
        a.hlines(1, -10, 0)  # Draw a horizontal line
        a.set_xlim(-11, 1)
        a.set_ylim(0.5, 1.5)
        a.annotate(u"Wahrscheinliches Ausmaß", xy=(-10, 1), xytext=(-10, 0.75))
        a.plot(xes, y, '|', c='black', ms=10)
        a.plot(-10, 1, '|', c='black', ms=30)
        a.plot(0.3, 1, ">", c='grey', ms=20)
        for i, txt in enumerate(xes):
            x = txt
            a.annotate(str(txt), xy=(x, 0.85), xytext=(x, 0.85))
        a.axis('off')
        risk_eval = self.sqlacc.getmeasures_risk(self.proj_id)
        eval = self.calculate_measure(risk_eval)
        ranking = self.calc_schwerp_rank(eval["x_mean"], eval["y_mean"]) * (-1)
        a.scatter(ranking, 1,  s=700, marker='*', c='red', label="Schwerpunkt")
        a.set_title(u"Risiken - Nach Maßnahmen")

        """ Chance and Risk
            Vor Maßnahme """
        a = f.add_subplot(325)
        x_coords_cr = [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        a.hlines(1, -10, 10)  # Draw a horizontal line
        a.set_xlim(-11, 11)
        a.set_ylim(0.5, 1.5)

        y_coords_cr = ones(shape(x_coords_cr))
        a.plot(x_coords_cr, y_coords_cr, '|', c='black', ms=10)
        a.plot([-10, 0], [1, 1], '|', c='black', ms=25)
        a.plot(10.8, 1, '>', c='grey', ms=15)
        a.annotate(u"Wahrscheinliches Ausmaß", xy=(0, 1), xytext=(-10, 0.75))
        for i, txt in enumerate(x_coords_cr):
            if i % 2 == 0:
                x = txt
                a.annotate(str(txt), xy=(x, 1), xytext=(x - 0.3, 0.90))
        a.axis('off')
        chance_eval = self.sqlacc.chance_eval(self.proj_id)
        eval = self.calculate(chance_eval)
        ranking_c = self.calc_schwerp_rank(eval["x_mean"], eval["y_mean"])
        a.scatter(ranking_c, 1, marker='*', c='green', s=400, label="Chance")
        a.set_title(u" C und R - Vor Maßnahmen")
        risk_eval = self.sqlacc.risk_eval(self.proj_id)
        eval = self.calculate(risk_eval)
        ranking_r = self.calc_schwerp_rank(eval["x_mean"], eval["y_mean"]) * (-1)
        a.scatter(ranking_r, 1, marker='*', c='red', s=400, label="Risiko")
        a.scatter(mean([ranking_c, ranking_r]), 1, marker='*', c='grey', s=1200, label='Bewertung')

        """ Chance and Risk
            Nach Maßnahme """
        a = f.add_subplot(326)
        a.hlines(1, -10, 10)  # Draw a horizontal line
        a.set_xlim(-11, 11)
        a.set_ylim(0.5, 1.5)
        a.plot(x_coords_cr, y_coords_cr, '|', c='black', ms=10)
        a.plot([-10, 0], [1, 1], '|', c='black', ms=25)
        a.plot(10.8, 1, '>', c='grey', ms=15)
        a.annotate(u"Wahrscheinliches Ausmaß", xy=(0, 1), xytext=(-10, 0.75))
        for i, txt in enumerate(x_coords_cr):
            if i % 2 == 0:
                x = txt
                a.annotate(str(txt), xy=(x, 1), xytext=(x - 0.3, 0.90))
        a.axis('off')
        chance_eval = self.sqlacc.getmeasures_chance(self.proj_id)
        eval = self.calculate_measure(chance_eval)
        ranking_c = self.calc_schwerp_rank(eval["x_mean"], eval["y_mean"])
        a.scatter(ranking_c, 1, marker='*', c='green', s=400, label="Chance")
        a.set_title(u"C und R - Nach Maßnahmen")
        risk_eval = self.sqlacc.getmeasures_risk(self.proj_id)
        eval = self.calculate_measure(risk_eval)
        ranking_r = self.calc_schwerp_rank(eval["x_mean"], eval["y_mean"]) * (-1)
        a.scatter(ranking_r, 1, marker='*', c='red', s=400, label="Risiko")
        a.scatter(mean([ranking_c, ranking_r]), 1, marker='*', c='grey', s=1200, label='Bewertung')
        return f