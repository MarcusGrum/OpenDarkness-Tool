#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Authors:    Marcus Grum, Karsten Tauchert, Norbert Gronau
    Copyright:  University of Potsdam
                Department of Business Informatics, esp. Processes and Systems
    Name:       benchmark_calculation.py
    Description:

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
# import numpy as np
from matplotlib.pyplot import figure
# import matplotlib.pyplot as plt
# import mysqlaccess as sqlacc
# from Accounts import Account


class FormProxy:

    def __init__(self, account):
        self.account = account
        self.accont_id = account.account_id

    def calculate_plot(self, signal):

        if signal == 1:
            f = Figure(figsize=(6, 6), dpi=75)
        else:
            f = figure(figsize=(8.27, 11.69), dpi=100)      # Din A4
            f.suptitle(u'Formalisierung / Proximität')
        a = f.add_subplot(111)
        a.set_xlabel(u'Proximität')
        a.set_ylabel(u'Formalisierung')
        a.set_ylim(0, 1)
        a.set_xlim(0, 1)
        a.hlines(0.5, 0, 1, linestyle='dashed')
        a.vlines(0.5, 0, 1, linestyle='dashed')

        a.annotate('Typ A', xy=(1, 1), xytext=(0.9, 0.9))
        a.annotate('Typ B', xy=(1, 0), xytext=(0.9, 0.1))
        a.annotate('Typ C', xy=(0, 1), xytext=(0.1, 0.9))
        a.annotate('Typ D', xy=(0, 0), xytext=(0.1, 0.1))

        mean = self.account.calculate_prox_form()

        a.plot(mean["xval"], mean["yval"], color='royalblue', marker='*', ms=30)

        return f
