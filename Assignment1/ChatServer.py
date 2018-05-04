import socket																# The socket module is the most important module used in this program.
import sys
from sys import argv

script, server_port_option, port_number = argv # Arguments to the main function

def Main(argv):
	host = '127.0.0.1' 
	port = int(port_number) 												# Converting port_number to an integer
	host_list = []          												# Creating a list to keep track of connected hosts 
	port_list = []															# Creating a list of the port numbers of the connected hosts for later use.
	
	if (server_port_option!='-sP'):        									# check for correct input flags to the python script (-sP)   
		print "invalid arguments. Exiting server script..."
		sys.exit(0)
	
	
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  					# Creating a socket. SOCK_DGRAM is a UDP socket.
	s.bind((host,port)) 								  					# binding the created socket object to a host and port.
	
	print "Server Initializing: "
	print "---Server Started---"
	
	
	while True:
		data, addr = s.recvfrom(128)   										# To receive the text typed by the clients. 128 is the buffer size. 
		
		if (str(addr) not in host_list):  									# Check whether the host sending the GREETING is already in the list of registered clients.
			host_list.append(str(addr))										# Add the addr to the list. Note that the addr variable is a 2 element tuple and must be typecast to a string
			port_list.append(addr[1])										# Add the port of the connecting host to port_list
			print str(addr) + "is registered and now active."	
			s.sendto ('GREETING received', addr)                			# Confirm receipt of GREETING signal
		
		
		else:													
			temp = host_list.index(str(addr))													# Get the index of the element in host_list that sent the message.
			sender = host_list[temp]								
			print "sending the message received from " + sender + " to all registered users."  
			
			for p in port_list:																	# Send the message sent by the registered users to each user in the host_list (all registered users)
				dest_addr = ('127.0.0.1', int(p))												# Since dest_addr argument to the sendto function must be a tuple consisting of 2 elements - host and address
				s.sendto(("message from" + sender + ": " + data), dest_addr)   					# send message to all users that sent a GREETING
	s.close()																					# Close the Socket
				
				
if __name__ == '__main__':
    Main(argv[1:]) 															# the element in the zero index of argv is the script name itself. Hence it is not considered as an Argument.
