#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Authors:    Marcus Grum, Karsten Tauchert, Norbert Gronau
    Copyright:  University of Potsdam
                Department of Business Informatics, esp. Processes and Systems
    Name:       intanalyse.py
    Description:
    This is the Class that creates a window-frame for welcoming the user and asking some preliminary questions in order
    to be able to do the assessment more proficient.
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
from Tkinter import Frame, Label, Scale
from gui.modules.Scrollinit import Scrollinit
from gui.modules.CreateToolTip import CreateToolTip

RISKINFO = (u"Bitte ergänzen Sie nachfolgende Fragen, um Ihre Risikoeinstellung "
            u"ermitteln zu können. Abhängig von Ihrer persönlichen Risikowahrnehmung "
            u"werden Sie offene Innovationsprojekte individuell beurteilen.")
PROXINFO = (u"Bitte ergänzen Sie nachfolgende Fragen, um Ihre Proximität ermitteln "
            u"zu können. Abhängig von Ihrer persönlichen Proximitätswahrnehmung werden "
            u"Sie offene Innovationsprojekte individuell beurteilen.")
FORMALINFO = (u"Bitte ergänzen Sie nachfolgende Fragen, um Ihre Formalisierung ermitteln "
              u"zu können. Abhängig von Ihrer persönlichen Formalisierungwahrnehmung werden "
              u"Sie offene Innovationsprojekte individuell beurteilen.")


class InternAnalyse:
    """

    """
    def __init__(self, sqlaccess, parent, account, project):
        self.sqlacc = sqlaccess
        self.parent = parent
        self.account = account
        self.account_id = self.account.account_id
        self.project = project
        self.status = 0
        self.intern_frame = Frame(self.parent, width=800, height=450)
        self.intern_frame.pack(side='top', fill='both', expand=1)

        self.risikoeinst = self.sqlacc.getriskassessment(self.account_id)
        self.formalization = self.sqlacc.getformalization(self.account_id)
        self.proximity = self.sqlacc.getproximity(self.account_id)

        self.risiko_scale = {}
        self.formal_scale = {}
        self.proxim_scale = {}

        # self.createframe()

        self.risk_prox_form()

    def risk_prox_form(self):
        """

        :return:
        """
        # noname = Frame(self.intern_frame)
        # noname.pack(side='bottom', fill='both', expand=1)

        scrolling = Scrollinit(self.intern_frame)
        scrollframes = scrolling.scrollbegin()
        canvas = scrollframes[0]
        frame = scrollframes[1]
        i = 1

        riskhead = Label(frame, text='Risikoeinstellung', cursor='question_arrow',
                         justify='left', font="Helvetica 12 bold")
        riskhead.grid(row=i, column=1, pady=1, sticky='w')
        CreateToolTip(riskhead, RISKINFO)
        i += 1

        # Label(frame, text=RISKINFO, justify='left', font="Helvetica 10", wraplength=700).grid(row=i, column=1, columnspan=5, pady=30, sticky='w')
        # i += 1

        Label(frame, text='Frage',
                 justify='left',
                 font="Helvetica 10 bold").grid(row=i, column=1, columnspan=2, pady=5, sticky='w')
        # Label(frame, text='Minimum',
        #         font="Helvetica 10 bold").grid(row=i, column=3, pady=5, padx=5, sticky='w')
        Label(frame, text='Skala',
                 font="Helvetica 10 bold").grid(row=i, column=4, columnspan=2, pady=5, sticky='w')
        # Label(frame, text='Maximum',
        #         font="Helvetica 10 bold").grid(row=i, column=6, padx=5, pady=5, sticky='w')
        i += 1

        for row in self.risikoeinst:
            quest_id = row["question_id"]
            Label(frame, text=row["question"],
                     wraplength=350, justify='left',
                     font="Helvetica 10").grid(row=i, column=1, columnspan=2, pady=5, sticky='w')
            Label(frame, text='Stimme absolut nicht zu',
                     font="Helvetica 10").grid(row=i, column=3, pady=5, padx=5, sticky='e')

            self.risiko_scale[quest_id] = Scale(frame, from_=0, to=1, tickinterval=0.1,  highlightthickness=1,
                                                highlightcolor='black',
                                                orient='horizontal', resolution=0.1, length=350)
            self.risiko_scale[quest_id].set(row["evaluation"])
            self.risiko_scale[quest_id].grid(row=i, column=4, columnspan=2, pady=5, sticky='w')

            Label(frame, text='Stimme voll zu',
                     font="Helvetica 10").grid(row=i, column=6, pady=5, padx=5, sticky='w')
            i += 1

        proxhead = Label(frame, text='Proximität', cursor='question_arrow',
                         justify='left', font="Helvetica 12 bold")
        proxhead.grid(row=i, column=1, pady=1, sticky='w')
        CreateToolTip(proxhead, PROXINFO)
        i += 1

        # Label(frame, text=PROXINFO, justify='left', font="Helvetica 10", wraplength=700).grid(row=i, column=1, columnspan=5, pady=30, sticky='w')
        # i += 1

        Label(frame, text='Frage',
                 justify='left',
                 font="Helvetica 10 bold").grid(row=i, column=1, columnspan=2, pady=5, sticky='w')
        # Label(frame, text='Minimum',
        #         font="Helvetica 10 bold").grid(row=i, column=3, pady=5, padx=5, sticky='w')
        Label(frame, text='Skala',
                 font="Helvetica 10 bold").grid(row=i, column=4, columnspan=2, pady=5, sticky='w')
        # Label(frame, text='Maximum',
        #         font="Helvetica 10 bold").grid(row=i, column=6, padx=5, pady=5, sticky='w')
        i += 1

        for row in self.proximity:
            quest_id = row["question_id"]
            Label(frame, text=row["question"], wraplength=350, justify='left',
                     font="Helvetica 10").grid(row=i, column=1, columnspan=2, pady=5, sticky='w')
            Label(frame, text=row["min"],
                     font="Helvetica 10").grid(row=i, column=3, pady=5, padx=5, sticky='e')
            self.proxim_scale[quest_id] = Scale(frame, from_=0, to=1, tickinterval=0.1,
                                                highlightthickness=1, highlightcolor='black',
                                                orient='horizontal', resolution=0.1, length=350)
            self.proxim_scale[quest_id].set(row["evaluation"])
            self.proxim_scale[quest_id].grid(row=i, column=4, columnspan=2, pady=5, sticky='ew')
            Label(frame, text=row["max"],
                     font="Helvetica 10").grid(row=i, column=6, pady=5, padx=5, sticky='w')
            i += 1

        formhead = Label(frame, text='Formalisierung', cursor='question_arrow',
                         justify='left', font="Helvetica 12 bold")
        formhead.grid(row=i, column=1, pady=1, sticky='w')
        CreateToolTip(formhead, FORMALINFO)
        i += 1

        # Label(frame, text=FORMALINFO, justify='left', font="Helvetica 10", wraplength=700).grid(row=i, column=1, columnspan=5, pady=30, sticky='w')
        # i += 1

        Label(frame, text='Frage',
                 justify='left',
                 font="Helvetica 10 bold").grid(row=i, column=1, columnspan=2, pady=5, sticky='w')
        # Label(frame, text='Minimum',
        #          font="Helvetica 10 bold").grid(row=i, column=3, pady=5, padx=5, sticky='w')
        Label(frame, text='Skala',
                 font="Helvetica 10 bold").grid(row=i, column=4, columnspan=2, pady=5, sticky='w')
        # Label(frame, text='Maximum',
        #         font="Helvetica 10 bold").grid(row=i, column=6, padx=5, pady=5, sticky='w')
        i += 1

        for row in self.formalization:
            quest_id = row["question_id"]
            Label(frame, text=row["question"],
                     wraplength=350, justify='left',
                     font="Helvetica 10").grid(row=i, column=1, columnspan=2, pady=5, sticky='w')
            Label(frame, text=row["min"],
                     font="Helvetica 10").grid(row=i, column=3, pady=5, padx=5, sticky='e')

            self.formal_scale[quest_id] = Scale(frame, from_=0, to=1, tickinterval=0.1, highlightthickness=1,
                                                highlightcolor='black', orient='horizontal',
                                                resolution=0.1, length=350)
            self.formal_scale[quest_id].set(row["evaluation"])
            self.formal_scale[quest_id].grid(row=i, column=4, pady=5, sticky='ew')

            Label(frame, text=row["max"],
                     font="Helvetica 10").grid(row=i, column=6, pady=5, padx=5, sticky='w')
            i += 1
        scrolling.scrollinit(canvas, frame)

    def save_entries(self):
        """

        :return:
        """
        account_id = self.account.account_id
        risiko = {}
        proxim = {}
        formal = {}

        for key in self.risiko_scale:
            risiko[key] = self.risiko_scale[key].get()
        for key in self.proxim_scale:
            proxim[key] = self.proxim_scale[key].get()
        for key in self.formal_scale:
            formal[key] = self.formal_scale[key].get()

        self.sqlacc.ins_interne(account_id, risiko, proxim, formal)
        # print "Interne gespeichert!"


