#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Authors:    Marcus Grum, Karsten Tauchert, Norbert Gronau
    Copyright:  University of Potsdam
                Department of Business Informatics, esp. Processes and Systems
    Name:       extananlyse.py
    Description:
    This is the Class that creates a window-frame for creating all the "questions" for risk and chance assessment.
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
from Tkinter import LabelFrame, Label, Scale
from gui.modules.Scrollinit import Scrollinit
from gui.modules.CreateToolTip import CreateToolTip

CHANCEINFO = (u"Bitte ergänzen Sie nachfolgende Fragen, um die Chancen einer Öffnung "
              u"Ihres Projekts ermitteln zu können. Beurteilen Sie die jeweils "
              u"genannte Chance hinsichtlich ihrer Eintrittswahrscheinlichkeit sowie dessen "
              u"Ausmaß. Abhängig von Ihrer persönlichen Chancenwahrnehmung werden Sie zu offenen "
              u"Innovationsprojekten individuell neigen, oder nicht.")
RISKINFO =(u"Bitte ergänzen Sie nachfolgende Fragen, um die Risiken einer Öffnung Ihres Projekts ermitteln "
           u"zu können. Beurteilen Sie das jeweils genannte Risiko hinsichtlich seiner "
           u"Eintrittswahrscheinlichkeit sowie dessen  Ausmaß. Abhängig von Ihrer persönlichen "
           u"Risikenwahrnehmung werden Sie zu offenen Innovationsprojekten individuell neigen, oder nicht.")

class ExternAnalyse:
    """
    This boss is delegating methods and functions and frames and labels in order to look neat and usable.
    """
    def __init__(self, sqlaccess, parent, project):
        self.sqlacc = sqlaccess
        self.parent = parent
        self.project = project
        self.questframe = LabelFrame(self.parent, width=800, height=450,
                                        text='Fragenkatalog:')
        self.questframe.pack(side='bottom', fill='both', expand=1)
        self.probscale_c = {}
        self.relescale_c = {}
        self.probscale_r = {}
        self.relescale_r = {}
        self.status = 0
        # self.headline()
        self.createquestions()

    def createquestions(self):
        """
        The data (qustions, probabilities, extents, and.. ar being pulled from the db, so this method can create
        the desired questions and scales.
        :return: 0
        """

        # proj_id = self.project.getprojid()
        evaled_questions_ch = self.sqlacc.getchanceeval(self.project.getprojid())
        evaled_questions_ri = self.sqlacc.getriskeval(self.project.getprojid())

        # self.windows["noname"] = Frame(self.questframe)
        # noname.pack(side='bottom', fill='both', expand=1)

        scrolling = Scrollinit(self.questframe)
        scrollframes = scrolling.scrollbegin()
        canvas = scrollframes[0]
        frame = scrollframes[1]
        info_text = ("Bitte beurteilen Sie, wie die folgenden Chancen und Risiken "
                     "Ihre Projektsituation beeinflussen, gemäß Wahrscheinlichkeit"
                     " und Ausmaß.")
        # tk.Label(frame, text=info_text,
        #         font="Helvetica 12 bold", wraplength=700, justify='left').grid(row=0, column=0,
        #                                                                        columnspan=5,
        #                                                                        pady=5, sticky='w')
        i = 1
        chancehead = Label(frame, text='Chancen', cursor='question_arrow',
              font="Helvetica 12 bold")
        chancehead.grid(row=i, column=0, pady=10, sticky='w')
        CreateToolTip(chancehead, CHANCEINFO)
        i += 1
        #Label(frame, text=CHANCEINFO,
        #      justify='left', font="Helvetica 10",
        #      wraplength=700).grid(row=i, column=0, columnspan=5, pady=30, sticky='w')
        i += 1
        Label(frame, text='ID',
              font="Helvetica 10 bold").grid(row=i, column=0, pady=5, sticky='w')
        Label(frame, text='Einflußfaktor',
              font="Helvetica 10 bold").grid(row=i, column=1, pady=5, sticky='w')
        Label(frame, text='Frage',
              font="Helvetica 10 bold").grid(row=i, column=2, columnspan=2, pady=5, sticky='w')
        Label(frame, text='Wahrscheinlichkeit',
              font="Helvetica 10 bold").grid(row=i, column=4, pady=5, sticky='w')
        Label(frame, text='Ausmaß',
              font="Helvetica 10 bold").grid(row=i, column=5, pady=5, sticky='w')
        i += 1
        for rows in evaled_questions_ch:
            chanceid = rows["question_id"]

            Label(frame, text=chanceid,
                  justify='left',
                  font="Helvetica 10").grid(row=i, column=0, pady=10, sticky='w')
            Label(frame, text=rows["influence_factor"],
                  wraplength=200, justify='left',
                  font="Helvetica 10").grid(row=i, column=1, pady=10, sticky='w')
            Label(frame, text=rows["question"],
                  wraplength=270, justify='left',
                  font="Helvetica 10").grid(row=i, column=2,
                                           columnspan=2, pady=10, sticky='w')
            self.probscale_c[chanceid] = (Scale(frame, from_=0, to=1,
                                                length=225, tickinterval=0.2,
                                                resolution=0.1, highlightthickness=1, highlightcolor='black',
                                                orient='horizontal'))
            self.probscale_c[chanceid].set(rows["probability"])
            self.probscale_c[chanceid].grid(row=i, column=4, pady=10,
                                            sticky='w')
            self.relescale_c[chanceid] = (Scale(frame, from_=0, to=10,
                                                length=225, tickinterval=1,
                                                resolution=1, highlightthickness=1, highlightcolor='black',
                                                orient='horizontal'))
            self.relescale_c[chanceid].set(rows["extent"])
            self.relescale_c[chanceid].grid(row=i, column=5, pady=10,
                                            sticky='w')
            i += 1
        riskhead = Label(frame, text='Risiken', cursor='question_arrow',
                         font="Helvetica 12 bold")
        riskhead.grid(row=i, column=0, pady=10, sticky='w')
        CreateToolTip(riskhead, RISKINFO)
        i += 1
        # Label(frame, text=RISKINFO,
        #       justify='left', font="Helvetica 10",
        #       wraplength=700).grid(row=i, column=0, columnspan=5, pady=30, sticky='w')
        # i += 1
        Label(frame, text='ID',
              font="Helvetica 10 bold").grid(row=i, column=0, pady=5, sticky='w')
        Label(frame, text='Einflußfaktor',
              font="Helvetica 10 bold").grid(row=i, column=1, pady=5, sticky='w')
        Label(frame, text='Frage',
              font="Helvetica 10 bold").grid(row=i, column=2, columnspan=2, pady=5, sticky='w')
        Label(frame, text='Wahrscheinlichkeit',
              font="Helvetica 10 bold").grid(row=i, column=4, pady=5, sticky='w')
        Label(frame, text='Ausmaß',
              font="Helvetica 10 bold").grid(row=i, column=5, pady=5, sticky='w')
        i += 1
        for rows in evaled_questions_ri:
            risikoid = rows["question_id"]
            Label(frame, text=risikoid,
                  justify='left',
                  font="Helvetica 10").grid(row=i, column=0, pady=10, sticky='w')
            Label(frame, text=rows["influence_factor"],
                  wraplength=250, justify='left',
                  font="Helvetica 10").grid(row=i, column=1, pady=10, sticky='w')
            Label(frame, text=rows["question"],
                  wraplength=300, justify='left',
                  font="Helvetica 10").grid(row=i, column=2, columnspan=2, pady=10, sticky='w')
            self.probscale_r[risikoid] = (Scale(frame, from_=0, to=1,
                                                length=225, tickinterval=0.2,
                                                resolution=0.1,
                                                orient='horizontal'))
            self.probscale_r[risikoid].set(rows["probability"])
            self.probscale_r[risikoid].grid(row=i, column=4, pady=10,
                                            sticky='w')
            self.relescale_r[risikoid] = (Scale(frame, from_=0, to=10,
                                                length=225, tickinterval=1,
                                                resolution=1,
                                                orient='horizontal'))
            self.relescale_r[risikoid].set(rows["extent"])
            self.relescale_r[risikoid].grid(row=i, column=5, pady=10,
                                            sticky='w')
            i += 1
        scrolling.scrollinit(canvas, frame)

    def saveresults(self):
        """
        After the button for saving the data is being pushed, this method does the work in inserting or updating
        the data in tha database.
        :return: None
        """
        prob_cha = {}
        scal_cha = {}
        for key in self.probscale_c:
            prob_cha[key] = self.probscale_c[key].get()
        for key in self.relescale_c:
            scal_cha[key] = self.relescale_c[key].get()
        self.sqlacc.inschanceeval(self.project.getprojid(), prob_cha, scal_cha)

        prob_ris = {}
        scal_ris = {}
        for key in self.probscale_r:
            prob_ris[key] = self.probscale_r[key].get()
        for key in self.relescale_r:
            scal_ris[key] = self.relescale_r[key].get()
        self.sqlacc.insriskeval(self.project.getprojid(), prob_ris, scal_ris)
        # print "Externe gespeichert"
