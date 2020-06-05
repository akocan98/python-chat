import socket
import struct
import sys
import threading
import pickle # from Germany :D
import random
import os
import urllib.request
import base64
import datetime
try:
    from Tkinter import *
except ImportError:
    from tkinter import *
import mainGui
import loginGui
import noConnectionGui
import addImg

PORT = 8080
HEADER_LENGTH = 2

gui_window = Tk()  
gui_frame = None
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def receive_fixed_length_msg(sock, msglen):
    message = b''
    while len(message) < msglen:
        chunk = sock.recv(msglen - len(message))  # preberi nekaj bajtov
        if chunk == b'':
            raise RuntimeError("socket connection broken")
        message = message + chunk  # pripni prebrane bajte sporocilu

    return message

def receive_message(sock):
    header = receive_fixed_length_msg(sock, HEADER_LENGTH)  # preberi glavo sporocila (v prvih 2 bytih je dolzina sporocila)
    message_length = struct.unpack("!H", header)[0]  # pretvori dolzino sporocila v int

    message = None
    if message_length > 0:  # ce je vse OK
        message = receive_fixed_length_msg(sock, message_length)  # preberi sporocilo

    msg = pickle.loads(message)
    return msg

def send_message(sock, message, usrname, helloPing = False, imageMessage = False):

    msgType = "mass" 
    recipient = "all"

    date_time = datetime.datetime.now().time() 

    message = message.strip()

    if len(message) < 1:
        return

    if message[0] == "@":
        msgType = "private"
        if message[1] == '"':
            recipient = message.split('"')[1]
            message = message.split('"')[2]
        elif message[1] == "'":
            recipient = message.split("'")[1]
            message = message.split("'")[2]
        else:
            recipient = (message.split(" ")[0])[1:]
            message = message.split(" ")
            del message[0]
            newMessage = ""
            for x in message:
                newMessage += x + " "
            message = newMessage


    sporocilo = { "username": usrname, "msg": message, "type": msgType, "recipient": recipient, "helloPing": helloPing, 'imageMessage': imageMessage, "date" : date_time }

    pickledSporocilo = pickle.dumps(sporocilo)
    #encoded_message = message.encode("utf-8")  # pretvori sporocilo v niz bajtov, uporabi UTF-8 kodno tabelo

    # ustvari glavo v prvih 2 bytih je dolzina sporocila (HEADER_LENGTH)
    # metoda pack "!H" : !=network byte order, H=unsigned short
    header = struct.pack("!H", len(pickledSporocilo))

    message = header + pickledSporocilo  # najprj posljemo dolzino sporocilo, slee nato sporocilo samo

    sock.sendall(message);

def clear_send_message(sock, message, usrname, gui_frame):
    gui_frame.chat_input.delete(0,"end")
    send_message(sock, message, usrname)

def close_send_message(sock, message, usrname, gui_frame):
    gui_frame.destroy()
    send_message(sock, message, usrname, False, True)

def get_dir_contents(p):
    path = os.path.abspath(p)

    files = []
    
    for r, d, f in os.walk(path):
        for file in f:
            if '.png' in file:
                files.append(file[0:len(file)-4])

    return files

def text_contains_emote(textStr, emotesArr):

    textStr = textStr.strip()

    if len(textStr) < 2:
        return False

    textArr = textStr.split(" ")

    contains = False

    if len(textArr) == 1:
        if textArr[0][0] == ":" and textArr[0][len(textArr[0])-1] == ":":
            return True
        else:
            return False

    for t in textArr:
        if t == "":
            continue
        if t[0] == ":" and t[len(t)-1] == ":" and t[1:len(t)-1] in emotesArr:
            return True

    return False

def message_receiver():

    global gui_frame
    global username

    while True:
        
        try:
            msg_received = receive_message(sock)
        except RuntimeError:
            print("You have been disconnected.")
            sys.exit()

        if len(msg_received) > 0:  # ce obstaja sporocilo

            chat_tag_config = "normal"

            if len(msg_received["msg"]) > 0:
                msg_received["msg"] = msg_received["msg"].strip()

            if msg_received["username"] and msg_received["username"].upper() == "SYSTEM":
                chat_tag_config = "system"
                   
            if msg_received['imageMessage']:

                #curr there's no parsing bad photos
                img = None

                usrSent = msg_received['msg'].split("@url@")[0]
                imgPath = msg_received['msg'].split("@url@")[1]

                if imgPath.startswith('http://') or imgPath.startswith('https://'):
                    image_byt = None
                    try:
                        image_byt = urllib.request.urlopen(imgPath).read()
                    except urllib.request.HTTPError as err:
                        print("You don't have permission to access this url")
                        continue
                    except:
                        print("Unexpected error:", sys.exc_info()[0])
                        continue
                    image_b64 = base64.encodestring(image_byt)
                    img = PhotoImage(data=image_b64)
                else:
                    try:
                        img = PhotoImage(file = os.path.abspath(imgPath))
                    except TclError:
                        print("Given path doesn't exist")
                        continue
                    except:
                        print("Unexpected error:", sys.exc_info()[0])
                        continue

                img = img.zoom(1) 
                img = img.subsample(5) 
                gui_frame.chat.config(state="normal")
                images_reference.append(img)
                gui_frame.chat.insert('1.0', "\n", chat_tag_config)
                gui_frame.chat.image_create('1.0', image = img)
                gui_frame.chat.insert('1.0', "["+usrSent+"]:", chat_tag_config)
                gui_frame.chat.config(state="disabled")

            elif msg_received['whisper']:
                chat_tag_config = "private_message"
                tekst = msg_received["msg"]

                emojis_to_parse = get_dir_contents("./emotes/")

                gui_frame.chat.config(state="normal")
                
                if text_contains_emote(tekst.strip(), emojis_to_parse):
                    tekst = tekst.split(" ")
            
                    gui_frame.chat.insert('1.0', "\n", chat_tag_config)

                    for t in reversed(tekst):
                        if t == "":
                            continue
                        if t[0] == ":" and t[len(t)-1] == ":" and t[1:len(t)-1] in emojis_to_parse:
                            gui_frame.chat.insert('1.0', " ", chat_tag_config)
                            img = PhotoImage(file = os.path.abspath("./emotes/"+t[1:len(t)-1]+".png"))
                            images_reference.append(img)
                            gui_frame.chat.image_create('1.0', image = img)
                        else:
                            gui_frame.chat.insert('1.0', t + " ", chat_tag_config)

                    gui_frame.chat.insert('1.0', "[" + msg_received["username"] + " whispered to you]: ", chat_tag_config)

                else:
                    tekst = "[" + msg_received["username"] + " whispered to you]: " + tekst
                    gui_frame.chat.insert('1.0', tekst + "\n", chat_tag_config)
                
                gui_frame.chat.config(state="disabled")
                print("[" + msg_received["username"] + " whispered to you]: " +  msg_received["msg"]) 
            
            elif msg_received['clientList']:
                gui_frame.online_users.delete(0,'end')
                print(msg_received["msg"].split("\n"))
                for oseba in msg_received["msg"].split("\n"):
                    if oseba:
                        gui_frame.online_users.insert(0, oseba)
            
            elif msg_received['nameSwitch']:
                username = msg_received["msg"]
                gui_frame.welcome.configure(text="Your username is: " + username + "!")
            
            else:

                tekst = msg_received["msg"]

                gui_frame.chat.config(state="normal")
                
                emojis_to_parse = get_dir_contents("./emotes/")

                if text_contains_emote(tekst.strip(), emojis_to_parse):
                    tekst = tekst.split(" ")
                    gui_frame.chat.insert('1.0', "\n", chat_tag_config)

                    for t in reversed(tekst):
                        if t == "":
                            continue
                        if t[0] == ":" and t[len(t)-1] == ":" and t[1:len(t)-1] in emojis_to_parse:
                            gui_frame.chat.insert('1.0', " ", chat_tag_config)
                            img = PhotoImage(file = os.path.abspath("./emotes/"+t[1:len(t)-1]+".png"))
                            images_reference.append(img)
                            gui_frame.chat.image_create('1.0', image = img)
                        else:
                            gui_frame.chat.insert('1.0', t + " ", chat_tag_config)

                    gui_frame.chat.insert('1.0', "[" + msg_received["username"] + "]: ", chat_tag_config)

                else:
                    tekst = "[" + msg_received["username"] + "]: " + tekst
                    gui_frame.chat.insert('1.0', tekst + "\n", chat_tag_config)
            
                gui_frame.chat.config(state="disabled")
                print("[" + msg_received["username"] + "]: " +  msg_received["msg"])

def on_user_select(e):
    
    global gui_frame

    gui_window = e.widget

    if not gui_window.curselection():
        return

    index = int(gui_window.curselection()[0])
    value = gui_window.get(index)

    if " " in value:
        value = '"' + value + '"'
    
    currText = gui_frame.chat_input.get()

    if len(currText) < 1 or currText[0] != "@":
        gui_frame.chat_input.insert(0, "@" + value + " ")
    else:
        gui_frame.chat_input.delete(0, "end")
        gui_frame.chat_input.insert(0, "@" + value + " ")

def send_img_prompt(sock, username):
    # ta komentar je tu samo, da lahko minimiziram funkcijo v sublimeu
    nov_window = Toplevel(gui_window)
    nov_window_frame = addImg.addImg(nov_window)
    nov_window_frame.send_img_button.configure(command = lambda: close_send_message(sock, nov_window_frame.url_box.get(), username, nov_window))

def clear_chat(gui_frame):
    #global gui_frame

    #TODO clear image reference array, no need for it to exist beyond here pa to
    gui_frame.chat.config(state="normal")
    gui_frame.chat.delete('1.0',"end")
    gui_frame.chat.config(state="disabled")

def logout(sock, gui_frame):
    #t.join()
    for widget in gui_window.winfo_children():
        widget.destroy()

    gui_window.destroy()
    sock.shutdown(socket.SHUT_RDWR)
    sys.exit()

def connect_to_server(usrname):

    global gui_frame
    global username

    username = usrname
    # povezi se na streznik
    try:
        sock.connect(("localhost", PORT))
    except ConnectionRefusedError:
        gui_frame = noConnectionGui.noConnectionGui(gui_window)

    print("[system] connected!")

    # ping da se predstavi
    send_message(sock, "ojla", username, True, False)

    # make gui kar je treba tuki 
    gui_frame = mainGui.mainGui(gui_window, username)
    gui_frame.send_button.configure(command = lambda: clear_send_message(sock, str(gui_frame.chat_input.get()), username, gui_frame))
    gui_frame.send_image.configure(command = lambda: send_img_prompt(sock, username))
    gui_frame.logout_button.configure(command = lambda: logout(sock, gui_frame))
    gui_frame.online_users.bind('<<ListboxSelect>>', on_user_select)
    gui_frame.clear_chat.configure(command=lambda: clear_chat(gui_frame))
    gui_frame.chat.config(state="disabled")
    gui_window.bind('<Return>', lambda eff: clear_send_message(sock, str(gui_frame.chat_input.get()), username, gui_frame))

    # zazeni message_receiver funkcijo v loceni niti    thread_msg.daemon = True
    thread_msg = threading.Thread(target=message_receiver)
    thread_msg.start()

    print(threading.activeCount())
    # pocakaj da uporabnik nekaj natipka in poslji na streznik
    while True:
        try:
            msg_send = input()
            send_message(sock, msg_send, username)
        except KeyboardInterrupt:
            sys.exit()

def init_server_thread(usrname):

    for widget in gui_window.winfo_children():
        widget.destroy()
    
    if len(usrname) < 1:
        pridevniki = [ "Happy", "Sad", "Hungry", "Warm", "Fair", "Assorted", "Supreme", "Wise", "Pretty", "Honorable", "Beautiful", "Caring", "Heroic", "Majestic", "Amazing" ]
        samostalniki = [ "Map", "Turtle", "House", "Lake", "Seagull", "Jacket", "Ship", "Sandwich", "Python", "Java", "Dinosaur"  ]
        usrname = pridevniki[random.randint(0, len(pridevniki)-1)] + samostalniki[random.randint(0, len(samostalniki)-1)] + str(random.randint(1, 999))

    # server laufa v loceni niti ni v mainu 
    thread_server = threading.Thread(target=connect_to_server, args=[usrname])
    thread_server.daemon = True
    thread_server.start()

# WINDOW INIT (tkinter mora bit v main threadu nevem zakaj )
username = ""
images_reference = []
guiFrame = loginGui.loginGui(gui_window)
gumb = Button(gui_window, text ="Login", command = lambda: init_server_thread(guiFrame.prijava.get()))
gumb.place(relx=0.683, rely=0.467, height=39, width=65)
gumb.configure(activebackground='#4c7fff',  background="#72beff", highlightbackground="#d9d9d9")
gumb.configure(activeforeground="#000000", disabledforeground="#a3a3a3", foreground="#000000")
gumb.configure(pady="0", width=65, text="Login", highlightcolor="black")
gui_window.mainloop()