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
from Tkinter import Toplevel, Label, Tk, Button


class CreateToolTip(object):
    """
    Creates a tooltip above the given widget
    """
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)

    def enter(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() - 20
        y += self.widget.winfo_rooty() + 30
        # creates a toplevel window
        # self.widget.after(1000)
        self.tw = Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self.tw, text=self.text, justify='left', wraplength=360,
                      background='ivory', relief='groove', borderwidth=2,
                      font=("Helvetica", "10", "normal"))
        label.pack(ipadx=1)

    def close(self, event=None):
        if self.tw:
            self.tw.destroy()

if __name__ == '__main__':
    root = Tk()

    btn1 = Button(root, text="button 1")
    btn1.pack(padx=10, pady=5)
    button1_ttp = CreateToolTip(btn1, "mouse is over button 1")

    btn2 = Button(root, text="button 2")
    btn2.pack(padx=10, pady=5)
    button2_ttp = CreateToolTip(btn2, "mouse is over button 2")

    root.mainloop()