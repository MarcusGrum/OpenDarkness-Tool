#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Authors:    Marcus Grum, Karsten Tauchert, Norbert Gronau
    Copyright:  University of Potsdam
                Department of Business Informatics, esp. Processes and Systems
    Name:       sqlaccess.py
    Description:
    MySQL-Methods for reaching out to the database and asking and entering a lot of data.
    It connects to the desired database and has its own queries for inserting, updating and retrieving data.
    Used by: OD_Tool_Class, Projects, Accounts, extanalyse, integrated, recomphase.
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
# import MySQLdb as Mydb
from MySQLdb import connect, cursors
from gui.modules.ResourcePath import resource_path
try:
    import configparser
except:
    from six.moves import configparser


class MySqlConnect:
    """
    Containing all methods and functions to access, read and write into the Database, based on
    MySQL.
    """

    def __init__(self, local_bind_p):

        config = configparser.ConfigParser()
        config.read(resource_path('gui/filingarea/odconfig.ini'))
        host = config.get('mysql.access.opendarkness', 'host')
        user = config.get('mysql.access.opendarkness', 'user')
        passwd = config.get('mysql.access.opendarkness', 'passwd')
        db = config.get('mysql.access.opendarkness', 'db')
        charset = config.get('mysql.access.opendarkness', 'charset')
        self.local_bind_p = local_bind_p
        self.connection = connect(host=host, port=self.local_bind_p, user=user,
                                  passwd=passwd,
                                  db=db, charset=charset, use_unicode=True)

    def getname(self):
        """
        Get all email-entries from Account-table for comparison
        :return: dict string
        """
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            sqlex = ("SELECT "
                     "email "
                     "FROM "
                     "Account")
            cursor.execute(sqlex)
            return cursor.fetchall()

    def getpass(self, email):
        """
        Get the password for a given email-addy.
        :param email: string
        :return: string
        """
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            sqlex = ("SELECT "
                     "account_pass "
                     "FROM "
                     "Account "
                     "WHERE "
                     "email='" + email + "'")
            cursor.execute(sqlex)
            accpass = cursor.fetchone()
            return accpass["account_pass"]

    def getprojid(self, accid):
        """
        Get the project_id connected to the account.
        :param accid: int
        :return: dict string
        """
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            sqlex = ("SELECT "
                     "project_id "
                     "FROM "
                     "Project "
                     "WHERE account_id=" + str(accid))
            cursor.execute(sqlex)
            return cursor.fetchall()

    def projid_by_name(self, proj_name):
        """
        Needed after creating a new project.
        Maybe there is a better way, but for the time being:
        Get the project_id connected to a project_name.
        :param proj_name: string
        :return: int
        """
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            proj_name = proj_name.encode('utf-8')
            # print proj_name
            sqlex = ("SELECT "
                     "project_id "
                     "FROM "
                     "Project "
                     "WHERE project_name= \"" + proj_name + "\"")
            cursor.execute(sqlex)
            project_id = cursor.fetchone()
            return project_id["project_id"]

    def getprojname(self, projid):
        """
        Get the name of the project connected to the given project_id.
        :param projid: int
        :return: string
        """
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            sqlex = ("SELECT "
                     "project_name "
                     "FROM "
                     "Project "
                     "WHERE project_id=" + str(projid))
            cursor.execute(sqlex)
            proname = cursor.fetchone()
            if proname is None:
                return ""
            else:
                return proname["project_name"]

    def getaccountid(self, email):
        """
        Get the account_id connected to the email.
        :param email: string
        :return: int
        """
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            sqlex = ("SELECT "
                     "account_id "
                     "FROM "
                     "Account "
                     "WHERE email='" + email + "'")
            cursor.execute(sqlex)
            accid = cursor.fetchone()
            return accid["account_id"]

    def getprojdescr(self, projid):
        """
        Get Project Description by project id
        :return: string
        """
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            sqlex = ("SELECT "
                     "project_description "
                     "FROM "
                     "Project "
                     "WHERE project_id=" + str(projid))
            cursor.execute(sqlex)
            description = cursor.fetchone()
            if description is None:
                return ""
            else:
                return description["project_description"]

    def getprojcount(self):
        """
        Get the count of projects. Used to be able to refer to the project_id.
        :return: int
        """
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            sqlex = "SELECT * FROM Project"
            cursor.execute(sqlex)
            count = cursor.fetchall()
            count = len(count)
            return count

    def setproject(self, proj_name, proj_descr, acc_id):
        """
        Enter the Project Data into the Database.
        :param proj_name: string
        :param proj_descr: string
        :param acc_id: int
        :return: 0
        """

        cursor = self.connection.cursor(cursors.DictCursor)
        proj_descr = proj_descr.encode('utf-8')
        proj_name = proj_name.encode('utf-8')

        sqlex = ("INSERT INTO "
                 "Project "
                 "( project_name, project_description, account_id) "
                 "VALUES "
                 "( '" + proj_name + "', '" + proj_descr + "', " +
                 str(acc_id) + ")")
        cursor.execute(sqlex)
        self.connection.commit()

    def inschanceeval(self, proj_id, probability, scale):
        """
        Write the evaluation data from the questions by chances.
        :param proj_id: int
        :param probability: float
        :param scale: float
        :return: 0
        """
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            for key in probability:
                sqlex = ("UPDATE "
                         "Chance_Evaluations "
                         "SET "
                         "extent =" + str(scale[key]) + ", "
                         "probability =" + str(probability[key]) +
                         "WHERE question_id=" + str(key) +
                         " AND "
                         "project_id=" + str(proj_id))
                cursor.execute(sqlex)
            self.connection.commit()

    def insriskeval(self, proj_id, probability, scale):
        """
        Write the evaluation data from the questions by risk.
        :param proj_id: int
        :param probability: float
        :param scale: float
        :return: 0
        """
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            for key in probability:
                sqlex = ("UPDATE "
                         "Risk_Evaluations "
                         "SET "
                         "extent =" + str(scale[key]) +
                         ", "
                         "probability =" + str(probability[key]) +
                         "WHERE question_id=" + str(key) +
                         " AND project_id=" + str(proj_id))
                cursor.execute(sqlex)
            self.connection.commit()

    def getchanceeval(self, proj_id):
        """
        Get the Chance questions with their associated evaluation.
        :param proj_id: int
        :return: dict string
        """
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            sqlex = ("SELECT "
                     "Chance_Evaluations.question_id, "
                     "probability, "
                     "extent, "
                     "Chance_Questions_Excerpt.influence_factor, "
                     "Chance_Questions_Excerpt.question "
                     "FROM "
                     "Chance_Evaluations "
                     "JOIN "
                     "Chance_Questions_Excerpt "
                     "ON Chance_Evaluations.question_id = Chance_Questions_Excerpt.question_id "
                     "WHERE project_id = " + str(proj_id))
            cursor.execute(sqlex)
            # evaluation = cursor.fetchall()
            # return evaluation
            return cursor.fetchall()

    def get_chance_eval(self, proj_id):
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            sqlex = ("SELECT "
                     "probability, extent "
                     "FROM "
                     "Chance_Evaluations "
                     "WHERE "
                     "project_id = " + str(proj_id))
            cursor.execute(sqlex)
            return cursor.fetchall()

    def getriskeval(self, proj_id):
        """
        Get the risk question with their associated evaluation.
        :param proj_id: int
        :return: dict string
        """
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            sqlex = ("SELECT "
                     "Risk_Evaluations.question_id, "
                     "probability, "
                     "extent, "
                     "Risk_Questions_Excerpt.influence_factor, "
                     "Risk_Questions_Excerpt.question "
                     "FROM "
                     "Risk_Evaluations "
                     "JOIN "
                     "Risk_Questions_Excerpt "
                     "ON Risk_Evaluations.question_id = Risk_Questions_Excerpt.question_id "
                     "WHERE project_id = " + str(proj_id))
            cursor.execute(sqlex)
            # evaluation = cursor.fetchall()
            # return evaluation
            return cursor.fetchall()

    def get_risk_eval(self, proj_id):
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            sqlex = ("SELECT "
                     "probability, extent "
                     "FROM "
                     "Risk_Evaluations "
                     "WHERE "
                     "project_id = " + str(proj_id))
            cursor.execute(sqlex)
            return cursor.fetchall()

    def initializerows(self, proj_id):
        """
        Intitializing rows for chance and risk evaluation after creating new project.
        Used to get the initial scale setting for the evaluation.
        :param proj_id: int
        :return: 0
        """
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            sqlex = ("SELECT "
                     "question_id "
                     "FROM "
                     "Chance_Questions_Excerpt")
            cursor.execute(sqlex)
            questions_c = cursor.fetchall()

            sqlex = ("SELECT "
                     "question_id "
                     "FROM "
                     "Risk_Questions_Excerpt")
            cursor.execute(sqlex)
            questions_r = cursor.fetchall()

            for row in questions_c:
                sqlex = ("INSERT INTO Chance_Evaluations "
                         "(project_id, question_id, extent, probability) VALUES (" +
                         str(proj_id) + ", " + str(row["question_id"]) + ", 0, 0)")
                cursor.execute(sqlex)

            for row in questions_r:
                sqlex = ("INSERT INTO Risk_Evaluations "
                         "(project_id, question_id, extent, probability) VALUES (" +
                         str(proj_id) + ", " + str(row["question_id"]) + ", 0, 0)")
                cursor.execute(sqlex)

            self.connection.commit()

            sqlex = ("SELECT "
                     "measures_id "
                     "FROM "
                     "Chance_Measures_Excerpt")
            cursor.execute(sqlex)
            chance_measures = cursor.fetchall()

            sqlex = ("SELECT "
                     "measures_id "
                     "FROM "
                     "Risk_Measures_Excerpt")
            cursor.execute(sqlex)
            risk_measures = cursor.fetchall()

            for row in chance_measures:
                sqlex = ("INSERT INTO "
                         "Chance_Measures_Evaluations "
                         "(measures_id, project_id, extent, probability) "
                         "VALUES "
                         "(" + str(row["measures_id"]) + ", " +
                         str(proj_id) + ", 0, 0)")
                cursor.execute(sqlex)

            for row in risk_measures:
                sqlex = ("INSERT INTO "
                         "Risk_Measures_Evaluations "
                         "(measures_id, project_id, extent, probability) "
                         "VALUES "
                         "(" + str(row["measures_id"]) + ", " +
                         str(proj_id) + ", 0, 0)")
                cursor.execute(sqlex)

            self.connection.commit()

    def chance_eval(self, proj_id):
        """
        Get the evaluation data from Chance_Evaluation table.
        And return
        :param proj_id: int
        :return: dict string
        """
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            sqlex = ("SELECT "
                     "extent, probability, "
                     "Chance_Questions_Excerpt.weight "
                     "FROM "
                     "Chance_Evaluations "
                     "JOIN "
                     "Chance_Questions_Excerpt "
                     "ON "
                     "Chance_Questions_Excerpt.question_id = Chance_Evaluations.question_id "
                     "WHERE project_id = " + str(proj_id))
            cursor.execute(sqlex)
            # evals = cursor.fetchall()
            # return evals
            return cursor.fetchall()

    def risk_eval(self, proj_id):
        """
        Get the risk evaluation from the Risk_Evaluation table.
        And return them
        :param proj_id: int
        :return: dict string
        """
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            sqlex = ("SELECT "
                     "extent, probability, "
                     "Risk_Questions_Excerpt.weight "
                     "FROM "
                     "Risk_Evaluations "
                     "JOIN "
                     "Risk_Questions_Excerpt "
                     "ON "
                     "Risk_Evaluations.question_id = Risk_Questions_Excerpt.question_id "
                     "WHERE project_id = " + str(proj_id))
            cursor.execute(sqlex)
            # evals = cursor.fetchall()
            # return evals
            return cursor.fetchall()

    def getmeasures_chance(self, proj_id):
        """
        Get the measures evaluation from the Chance_Measures_Evaluation table.
        And return them.
        :param proj_id: int
        :return: dict string
        """
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            sqlex = ("SELECT "
                     "Chance_Measures_Excerpt.measures_id, Chance_Measures_Excerpt.influence_factor, "
                     "extent, probability, "
                     "Chance_Measures_Excerpt.measure, Chance_Measures_Excerpt.weight "
                     "FROM "
                     "Chance_Measures_Evaluations "
                     "JOIN "
                     "Chance_Measures_Excerpt "
                     "ON Chance_Measures_Evaluations.measures_id = Chance_Measures_Excerpt.measures_id "
                     "WHERE project_id = " + str(proj_id))
            cursor.execute(sqlex)
            # evals = cursor.fetchall()
            # return evals
            return cursor.fetchall()

    def getmeasures_risk(self, proj_id):
        """
        Get the measures evaluation from the Risk_Measures_Evaluation table.
        And return them.
        :param proj_id: int
        :return: dict string
        """
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            sqlex = ("SELECT "
                     "Risk_Measures_Excerpt.measures_id, Risk_Measures_Excerpt.influence_factor, extent, probability, "
                     "Risk_Measures_Excerpt.measure, Risk_Measures_Excerpt.weight "
                     "FROM "
                     "Risk_Measures_Evaluations "
                     "JOIN "
                     "Risk_Measures_Excerpt "
                     "ON Risk_Measures_Evaluations.measures_id = Risk_Measures_Excerpt.measures_id "
                     "WHERE project_id = " + str(proj_id))
            cursor.execute(sqlex)
            # evals = cursor.fetchall()
            # return evals
            return cursor.fetchall()

    def insmeasure_chance(self, proj_id, probability, extent):
        """
        Write the measures evaluation of the tool into the Chance_Measures_Evaluation table.
        :param proj_id: int
        :param probability: string?
        :param extent: string?
        :return: 0
        """
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            for key in probability:
                sqlex = ("UPDATE "
                         "Chance_Measures_Evaluations "
                         "SET "
                         "extent = " + str(extent[key]) + ", "
                         "probability = " + str(probability[key]) +
                         "WHERE "
                         "measures_id = " + str(key) +
                         " AND "
                         "project_id = " + str(proj_id))
                cursor.execute(sqlex)
            self.connection.commit()

    def insmeasure_risk(self, proj_id, probability, extent):
        """
        Write the measures evaluation data into the Risk_Measures_Evaluation table.
        :param proj_id: int
        :param probability: string?
        :param extent: string?
        :return:
        """
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            for key in probability:
                sqlex = ("UPDATE "
                         "Risk_Measures_Evaluations "
                         "SET "
                         "extent = " + str(extent[key]) + ", "
                         "probability = " + str(probability[key]) +
                         "WHERE "
                         "measures_id = " + str(key) +
                         " AND "
                         "project_id = " + str(proj_id))
                cursor.execute(sqlex)
            self.connection.commit()

    def initmeasures(self, proj_id):
        """

        :param proj_id:
        :return:
        """
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            sqlex = ("SELECT "
                     "measures_id, Chance_Evaluations.extent, Chance_Evaluations.probability "
                     "FROM "
                     "Chance_Measures_Excerpt "
                     "JOIN "
                     "Chance_Evaluations "
                     "ON Chance_Measures_Excerpt.question_id = Chance_Evaluations.question_id "
                     "WHERE Chance_Evaluations.project_id = " + str(proj_id))
            cursor.execute(sqlex)
            chance_evals = cursor.fetchall()

            sqlex = ("SELECT "
                     "measures_id, Risk_Evaluations.extent, Risk_Evaluations.probability "
                     "FROM "
                     "Risk_Measures_Excerpt "
                     "JOIN "
                     "Risk_Evaluations "
                     "ON Risk_Measures_Excerpt.question_id = Risk_Evaluations.question_id "
                     "WHERE Risk_Evaluations.project_id = " + str(proj_id))
            cursor.execute(sqlex)
            risk_evals = cursor.fetchall()

            for row in chance_evals:
                sqlex = ("UPDATE "
                         "Chance_Measures_Evaluations "
                         "SET "
                         "extent = " + str(row["extent"]) + ", "
                         "probability = " + str(row["probability"]) +
                         " WHERE "
                         "measures_id = " + str(row["measures_id"]) +
                         " AND "
                         "project_id = " + str(proj_id))
                # print "extent: ", row["extent"]
                cursor.execute(sqlex)
            for row in risk_evals:
                sqlex = ("UPDATE "
                         "Risk_Measures_Evaluations "
                         "SET "
                         "extent = " + str(row["extent"]) + ", "
                         "probability = " + str(row["probability"]) +
                         " WHERE "
                         "measures_id = " + str(row["measures_id"]) +
                         " AND "
                         "project_id = " + str(proj_id))
                cursor.execute(sqlex)
            self.connection.commit()

    def get_formalization(self):
        """

        :return:
        """
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            sqlex = ("SELECT "
                     "* "
                     "FROM "
                     "Formalization_Questions")
            cursor.execute(sqlex)
            # questions = cursor.fetchall()
            # return questions
            return cursor.fetchall()

    def get_proximity(self):
        """

        :return:
        """
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            sqlex = ("SELECT "
                     "* "
                     "FROM "
                     "Proximity_Questions ")
            cursor.execute(sqlex)
            # questions = cursor.fetchall()
            # return questions
            return cursor.fetchall()

    def get_risikoeinstellung(self):
        """

        :return:
        """
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            sqlex = ("SELECT "
                     "* "
                     "FROM "
                     "Risikoeinstellung_Fragen")
            cursor.execute(sqlex)
            # questions = cursor.fetchall()
            # return questions
            return cursor.fetchall()

    def ins_interne(self, account_id, risiko_eval, proxim_eval, formal_eval):
        """
        Function to insert all data from the intern analysis.
        :param account_id: int
        :param risiko_eval: float dict
        :param proxim_eval: float dict
        :param formal_eval: float dict
        :return: true
        """
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
        # *** Risikoeinstellung ***
            sqlex = ("SELECT EXISTS(SELECT 1 FROM Risikoeinstellung_Bewertung "
                     "WHERE account_id=" + str(account_id) + ") AS mycheck")
            cursor.execute(sqlex)
            check = cursor.fetchone()

            if check["mycheck"] == 0:
                # INSERT
                for key in risiko_eval:
                    sqlex = ("INSERT INTO "
                             "Risikoeinstellung_Bewertung "
                             "(question_id, evaluation, account_id) "
                             "VALUES ("
                             + str(key) + ", " + str(risiko_eval[key]) + ", " + str(account_id) + ")")
                    cursor.execute(sqlex)

            else:
                # UPDATE
                for key in risiko_eval:
                    sqlex = ("UPDATE "
                             "Risikoeinstellung_Bewertung "
                             "SET "
                             "evaluation = " + str(risiko_eval[key]) +
                             "WHERE "
                             "account_id = " + str(account_id) +
                             " AND "
                             "question_id = " + str(key))
                    cursor.execute(sqlex)

            # *** Proximität ***
            sqlex = ("SELECT EXISTS(SELECT 1 FROM Proximity_Evaluation "
                     "WHERE account_id=" + str(account_id) + ") AS mycheck")
            cursor.execute(sqlex)
            check = cursor.fetchone()

            if check["mycheck"] == 0:
                # INSERT
                for key in proxim_eval:
                    sqlex = ("INSERT INTO "
                             "Proximity_Evaluation "
                             "(question_id, evaluation, account_id) "
                             "VALUES ("
                             + str(key) + ", " + str(proxim_eval[key]) + ", " + str(account_id) + ")")
                    cursor.execute(sqlex)

            else:
                # UPDATE
                for key in proxim_eval:
                    sqlex = ("UPDATE "
                             "Proximity_Evaluation "
                             "SET "
                             "evaluation = " + str(proxim_eval[key]) +
                             "WHERE "
                             "account_id = " + str(account_id) +
                             " AND "
                             "question_id = " + str(key))
                    cursor.execute(sqlex)
            # *** Formalization ***
            sqlex = ("SELECT EXISTS(SELECT 1 FROM Formalization_Evaluation "
                     "WHERE account_id=" + str(account_id) + ") AS mycheck")
            cursor.execute(sqlex)
            check = cursor.fetchone()

            if check["mycheck"] == 0:
                # INSERT
                for key in formal_eval:
                    sqlex = ("INSERT INTO "
                             "Formalization_Evaluation "
                             "(question_id, evaluation, account_id) "
                             "VALUES ("
                             + str(key) + ", " + str(formal_eval[key]) + ", " + str(account_id) + ")")
                    cursor.execute(sqlex)
            else:
                # UPDATE
                for key in formal_eval:
                    sqlex = ("UPDATE "
                             "Formalization_Evaluation "
                             "SET "
                             "evaluation = " + str(formal_eval[key]) +
                             "WHERE "
                             "account_id = " + str(account_id) +
                             " AND "
                             "question_id = " + str(key))
                    cursor.execute(sqlex)
            self.connection.commit()

    def init_internstuff(self, account_id):
        """

        :param account_id:
        :return:
        """
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            sqlex = ("SELECT "
                     "question_id "
                     "FROM "
                     "Formalization_Questions")
            cursor.execute(sqlex)
            questions = cursor.fetchall()

            for key in questions:
                sqlex = ("INSERT INTO "
                         "Formalization_Evaluation "
                         "(question_id, evaluation, account_id) "
                         "VALUES ("
                         + str(key["question_id"]) + ", 0, " + str(account_id) + ")")
                cursor.execute(sqlex)

            sqlex = ("SELECT "
                     "question_id "
                     "FROM "
                     "Proximity_Questions ")
            cursor.execute(sqlex)
            questions = cursor.fetchall()

            for key in questions:
                sqlex = ("INSERT INTO "
                         "Proximity_Evaluation "
                         "(question_id, evaluation, account_id) "
                         "VALUES ("
                         + str(key["question_id"]) + ", 0, " + str(account_id) + ")")
                cursor.execute(sqlex)

            sqlex = ("SELECT "
                     "question_id "
                     "FROM "
                     "Risikoeinstellung_Fragen")
            cursor.execute(sqlex)
            questions = cursor.fetchall()

            for key in questions:
                sqlex = ("INSERT INTO "
                         "Risikoeinstellung_Bewertung "
                         "(question_id, evaluation, account_id) "
                         "VALUES ("
                         + str(key["question_id"]) + ", 0, " + str(account_id) + ")")
                cursor.execute(sqlex)
            self.connection.commit()

    def getriskassessment(self, account_id):
        """

        :param account_id:ß
        :return:
        """
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            sqlex = ("SELECT "
                     "Risikoeinstellung_Bewertung.question_id, evaluation, Risikoeinstellung_Fragen.question "
                     "FROM "
                     "Risikoeinstellung_Bewertung "
                     "JOIN "
                     "Risikoeinstellung_Fragen "
                     "ON Risikoeinstellung_Bewertung.question_id = Risikoeinstellung_Fragen.question_id "
                     "WHERE "
                     "Risikoeinstellung_Bewertung.account_id = " + str(account_id))
            cursor.execute(sqlex)
            # assessment = cursor.fetchall()
            # return assessment
            return cursor.fetchall()

    def getproximity(self, account_id):
        """

        :return:
        """
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            sqlex = ("SELECT "
                     "Proximity_Questions.question_id, question, min, max, Proximity_Evaluation.evaluation "
                     "FROM "
                     "Proximity_Questions "
                     "JOIN "
                     "Proximity_Evaluation "
                     "ON Proximity_Evaluation.question_id = Proximity_Questions.question_id "
                     "WHERE "
                     "Proximity_Evaluation.account_id = " + str(account_id))
            cursor.execute(sqlex)
            # proximity = cursor.fetchall()
            # return proximity
            return cursor.fetchall()

    def getformalization(self, account_id):
        """

        :param account_id:
        :return:
        """
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            sqlex = ("SELECT "
                     "Formalization_Questions.question_id, question, min, max, Formalization_Evaluation.evaluation "
                     "FROM "
                     "Formalization_Questions "
                     "JOIN "
                     "Formalization_Evaluation "
                     "ON Formalization_Evaluation.question_id = Formalization_Questions.question_id "
                     "WHERE "
                     "Formalization_Evaluation.account_id = " + str(account_id))
            cursor.execute(sqlex)
            # formalization = cursor.fetchall()
            # return formalization
            return cursor.fetchall()

    def get_measure_status(self, project_id):
        """

        :return:
        """
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            sqlex = ("SELECT "
                     "project_id, AVG(probability) as prob_avg, AVG(extent) as ext_avg "
                     "FROM "
                     "Chance_Measures_Evaluations "
                     "WHERE "
                     "project_id = " + str(project_id) + " " +
                     "GROUP BY "
                     "project_id")
            cursor.execute(sqlex)
            return cursor.fetchone()

    def get_riskformprox_status(self, account_id):
        count = []
        with self.connection:
            cursor = self.connection.cursor(cursors.DictCursor)
            sqlex = ("SELECT EXISTS(SELECT 1 FROM "
                     "Proximity_Evaluation "
                     "WHERE "
                     "account_id = " + str(account_id) + ") AS mycheck")
            cursor.execute(sqlex)
            count.append(cursor.fetchone())

            sqlex = ("SELECT EXISTS(SELECT 1 FROM "
                     "Formalization_Evaluation "
                     "WHERE "
                     "account_id = " + str(account_id) + ") AS mycheck")
            cursor.execute(sqlex)
            count.append(cursor.fetchone())

            sqlex = ("SELECT EXISTS(SELECT 1 FROM "
                     "Risikoeinstellung_Bewertung "
                     "WHERE "
                     "account_id = " + str(account_id) + ") AS mycheck")
            cursor.execute(sqlex)
            count.append(cursor.fetchone())

            # print "Count riskformprox blabal: ", count
            tmp = 0
            for i in range(len(count)):
                tmp += count[i]["mycheck"]

            return tmp

    def create_user_account(self, username, userpassword):
        """

        :param username: string
        :param userpassword: string
        :return: boolean or Exception
        """

        cursor = self.connection.cursor(cursors.DictCursor)
        try:
            sqlex = ("INSERT INTO "
                     "Account "
                     "(email, account_pass) "
                     "VALUES "
                     "(\"" + str(username) + "\", \"" + str(userpassword) + "\")")
            # print "sqlex: ", sqlex
            cursor.execute(sqlex)

            self.connection.commit()
            # print "Angelegt: ", True
        except Exception as e:
            pass
            # sqlex_1 = ("INSERT INTO "
            #            "Account "
            #            "(email, account_pass) "
            #            "VALUES "
            #            "(\"fuck\", \"you\")")
            # cursor.execute(sqlex_1)
            # print "sqlex_1: ", sqlex_1
            # print "Ausnahme: ", e

    def close_connection(self):
        """

        :return:
        """
        try:
            self.connection.close()
            print "Verbindung getrennt"
        except BaseException as base_e:
            # print base_e
            pass