# code by 6icada
# Please do not copy code

# Tring to import libraries
try:
    import socket
    import threading
    import sys
    import os
except:
    # ERROR MSG
    print(f'[ERROR]: Can\'t import libraries...')
    exit()

# Check args
if len(sys.argv) == 1:
    print('PyChat arguments:')
    print('-S -- Server')
    print('-C -- Client')
    print('-h -- This MSG')
else:
    if sys.argv[1] == '-S':
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
    elif sys.argv[1] == '-C':
        # Adding global vars
        hostname = socket.gethostname()

        # ConnectServer function
        def ConnectServer():
            # Adding vars
            HOST = input('Enter IPv4 address: ')
            PORT = 4444
            Client_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Tring to connect to the server
            try:
                Client_Socket.connect((HOST, PORT))

                # MSG when joining to the server
                print(f'[INFO]: You joined the server {HOST}:{PORT} as "{hostname}"')
            except:
                # WARNING MSG
                print(f'[WARNING]: Can\'t find server...')
                print(f'[INFO]: Try to check connection.If connection works then maybe server is down...')
                exit()

            # Write function (To write MSGs to the server)
            def Write():
                # Sending hostname to the server
                Client_Socket.send(hostname.encode('utf-8'))

                # Main loop for Write function
                while True:
                    # Adding vars
                    MSGToSend = input()
                    payload = f'{MSGToSend}'
                
                    # Check length of MSGToSend
                    if len(MSGToSend) == 0:
                        pass
                    else:
                        # Check if MSG is command or not
                        if MSGToSend[0] == '/':
                            # Commands
                            if MSGToSend == '/exit':
                                # Sending MSGToSend to the client
                                Client_Socket.send(MSGToSend.encode('utf-8'))

                                # Closing connection
                                Client_Socket.close()
                                exit()
                        else:
                            # Encoding MSGToSend
                            encodedMSGToSend = payload.encode('utf-8')

                            # Sending encodedMSGToSend to the server
                            Client_Socket.send(encodedMSGToSend)

            # Receive function (To receive MSGs from the server)
            def Receive():
                while True:
                    # Adding vars
                    receivedMSG = Client_Socket.recv(99999)

                    # Decoding receivedMSG
                    decodedReceivedMSG = receivedMSG.decode('utf-8')
                    
                    # Checking decodedReceivedMSG
                    if decodedReceivedMSG == '[WARNING]: Server is full':
                        # Close connection
                        Client_Socket.close()

                        # Exiting
                        exit()
                    else:
                        # Printing decodedReceivedMSG
                        print(f'{decodedReceivedMSG}')

            # Making threads
            writeThread = threading.Thread(target=Write)
            writeThread.start()
            receiveThread = threading.Thread(target=Receive)
            receiveThread.start()

        # Calling functions
        ConnectServer()
    elif sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print('PyChat arguments:')
        print('-S -- Server')
        print('-C -- Client')
        print('-h -- This MSG')
    else:
        # ERROR MSG
        print('[ERROR]: Invalid argument! type -h or --help for help!')