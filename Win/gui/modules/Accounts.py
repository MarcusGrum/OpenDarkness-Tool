#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Authors:    Marcus Grum, Karsten Tauchert, Norbert Gronau
    Copyright:  University of Potsdam
                Department of Business Informatics, esp. Processes and Systems
    Name:       Accounts.py
    Description:
    Class to keep the user information at hand.
    Getter methods for project-ids and account-ids
    Setter methods for new users needed??
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
from numpy import mean


class Account:
    """

    """
    def __init__(self, sqlaccess, email):
        """
        sqlacc allows the comunication to the db.
        email is the minimum of information needed to create an account, password is given on the
        way, but entered directly into db.
        :param sqlaccess: 
        :param email: 
        """
        self.name = email
        # self.sqlacc is the instance to communicate to the database.
        self.sqlacc = sqlaccess
        self.account_id = self.sqlacc.getaccountid(email)
        self.project_ids = self.sqlacc.getprojid(self.account_id)
        self.prequest_status = self.sqlacc.get_riskformprox_status(self.account_id)
        if self.prequest_status == 0:
            self.sqlacc.init_internstuff(self.account_id)
        self.riskassessment = {}
        self.formalization = {}
        self.proximity = {}

    def getaccid(self):
        """
        Getter: account id
        
        :return: string
        """
        return self.account_id

    def getprojid(self):
        """
        Getter: project ids (one or more)
        :return: list
        """
        ids = []
        for i in range(len(self.project_ids)):
            ids.append(self.project_ids[i]["project_id"])

        return ids                  # List of Project ids

    def update_projectids(self):
        """
        Updates the project ids. Used after creating new project.
        :return: list
        """
        self.project_ids = self.sqlacc.getprojid(self.account_id)

    def getemail(self):
        """
        Getter: email address
        :return: string
        """
        return self.name

    def getpasswd(self):
        """
        Getter: password (from db, not this)
        :return: string
        """
        pword = self.sqlacc.getpass(self.name)
        return pword

    def getriskassessment(self):
        """
        Gets the assessment, the evaluation, of the Risikoeinstellung-Fragen.
        :return: dict
        """
        return self.riskassessment

    def getproximity(self):
        """
        Gets the evaluation of the Proximity questions.
        :return: dict
        """
        return self.proximity

    def getformalization(self):
        """
        Gets the evaluation of the Formaliztion questions.
        :return: dict
        """
        return self.formalization

    def setprojectids(self):
        """
        Ups, a double. FIXIT!
        :return: list
        """
        self.project_ids = self.sqlacc.getprojid(self.account_id)

    def setstuff(self):
        """
        Sets the riskassessment, formalization and proximity evalution.
        :return:
        """
        self.riskassessment = self.sqlacc.getriskassessment(self.account_id)
        self.formalization = self.sqlacc.getformalization(self.account_id)
        self.proximity = self.sqlacc.getproximity(self.account_id)

    def calculate_risk_ass(self):
        """
        Calculates the Risikoeinstellung of the account.
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
        self.setstuff()
        info = {}
        eval = []

        for key in self.riskassessment:
            eval.append(key["evaluation"])

        info["mean"] = mean(eval)
        if info["mean"] < 0.3333:
            info["type"] = 'risikoavers'
            info["text"] = risikoavers
        elif info["mean"] > 0.6666:
            info["type"] = 'risikoaffin'
            info["text"] = risikoaffin
        else:
            info["type"] = 'risikoneutral'
            info["text"] = risikoneutral
        return info

    def calculate_prox_form(self):
        """
        Calculates the Kooperationstyp and returns it.
        :return:
        """
        self.setstuff()
        info = {}
        mean_form = []
        mean_prox = []

        for row in self.formalization:
            mean_form.append(row["evaluation"])
        for row in self.proximity:
            mean_prox.append(row["evaluation"])

        info["xval"] = mean(mean_prox)
        info["yval"] = mean(mean_form)

        if info["xval"] <= 0.5 and info["yval"] <= 0.5:
            type = "Type D"
            text = ("Es gibt eine stille Übereinkunft bzgl. Rechte und Pflichten zur Erreichung des Kooperationsziels."
                    " Kollaborationsmitglieder treffen gemeinsame Entscheidungen. Beteiligte kennen sich nicht sehr gut "
                    "(z.B. verteiltes Problemlösen, Innovationswettbewerbe).")
        elif info["xval"] <= 0.5 and info["yval"] > 0.5:
            type = "Type C"
            text = ("Kollaboration ist auf allgemeine, zukünftige strategische Ziele ausgerichtet. Beteiligte "
                    "fokussieren indirekt ihre Aktivitäten auf das gemeinsame Ziel (z.B. Konsortium, "
                    "strategisches Netzwerk).")
        elif info["xval"] > 0.5 and info["yval"] <= 0.5:
            type = "Type B"
            text = ("Projektaufgaben sind klar unter den Beteiligten der zeitlich befristeten Kollaboration"
                    " aufgeteilt. Projektaktivitäten werden mit Hilfe von IuK Technologie koordiniert "
                    "(z.B. Open Source Software).")
        else:
            type = "Type A"
            text = ("Rechte und Pflichten sind klar zwischen den Beteiligten der Kooperation verteilt. "
                    "Die fokale Organisation führt die Unternehmung. Projektorientierte Arbeitsteilung und "
                    "Steuerung erfolgt mittels klassischer Koordiantionsinstrumente (z.B. Allianz).")

        info["type"] = type
        info["text"] = text

        return info
