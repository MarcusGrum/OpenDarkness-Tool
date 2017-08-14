#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Authors:    Marcus Grum, Karsten Tauchert, Norbert Gronau
    Copyright:  University of Potsdam
                Department of Business Informatics, esp. Processes and Systems
    Name:       riskassessment.py
    Description:
    Calculates the plot for Risikoeinstellung.
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
import matplotlib.pyplot as plt
import numpy as np


class RiskAssessment:

    def __init__(self, account):
        self.account = account

    def calculate_plot(self, signal):

        if signal == 1:
            f = Figure(figsize=(6, 6), dpi=75)
        else:
            # f = plt.figure(figsize=(4, 6))
            f = plt.figure(figsize=(8.27, 11.69), dpi=100)      # Din A4
            f.suptitle('Risikoeinstellung')
        a = f.add_subplot(111)

        xes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        a.hlines(1, 0, 10)  # Draw a horizontal line
        a.set_xlim(-1, 11)
        a.set_ylim(0.5, 1.5)
        y = np.ones(np.shape(xes))  # Make all y values the same
        a.plot(xes, y, '|', c='black', ms=10)
        a.plot(3.333, 1, '|', c='red', ms=70)
        a.plot(6.666, 1, '|', c='red', ms=70)
        a.plot([10, 0], [1, 1], '|', c='grey', ms=70)
        for i, txt in enumerate(xes):
            x = i - 0.1
            txt /= 10.0
            a.annotate(str(txt), xy=(x, 0.85), xytext=(x, 0.85))
        a.axis('off')

        info = self.account.calculate_risk_ass()
        a.scatter(info["mean"]*10, 1, c='gold', marker='*', s=800)
        # a.set_title(u"Risikoeinstellung")

        a.text(0.1, 1.1, 'risikoavers')
        a.text(3.43, 1.1, 'risikoneutral')
        a.text(6.76, 1.1, 'risikoaffin')

        #a.annotate(info["text"], xy=(info["mean"]*10, 1), xytext=(4, 1.2))

        return f
