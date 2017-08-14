#!/usr/bin/python
# -*- coding: utf-8 -*-
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
import time
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from ResourcePath import resource_path


class TitlePagePDF:

    def __init__(self, project, account):

        self.path = resource_path("gui/filingarea/plot_title.pdf")
        self.doc = SimpleDocTemplate(self.path, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        self.subjects = ["Projektname:", "Projektbeschreibung:", "Benutzername:", "Datum:"]
        self.project = project
        self.account = account
        self.logo_path = resource_path("gui/images/OD_logo_long.png")
        self.date = time.strftime("%d.%m.%Y")

    def generate_title(self):

        Title = []
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Centered', alignment=TA_CENTER, wordWrap=True, leading=20))

        im = Image(self.logo_path, 138, 30, hAlign="RIGHT")
        Title.append(im)
        Title.append(Spacer(1, 55))



        # Titel
        ptext = """<font size=20 fontName="Times-Bold">OpenDarkness Tool</font>"""
        Title.append(Paragraph(ptext, styles["Centered"]))
        Title.append(Spacer(1, 20))

        ptext = """<font size=18 fontName="Times-Bold">Zusammenstellung der Plots</font>"""
        Title.append(Paragraph(ptext, styles["Centered"]))
        Title.append(Spacer(1, 100))

        # Projektname
        ptext = """<font size=14 fontName="Times-Bold">%s</font>""" % self.subjects[0]
        Title.append(Paragraph(ptext, styles["Centered"]))
        Title.append(Spacer(1, 10))

        ptext = """<font size=12 fontName="Times-Italic">%s</font>""" % self.project.getprojname()
        Title.append(Paragraph(ptext, styles["Centered"]))
        Title.append(Spacer(1, 40))

        # Projektbeschreibung
        ptext = '<font size=14 fontName="Times-Bold">%s</font>' % self.subjects[1]
        Title.append(Paragraph(ptext, styles["Centered"]))
        Title.append(Spacer(1, 12))

        ptext = '<font size=12 fontName="Times-Italic">%s</font>' % self.project.getdescription()
        Title.append(Paragraph(ptext, styles["Centered"]))
        Title.append(Spacer(1, 40))

        # Benutzer
        ptext = '<font size=14 fontName="Times-Bold">%s</font>' % self.subjects[2]
        Title.append(Paragraph(ptext, styles["Centered"]))
        Title.append(Spacer(1, 12))

        ptext = '<font size=12 fontName="Times-BoldItalic">%s</font>' % self.account.getemail()
        Title.append(Paragraph(ptext, styles["Centered"]))
        Title.append(Spacer(1, 120))

        # Datum
        ptext = '<font size=14 fontName="Times-Bold">%s</font>' % self.subjects[3]
        Title.append(Paragraph(ptext, styles["Centered"]))
        Title.append(Spacer(1, 12))

        ptext = '<font size=12 fontName="Times-Italic">%s</font>' % self.date
        Title.append(Paragraph(ptext, styles["Centered"]))
        Title.append(Spacer(1, 12))

        self.doc.build(Title)
