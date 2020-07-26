import socket 
import select 

HEADER_LEN = 10
IP = "0.0.0.0"
PORT = 1234


"""setup start"""
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#allow to reconnect and reuse address
#set property SO_REUSEADDR to true for option SOL_SOCKET
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))

server_socket.listen()
"""setup end"""

#get list of clints, including server
sockets_list = [server_socket]
clients = {}
#recieve messages
def recieve_message(client_socket: socket):
    try:
        message_header = client_socket.recv(HEADER_LEN)
        if not len(message_header):
            return False;
        message_length = int(message_header.decode("utf-8").strip())
        return {"header":message_header, "data":client_socket.recv(message_length)}
    except:
        return False

while True:
    read_sockets, _ , exception_sockets = select.select(sockets_list, [], sockets_list)
    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user  = recieve_message(client_socket)
            if user == False:
                continue
            sockets_list.append(client_socket)
            clients[client_socket] = user
            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username: {user['data'].decode('utf-8')}")
        else:
            message = recieve_message(notified_socket)
            if message is False:
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            user = clients[notified_socket]
            print(f"recieved message from {user['data'].decode('utf-8')}:{message['data'].decode('utf-8')}")
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header']+message['data'])