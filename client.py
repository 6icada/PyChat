# Code by 6icada
# Please do not copy code

# Tring to import libraries
try:
    import socket
    import threading
except:
    # ERROR MSG
    print(f'[ERROR]: Can\'t import libraries...')
    exit()

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
