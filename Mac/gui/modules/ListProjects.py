#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Authors:    Marcus Grum, Karsten Tauchert, Norbert Gronau
    Copyright:  University of Potsdam
                Department of Business Informatics, esp. Processes and Systems
    Name:       ListProjects.py
    Description:
    This creates a PDF-file with all Projects of the account connected to it.
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
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from ResourcePath import resource_path


class ListProjects:

    def __init__(self, sqlaccess, project, account):
        """
        sqlaccess for the access to the db
        :param sqlaccess: 
        :param project: 
        :param account: 
        """

        self.sqlacc = sqlaccess
        self.account = account
        self.project = project
        self.path = resource_path("gui/filingarea/project_list.pdf")
        self.doc = SimpleDocTemplate(self.path, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72,
                                     bottomMargin=18)
        self.logo_path = resource_path("gui/images/OD_logo_long.png")
        self.project_ids = self.account.getprojid()
        self.proj_names = {}
        self.proj_description = {}
        for i in range(len(self.project_ids)):
            self.proj_names[self.project_ids[i]] = self.sqlacc.getprojname(self.project_ids[i])
            self.proj_description[self.project_ids[i]] = self.sqlacc.getprojdescr(self.project_ids[i])

    def generate_pdf(self):
        """
        generates the actual pdf with all projects.
        :return: file
        """
        appendix = []
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='left', alignment=TA_LEFT, wordWrap=True, leading=20))
        styles.add(ParagraphStyle(name='Centered', alignment=TA_CENTER, wordWrap=True, leading=20))

        im = Image(self.logo_path, 138, 30, hAlign="RIGHT")
        appendix.append(im)
        appendix.append(Spacer(1, 55))

        # Titel
        ptext = """<font size=20 fontName="Times-Bold">OpenDarkness Tool</font>"""
        appendix.append(Paragraph(ptext, styles["Centered"]))
        appendix.append(Spacer(1, 20))

        ptext = """<font size=18 fontName="Times-Bold">Zusammenstellung der Projekte</font>"""
        appendix.append(Paragraph(ptext, styles["Centered"]))
        appendix.append(Spacer(1, 100))
        
        for i in range(len(self.project_ids)):
            proj_id = self.project_ids[i]
            ptext = """<font size=12 fontName="Times-Roman">Projekt ID: %s</font>""" % proj_id
            appendix.append(Paragraph(ptext, styles["left"]))
            appendix.append(Spacer(1, 12))

            ptext = """<font size=12 fontName="Times-Roman">Projektname: %s</font>""" % self.proj_names[proj_id]
            appendix.append(Paragraph(ptext, styles["left"]))
            appendix.append(Spacer(1, 12))
            
            ptext = """<font size=12 fontName="Times-Roman">Projektbeschreibung: %s</font>""" % self.proj_description[proj_id]
            appendix.append(Paragraph(ptext, styles["left"]))
            appendix.append(Spacer(1, 30))
            print "Projekt ID:", proj_id
        print "Liste erstellt"
        self.doc.build(appendix)
