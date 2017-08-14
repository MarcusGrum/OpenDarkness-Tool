#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Authors:    Marcus Grum, Karsten Tauchert, Norbert Gronau
    Copyright:  University of Potsdam
                Department of Business Informatics, esp. Processes and Systems
    Name:       Integrated.py
    Description:
    This is the Class that creates a window-frame for creating all the "measures" for risk and chance assessment.
    The user is able to select the preferred and correlating numbers on the sliders.
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
from Tkinter import Label,LabelFrame, Scale
from gui.modules.Scrollinit import Scrollinit
from gui.modules.CreateToolTip import CreateToolTip

CHANCEINFO = (u"Bitte ergänzen Sie nachfolgende Fragen, um zu ermitteln, ob nachfolgend "
              u"gezeigte Maßnahmen die Chancen einer Öffnung Ihres Projekts verbessern. "
              u"Dies betrifft sowohl die Erhöhung der Eintrittswahrscheinlichkeit einer "
              u"Chance sowie deren Ausmaß.")
RISKINFO = (u"Bitte ergänzen Sie nachfolgende Fragen, um zu ermitteln, ob nachfolgend "
            u"gezeigte Maßnahmen die Risiken einer Öffnung Ihres Projekts verbessern. "
            u"Dies betrifft sowohl die Verminderung der Eintrittswahrscheinlichkeit "
            u"eines Risikos sowie dessen Ausmaß.")

class IntegratedAnalyse:
    """

    """
    def __init__(self, sqlaccess, parent, account, project):
        self.sqlacc = sqlaccess
        self.parent = parent
        self.account = account
        self.project = project
        self.status = 0
        self.measuresframe = LabelFrame(self.parent, text='Maßnahmen', width=800, height=450)
        self.measuresframe.pack(side='bottom', fill='both', expand=1)

        self.cha_probscale = {}
        self.cha_relescale = {}
        self.ris_probscale = {}
        self.ris_relescale = {}

        self.init_measure()
        self.createmeasures()

    def init_measure(self):
        """

        :return:
        """
        measures_status = self.sqlacc.get_measure_status(self.project.proj_id)
        print measures_status
        if (measures_status["prob_avg"] and measures_status["ext_avg"]) == 0:
            # print u"möööp... keine vorhanden Daten!"
            self.sqlacc.initmeasures(self.project.getprojid())

    def createmeasures(self):
        """

        :return:
        """
        proj_id = self.project.proj_id
        riskass = self.getrisk()
        proxform = self.getproxform()
        measure_intro = ("Bitte beurteilen sie wie die nachfolgenden Maßnahmen "
                         "Ihre Projektsituation verbessern.")
        # topframe = Frame(self.measuresframe, width=800, height=600)
        # topframe.pack(side='bottom', fill='both', expand=1)

        measures_chance = self.sqlacc.getmeasures_chance(proj_id)
        measures_risk = self.sqlacc.getmeasures_risk(proj_id)

        # measures_chance = self.project.chance_measures
        # measures_risk = self.project.risk_measures


        scrolling = Scrollinit(self.measuresframe)
        scrollframes = scrolling.scrollbegin()
        canvas = scrollframes[0]
        frame = scrollframes[1]

        # i = 1
        # Label(frame, text=measure_intro, justify='left',
        #         font="Helvetica 12 bold").grid(row=i, column=0, columnspan=5,
        #                                        pady=5, sticky='w')

        i = 1
        chancehead = Label(frame, text='Chancen', justify='left', cursor='question_arrow',
                           font="Helvetica 12 bold")
        chancehead.grid(row=i, column=0, pady=5, sticky='w')
        CreateToolTip(chancehead, CHANCEINFO)
        i += 1

        # Label(frame, text=CHANCEINFO, justify='left', font="Helvetica 10", wraplength=700).grid(row=i, column=0, columnspan=5, pady=30, sticky='w')
        # i += 1

        Label(frame, text='ID', justify='left',
                 font="Helvetica 10 bold").grid(row=i, column=0, pady=5, sticky='w')
        Label(frame, text='Einflussfaktor', justify='left',
                 font="Helvetica 10 bold").grid(row=i, column=1, pady=5, sticky='w')
        Label(frame, text='Maßnahme', justify='left',
                 font="Helvetica 10 bold").grid(row=i, column=2, columnspan=2, pady=5,  sticky='w')
        Label(frame, text='Wahrscheinlichkeit', justify='left',
                 font="Helvetica 10 bold").grid(row=i, column=4, pady=5, sticky='w')
        Label(frame, text='Ausmaß', justify='left',
                 font="Helvetica 10 bold").grid(row=i, column=5, pady=5, sticky='w')

        i += 1
        for rows in measures_chance:
            chanceid = rows["measures_id"]

            Label(frame, text=chanceid,
                     justify='left', font="Helvetica 10").grid(row=i, column=0, pady=10, sticky='w')
            Label(frame, text=rows["influence_factor"],
                     justify='left', wraplength=200).grid(row=i, column=1, pady=10, sticky='w')
            Label(frame, text=rows["measure"],
                     wraplength=350, justify='left',
                     font="Helvetica 10").grid(row=i, column=2, columnspan=2, pady=10, sticky='w')
            self.cha_probscale[chanceid] = (Scale(frame, from_=rows["probability"], to=1,
                                                  length=225, tickinterval=0.1,
                                                  highlightthickness=1, highlightcolor='black',
                                                  resolution=0.1,
                                                  orient='horizontal'))
            self.cha_probscale[chanceid].grid(row=i, column=4, pady=10,
                                              sticky='w')
            self.cha_relescale[chanceid] = (Scale(frame, from_=rows["extent"], to=10,
                                                  length=225, tickinterval=1,
                                                  resolution=1,
                                                  highlightthickness=1, highlightcolor='black',
                                                  orient='horizontal'))
            self.cha_relescale[chanceid].grid(row=i, column=5, pady=10,
                                              sticky='w')

            i += 1
        riskhead = Label(frame, text='Risiken', cursor='question_arrow',
                         font="Helvetica 12 bold")
        riskhead.grid(row=i, column=0, pady=5)
        CreateToolTip(riskhead, RISKINFO)
        i += 1

        # Label(frame, text=RISKINFO, justify='left', font="Helvetica 10", wraplength=700).grid(row=i, column=0, columnspan=5, pady=30, sticky='w')
        # i += 1

        Label(frame, text='ID',
                 font="Helvetica 10 bold").grid(row=i, column=0, pady=5, sticky='w')
        Label(frame, text='Einflussfaktor',
                 font="Helvetica 10 bold").grid(row=i, column=1, pady=5, sticky='w')
        Label(frame, text='Maßnahme',
                 font="Helvetica 10 bold").grid(row=i, column=2, columnspan=2, pady=5, sticky='w')
        Label(frame, text='Wahrscheinlichkeit',
                 font="Helvetica 10 bold").grid(row=i, column=4, pady=5, sticky='w')
        Label(frame, text='Ausmaß',
                 font="Helvetica 10 bold").grid(row=i, column=5, pady=5, sticky='w')

        i += 1
        for rows in measures_risk:
            riskid = rows["measures_id"]

            Label(frame, text=riskid,
                     justify='left', font="Helvetica 10").grid(row=i, column=0, pady=10, sticky='w')
            Label(frame, text=rows["influence_factor"],
                     justify='left', wraplength=200).grid(row=i, column=1, pady=10, sticky='w')
            Label(frame, text=rows["measure"],
                     wraplength=350, justify='left',
                     font="Helvetica 10").grid(row=i, column=2, columnspan=2, pady=10, sticky='w')
            self.ris_probscale[riskid] = (Scale(frame, from_=0, to=rows["probability"],
                                                   length=225, tickinterval=0.2,
                                                   resolution=0.1,
                                                highlightthickness=1, highlightcolor='black',
                                                   orient='horizontal'))
            self.ris_probscale[riskid].set(rows["probability"])
            self.ris_probscale[riskid].grid(row=i, column=4, pady=10,
                                            sticky='w')
            self.ris_relescale[riskid] = (Scale(frame, from_=0, to=rows["extent"],
                                                   length=225, tickinterval=1,
                                                   resolution=1,
                                                highlightthickness=1, highlightcolor='black',
                                                   orient='horizontal'))
            self.ris_relescale[riskid].set(rows["extent"])
            self.ris_relescale[riskid].grid(row=i, column=5, pady=10,
                                            sticky='w')
            i += 1
        i += 1
        Label(frame, text="Risikoeinstellung: ",
                 font="Helvetica 12 bold").grid(row=i, column=0, columnspan=2, pady=5, sticky='w')
        # *** Fill ***
        i += 1
        Label(frame, text=riskass,
                 font="Helvetica 10", wraplength=700, justify='left').grid(row=i, column=0, columnspan=3, pady=5, sticky='w')
        i += 1
        Label(frame, text="Proximität und Formalisierung:",
                 font="Helvetica 12 bold").grid(row=i, column=0, columnspan=2, pady=5, sticky='w')
        # *** Fill ***
        i += 1
        Label(frame, text=proxform,
                 font="Helvetica 10", wraplength=700, justify='left').grid(row=i, column=0, columnspan=3,
                                                                           pady=5, sticky='w')
        scrolling.scrollinit(canvas, frame)

    def getrisk(self):
        """

        :return:
        """
        risikoaffin = ("Nach der Auswertung der Fragen, wird Ihnen eine \"risikoaffine\" Tendenz zugeschrieben.\n"
                       "Unsere Empfehlung wäre, dass Sie sich einen Partner suchen, der Risiken streng bewertet "
                       "und somit eine Unterschätzung der Risiken minimiert.")
        risikoneutral = ("Nach der Auswertung der Fragen, wird Ihnen eine \"risikoneutrale\" Tendenz zugeschrieben.\n"
                         "Unsere Empfehlung wäre, dass Sie sich einen erfahrenen Partner suchen der Ihnen bei der "
                         "Einschätzung der Risiken und der Umsetzung von Standards behilflich sein kann")
        risikoavers = ("Nach der Auswertung der Fragen, wird Ihnen eine \"risikoaverse\" Tendenz zugeschrieben.\n"
                       "Unsere Empfehlung wäre, dass Sie sich einen erfahrenen Partner suchen, der Ihnen Sicherheit "
                       "im Umgang mit Risiken gibt und eine eventuelle Überschätzung der Risiken minimiert.")
        info_risk = self.account.calculate_risk_ass()
        if info_risk["type"] == "risikoaffin":
            return risikoaffin
        elif info_risk["type"] == 'risikoneutral':
            return risikoneutral
        else:
            return risikoavers

    def getproxform(self):
        """

        :return:
        """

        res = self.account.calculate_prox_form()
        text = str(res["type"]) + "\n" + str(res["text"])
        # ** empfehlung und schmuh
        return text

    def save_measures(self):
        """

        :return:
        """
        prob_cha = {}
        scal_cha = {}
        for key in self.cha_probscale:
            prob_cha[key] = self.cha_probscale[key].get()
        for key in self.cha_relescale:
            scal_cha[key] = self.cha_relescale[key].get()
        self.sqlacc.insmeasure_chance(self.project.getprojid(), prob_cha, scal_cha)

        prob_ris = {}
        scal_ris = {}
        for key in self.ris_probscale:
            prob_ris[key] = self.ris_probscale[key].get()
        for key in self.ris_relescale:
            scal_ris[key] = self.ris_relescale[key].get()
        self.sqlacc.insmeasure_risk(self.project.getprojid(), prob_ris, scal_ris)
        # print "Maßnahmen gespeichert!"
