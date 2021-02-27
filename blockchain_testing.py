# import base64
# import ecdsa

# # to_string() gives in bytes format, then hex() coverts it in hex code in string format.
# private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
# readable_private_key = private_key.to_string().hex()
# print(readable_private_key) #readable private key
# public_key = private_key.get_verifying_key()
# print(public_key.to_string().hex())
# print(base64.b64encode(public_key.to_string())) #encodes bytes format to ascii string format but still in bytes format.
# readable_public_key = base64.b64encode(public_key.to_string()).decode() #actual ascii string. 
# print(readable_public_key) # PUBLIC KEY readable

# #using private_key object we can sign on bytes object which gives sign in bytes format and using public key we can verify it.
# msg = b'hello'
# signature = private_key.sign(msg)
# print(public_key.verify(signature, msg)) #tells is the msg signed with private key associated with this public key.

# # recreating private and public key objects from readable formats
# recreated_private_key = ecdsa.SigningKey.from_string(bytes.fromhex(readable_private_key), curve=ecdsa.SECP256k1)
# print(recreated_private_key) 
# print(recreated_private_key.get_verifying_key())


from flask import Flask, request, jsonify
import requests
from main import Block, Blockchain
import json

'''
    - jsonify gives neat looking json format.

'''

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# b = Block(0, 0, 'got 7$', '4e370ce41af3ed217c1e6fd778', '0')
b = Blockchain()
b.genesis_block()
# b.unconfirmed_transactions = ['elon paid me 7 bitcoin', 'george paid me 3 ETH']
# b.mine()
b.unconfirmed_transactions = ['elon paid me 100 bitcoins', 'george paid me 10 ETH']
# b.mine()

@app.route('/block', methods=['GET'])
def get_block():
    blocks = []
    for each_block in b.chain:
        blocks.append(each_block.__dict__)
    return jsonify(blocks)

@app.route('/mine', methods=['GET', 'POST'])
def mining():
    mined_block = b.mine()
    print(request.host_url) #gives host url, can be then added to peers set.
    return jsonify({
        'index': mined_block.index,
        'timestamp': mined_block.timestamp,
        'transactions': mined_block.transactions, 
        'prev_hash': mined_block.prev_hash,
        'proof_of_work': mined_block.proof_of_work,
        'hash': mined_block.hash
        })

app.run(debug=True, port=5000)

# TODO: so during mining, we will add host_url to peers set, if it already exists it doesn't gonna matter.