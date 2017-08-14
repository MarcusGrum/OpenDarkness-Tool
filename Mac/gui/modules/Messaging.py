#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
My own Messaging, Info and Warning method.
Written for Tkinter.
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
from tkinter.ttk import Label, Frame
from Tkinter import Toplevel, Button
from time import time


class Message:

    def __init__(self, father):
        self.child = father
        self.msg = Toplevel(self.child)
        self.icons = []

    def infomsg(self, title, message, countdown):
        self.msg.title(title)
        hint = "Schließt automatisch in " + str(countdown) + "s. oder wenn Sie auf den Button drücken."
        Label(self.msg, text=message,
              wraplength=360,
              font="Helvetica 10").grid(row=0, column=0, sticky='news', pady=5, padx=5)
        Label(self.msg, text=hint,
              wraplength=360,
              font="Helvetica 8").grid(row=1, column=0, sticky='news', pady=5, padx=5)
        okbutton = Button(self.msg, text="OK",
                          font="Helvetica 10", command=self.msgdestroy)
        okbutton.grid(row=2, column=0, sticky='ns', pady=5, padx=5)
        okbutton.focus()
        timer = countdown
        while timer >= 0:
            self.child.after(1000)
            okbutton["text"] = "Schließt in " + str(timer) + "s."
            print timer
            self.child.update()
            timer -= 1
        self.msgdestroy()

    def warnmsg(self, title, message, exception):
        self.msg.title(title)
        excmsg = "Hinweis:\n" + str(exception)
        Label(self.msg, text=message,
              wraplength=360,
              font="Helvetica 10 bold").grid(row=0, column=0, sticky='news', pady=5, padx=5)
        Label(self.msg, text=excmsg,
              wraplength=360,
              font="Helvetica 10 italic").grid(row=1, column=0, sticky='news', pady=5, padx=5)
        btn = Button(self.msg, text="OK",
               font="Helvetica 10",
               command=self.msgdestroy)
        btn.grid(row=2, column=0, sticky='news', pady=5, padx=5)
        btn.focus()

    def askimsg(self, title, message, countdown):
        """

        :param title:
        :param message:
        :param countdown:
        :return:
        """
        self.msg.title(title)
        Label(self.msg, text="\"INFO\"", font="Helvetica 14").grid(row=0, column=0, sticky="news", pady=5, padx=5)
        Label(self.msg, text=message, font="Helvetica 10 bold",
              wraplength=360).grid(row=0, column=1, sticky="news", pady=5, padx=5)
        Button(self.msg, text="JA", font="Helvetica 10", command=self.rettrue).grid(row=2, column=1, sticky="news", pady=5, padx=5)
        Button(self.msg, text="NEIN", font="Helvetica 10", command=self.retfalse).grid(row=2, column=2, sticky="news", pady=5, padx=5)

    def rettrue(self):
        return True

    def retfalse(self):
        return False

    def countdown(self, btn, timer):
        btn["text"] = timer

    def msgdestroy(self):
        self.msg.destroy()
