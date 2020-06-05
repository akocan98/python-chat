import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)
import socket
import struct
import threading
import pickle
import random

PORT = 8080
HEADER_LENGTH = 2

class pajac:

    def __init__(self, sock, conn):
        self.test = "test"
        self.sock = sock
        self.unique = conn
        self.username = None # je none dokler kej ne reče

    def set_username(usr):
        self.username = username

def receive_fixed_length_msg(sock, msglen):
    message = b''
    while len(message) < msglen:
        chunk = sock.recv(msglen - len(message))  # preberi nekaj bajtov
        if chunk == b'':
            raise RuntimeError("socket connection broken")
        message = message + chunk  # pripni prebrane bajte sporocilu

    return message

def setUsername(sock, usr):
    
    sock_client = None
    usernameTaken = False

    if usr == "System":
        return True

    for client in clients:
        if client.username == None and client.unique == sock.getpeername():
            sock_client = client
            client.username = usr
        elif client.username == usr and client.unique != sock.getpeername():
            usernameTaken = True

    if usernameTaken:
        pridevniki = [ "Happy", "Sad", "Hungry", "Warm", "Fair", "Assorted", "Supreme", "Wise", "Pretty" ]
        samostalniki = [ "Map", "Turtle", "House", "Lake", "Seagull", "Jacket", "Ship", "Sandwich", "Python", "Java"  ]
        sock_client.username = pridevniki[random.randint(0, len(pridevniki)-1)] + samostalniki[random.randint(0, len(samostalniki)-1)] + str(random.randint(1, 999))
        return str(sock_client.username)

    return True

def receive_message(sock):

    header = receive_fixed_length_msg(sock, HEADER_LENGTH)  # preberi glavo sporocila (v prvih 2 bytih je dolzina sporocila)
    message_length = struct.unpack("!H", header)[0]  # pretvori dolzino sporocila v int

    message = None
    if message_length > 0:  # ce je vse OK
        message = receive_fixed_length_msg(sock, message_length)  # preberi sporocilo

    msg = pickle.loads(message)

    if msg["helloPing"]:
        set_usr = setUsername(sock, msg['username'])
        if isinstance(set_usr, bool):
            msg["name_switched"] = False
        else:
            msg["name_switched"] = True
            msg["new_name"] = set_usr

    return msg

def send_message(sock, message, username, whisper = False, clientlist = False, nameswitch = False, imageMessage = False):
    
    sporocilo = { 
    "username": username, 
    "msg": message, 
    "whisper": whisper, 
    "clientList": clientlist, 
    "nameSwitch": nameswitch, 
    "imageMessage": imageMessage}

    pickledSporocilo = pickle.dumps(sporocilo)
    #encoded_message = message.encode("utf-8")  # pretvori sporocilo v niz bajtov, uporabi UTF-8 kodno tabelo

    # ustvari glavo v prvih 2 bytih je dolzina sporocila (HEADER_LENGTH)
    # metoda pack "!H" : !=network byte order, H=unsigned short
    header = struct.pack("!H", len(pickledSporocilo))

    message = header + pickledSporocilo  # najprj posljemo dolzino sporocilo, slee nato sporocilo samo

    sock.sendall(message);

def client_thread(client_sock, client_addr):
    global clients

    try:

        while True:  # neskoncna zanka
            msg_received = receive_message(client_sock)

            msg_received["msg"] = msg_received["msg"] + " (" +  str(msg_received["date"])[0:8] + ")"

            if not msg_received:  # ce obstaja sporocilo
                break

            if msg_received["helloPing"]:
                print("[System] New hello ping:", msg_received)
                print("[System] we now have " + str(len(clients)) + " clients")

                send_message(client_sock, "Welcome to the chat. You can send images, emotes (ico ns below) & plain text. To private message someone, click on their name on the right.", "System")
                
                if msg_received["name_switched"]:
                    send_message(client_sock, "The name you requested was already taken so we gave you a random one.", "System")
                    send_message(client_sock, msg_received['new_name'], "System", False, False, True)    
                # send client list to all clients
                clientList = ""
			
                for client in clients:
                    clientList += client.username + "\n"

                for client in clients:
                    send_message(client.sock, clientList, "System", False, True)   

                continue

            if len(msg_received['msg']) < 2:
                send_message(client_sock, "Your message is too short.", "System")
                continue

            if msg_received['imageMessage']:  
                #TODO VALIDATE URLS
                print("[System] New image message:", msg_received)
                for client in clients:
                    send_message(client.sock, msg_received['username'] + "@url@" + msg_received["msg"], msg_received["username"], False, False, False, True) 

            elif msg_received['type'] == 'mass':
                print("[System] New global message:", msg_received)
                for client in clients:
                    send_message(client.sock, msg_received["msg"], msg_received["username"])
            
            elif msg_received['type'] == 'private':
                print("[System] New private message:", msg_received)
                found_recipient = False
                
                if msg_received['username'] == msg_received['recipient']:
                    send_message(client_sock, "You can't private message yourself.", "System")
                    continue

                for client in clients:
                    if client.username == msg_received['recipient']:
                        send_message(client.sock, msg_received["msg"], msg_received["username"], True, False)
                        found_recipient = True
                if found_recipient:
                    send_message(client_sock, "You whispered to " + msg_received["recipient"] + ": "+ msg_received["msg"], "System")
                else:
                    send_message(client_sock, "There's nobody online with the username " + msg_received["recipient"] + ".", "System")
    except:
        # tule bi lahko bolj elegantno reagirali, npr. na posamezne izjeme. Trenutno kar pozremo izjemo
        pass

    # prisli smo iz neskoncne zanke
    with clients_lock:
        
        for client in clients: 
            if client.sock == client_sock:
                clients.remove(client)
                break
        
        clientList = ""
        
        for client in clients:
            #print(client.username)
            clientList += client.username + "\n"

        for client in clients:
            send_message(client.sock, clientList, "System", False, True)  
        

    print("[System] we now have " + str(len(clients)) + " clients")
    client_sock.close()

# kreiraj socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", PORT))
server_socket.listen(1)

# cakaj na nove odjemalce
print("[System] listening ...")
clients = set()
clients_lock = threading.Lock()

while True:
    try:
        # pocakaj na novo povezavo - blokirajoc klic
        client_sock, client_addr = server_socket.accept()
        with clients_lock:
            clients.add(pajac(client_sock, client_addr))
        thread = threading.Thread(target=client_thread, args=(client_sock, client_addr));
        thread.daemon = True
        thread.start()

    except KeyboardInterrupt:
        break

print("[System] closing server socket ...")
server_socket.close()
