# Code by 6icada
# Please do not copy code

# Tring to import libraries
try:
    import socket
    import threading
    import os
except:
    # ERROR MSG
    print(f'[ERROR]: Can\'t import libraries...')
    exit()

# MakeSocket function
def MakeSocket():
    # Adding vars
    HOST = '0.0.0.0'
    PORT = 4444
    clients = []
    Server_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Binding Server_Socket
    Server_Socket.bind((HOST, PORT))
    Server_Socket.listen()

    # MSG when server starts
    print(f'[START]: Server started on {HOST}:{PORT}')

    # Handle function (To handle client)
    def Handle():
        # Check if clients list is full
        if len(clients) >= 5 or len(clients) == 5:
            # NHandle function
            def NHandle():
                while True:
                    # Adding vars
                    client, address = Server_Socket.accept()

                    # Sending WARNING to the client
                    client.send('[WARNING]: Server is full'.encode('utf-8'))

                    # Closing connection
                    client.close()

                    # MSG when connection is already closed
                    print(f'[WARNING]: {address} tried to connect to the server')

                    exit()

            # New clients can't connect.Reason is that 5 clients are MAX on the server
            newThread = threading.Thread(target=NHandle)
            newThread.start()
            newThread.join()
        else:
            # Adding vars
            client, address = Server_Socket.accept()
            clientHostname = client.recv(9000)
            decodedClientHostname = clientHostname.decode('utf-8')

            # Adding client to the clients list
            clients.append(client)

            # MSG when client connects
            print(f'[INFO]: Connection from {address}')
            
            # Send MSG when client connects to other clinets
            for Client in clients:
                if Client == client:
                    pass
                else:
                    if len(clients) == 0:
                        pass
                    else:
                        Client.send(f'[INFO]: {decodedClientHostname} joined!'.encode('utf-8'))

            # Main loop for Handle function
            while True:
                # Receiving MSG from client
                receivedMSG = client.recv(99999)
                decodedReceivedMSG = receivedMSG.decode('utf-8')

                # If length of receivedMSG == 0 then do nothing
                if len(receivedMSG) == 0:
                    pass
                else:
                    # Check if MSG is command or not
                    if decodedReceivedMSG[0] == '/':
                        # Commands
                        if decodedReceivedMSG == '/exit':
                            # Closing connection
                            client.close()

                            # Printing MSG when client exits
                            print(f'[INFO]: {address} disconnected')

                            # Sending MSG to other cloents
                            for Client in clients:
                                if Client == client:
                                    pass
                                else:
                                    Client.send(f'[INFO]: {address} disconnected'.encode('utf-8'))

                            # Removing client from clients list
                            clients.remove(client)
                    else:
                        # Printing decodedReceivedMSG
                        print(f'{decodedClientHostname}: {decodedReceivedMSG}')

                        # Sending receivedMSG to other clients
                        for Client in clients:
                            if Client == client:
                                pass
                            else:
                                Client.send(f'{decodedClientHostname}: {decodedReceivedMSG}'.encode('utf-8'))

    # Making threads
    counter1 = 1
    limit = 5
    while counter1 <= limit:
        handleThread = threading.Thread(target=Handle)
        handleThread.start()

        counter1 = counter1 + 1

# Calling functions
MakeSocket()
