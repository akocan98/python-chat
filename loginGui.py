import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True


class loginGui:
    def __init__(self, top=None):

        _bgcolor = "#d6ecff" 
        _fgcolor = '#000000'

        top.geometry("950x500")
        top.title("RK Chat - Login")
        top.configure(background=_bgcolor)
        top.configure(highlightbackground=_bgcolor)
        top.configure(highlightcolor="black")

        self.rk_label = tk.Label(top)
        self.rk_label.place(relx=0.175, rely=0.322, height=46, width=114)
        self.rk_label.configure(activebackground="#f9f9f9")
        self.rk_label.configure(activeforeground="black")
        self.rk_label.configure(background=_bgcolor)
        self.rk_label.configure(disabledforeground="#a3a3a3")
        self.rk_label.configure(font="-family {Segoe UI} -size 22 -weight bold")
        self.rk_label.configure(foreground=_fgcolor)
        self.rk_label.configure(highlightbackground=_bgcolor)
        self.rk_label.configure(highlightcolor="black")
        self.rk_label.configure(text="RK Chat")

        self.prijava = tk.Entry(top)
        self.prijava.place(relx=0.1767, rely=0.467,height=40, relwidth=0.49)
        self.prijava.configure(background="white")
        self.prijava.configure(disabledforeground="#a3a3a3")
        self.prijava.configure(font="TkFixedFont")
        self.prijava.configure(foreground=_fgcolor)
        self.prijava.configure(insertbackground="black")
        self.prijava.configure(width=294)
        self.prijava.configure(font="-family {Segoe UI} -size 15")

        self.username_izbor = tk.Label(top)
        self.username_izbor.place(relx=0.175, rely=0.411, height=21)
        self.username_izbor.configure(background=_bgcolor)
        self.username_izbor.configure(disabledforeground="#a3a3a3")
        self.username_izbor.configure(foreground=_fgcolor)
        self.username_izbor.configure(text="Select a username or leave it empty and get a random one:")