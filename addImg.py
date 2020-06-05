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

class addImg:
    def __init__(self, top=None):

        _bgcolor = "#d6ecff"
        _bg_button = "#72beff"
        _fgcolor = '#000000' 
        _bg_active = '#4c7fff' 

        top.geometry("400x256")
        top.title("RK Chat - Send Image")
        top.configure(background=_bgcolor)
        top.configure(highlightbackground=_bgcolor)
        top.configure(highlightcolor="black")

        self.main_label = tk.Label(top)
        self.main_label.place(relx=-0.013, rely=0.195, height=23, width=262)
        self.main_label.configure(activebackground="#f9f9f9")
        self.main_label.configure(activeforeground="black")
        self.main_label.configure(background=_bgcolor)
        self.main_label.configure(disabledforeground="#a3a3a3")
        self.main_label.configure(font="-family {Segoe UI} -size 13 -weight bold")
        self.main_label.configure(foreground=_fgcolor)
        self.main_label.configure(highlightbackground=_bgcolor)
        self.main_label.configure(highlightcolor="black")
        self.main_label.configure(text='Enter the path to the image:')
        self.main_label.configure(width=262)

        self.descr_label = tk.Label(top)
        self.descr_label.place(relx=0.0, rely=0.293, height=21, width=282)
        self.descr_label.configure(activebackground="#f9f9f9")
        self.descr_label.configure(activeforeground="black")
        self.descr_label.configure(background=_bgcolor)
        self.descr_label.configure(disabledforeground="#a3a3a3")
        self.descr_label.configure(font="-family {Segoe UI} -size 10")
        self.descr_label.configure(foreground=_fgcolor)
        self.descr_label.configure(highlightbackground=_bgcolor)
        self.descr_label.configure(highlightcolor="black")
        self.descr_label.configure(text='You can use Relative paths or Absolute paths')
        self.descr_label.configure(width=282)

        self.descr_2_label = tk.Label(top)
        self.descr_2_label.place(relx=0.0, rely=0.371, height=21, width=335)
        self.descr_2_label.configure(background=_bgcolor)
        self.descr_2_label.configure(disabledforeground="#a3a3a3")
        self.descr_2_label.configure(font="-family {Segoe UI} -size 10")
        self.descr_2_label.configure(foreground=_fgcolor)
        self.descr_2_label.configure(text="")
        self.descr_2_label.configure(width=335)

        self.url_box = tk.Entry(top)
        self.url_box.place(relx=0.025, rely=0.508,height=30, relwidth=0.91)
        self.url_box.configure(background="white")
        self.url_box.configure(disabledforeground="#a3a3a3")
        self.url_box.configure(font="-family {Courier New} -size 11")
        self.url_box.configure(foreground=_fgcolor)
        self.url_box.configure(highlightbackground=_bgcolor)
        self.url_box.configure(highlightcolor="black")
        self.url_box.configure(insertbackground="black")
        self.url_box.configure(selectbackground="#c4c4c4")
        self.url_box.configure(selectforeground="black")

        self.send_img_button = tk.Button(top)
        self.send_img_button.place(relx=0.034, rely=0.65, height=34, width=117)
        self.send_img_button.configure(activebackground=_bg_active)
        self.send_img_button.configure(activeforeground=_fgcolor)
        self.send_img_button.configure(background=_bg_button)
        self.send_img_button.configure(disabledforeground="#a3a3a3")
        self.send_img_button.configure(foreground=_fgcolor)
        self.send_img_button.configure(highlightbackground=_bgcolor)
        self.send_img_button.configure(highlightcolor="black")
        self.send_img_button.configure(pady="0")
        self.send_img_button.configure(text="Send image")
        self.send_img_button.configure(width=117)