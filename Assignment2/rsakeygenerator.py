from sys import argv
#### public key encryption
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
script, public_key_file, private_key_file = argv

def asymm_keygen(public_file, private_file):
	#Generating private key
	priv_key = rsa.generate_private_key(public_exponent = 65537, 
	key_size = 2048, backend = default_backend()                 #2048 bit key
	)
	#Serializing the private key
	pemmy1 = priv_key.private_bytes(
	encoding = serialization.Encoding.PEM,
	format = serialization.PrivateFormat.PKCS8,
	encryption_algorithm = serialization.BestAvailableEncryption("P@$$w0r9")
	)
	
	pemmy1.splitlines()[0]
	
	#Writing private key to a pem file
	priv_key_f = open(private_file, 'w')
	priv_key_f.write(pemmy1)
	
	# Generating corresponding public key
	pub_key = priv_key.public_key()
	
	#Serializing public key
	pemmy2 = pub_key.public_bytes(
	encoding = serialization.Encoding.PEM,
	format = serialization.PublicFormat.SubjectPublicKeyInfo
	)
	
	pemmy2.splitlines()[0]
	
	#Writing Public key to a pem file
	public_key = open(public_file, 'w')
	public_key.write(pemmy2)
	
	

def main(argv):
	asymm_keygen(public_key_file, private_key_file)
	
if __name__ == '__main__':
	main(argv[1:])