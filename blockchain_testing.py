import base64
import ecdsa

# to_string() gives in bytes format, then hex() coverts it in hex code in string format.
private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
readable_private_key = private_key.to_string().hex()
print(readable_private_key) #readable private key
public_key = private_key.get_verifying_key()
print(public_key.to_string().hex())
print(base64.b64encode(public_key.to_string())) #encodes bytes format to ascii string format but still in bytes format.
readable_public_key = base64.b64encode(public_key.to_string()).decode() #actual ascii string. 
print(readable_public_key) # PUBLIC KEY readable

#using private_key object we can sign on bytes object which gives sign in bytes format and using public key we can verify it.
msg = b'hello'
signature = private_key.sign(msg)
print(public_key.verify(signature, msg)) #tells is the msg signed with private key associated with this public key.

# recreating private and public key objects from readable formats
recreated_private_key = ecdsa.SigningKey.from_string(bytes.fromhex(readable_private_key), curve=ecdsa.SECP256k1)
print(recreated_private_key) 
print(recreated_private_key.get_verifying_key())
