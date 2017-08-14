#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Authors:    Marcus Grum, Karsten Tauchert, Norbert Gronau
    Copyright:  University of Potsdam
                Department of Business Informatics, esp. Processes and Systems
    Name:       ODGui.py
    Descrrption:
    This is the graphical user interface for the OD Tool.
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
import FileDialog  # MUST for pyinstaller
from ttk import Frame, Labelframe, Entry, Notebook, Style
from Tkinter import Menu, Button, PhotoImage, Toplevel, StringVar, Label, Text, WORD, END
from tkMessageBox import showerror, showwarning, askokcancel, askretrycancel, showinfo, askyesno
from PIL import Image, ImageTk
from sshtunnel import SSHTunnelForwarder
from os import system
import configparser
from webbrowser import open_new
from random import randint
from time import time
from SqlAccess import MySqlConnect as sqlacc
from modules.ResourcePath import resource_path
from modules.CreateToolTip import CreateToolTip
from modules.Accounts import Account
from modules.Projects import Project
from modules.ShowLicences import ShowLicences
from modules.Scrollinit import Scrollinit
from tabs.Decisphase import Decisphase
from tabs.Extanalyse import ExternAnalyse
from tabs.Intanalyse import InternAnalyse
from tabs.Integrated import IntegratedAnalyse
from tabs.Recomphase import Recomphase


class ODGui:
    def __init__(self, master):
        """
        Uses the root tk ans builds on that.
        Initializes some useful status variables and other dictionaries where the windows projects
        and account will be placed in.
        :param master:
        """
        self.master = master
        self.mainwindow = Frame(self.master, width=1000, height=600)
        self.iconpath = resource_path('gui\\images\\OD_icon.ico')
        self.mainwindow.pack(fill='both', expand=1)

        self.config = configparser.ConfigParser()
        self.config.read(resource_path('gui\\filingarea\\odconfig.ini'))

        self.windows = {}
        self.buttons = {}
        self.images = {}
        self.icons = {}
        self.entries = {}
        self.buttonnames = ["Verbinden", "Anmelden", "Alle Projekte", "Neues Projekt", "Neuer Benutzer", "Speichern",
                            "Schließen"]
        self.buttoncommands = [self.connecttoserver, self.userlogin, self.projectpage,
                               self.createproject, self.createuser, self.saveall, self.exitapp]
        self.buttontooltips = ["Serververbindung herstellen oder trennen.",
                               "Als Benutzer anmelden oder abmelden.",
                               "Alle Ihre Projekte auflisten und einsehen.",
                               "Ein neues Projekt erstellen.",
                               "Einen neuen Benutzer erstellen.",
                               "Speichern aller Projektdaten",
                               "Beenden des Tools"]
        self.timestatus = time()
        self.account = {}
        self.project = {}
        self.tabs = {}
        self.tabslist = []
        # Status variables
        self.connectionstatus = 0
        self.loginstatus = 0
        self.projectstatus = 0
        self.projectspagestatus = 0
        self.startscreenstatus = 0
        self.tabstatus = {"intern": 0, "extern": 0, "integrated": 0}

        self.loadicons()
        self.startapp()

        # Initializing different things. Icons

    def loadicons(self):
        """
        Initiates and loads all icons, in order to be used later.
        :return:
        """
        pathstring = "gui\\images\\"
        self.icons["initicons"] = []
        self.icons["iconnames"] = ["Disconnected-26.gif", "User-26.gif", "List-26.gif",
                                   "Add-List-26.gif", "Add-User-26.gif", "Save-26.gif", "Exit-26.gif"]
        for i in xrange(len(self.buttonnames)):
            iconpath = pathstring + self.icons["iconnames"][i]
            self.icons["initicons"].append(PhotoImage(file=resource_path(iconpath)))
        self.icons["serverconnected"] = PhotoImage(file=resource_path("gui\\images\\Connected-26.gif"))
        self.icons["userloggedin"] = PhotoImage(file=resource_path("gui\\images\\Checked-User-26.gif"))

        # "First Level" of design of the User Interface

    def menubar(self):
        """
        It is what it is. All functions can be accessed by the menubar.
        :return:
        """
        m_bar = Menu(self.master)
        m_bar.configure(font="Helvetica 14")
        menu_dict = dict()
        menu_dict['file'] = Menu(m_bar, font="Helvetica 10", tearoff=0)
        # menu_dict['edit'] = Menu(m_bar, font="Helvetica 10", tearoff=0)
        menu_dict['proj'] = Menu(m_bar, font="Helvetica 10", tearoff=0)
        menu_dict['help'] = Menu(m_bar, font="Helvetica 10", tearoff=0)
        menu_dict['file'].add_command(label='Verbinden', command=self.connecttoserver)
        menu_dict['file'].add_separator()
        menu_dict['file'].add_command(label="Benutzer anlegen", command=self.createuser)
        menu_dict['file'].add_separator()
        menu_dict['file'].add_command(label="Benutzer anmelden", command=self.userlogin)
        menu_dict['file'].add_command(label="Benutzer abmelden", command=self.userlogin)
        menu_dict['file'].add_separator()
        menu_dict['file'].add_separator()
        menu_dict['file'].add_command(label=u"Schließen", command=self.exitapp)
        menu_dict['proj'].add_command(label=u"Projektauswahl", command=self.projectpage)
        menu_dict['proj'].add_separator()
        menu_dict['proj'].add_command(label="Neues Projekt", command=self.createproject)
        menu_dict['proj'].add_command(label="Speichern", command=self.saveall)
        menu_dict['proj'].add_separator()
        menu_dict['proj'].add_command(label=u"Maßnahmen zurücksetzen", command=self.initializemeasures)
        menu_dict['help'].add_command(label="Handbuch", command=self.openmanual)  # ** command=self.open_handbuch
        menu_dict['help'].add_separator()
        menu_dict['help'].add_command(label="Info", command=self.infowindow)
        m_bar.add_cascade(label="Datei", menu=menu_dict['file'])
        m_bar.add_cascade(label="Projekte", menu=menu_dict['proj'])
        m_bar.add_cascade(label="Hilfe", menu=menu_dict['help'])
        self.master.config(menu=m_bar)

    def header(self):
        """
        Little besides the information frame.
        :return:
        """
        self.windows["header"] = Frame(self.mainwindow)
        self.windows["header"].pack(side='top', expand=0)  # expand 1 or 0 !!!!
        logopath = resource_path("gui\\images\\OD_logo_long.png")
        load = Image.open(logopath)
        logo_od = ImageTk.PhotoImage(load)
        logopen = Label(self.windows["header"], image=logo_od)
        logopen.image = logo_od
        logopen.pack(side='right', fill='x', expand=1)

    def toolbar(self):
        """
        Toolbar that includes all major functions of the tool.
        :return:
        """
        self.windows["toolbar"] = Labelframe(self.mainwindow, text="Toolbar", width=800, height=42)
        self.windows["toolbar"].pack(side='top', fill='x', expand=1)
        for i in range(len(self.buttonnames)):
            self.buttons[i] = Button(self.windows["toolbar"], text=self.buttonnames[i],
                                     command=self.buttoncommands[i], background="DarkGoldenrod1",
                                     relief='groove', font="Helvetica 10",
                                     image=self.icons["initicons"][i], compound='left',
                                     padx=3, pady=3)
            self.buttons[i].pack(side='left', fill='both', expand=1)
            CreateToolTip(self.buttons[i], self.buttontooltips[i])
        if self.connectionstatus == 0:
            self.buttons[0]["background"] = "light salmon"
        if self.loginstatus == 0:
            self.buttons[1]["background"] = "light salmon"

    def startscreen(self):
        """
        Like it says, this creates the screen/window at the start.
        With showing a lot of logos.
        :return:
        """
        print "Start init"
        if self.connectionstatus == 0:
            self.windows["startscreen"] = Labelframe(self.mainwindow, text="Logo")
            self.windows["startscreen"].pack(side='bottom', fill='both', expand=1)
            photo = PhotoImage(file=resource_path("gui\\images\\OD_icon.gif"))
            for i in xrange(30):
                ranx = randint(0, 4)
                rany = randint(0, 14)
                piclbl = Label(self.windows["startscreen"], image=photo)
                piclbl.image = photo
                piclbl.grid(row=ranx, column=rany)
                self.master.after(50)
                self.master.update()
            self.windows["startscreen"].destroy()

        self.windows["startscreen"] = Labelframe(self.mainwindow, text="Logo", width=700)
        self.windows["startscreen"].pack(side='bottom', fill='both', expand=1)
        logopath = resource_path("gui\\images\\big_start_logo.png")
        logoparty = ImageTk.PhotoImage(Image.open(logopath))
        logo = Label(self.windows["startscreen"], image=logoparty)
        logo.image = logoparty
        logo.pack()
        # self.acceptLicence()

        # "Second Level" of design of the User Interface

    def acceptLicence(self):
        """
        Ask user to accept GPL licence. If declined by user, leave App automatically.
        :return:
        """
        topWin = Toplevel(self.mainwindow)
        Label(topWin, text="Mit dem Druck auf \"Bestätigen\" bestätigen Sie die Lizenzbedingungen der App.\n"
                           "Falls Sie diese, mit einem Druck auf \"Ablehnen\", nicht bestätigen,\n"
                           "wird die App automatisch geschlossen",
              font='Helvetica 12').pack(side='top', expand=1, fill="both")
        Button(topWin, text="Bestätigen", font='Hellvetica 12', command=topWin.destroy).pack(side='left', expand=1, fill="both")
        Button(topWin, text="Ablehnen", font='Hellvetica 12', command=self.exitapp).pack(side='right', expand=1, fill="both")
        Button(topWin, text="Lizenzen", font='Hellvetica 12', command=self.openlicences).pack(side='bottom', expand=1, fill="both")


    def projectdata(self):
        """
        Opens a list of all projects the users has.
        A little frame with information about project and user.
        :return:
        """
        self.windows["projectdata"] = Frame(self.mainwindow)
        self.windows["projectdata"].pack(fill="x", expand=1)

        projectdata = Labelframe(self.windows["projectdata"], text="Projektdaten:")
        logoframe = Labelframe(self.windows["projectdata"], text="Toollogo:")
        projectdata.pack(side='left', fill='both', expand=1)
        logoframe.pack(side='left', fill='both', expand=0)

        # Projectdata frame
        Label(projectdata, text='Projektname:',
              font='Helvetica 12 bold').grid(row=0, column=0, columnspan=2, sticky='w', padx=10)
        Label(projectdata, text=self.project["Project"].getprojname(),
              font='Helvetica 12 italic').grid(row=0, column=2, columnspan=3, sticky='w', padx=10)
        Label(projectdata, text='Author:',
              font='Helvetica 12 bold').grid(row=1, column=0, columnspan=2, sticky='w', padx=10)
        Label(projectdata, text=self.account["Account"].getemail(),
              font='Helvetica 12 italic').grid(row=1, column=2, columnspan=3, sticky='w', padx=10)

        # Logo Frame
        logopath = resource_path("gui\\images\\OD_logo_small.png")
        load = Image.open(logopath)
        logo_od = ImageTk.PhotoImage(load)
        logopen = Label(logoframe, image=logo_od)
        logopen.image = logo_od
        logopen.pack(side='right', fill='x', expand=0)

    def projectpage(self):
        """
        Lists all projects of the user in one window.
        The user can than choose to openor delete that project.
        :return: None
        """

        if self.projectspagestatus == 1:
            pass
        else:
            self.projectspagestatus = 1
            if self.loginstatus == 1 and self.connectionstatus == 1:

                if self.projectstatus == 0:
                    pass
                # do nothing, just build the page
                else:
                    self.windows["base"].destroy()
                    self.windows["projectdata"].destroy()
                    self.tabslist = []
                # kill previous windows, and then build page
                self.windows["projectsframe"] = Labelframe(self.mainwindow, text='Projekte:')
                self.windows["projectsframe"].config(width=1000, height=700)
                self.windows["projectsframe"].pack(side='bottom', fill='both', expand=1)

                scrolling = Scrollinit(self.windows["projectsframe"])
                scrollframes = scrolling.scrollbegin()
                canvas = scrollframes[0]
                frame = scrollframes[1]

                projekte = Frame(frame, width=800, height=600)
                projekte.pack(side='bottom', fill='both', expand=1)
                Label(projekte, text='Aktion',
                      font="Helvetica 10 bold").grid(row=2, column=0, columnspan=2, padx=5, sticky='w')
                Label(projekte, text='Projekt ID',
                      font="Helvetica 10 bold").grid(row=2, column=2, padx=5, sticky='w')
                Label(projekte, text='Projekt Name',
                      font="Helvetica 10 bold").grid(row=2, column=3, padx=5, sticky='w')
                Label(projekte, text='Projekt Beschreibung',
                      font="Helvetica 10 bold").grid(row=2, column=4, columnspan=3, padx=5, pady=5, sticky='w')

                projects = {}
                for value in self.account["Account"].getprojid():
                    projects[value] = Project(self.sqlacc, value)
                i = 3
                for k in sorted(projects.keys()):
                    Button(projekte, text='Öffnen',
                           font="Helvetica 10",
                           command=lambda k=k: self.analysepage(projects[k])).grid(row=i, column=0, padx=5, pady=5,
                                                                                   sticky='news')
                    Button(projekte, text="Löschen",
                           font="Helvetica 10",
                           command=lambda k=k: self.deleteproject(k)).grid(row=i, column=1, padx=5, pady=5,
                                                                           sticky='news')
                    Label(projekte, text=projects[k].getprojid(),
                          justify='left', font="Helvetica 10").grid(row=i, column=2, padx=5, pady=5, sticky='w')
                    Label(projekte, text=projects[k].getprojname(),
                          justify='left', font="Helvetica 10").grid(row=i, column=3, padx=5, pady=5, sticky='w')
                    Label(projekte, text=projects[k].getdescription(),
                          wraplength=450, justify='left', font="Helvetica 10").grid(row=i, column=4, columnspan=3,
                                                                                    pady=5,
                                                                                    padx=5, sticky='w')
                    i += 1
                scrolling.scrollinit(canvas, frame)
            else:
                showwarning("Anmeldefehler!!", "Sie haben sich wahrscheinlich noch nicht angemeldet, "
                                               "und/oder Sie sind noch nicht mit dem Server verbunden.\n"
                                               "Bitte holen Sie die nötigen Schritte nach, um die Projektliste "
                                               "einsehen zu können.\n"
                                               "Vielen Dank!")

    def analysepage(self, project):
        """
        Creates a Notebook style tabbed window/frame.
        Each tab consists of different tasks for the user.
        :param project:
        :return:
        """
        if self.projectstatus == 1:
            self.windows["base"].destroy()

        self.project["Project"] = project
        self.projectstatus = 1

        if self.projectspagestatus == 1:
            self.windows["projectsframe"].destroy()
            self.projectspagestatus = 0
            print "Projectspagestatus 0"

        self.projectdata()
        self.windows["base"] = Frame(self.mainwindow, height=800, width=1000)
        self.windows["base"].pack(side='top', fill='both', expand=1)

        s = Style()
        s.configure('TNotebook.Tab', padding=[3, 3], font="Helvetica 12")
        s.configure('TNotebook', tabmargins=[2, 5, 2, 0])
        tab = Notebook(self.windows["base"])
        tab.pack(fill='both', expand=1)
        tab.enable_traversal()

        tabstext = ['Interne Analyse', 'Externe Analyse',
                    'Integrierte Analyse', 'Empfehlung',
                    'Entscheidung']
        for j in range(5):
            self.tabslist.append(Frame(tab))
            tab.add(self.tabslist[j], text=tabstext[j])
        tab.bind("<Button-1>", self.showtabnm)

        self.tabstatus["intern"] = 1
        self.tabs["Extern"] = ExternAnalyse(self.sqlacc, self.tabslist[1], self.project["Project"])
        self.tabs["Integrated"] = IntegratedAnalyse(self.sqlacc, self.tabslist[2],
                                                    self.account["Account"], self.project["Project"])
        self.tabs["Recom"] = Recomphase(self.sqlacc, self.tabslist[3],
                                        self.account["Account"], self.project["Project"])
        self.tabs["Decis"] = Decisphase(self.sqlacc, self.tabslist[4],
                                        self.account["Account"], self.project["Project"])
        self.tabs["Interne"] = InternAnalyse(self.sqlacc, self.tabslist[0],
                                             self.account["Account"], self.project["Project"])
        tab.select(self.tabslist[0])

    def showtabnm(self, event):
        """
        Checks for name of the tab and by clicking on that tab it starts some methods.
        Saves the entries of the previous tab.
        :param event:
        :return:
        """
        if self.loginstatus == 1 and self.connectionstatus == 1:
            if event.widget.identify(event.x, event.y) == 'label':
                index = event.widget.index('@%d,%d' % (event.x, event.y))
                tab_label = event.widget.tab(index, 'text')
                if tab_label == "Interne Analyse":
                    self.tabstatus["intern"] = 1
                    if self.tabstatus["extern"] == 1:
                        self.tabs["Extern"].saveresults()
                        self.tabstatus["extern"] = 0
                    elif self.tabstatus["integrated"] == 1:
                        self.tabs["Integrated"].save_measures()
                        self.tabstatus["integrated"] = 0
                    else:
                        pass
                    self.tabs["Interne"].intern_frame.destroy()
                    self.tabs["Interne"] = InternAnalyse(self.sqlacc, self.tabslist[0],
                                                         self.account["Account"], self.project["Project"])
                elif tab_label == "Externe Analyse":
                    self.tabstatus["extern"] = 1
                    if self.tabstatus["intern"] == 1:
                        self.tabs["Interne"].save_entries()
                        self.tabstatus["intern"] = 0
                    elif self.tabstatus["integrated"] == 1:
                        self.tabs["Integrated"].save_measures()
                        self.tabstatus["integrated"] = 0
                    self.tabs["Extern"].questframe.destroy()
                    self.tabs["Extern"] = ExternAnalyse(self.sqlacc, self.tabslist[1],
                                                        self.project["Project"])
                elif tab_label == "Integrierte Analyse":
                    self.tabstatus["integrated"] = 1
                    if self.tabstatus["extern"] == 1:
                        self.tabs["Extern"].saveresults()
                        self.tabstatus["extern"] = 0
                    elif self.tabstatus["intern"] == 1:
                        self.tabs["Interne"].save_entries()
                        self.tabstatus["intern"] = 0
                    self.tabs["Integrated"].measuresframe.destroy()
                    self.tabs["Integrated"] = IntegratedAnalyse(self.sqlacc, self.tabslist[2],
                                                                self.account["Account"], self.project["Project"])
                elif tab_label == "Empfehlung":
                    if self.tabstatus["intern"] == 1:
                        self.tabs["Interne"].save_entries()
                        self.tabstatus["intern"] = 0
                    elif self.tabstatus["extern"] == 1:
                        self.tabs["Extern"].saveresults()
                    elif self.tabstatus["integrated"] == 1:
                        self.tabs["Integrated"].save_measures()
                        self.tabstatus["integrated"] = 0
                    self.tabs["Recom"].graphicframe.destroy()
                    self.tabs["Recom"] = Recomphase(self.sqlacc, self.tabslist[3],
                                                    self.account["Account"], self.project["Project"])
                else:
                    if self.tabstatus["intern"] == 1:
                        self.tabs["Interne"].save_entries()
                        self.tabstatus["intern"] = 0
                    elif self.tabstatus["extern"] == 1:
                        self.tabs["Extern"].saveresults()
                        self.tabstatus["extern"] = 0
                    elif self.tabstatus["integrated"] == 1:
                        self.tabs["Integrated"].save_measures()
                        self.tabstatus["integrated"] = 0
                    self.tabslist[4].update()
        else:
            showerror("Anmeldefehler!", "Sie sind nicht mehr angemeldet!\n"
                                        "Bitte melden Sie sich an damit Sie Ihr Projekt bearbeiten können!")

        # Callbacks

    def startapp(self):
        """
        Starts the app!
        Main functions are Menubar and toolbar, they have to stay always. The startscreen is just a temporary thing.
        :return:
        """
        self.menubar()
        # self.header()
        self.toolbar()
        self.startscreen()
        print self.timestatus

    def exitapp(self):
        """
        This exits the tool and closes the connections to MySQL and the server.
        The user is asked  if he really wants to quit the app.
        :return:
        """
        endtime = time()
        difftime = endtime - self.timestatus
        print difftime
        if difftime >= 15:
            if askokcancel("Tool beenden?", "Sind Sie sicher, dass Sie das Tool beenden wollen?\n"
                                            "Nicht gespeicherte Änderungen könnten verloren gehen!"):
                # self.master.after(10000)
                if self.connectionstatus == 1:
                    self.connecttoserver()
                self.master.after(300)
                self.master.quit()
                self.master.destroy()
        else:
            if self.connectionstatus == 1:
                self.connecttoserver()
            self.master.after(300)
            self.master.quit()
            self.master.destroy()

    def initializemeasures(self):
        """
        Normalizes all entries in measures. Used when the users wants to start fresh or entered
        new data into the previous questionaire.
        :return:
        """
        if self.projectstatus == 0:
            showerror("Anmeldefehler!", "Sie bearbeiten momentan kein Projekt, "
                                        "und/oder Sie sind noch nicht angemeldet, "
                                        "deshalb hat diese Aktion keine Auswirkung. "
                                        "Bitte wählen Sie zuerst ein Projekt zum Bearbeiten aus.\n"
                                        "Vielen Dank!")
        else:
            self.sqlacc.initmeasures(self.project["Project"].getprojid())
            self.tabs["Integrated"].measuresframe.destroy()
            self.tabs["Integrated"] = IntegratedAnalyse(self.sqlacc, self.tabslist[2],
                                                        self.account, self.project["Project"])

    def saveall(self):
        """
        Well, saves all entries.
        :return:
        """
        if self.loginstatus == 0:
            showerror("Nicht angemeldet!", "Es tut uns leid, aber Sie sind "
                                           "noch nicht angemeldet, deshalb hat dieser Vorgang "
                                           "noch keine Auswirkung!\n"
                                           "Bitte melden Sie sich an!")
        else:
            self.timestatus = time()
            self.tabs["Interne"].save_measures()
            self.tabs["Integrated"].save_entries()
            self.tabs["Extern"].saveresults()

    def connecttoserver(self):
        """
        self explanatory
        Opens a sshtunnel and connects to server, in order to connect to the mysql db.
        :return:
        """
        if self.connectionstatus == 0:
            sshdata = self.config['sshtunnel.opendarkness']

            try:
                self.server = SSHTunnelForwarder((sshdata['server.address'], int(sshdata['server.port'])),
                                                 ssh_password=sshdata['ssh_password'],
                                                 ssh_username=sshdata['ssh_username'],
                                                 remote_bind_address=(sshdata['remote_bind_address.address'],
                                                                      int(sshdata['remote_bind_address.port'])))
                self.server.start()
                print "is active = ", self.server.is_active
                print "check tunnels = ", self.server.check_tunnels()
                print "tunnel is up = ", self.server.tunnel_is_up
                self.sqlacc = sqlacc(self.server.local_bind_port)
                self.buttons[0]["text"] = "Trennen"
                self.buttons[0]["background"] = "green yellow"
                self.buttons[0].config(image=self.icons["serverconnected"])
                self.master.update()
                self.connectionstatus = 1

            except Exception as e:
                showwarning("Verbindungsfehler!", "Es gab ein Problem beim Verbinden mit dem Server."
                                                  " Bitte versuchen Sie es zu einem späteren Zeitpunkt noch einmal."
                                                  " Falls das Problem bestehen bleibt,"
                                                  " schauen Sie im Handbuch nach einer Lösungen"
                                                  " und/oder kontaktieren Sie bitte den Service.\n\n"
                                                  "Folgender Fehler wurde gemeldet:\n" + str(e))

                print e

        else:
            if self.loginstatus == 1:
                self.userlogin()
            if self.projectspagestatus == 1 and self.loginstatus == 1:
                self.windows["projectsframe"].destroy()

            self.buttons[0]["background"] = "light salmon"
            self.buttons[0]["text"] = "Verbinden"
            self.buttons[0]["image"] = self.icons["initicons"][0]
            self.connectionstatus = 0
            self.sqlacc.close_connection()
            self.server.stop()
            print "is active = ", self.server.is_active

        # Creating User / Project Methods

    def createuser(self):
        """
        self explanatory.
        Opens top window and asks for credentials.
        Saves and inserts new user.
        :return:
        """
        self.account["email"] = StringVar()
        self.account["pass"] = StringVar()

        if self.loginstatus == 1:
            showerror("Anmeldefehler!", "Sie sind leider mit einem anderen Konto angemeldet. "
                                        "Bitte melden Sie sich zuerst ab, danach könnten Sie "
                                        "einen neuen Benutzer erstellen.\n"
                                        "Wir empfehlen Ihnen, bei Ihrem ersten Konto zu bleiben.\n"
                                        "Vielen Dank!")
        elif self.connectionstatus == 0:
            showerror("Anmeldefehler!", "Sie sind leider noch nicht mit dem Server verbunden. "
                                        "Holen Sie dieses bitte nach, um mit der Benutzererstellung fortfahren "
                                        "zu können\n"
                                        "Vielen Dank!")
        else:
            self.windows["usrcreatewin"] = Toplevel(self.master)
            self.windows["usrcreatewin"].title("Benutzer-Erstellung")
            self.windows["usrcreatewin"].iconbitmap(self.iconpath)

            head_msg = "Bitte geben Sie einen \"Benutzernamen\" und ein \"Passwort\" an."
            tipp_msg = ("Hinweis:\nBitte verwenden Sie ausschließlich Ihre E-Mail-Adresse."
                        "So können Missverständnisse vermieden und der Kontakt mit dem Support vereinfacht werden.")

            Label(self.windows["usrcreatewin"], text=head_msg,
                  wraplength=360, justify='left',
                  font="Helvetica 10 bold").grid(row=1, column=1, columnspan=2, pady=5, padx=5, sticky="w")
            Label(self.windows["usrcreatewin"], text=tipp_msg,
                  wraplength=360, justify='left',
                  font="Helvetica 8").grid(row=4, column=1, columnspan=2, pady=5, padx=5, sticky='w')
            Label(self.windows["usrcreatewin"], text="Benutzername:",
                  font="Helvetica 10 bold").grid(row=2, column=1, pady=5, padx=5, sticky='w')
            Label(self.windows["usrcreatewin"], text="Passwort",
                  font="Helvetica 10 bold").grid(row=3, column=1, pady=5, padx=5, sticky='w')
            userentry = Entry(self.windows["usrcreatewin"],
                              textvariable=self.account["email"], font="Helvetica 10", cursor='xterm')
            userentry.grid(row=2, column=2, pady=5, padx=5, sticky='we')
            userentry.focus()
            Entry(self.windows["usrcreatewin"],
                  textvariable=self.account["pass"], show='*', cursor='xterm',
                  font="Helvetica 10").grid(row=3, column=2, pady=5, padx=5, sticky='we')
            Button(self.windows["usrcreatewin"], text="Anlegen",
                   font="Helvetica 10",
                   command=self.insertcheckuser).grid(row=5, column=1, pady=5, padx=5, sticky='news')
            Button(self.windows["usrcreatewin"], text="Abbrechen",
                   font="Helvetica 10",
                   command=self.windows["usrcreatewin"].destroy).grid(row=5, column=2, pady=5, padx=5, sticky='news')

    def createproject(self):
        """
        self explanatory.
        Opens a top window and asks for information about new project.
        After pressing "Speichern und weiter" the project will be saved and the user will
        be forwarded to the analyse page.
        :return:
        """
        proj_greeting = ("Willkommen bei der Projekterstellung!\n"
                         "Bitte geben Sie einen \"Namen\" für Ihr "
                         "Projekt ein und eine kurze \"Beschreibung\", die auf die Öffnungsvariante des Projekts schließen lässt "
                         "(Projektpartner, Communities, Kollaborationstools, ...).\n"
                         "Vielen Dank!")
        if self.loginstatus == 0:
            showerror("Nicht angemeldet!", "Es tut uns leid, aber Sie sind "
                                           "noch nicht angemeldet, deshalb hat dieser Vorgang "
                                           "noch keine Auswirkung!\n"
                                           "Bitte melden Sie sich an!")
        else:
            proj_count = self.sqlacc.getprojcount()
            proj_count += 1
            accountname = self.account["Account"].getemail()
            hint = ("Bemerkung:\n"
                    "Wenn Sie auf \"Speichern und Weiter\" klicken, dann werden "
                    "die Daten in der Datenbank gespeichert und Sie können mit der Projektbearbeitung "
                    "fortsetzen, oder das Tool beenden und das Projekt später bearbeiten.")
            self.project["newproject"] = Project(self.sqlacc, proj_count)

            self.windows["createframe"] = Toplevel(self.master)
            self.windows["createframe"].title('Projekterstellung')
            self.windows["createframe"].iconbitmap(self.iconpath)

            Label(self.windows["createframe"], text=proj_greeting,
                  font="Helvetica 10 bold", wraplength=360, justify='left').grid(row=0, column=0, columnspan=2, pady=5,
                                                                                 sticky='w')
            Label(self.windows["createframe"], text='Benutzer:',
                  font="Helvetica 10 bold").grid(row=1, column=0, padx=5, pady=5, sticky='w')
            Label(self.windows["createframe"], text=accountname, font="Helvetica 10 italic").grid(row=1, column=1,
                                                                                                  padx=5, pady=5,
                                                                                                  sticky='w')
            Label(self.windows["createframe"], text='Projektname:',
                  font="Helvetica 10 bold").grid(row=2, column=0, padx=5, pady=5, sticky='w')
            self.entries["entry1"] = Entry(self.windows["createframe"], font="Helvetica 10", cursor='xterm')
            self.entries["entry1"].grid(row=2, column=1, padx=5, pady=5, sticky='w')
            self.entries["entry1"].focus()
            Label(self.windows["createframe"], text='Projektbeschreibung:',
                  font="Helvetica 10 bold").grid(row=3, column=0, padx=5, pady=5, sticky='w')
            self.entries["description"] = Text(self.windows["createframe"], width=44, height=4, wrap=WORD,
                                               cursor='xterm')  # tk.WORD
            self.entries["description"].grid(row=4, column=0, columnspan=2, padx=5, pady=5, stick='we')

            Label(self.windows["createframe"], text=hint,
                  font="Helvetica 8", wraplength=360,
                  justify='left').grid(row=5, column=0, columnspan=2, pady=5, padx=5, sticky='we')

            save_button = Button(self.windows["createframe"], text='Speichern und Weiter',
                                 command=self.savengo, font="Helvetica 10")
            save_button.grid(row=6, column=0, sticky='news',
                             padx=5, pady=5)

            cancel_but = Button(self.windows["createframe"], text='Abbrechen',
                                command=self.windows["createframe"].destroy,
                                font="Helvetica 10")
            cancel_but.grid(row=6, column=1, sticky='news', padx=5, pady=5)

    def insertcheckuser(self):
        """
        Checks the entries for mistakes and easy passwords. Creates the new user and inserts him
        into the db.
        :return:
        """
        self.windows["usrcreatewin"].destroy()
        dumbpwds = ["password", "passwort", "Passwort", "PassWort", "PassWord", "Password", "123456",
                    "654321", "pass123", "blablabla", "abc123", "fuckyou"]
        user_err = ("Es tut uns leid, aber dieser Benutzername ist schon vergeben!\n\n"
                    "Bitte wählen Sie einen andern Benutzernamen.\n"
                    "Daher empfielt sich die Benutzung der E-MAil-Adresse.\n"
                    "Falls es bei der Eingabe Ihrer E-Mail zu diesem Fehler kam, kontrollieren Sie auf Richtigkeit\n"
                    "Ihrer Eingabe und/oder konsultieren Sie das Handuch.\n"
                    "Vielen Dank")
        pass_err = ("Es tut uns leid, aber die Wahl Ihres Passwortes entsprach nicht "
                    "der Mindestanforderung eines relativ sicheren Passwortes.\n\n"
                    "Sehen Sie im Benutzerhandbuch nach, um Tips zu bekommen, wie ein Passwort "
                    "auszusehen hat.\n\n"
                    "Vielen Dank")
        userdone = ("Vielen Dank für Ihre Anmeldung.\n\n"
                    "Ihr Benutzeraccount wurde für Sie angelegt, und Sie können diesen jetzt benutzen.\n"
                    "Melden Sie sich einfach nur an und schon können Sie Ihr erstes Projekt bewerten.\n")

        usr = self.account["email"].get()
        pwd = self.account["pass"].get()
        tmp = self.sqlacc.getname()
        check = 0
        # Umlaute miteinbeziehen :(

        for user in tmp:
            if user["email"] == usr:
                check = 1

            # print "User already exists, duh!"
            # self.create_user()

        if check == 1:
            if askretrycancel("Benutzername Fehler!", message=user_err):
                self.createuser()

        else:
            if usr == pwd:
                if askretrycancel("Passwort Fehler!", message=pass_err):
                    self.createuser()
            elif len(pwd) <= 5:
                if askretrycancel("Passwort Fehler!", message=pass_err):
                    self.createuser()
            elif any(pwd == dumb for dumb in dumbpwds):
                if askretrycancel("Passwort Fehler!", message=pass_err):
                    self.createuser()
            else:
                showinfo("Benutzer angelegt!", message=userdone)
                self.sqlacc.create_user_account(usr, pwd)

    def savengo(self):
        """
        Saves the data into a Project instance from a recently created project and inserts it
        into the db.
        Opens the analyse-page.
        :return:
        """
        self.project["newproject"].setprojdescr(self.entries["description"].get('1.0', END))
        self.project["newproject"].setprojname(self.entries["entry1"].get())
        self.project["newproject"].setprojaccount(self.account["Account"].getaccid())
        self.project["newproject"].project2sql()
        self.project["newproject"].setprojid()
        self.sqlacc.initializerows(self.project["newproject"].getprojid())

        self.account["Account"].update_projectids()
        self.windows["createframe"].destroy()
        self.analysepage(self.project["newproject"])

        # User Login

    def userlogin(self):
        """
        self explanatory!
        Opens a window to enter credentials. Uses logincheck method to check the credentials.
        :return:
        """
        if self.loginstatus == 0 and self.connectionstatus == 1:

            self.account["email"] = StringVar()
            self.account["pass"] = StringVar()

            greeting = "Bitte geben Sie Ihre \"Anmeldedaten\" ein."
            hint = ("Bemerkung:\nIm Moment gibt es noch keine Möglichkeit die Daten "
                    "vorzumerken. Sie müssen die Benutzerdaten bei "
                    "jeder Anmeldung per Hand eingeben.")
            self.windows["loginwin"] = Toplevel(self.mainwindow)
            self.windows["loginwin"].iconbitmap(self.iconpath)
            self.windows["loginwin"].title('Benutzeranmeldung')

            Label(self.windows["loginwin"], text=greeting,
                  wraplength=360, justify='left',
                  font="Helvetica 10 bold").grid(row=0, column=0, columnspan=2,
                                                 padx=5, pady=5, sticky='w')
            Label(self.windows["loginwin"], text="Benutzername:",
                  justify='left',
                  font="Helvetica 10 bold").grid(row=2, column=0, pady=5, padx=5, sticky='w')
            Label(self.windows["loginwin"], text="Passwort:",
                  justify='left',
                  font="Helvetica 10 bold").grid(row=3, column=0, pady=5, padx=5, sticky='w')
            name = Entry(self.windows["loginwin"],
                         textvariable=self.account["email"],
                         font="Helvetica 10")
            passwd = Entry(self.windows["loginwin"], show='*',
                           textvariable=self.account["pass"],
                           font="Helvetica 10")
            Label(self.windows["loginwin"], text=hint, justify='left',
                  font="Helvetica 8", wraplength=360).grid(row=4, column=0, columnspan=2, pady=5, padx=5, sticky='w')
            name.grid(row=2, column=1, pady=5, padx=5, sticky='news')
            passwd.grid(row=3, column=1, pady=5, padx=5, sticky='news')
            name.focus()

            # For testing purpose
            self.account["email"].set("max.mustermann@email.de")
            self.account["pass"].set("mustermann")

            Button(self.windows["loginwin"], text='Einloggen', font="Helvetica 10",
                   command=self.logincheck).grid(row=5, column=0, pady=5, padx=5, sticky='news')
            Button(self.windows["loginwin"], text='Abbrechen', font="Helvetica 10",
                   command=self.windows["loginwin"].destroy).grid(row=5, column=1, pady=5, padx=5, sticky='news')

        elif self.connectionstatus == 0:
            showerror("Verbindungsfehler!", "Sie sind leider noch nicht mit dem Server verbunden, "
                                            "deshalb können Sie sich noch nicht mit Ihrem Kontso anmelden!\n"
                                            "Bitte verbinden Sie sich vorerst mit dem Server!\n"
                                            "Vielen Dank!")

        else:
            self.buttons[1]["text"] = "Anmelden"
            self.buttons[1]["background"] = "light salmon"
            self.buttons[1]["image"] = self.icons["initicons"][1]
            self.loginstatus = 0
            # if self.startscreenstatus == 1:
            #    self.windows["startscreen"].destroy()
            if self.projectstatus == 1:
                self.windows["base"].destroy()
                self.windows["projectdata"].destroy()
                self.projectstatus = 0
                self.startscreen()
                print "Projektstatus 1"
            if self.projectspagestatus == 1:
                self.windows["projectsframe"].destroy()
                self.projectspagestatus = 0
                self.startscreen()
                print "Projetpagestatus 1"

    def logincheck(self):
        """ Checks the login account and advance to projectpage if the
            user-account is in database, else don't
            :return:
        """
        try:
            users = self.sqlacc.getname()
            passwd = self.account["pass"].get()
            email = self.account["email"].get()
        except Exception as e:
            showwarning("Verbingungsfehler", "Sie haben noch keine Verbindung zum Server aufgebaut! "
                                             "Bitte stellen Sie eine Verbindung her. "
                                             "Dazu klicken Sie bitte auf \"Verbinden\".\n"
                                             "Vielen Dank!\n\n"
                                             "Folgender Fehler wurde gemeldet:\n" + str(e))

        for user in users:
            if user["email"] == email:
                self.account["Account"] = Account(self.sqlacc, user["email"])
                if self.account["Account"].getpasswd() == passwd:
                    self.windows["loginwin"].destroy()
                    self.windows["startscreen"].destroy()
                    self.loginstatus = 1
                    self.buttons[1]["text"] = "Abmelden"
                    self.buttons[1]["background"] = "green yellow"
                    self.buttons[1]["image"] = self.icons["userloggedin"]
                    break
                else:
                    showerror("Anmeldefehller", "Sie haben die falschen Anmeldedaten eingegeben "
                                                "oder Sie haben noch keinen Benutzer erstellt!")
                    break

    def deleteproject(self, proj_id):
        """
        Deletes the whole project from account. Leaves the data of the questionaires.
        :param proj_id:
        :return:
        """
        projectname = self.sqlacc.getprojname(proj_id)
        if askyesno("Projekt löschen!",
                    "Sie sind dabei das gewählte Projekt:\n\"" + str(projectname) +
                    "\"\nzu löschen.\nWenn Sie dieses ausführen gehen alle Daten verloren.\n"
                    "Sind Sie sicher?"):
            self.sqlacc.deleteproject(proj_id)
            self.account["Account"].update_projectids()
            self.windows["projectsframe"].destroy()
            self.master.after(300)
            self.projectspagestatus = 0
            self.master.after(300)
            self.projectpage()

        # Different extra windows

    def infowindow(self):
        """
        This creates a little top-window to show some information about the tool and its creators.
        Opens the internet browser by clicking on link.
        :return:
        """
        infowindow = Toplevel(self.master)
        infowindow.title("Info")
        infowindow.iconbitmap(self.iconpath)
        infowindow.geometry("375x215+120+120")
        Label(infowindow, text="LSWI-Rafoi-Tool",
              fg="orange",
              font="Helvetica 18 italic bold").grid(row=1, column=1, columnspan=3, sticky="news", pady=10)

        logopath = resource_path("gui\\images\\OD_logo_long.png")
        load = Image.open(logopath)
        logo = ImageTk.PhotoImage(load)
        logopen = Label(infowindow, image=logo)
        logopen.image = logo
        logopen.grid(row=2, column=1, columnspan=3, sticky="we")
        linktext = "http://www.lswi.de"
        link = Label(infowindow, text=linktext,
                     fg='blue', cursor='hand2', font="Helvetica 12 underline italic")
        link.grid(row=3, column=2, sticky="news", pady=5)
        link.bind("<Button-1>", self.openlink)
        Button(infowindow, text="Beteiligte",
               font="Helvetica 12", command=self.partieswindow).grid(row=4, column=1, sticky="news", pady=5, padx=5)
        Button(infowindow, text="Lizenzen",
               font="Helvetica 12", command=self.openlicences).grid(row=4, column=2, sticky="news", pady=5, padx=5)
        Button(infowindow, text="Schließen",
               font="Helvetica 12", command=infowindow.destroy).grid(row=4, column=3, sticky="news", pady=5, padx=5)

    def openlink(self, event):
        """
        self explanatory
        :param event:
        :return:
        """
        open_new(r"http://www.lswi.de")

    def partieswindow(self):
        """
        Just a picture of all participating parties.
        :return:
        """
        topwindow = Toplevel(self.master)
        topwindow.iconbitmap(self.iconpath)
        logopath = resource_path("gui\\images\\parties.png")
        logoparty = ImageTk.PhotoImage(Image.open(logopath))
        logo = Label(topwindow, image=logoparty)
        logo.image = logoparty
        logo.pack(side='top')
        Button(topwindow, text=u"Schließen",
               font="Helvetica 10",
               command=topwindow.destroy).pack(side='bottom', fill='x', expand=1)
    
    def openlicences(self):
        """
        
        :return:
        """
        ShowLicences(self.mainwindow)
    
    def openmanual(self):
        """
        self explanatory!
        Opens the standard reader for PDF-files with the given PDF-file.
        :return:
        """
        print "Manual..."
        manualpath = resource_path("gui\\filingarea\\Handbuch_OD_Tool.pdf")
        open_command = "start " + str(manualpath)
        system(open_command)

    # Little Helpers
    def checksshconnection(self):
        """
        For later use...
        Checks if the ssh connection is still active/open.
        :return: Boolean
        """
        return self.server.is_active
