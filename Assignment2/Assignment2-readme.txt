In this assignment, a system for secure email communication has been designed.
The way this is secure is that any kind of file that has to be sent via email - Text, Image or Video can be encrypted by the sender and then decrypted by the receiver.

Below is a description of the system and some of its salient features:

-> Both Symmetric and Asymmetric encryption has been used.
-> For symmetric encryption, AES-256 has been used in Cipher Block Chaining (CBC) mode. 256 bit key is used, since a lower key length will make an adversary’s job much easier in cracking.
-> Both, the symmetric key (256 bits) and Initialization vector (128 bits) are randomized using the Operating System’s Random Number Generator.
-> RSA has been used for key exchange. The key size used is 2048 bits, since lower key sizes can be broken.
-> RSA has also been used for signing. For signing, SHA-256 is used as the hashing algorithm because of greater resistance to collisions when compared to SHA1 or MD5.
-> A scheme similar to a digital envelope has been used to encrypt and sign data.

-> For Encryption:
	$ In case of sender, data (original message) is first encrypted with symmetric key.
	$ The symmetric key is encrypted with the destination’s public key.
	$ This encrypted key is appended to the cipher text along with other information such as initialization vector and padding variable.
	$ The resulting text is signed using the sender’s private key.

-> For Decryption:
	$ In case of receiver, the sender’s signed data is first verified to check for integrity. For this, the sender’s public key is used.
	$ Then, the symmetric key, initialization vector and padding variable is extracted from the text using the delimiters embedded in the text.
	$ The symmetric key is obtained from its encrypted form using the destination’s private key.
	$ The resulting cipher text is decrypted using the shared key to obtain the original message.


###########################################################################################################################################################################################


There are 3 python scripts attached with this assignment:

1. fcrypt.py (main script)
2. rsakeygenerator.py (To generatew RSA keys)
3. symencryption.py (For session communication once shared key for that session has been exchanged)


###########################################################################################################################################################################################


To run the scripts:

1. Use rsakeygenerator.py to generate the respective keys for the source and destination.
python rsakeygenerator.py public_key_file private_key_file 

2. Run fcrypt as follows:

To encrypt a file:
python fcrypt.py -e destination_public_key_file source_private_key_file input_plain_text_file cipher_text_file

To decrypt a file:
python fcrypt.py -d source_public_key_file destination_private_key_file output_plain_text_file(after decryption) cipher_text_file

3. (Optional) Once the shared key has been exchanged,it can be used to communicate for one session using the code below. Please note that 
no RSA is used since keys have already been exchanged for that session. This leads to more speedy communication since only symmetric encryption is used.
