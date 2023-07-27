# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 21:13:33 2023

@author: Devam
"""

import socket


#comman info which is gonna get used through out the program 
Header=64
PORT=5050
Format='utf-8'

#funcion for the client side of the archiecture
def client(SERVER):
    # connects the client to the server
    ADDR=(SERVER,PORT)
    client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    
    #function to interect with server
    def send(msg):
        # for new line
        print()
        #encodes the message with utf-8 format
        message=msg.encode(Format)
        
        msg_length=len(message)
        send_length=str(msg_length).encode(Format)
        
        #pads the bits as it need to be 64 bit message
        send_length+=b' ' * (Header-len(send_length))
        
        #first send the length of the message to start the listining on the server
        client.send(send_length)
        
        #then send the encoded message itself
        client.send(message)
        
        #receives the message for the server
        back=str(client.recv(64))
        
        #display
        print('other:',str(back[2:-1]))#we receive the message form the server in b'message' format so slice the message to remove b''.
        #b'' string is a byte type... 
        
        #return the message to check whether we want to continue the protocal or end it
        return str(back[2:-1])
    
    # takes message to send
    msg_sent=input('you:')
    revcieved=send(msg_sent)
    
    #Exit control
    if msg_sent=='!disconnect':
       return 'you'
    elif  revcieved=='!disconnect':
        return 'other'
    else:
        return True
       
    
#function for the server side of the archiecture
def Server():
    
    # starts the server
    SERVER=socket.gethostbyname(socket.gethostname())
    ADDR=(SERVER,PORT)
    
    server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #binds the server and client
    server.bind(ADDR)

    #Handles the exchange of messages
    
    def HandleClient(conn,addr):
        # exit control variable
        connected=True
        
        msg_length=conn.recv(Header).decode(Format)
        
        #if msg_length is send that mean client has send the msg
        #so but puting if here we will not have to deal with error later
        if msg_length:
            msg_length=int(msg_length)
            
            # recieves the msg sent by client
            msg=conn.recv(msg_length).decode(Format)
            #display
            print('other:',msg)
            
            #Exit control if client don't want to talk
            if str(msg)=='!disconnect':
                connected="Other"
                return connected
            #if client want to continue, we sent the message: or 
            #if we can to disconnect we will simple send '!disconnect' message
            send_back=input('you:')
            conn.send(send_back.encode(Format))
            
            #Exit control
            if send_back=='!disconnect':
                connected="You"
                return connected
        return connected
                
    
    
    def start():
        
       #starts listening on server side
       
       server.listen()
       
       #used for exit control
       convo=True
       
       conn,addr=server.accept() 
       
       #after geting data for the client sends it to HandleClient function
       convo=HandleClient(conn, addr)
       
       return convo
    
    Keep_going=start()
    
    #returing true or false on whether to sender or receiver want to continue or not.
    return Keep_going
   
    
#Start of exicution---------------------------------------------------------------------------------------------------------------------------------
    
print('Welcome to Domchat')
print(socket.gethostbyname(socket.gethostname()))
# asks for the IP of the person we want to continue 
IP=input('Enter the IP of the person u want to talk to!:')
print('Would you like to be initiate the converzation or wait!!?')
print('1 for Initiate:')
print('2 for waiting.')
print('[*]NOTE: \n->Both can\'t wait or initiate at the same time and must have each other\'s IP entered... \n->And other person must be waiting for u to initiate. \n->If want to discontinue then type \'!disconnect\' ')

#checks whether the input enters is valid or not
while True:
    select=input('Enter:-')
    if select not in [1,2]:
        break
    else:
        print('invalid input!!!')

#will start client or server according to the data entered by the user
while True:
    #if client
    if select=='1':
        
        #an error occurs if the server is not on and we start client 
        #to handle that we use try except block
        try:
            your_msg=client(IP)
            if your_msg=='you':
                break
            elif your_msg=='other':
                print('Seems like the other person does not want to continue ;_; ')
                break
            elif your_msg:
                pass
        except:
            
            print('Looks like other person is not waiting..Try again...')
            break
        
    #if server
    elif select=='2':
         serv=Server()
         if serv=='You':
             break
         elif serv=='Other':
             print('Seems like the other person does not want to continue ;_; ')
             break
         elif serv:
             pass
        
#last display msg. 
print('Thanks for using our system!')

