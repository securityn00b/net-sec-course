import socket                                                           				# The socket module is the most important module used in this program.
import sys
from sys import argv

script, server_ip_option, server_ip, server_port_option, server_port = argv             # Arguments provided with the script

def Main(argv):
		
	if (server_ip_option!='-sIP' or server_port_option!='-sP'):			# check for correct input flags to the python script - -sIP (for Server IP) and -sP (for Server port)   
		print "invalid arguments. Exiting program..."
		sys.exit(0);
	
	server = (server_ip,int(server_port))								# Creating a host,port tuple, to be used in the sendto function.
	
	host = '127.0.0.1'
	port_info = 0														# Port 0 indicates that the Operating System will choose any free UDP port for the client
	user_prompt = '->'													# Creating a variable for the user prompt. That way, changes it here will change the prompt everywhere.
	
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)				# Creating a UDP socket. AF_INET in the socket family (used for IPv4 addresses) and the SOCK_DGRAM indicates that this is a UDP socket.
	s.bind((host, port_info))											# Binding the socket to a host and port.	
	temp, port = s.getsockname()										# Return socket's address.
	
	print "Connecting to server using port " + str (port)               # These next 2 statements send GREETING message to server
	s.sendto('GREETINGS', server)
	
	data, addr = s.recvfrom(128)										# These 2 statements print the server's confirmation that the host has sent the GREETING message.			
	print data
	message = raw_input (user_prompt)									
	
	while (message != 'quitc'):											# program exits only if users types quitc
		s.sendto(message, server)										# send message to the server.
		data, addr = s.recvfrom(128)									# Receive messages from the server. 128 indicates the buffer length.
		print "Message from server: " + str(data)
		message = raw_input (user_prompt)
	
	s.close();															# Close the socket object so that it cannot send or accept any more connection				


if __name__ == '__main__' :
	Main(argv[1:])														# the element in the zero index of argv is the script name itself. Hence it is not considered as an Argument.
	
	
