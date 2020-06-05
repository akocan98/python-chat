import sys
import os

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

class mainGui:

  def __init__(self, top=None, username="undef"):
    _bgcolor = "#d6ecff"
    _bg_button = "#72beff"
    _fgcolor = '#000000' 
    _bg_active = '#4c7fff' 

    self.emotes = []
    self.emotes_names = []
    self.img_ref = []

    top.geometry("950x500")
    top.title("RK Chat")
    top.configure(background=_bgcolor)
    top.configure(highlightbackground=_bgcolor)
    top.configure(highlightcolor="black")

    self.chat_input = tk.Entry(top)
    self.chat_input.place(relx=0.017, rely=0.856,height=30, relwidth=0.54)
    self.chat_input.configure(background="white")
    self.chat_input.configure(disabledforeground="#a3a3a3")
    self.chat_input.configure(font="TkFixedFont")
    self.chat_input.configure(foreground=_fgcolor)
    self.chat_input.configure(highlightbackground=_bgcolor)
    self.chat_input.configure(highlightcolor="black")
    self.chat_input.configure(insertbackground="black")
    self.chat_input.configure(selectbackground="#c4c4c4")
    self.chat_input.configure(selectforeground="black")

    self.online_users = tk.Listbox(top)
    self.online_users.place(relx=0.667, rely=0.022, relheight=0.96, relwidth=0.307)
    self.online_users.configure(background="white")
    self.online_users.configure(disabledforeground="#a3a3a3")
    self.online_users.configure(font="-family TkFixedFont -size 13")
    self.online_users.configure(foreground=_fgcolor)
    self.online_users.configure(highlightbackground=_bgcolor)
    self.online_users.configure(highlightcolor="black")
    self.online_users.configure(selectbackground="#c4c4c4")
    self.online_users.configure(selectforeground="black")
    self.online_users.configure(width=184)

    self.chat = tk.Text(top)
    self.chat.place(relx=0.017, rely=0.322, relheight=0.516, relwidth=0.64)
    self.chat.configure(background="white")
    self.chat.configure(font="TkFixedFont")
    self.chat.configure(foreground=_fgcolor)
    self.chat.configure(highlightbackground=_bgcolor)
    self.chat.configure(highlightcolor="black")
    self.chat.configure(selectbackground="#c4c4c4")
    self.chat.configure(selectforeground="black")
    self.chat.configure(width=384)
    self.chat.tag_config("system", foreground="grey")
    self.chat.tag_config("private_message", foreground="green")
    self.chat.tag_config("normal", foreground="black")

    self.welcome = tk.Label(top)
    self.welcome.place(relx=0.016, rely=0.089, height=23)
    self.welcome.configure(activebackground="#f9f9f9")
    self.welcome.configure(activeforeground="black")
    self.welcome.configure(background=_bgcolor)
    self.welcome.configure(disabledforeground="#a3a3a3")
    self.welcome.configure(font="-size 11 -weight bold")
    self.welcome.configure(foreground=_fgcolor)
    self.welcome.configure(highlightbackground=_bgcolor)
    self.welcome.configure(highlightcolor="black")
    self.welcome.configure(text="Your username is: " + username)

    self.send_button = tk.Button(top)
    self.send_button.place(relx=0.567, rely=0.856, height=29, width=85)
    self.send_button.configure(activebackground=_bg_active)
    self.send_button.configure(activeforeground=_fgcolor)
    self.send_button.configure(background=_bg_button)
    self.send_button.configure(disabledforeground="#a3a3a3")
    self.send_button.configure(foreground=_fgcolor)
    self.send_button.configure(highlightbackground=_bgcolor)
    self.send_button.configure(highlightcolor="black")
    self.send_button.configure(pady="0")
    self.send_button.configure(text="Send")

    self.commands = tk.Label(top)
    self.commands.place(relx=0.008, rely=0.276, height=21, width=354)
    self.commands.configure(background=_bgcolor)
    self.commands.configure(disabledforeground="#a3a3a3")
    self.commands.configure(font="-family TkFixedFont -size 8")
    self.commands.configure(foreground=_fgcolor)
    self.commands.configure(text="You can private message users by clicking on their name on the right")
    self.commands.configure(width=354)

    self.main_text = tk.Label(top)
    self.main_text.place(relx=0.017, rely=0.022, height=37, width=91)
    self.main_text.configure(background=_bgcolor)
    self.main_text.configure(disabledforeground="#a3a3a3")
    self.main_text.configure(font="-family TkFixedFont -size 17 -weight bold")
    self.main_text.configure(foreground=_fgcolor)
    self.main_text.configure(text='''RK Chat''')

    self.send_image = tk.Button(top)
    self.send_image.place(relx=0.017, rely=0.222, height=24, width=170)
    self.send_image.configure(activebackground=_bg_active)
    self.send_image.configure(activeforeground=_fgcolor)
    self.send_image.configure(background=_bg_button)
    self.send_image.configure(cursor="fleur")
    self.send_image.configure(disabledforeground="#a3a3a3")
    self.send_image.configure(foreground=_fgcolor)
    self.send_image.configure(highlightbackground=_bgcolor)
    self.send_image.configure(highlightcolor="black")
    self.send_image.configure(pady="0")
    self.send_image.configure(text="Click here to send an image")
    self.send_image.configure(width=67)

    self.clear_chat = tk.Button(top)
    self.clear_chat.place(relx=0.2, rely=0.222, height=24, width=67)
    self.clear_chat.configure(activebackground=_bg_active)
    self.clear_chat.configure(activeforeground=_fgcolor)
    self.clear_chat.configure(background=_bg_button)
    self.clear_chat.configure(disabledforeground="#a3a3a3")
    self.clear_chat.configure(foreground="#000000")
    self.clear_chat.configure(highlightbackground="#d9d9d9")
    self.clear_chat.configure(highlightcolor="black")
    self.clear_chat.configure(pady="0")
    self.clear_chat.configure(text="Clear chat")
    self.clear_chat.configure(width=67)

    all_emotes = self.get_emotes()
    offset = 0.017

    self.logout_button = tk.Button(top)
    self.logout_button.place(relx=0.017, rely=0.156, height=24, width=155)
    self.logout_button.configure(activebackground=_bg_active)
    self.logout_button.configure(activeforeground=_fgcolor)
    self.logout_button.configure(background=_bg_button)
    self.logout_button.configure(disabledforeground="#a3a3a3")
    self.logout_button.configure(foreground="#000000")
    self.logout_button.configure(highlightbackground="#d9d9d9")
    self.logout_button.configure(highlightcolor="black")
    self.logout_button.configure(pady="0")
    self.logout_button.configure(text="Exit client")

    for emote in all_emotes:
        emote_widget = tk.Button(top)
        self.emotes.append(emote_widget)
        self.emotes_names.append(emote)
        #self.emotes[len(self.emotes)-1] = emote
        self.emotes[len(self.emotes)-1].place(relx=offset, rely=0.933, height=22, width=22)
        self.emotes[len(self.emotes)-1].configure(activebackground=_bg_active)
        self.emotes[len(self.emotes)-1].configure(activeforeground=_fgcolor)
        self.emotes[len(self.emotes)-1].configure(background="#ffffff")
        self.emotes[len(self.emotes)-1].configure(disabledforeground="#a3a3a3")
        self.emotes[len(self.emotes)-1].configure(foreground=_fgcolor)
        self.emotes[len(self.emotes)-1].configure(highlightbackground="#000000")
        self.emotes[len(self.emotes)-1].configure(highlightcolor="#000000")
        photo_location = os.path.abspath("./emotes/"+emote+".png")
        self.img_ref.append(tk.PhotoImage(file=photo_location))
        self.emotes[len(self.emotes)-1].configure(image=self.img_ref[len(self.emotes)-1])
        self.emotes[len(self.emotes)-1].configure(pady="0")
        emote_text = ":" + emote + ":"
        self.emotes[len(self.emotes)-1].configure(command = lambda emote=emote: self.write_emote(top, ":"+emote+":"))
        offset += 0.0229




  def write_emote(self, top=None, msg=""):

    if not top:
        return

    curr_text = self.chat_input.get()

    if len(curr_text) == 0:
        self.chat_input.insert("end", msg + " ")
    elif curr_text[len(curr_text)-1] == ' ':
        self.chat_input.insert("end", msg + " ")
    else:
        self.chat_input.insert("end", " " + msg + " ")

  def get_emotes(self):
    path = os.path.abspath("./emotes/")

    files = []
    
    for r, d, f in os.walk(path):
        for file in f:
            if '.png' in file:
                files.append(file[0:len(file)-4])

    return files  