""" The AutoScroll method implants a vertical and horizontal scrollbar,
    that appears or dissapears if needed. """
from Tkinter import Canvas, Frame
from .Autoscrollbar import AutoScrollbar
from os import name

class Scrollinit:

    def __init__(self, parent):
        self.canvas = {}
        self.parent = parent

    def scrollbegin(self):
        """ Basic commands to beable to use AutoScroll.
            Has to be called before something goes into the frame."""
        vscrollbar = AutoScrollbar(self.parent)
        vscrollbar.grid(row=0, column=1, sticky='ns')
        hscrollbar = AutoScrollbar(self.parent, orient='horizontal')
        hscrollbar.grid(row=1, column=0, sticky='ew')

        self.canvas["canvas"] = Canvas(self.parent, yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)
        self.canvas["canvas"].grid(row=0, column=0, sticky='news')

        if name == 'nt':
            # win
            self.canvas["canvas"].bind_all("<MouseWheel>", self.on_mousewheel)
        else:
            # linux
            self.canvas["canvas"].bind_all("<Button-4>", self.on_mousewheel)
            self.canvas["canvas"].bind_all("<Button-5>", self.on_mousewheel)

        vscrollbar.config(command=self.canvas["canvas"].yview)
        hscrollbar.config(command=self.canvas["canvas"].xview)

        # make the canvas expandable
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)

        # create canvas contents
        frame = Frame(self.canvas["canvas"])
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(1, weight=1)
        scrolllist = [self.canvas["canvas"], frame]

        return scrolllist

    def scrollinit(self, canvas, frame):
        """ Initializing the window to be able to use AutoScroll.
            Has to be called after the stuff went into window, somehow-"""
        canvas.create_window(0, 0, anchor='nw', window=frame)
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def on_mousewheel(self, event):
        if name == 'nt':
            # win
            self.canvas["canvas"].yview_scroll(-1 * (event.delta / 120), "units")
        elif name == 'posix':
            # linux
            if event.num == 4:
                self.canvas["canvas"].yview_scroll(-1, "units")
            else:
                self.canvas["canvas"].yview_scroll(1, "units")