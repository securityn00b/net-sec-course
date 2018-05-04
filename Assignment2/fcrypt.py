#Main Program for encryption.

from sys import argv
import os
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature 

script, e_or_d, public_key_file, private_key_file, plain_text_file, cipher_text_file = argv


backend = default_backend()


def main(argv):
		
	if (e_or_d == '-e' or e_or_d == '-E'):
		print "\n\t--------------------------------FILE EN/DE->CRYPTION PROGRAM----------------------------------"
		
		s_ifile = open (plain_text_file, 'rb')
		plain_text = s_ifile.read()
		s_ifile.close()
		
		#Generating a random key, IV
		key, iniv = sym_keygen()
		
		#Creating a shared key file for a particular session
		sk = open ('sessionkey', 'wb')
		sk.write(key)
		sk.close()
		
		#encrypting data using symmetric key
		ciph_text, padding_variable = sym_encr(plain_text, key, iniv)
		
		#Encrypting the Key using destination's public key
		encrypted_key_file = asymm_encr(key, public_key_file)
		s_ofile = open (cipher_text_file, 'wb')
		
		#Appending the encrypted_key_file, initialization vector and padding variable to the cipher text
		s_ofile.write(ciph_text + 'asdfgh' + encrypted_key_file +  'qwerty' + iniv  + 'bogus' + str(padding_variable))
		s_ofile.close()
				
		#Signing the cipher text and encrypted key with sender's private key
		s_ofile1 = open (cipher_text_file, 'rb')
		un_signed_file = s_ofile1.read()
		signed_file = digisign(un_signed_file, private_key_file)
		s_ofile1.close()
		
		#Generating Signature file name
		fn = os.path.basename(cipher_text_file)
		fn1 = os.path.splitext(fn)
		d = fn1[0]
		d1 = d + '_signed' + fn1[1]
		
		#Creating the signature file
		sfo = open (d1, 'wb')
		sfo.write(signed_file)
		print "File signed."
		sfo.close()
		
		
	elif (e_or_d == '-d' or e_or_d == '-D'):
		print "\n\t--------------------------------FILE EN/DE->CRYPTION PROGRAM----------------------------------"
		
		#steps leading to finding the signature file
		fn2 = os.path.basename(plain_text_file)
		fn3 = os.path.splitext(fn2)
		d2 = fn3[0]
		d3 = d2 + '_signed' + fn3[1]
			
		#verifying the signature
		d_ifile_signed = open (str(d3), 'rb')
		signa = d_ifile_signed.read()
		d_ifile_signed.close()
		messa = open(plain_text_file, 'rb')
		message_to_be_verified = messa.read()
		digiverify(str(signa), str(message_to_be_verified), private_key_file)
		messa.close()
		
		#Separating the iv, padding_variable and encrypted_key
		d_ifile = open (plain_text_file, 'rb')
		cipher_kitchensink = d_ifile.read()
		d_ifile.close()
		a = cipher_kitchensink.split('asdfgh')
		b = a[1].split('qwerty')
		c = b[1].split('bogus')
		cipht = a[0]
		encrypted_shared_key = b[0]
		initialization_vector = c[0]
		padding_config = c[1]
		
		#Decrypting the encrypted shared key
		shared_key = asymm_decr(encrypted_shared_key, public_key_file)
				
		#Creating a shared key file for a particular session
		sk1 = open ('sessionkey1', 'wb')
		sk1.write(shared_key)
		sk1.close()
		
		#Decrypting the plain text document
		plain_text_after_decryption = sym_decr(cipht, shared_key, initialization_vector, int(padding_config))
		#print plain_text_after_decryption
		d_ofile = open(cipher_text_file, 'wb')
		d_ofile.write(plain_text_after_decryption)
	
	else:
		print "Invalid arguments. Program is exiting..."
		sys.exit(0)
	
	
	
#Generating a random symmetric key and IV		
def sym_keygen():
	key = os.urandom(32)        			#key value is 32 bytes i.e. 256 bits.
	ini_vector = os.urandom(16) 			#IV is 16 bytes i.e. 128 bits. 
	return key, ini_vector


#Symmetric Encryption function	
def sym_encr(input_string, key, iv):
	cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)  #AES with CBS chosen
	encryptor = cipher.encryptor()
	
	#Padding the input
	length = 16 - (len(input_string)%16) 
	input_string += chr(length) * length
	
	#Encrypting the plain text
	ct = encryptor.update(input_string) + encryptor.finalize()
	return ct, length


#Symmetric Decryption function
def sym_decr(cipher_text, key, iv, padvar):
	cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
	decryptor = cipher.decryptor()
	
	#Decrypting the cipher text
	plain_text_tentative = decryptor.update(cipher_text) + decryptor.finalize()
	
	#removing the redundant padding
	plain_text = plain_text_tentative[:-(padvar)]
	return plain_text


#Asymmetric Encryption function (RSA)	
def asymm_encr(message, public_key_file):
	
	#Loading the .pem key
	with open(public_key_file, 'rb') as key_file:
		public_key = serialization.load_pem_public_key(
		key_file.read(),
		backend = default_backend()
		)
	
	#Encrypting the text
	ciphertext = public_key.encrypt(
	message,
	padding.OAEP(
		mgf = padding.MGF1(algorithm = hashes.SHA1()),
		algorithm = hashes.SHA1(),
		label = None
			)
	)
	return ciphertext

#Assymmetric Decryption function (RSA)	
def asymm_decr(ciphertext, private_key_file):
	
	#Loading the .pem key
	with open(private_key_file, 'rb') as key_file1:
		private_key = serialization.load_pem_private_key(
		key_file1.read(),
		password = None,
		backend = default_backend()
		)
	
	#Decrypting the text
	plaintext = private_key.decrypt(
		ciphertext, 
		padding.OAEP(
		mgf = padding.MGF1(algorithm = hashes.SHA1()),
		algorithm = hashes.SHA1(),
		label = None
		)
	)
	return plaintext	

#Digital Signing function	
def digisign(message, private_key_file):
	
	#Loading the .pem key
	with open(private_key_file, 'rb') as key_file1:
		private_key = serialization.load_pem_private_key(
		key_file1.read(),
		password = None,
		backend = default_backend()
		)
	
	#Signing function
	signer = private_key.signer(
		padding.PSS(
			mgf = padding.MGF1(hashes.SHA256()),     #SHA256 used.
			salt_length = padding.PSS.MAX_LENGTH
			),
		hashes.SHA256()
	)
	signer.update(message)
	signature = signer.finalize()
	return signature

def digiverify(signature, message, public_key_file):
	
	#Loading the .pem key
	with open(public_key_file, 'rb') as key_file2:
		public_key = serialization.load_pem_public_key(
		key_file2.read(),
		backend = default_backend()
		)
	
	#Verifying function
	verifier = public_key.verifier(
		signature,
		padding.PSS(
		mgf = padding.MGF1(hashes.SHA256()),      #SHA256 used.
		salt_length = padding.PSS.MAX_LENGTH
		),
		hashes.SHA256()
	)
	verifier.update(message)
	try:
		verifier.verify()
	except InvalidSignature:
		print "data has been changed. Mayday!Mayday! Program is exiting..."
		sys.exit(0)
	else:
		print 'integrity verified. Message was not modified in transit.'
		
		
		
		
		
if __name__ == "__main__":
	main(argv[1:])