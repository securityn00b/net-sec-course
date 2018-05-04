#This code is used only for symmetric encryption ^^^once the shared key has been exchanged using asymmetric encryption^^^.

from sys import argv
import os
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend 


script, input_file, symmetric_key = argv

#Choose backend. The default is openssl
backend = default_backend()                                                		


def main(argv):
	print "----------------------TEXT FILE DECRYPTOR AFTER KEY EXCHANGE------------------------"
	
	print "Do you want encrypt or decrypt the file?"
	choice = raw_input ('-->')
	
	#If encryption is chosen
	if choice=='e':
		f = open(input_file)
		plain_text = f.read()
		f.close()
		print "plain text is:" 
		print plain_text
		
		#Reading the session key file
		g = open(symmetric_key)
		session_key = g.read()
		g.close()
		
		#randomize_initialization_vector
		iniv = sym_ivgen()
		
		#encrypt plain text using symmetric key
		cipher_text, padding_variable = sym_encr(plain_text, session_key, iniv)
		
		#Giving a name to the cipher text file
		fn = os.path.basename(input_file)
		d = os.path.splitext(fn)
		d1 = d[0]
		d2 = d1 + '_enc'
		h = open (d2, 'w')
		
		#appending initialization vector and padding variables to the cipher text
		h.write (cipher_text + 'zxcvb' + iniv + 'uiopl' + str(padding_variable))
		h.close()
	
	#If decryption is chosen
	elif choice=='d':
		
		#Reading the session key file
		g1 = open (symmetric_key, 'rb')
		session_key = g1.read()
		g1.close()
		
		#Reading the cipher text file
		f1 = open (input_file, 'rb')
		ciph_text_temp = f1.read()
		f1.close()
		
		#separating initialization vector, cipher text and padding variable
		w = ciph_text_temp.split('zxcvb')
		cipher_text_final = w[0]
		x = w[1].split('uiopl')
		inivector = x[0]
		pad_variable = x[1]
				
		#Decrypting cipher text
		plain_text_after_decryption = sym_decr(cipher_text_final, session_key, inivector, pad_variable)
		print "After decryption:"
		print plain_text_after_decryption
	
	else:
		print "invalid choice. Program exiting..."
	
	

#To generate random IV	
def sym_ivgen():
	ini_vector = os.urandom(16)
	return ini_vector

	
#Encryption function	
def sym_encr(input_string, key, iv):
	cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
	encryptor = cipher.encryptor()
	length = 16 - (len(input_string)%16)
	input_string += chr(length) * length  
	ct = encryptor.update(input_string) + encryptor.finalize()
	return ct, length

	
#Decryption function
def sym_decr(cipher_text, key, iv, padvar):
	cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
	decryptor = cipher.decryptor()
	plain_text_tentative = decryptor.update(cipher_text) + decryptor.finalize()
	plain_text = plain_text_tentative[:-(int(padvar))]
	return plain_text
	
	
if __name__ == "__main__":
	main(argv[1:])