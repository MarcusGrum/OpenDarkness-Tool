#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Authors:    Marcus Grum, Karsten Tauchert, Norbert Gronau
    Copyright:  University of Potsdam
                Department of Business Informatics, esp. Processes and Systems
    Name:       Projects.py
    Description:
    This is the Project class. It contains methods and variables
    to a certain user account. The variables contain the id, name and
    the description of all the project that belong to the user.
    It is a module for the OpenDarkness Tool.
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
# import mysqlaccess as sqlacc
# from .mysqlaccess import MySqlConnect as sqlacc

class Project:

    def __init__(self, sqlaccess,  proj_id):

        # self.local_bind_p = local_bind_p
        self.sqlacc = sqlaccess
        self.proj_id = proj_id
        # Fehlerbehandlung falls keine Einträge für ID -> FIX
        self.project_nm = self.sqlacc.getprojname(self.proj_id)
        self.project_descr = self.sqlacc.getprojdescr(self.proj_id)
        self.proj_account = ""
        self.measure_status = 0
        self.chance = {}
        self.risk = {}
        self.chance_measures = {}
        self.risk_measures = {}

    def getprojname(self):

        return self.project_nm

    def getprojid(self):

        return self.proj_id

    def getdescription(self):

        return self.project_descr

    def getchance(self):

        return self.chance

    def getrisk(self):

        return self.risk

    def getchance_measure(self):

        return self.chance_measures

    def getrisk_measure(self):

        return self.risk_measures

    def getriskassessment(self):

        return self.riskassesment

    def getproxform(self):

        return self.form_prox

    # ****** SETTER  ******
    def setprojaccount(self, acc_id):
        self.proj_account = acc_id

    def setprojname(self, name):

        self.project_nm = name

    def setprojdescr(self, proj_descr):

        self.project_descr = proj_descr

    def setprojid(self):

        self.proj_id = self.sqlacc.projid_by_name(self.project_nm)

    def set_chance(self, probability, extent):

        self.chance["probability"] = probability
        self.chance["extent"] = extent

        # self.chance = self.sqlacc.getchanceeval(self.proj_id)

    def set_risk(self, probability, extent):

        self.risk["probability"] = probability
        self.risk["extent"] = extent

        # self.risk = self.sqlacc.getriskeval(self.proj_id)

    def set_chance_measures(self, probaility, extent):

        self.chance_measures["probability"] = probaility
        self.chance_measures["exetnt"] = extent

        # self.chance_measures = self.sqlacc(self.proj_id)

    def set_risk_measures(self, probability, extent):

        self.risk_measures["probability"] = probability
        self.risk_measures["extent"] = extent

        # self.chance_measures = self.sqlacc(self.proj_id)

    # def setstuff(self):
    #
    #     self.chance = self.sqlacc.getchanceeval(self.proj_id)
    #     self.risk = self.sqlacc.getriskeval(self.proj_id)
    #     self.chance_measures = self.sqlacc.getmeasures_chance(self.proj_id)
    #     self.risk_measures = self.sqlacc.getmeasures_risk(self.proj_id)

    def project2sql(self):
        self.sqlacc.setproject(self.project_nm, self.project_descr, self.proj_account)

    def showdata(self):

        print self.proj_id, self.project_nm, self.project_descr

    def get_measure_status(self):

        self.measure_status = self.sqlacc.return_measure_status(self.proj_id)

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
        print "Externe gespeichert"