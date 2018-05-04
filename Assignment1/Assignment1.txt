Sockets Communication - Bare Bones chatting application 

There are 2 programs. 
One for the server, named "ChatServer.py" and one for the client names "ChatClient.py"


#####Usage#####

1. Open powershell in Windows or the appropriate shell in Linux i.e. bash
2. type "python ChatServer.py -sP <port number to be used>". For Example, "python ChatServer.py -sP 7000"               ----> for the server script 
3. Once the server script is started, 
start the client script by typing "python ChatClient.py -sIP <IP of server(127.0.0.1 in this case)> -sP <server port(same as above)>"   
For Example, "python ChatClient.py -sIP 127.0.0.1 -sP 7000"      ----> for the client scipt



[Limitations]

1. The code runs well for one client but there are some issues with multiple clients. At the time, I was just beginning to understand multithreading and faced lots of
problems using threads properly. 
2. The code sort of runs with multiple clients but there is substantial delay in the arrival of messages sent from the server to all hosts. 
Eg. I type 'hello' in 1 host now, but it only reaches all hosts after typing 2 or 3 lines of text in other hosts. 
