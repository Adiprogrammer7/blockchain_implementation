from ecdsa import SigningKey, SECP256k1

def generate_wallet():
	'''- private/secret/signing key(sk) will be used to generate signature which can be verified with 
	the public key(pk) associated with that private key only.
	- to_string() will give bytes format then hex() will give hexcode in string format.'''
	
	sk = SigningKey.generate(curve= SECP256k1) #gives SigningKey object
	readable_sk = sk.to_string().hex() 
	pk = sk.get_verifying_key() #public key corresponding to private key
	readable_pk = pk.to_string().hex()
	
	print('Private Key: {} \nPublic Key: {}'.format(readable_sk, readable_pk))

	# saving in file
	with open('wallet.txt', 'w') as file:
		file.write("Private Key/Signing Key: {}\nPublic Key/Wallet Address: {}".format(readable_sk, readable_pk))
	print("Your credentials saved in 'wallet.txt' file!")

generate_wallet()