from hashlib import sha256
from datetime import datetime
from ecdsa import SigningKey, SECP256k1, VerifyingKey
from base64 import b64encode 
import json
import requests
from flask import request

class Block:
	def __init__(self, index, timestamp, transactions, prev_hash, proof_of_work=0):
		self.index = index
		self.timestamp = timestamp
		self.transactions = transactions
		self.prev_hash = prev_hash
		self.proof_of_work = proof_of_work

	# gives hash of complete block along with the proof of work
	@property 
	def hash(self):
		block_string = str(self.index) + str(self.timestamp) + str(self.transactions) + str(self.prev_hash) + str(self.proof_of_work)
		return sha256(block_string.encode()).hexdigest()

# b = Block(0, 0, 'got 7$', '4e370ce41af3ed217c1e6fd778', '0')
# print(b.hash)

class Blockchain:
	def __init__(self):
		#starts with this no. of zeros for proof_of_work
		self.zeros_difficulty = 2 
		self.unconfirmed_transactions = []
		self.chain = []

	# genesis block is the first block in a blockchain, its prev_hash would be 0
	def genesis_block(self):
		g_block = Block(0, str(0), [], 0, 0)
		self.chain.append(g_block)

	@property 
	def last_block(self):
		if self.chain:
			return self.chain[-1]
		else:
			return False
	
	# the block should have valid prev_hash and valid proof_of_work to be added in blockchain.
	def add_block(self, block):
		if self.last_block and self.last_block.hash == block.prev_hash:
			if self.is_valid_proof(block):
				self.chain.append(block)
				return True
		return False

	def mine(self):
		'''this adds all unconfirmed transactions into a block and
			finds valid proof_of_work for that block in order to 
			add it to blockchain'''
		if not self.unconfirmed_transactions:
			return False
		else:
			for transaction in self.unconfirmed_transactions:
				if not self.is_valid_transaction(transaction): 
					self.unconfirmed_transactions.remove(transaction) # removing invalid transactions.

			new_block = Block(index= self.last_block.index + 1, timestamp= str(datetime.now()), 
						transactions= self.unconfirmed_transactions, prev_hash= self.last_block.hash)

			#Calulates proof_of_work
			while not new_block.hash.startswith('0' * self.zeros_difficulty):
				new_block.proof_of_work += 1

			self.add_block(new_block)
			self.unconfirmed_transactions = [] 
			return new_block
			return True

	def is_valid_transaction(self, transaction_dict):
		signature = transaction_dict['signature']
		signature = bytes.fromhex(signature) #converting hex string back to bytes to be able to verify.
		public_key = transaction_dict['message']['from_addr']
		public_key = VerifyingKey.from_string(bytes.fromhex(public_key), curve=SECP256k1) #getting public key in bytes from public key in hex string format.
		msg = json.dumps(transaction_dict['message']).encode() #converting msg back in bytes format.
		if public_key.verify(signature, msg):
			return True
		return False

	# checking if block hash(calculated with proof_of_work) starts with given no. of zeros_difficulty
	def is_valid_proof(self, block):
		if block.hash.startswith('0' * self.zeros_difficulty):
			return True

	def is_valid_chain(self):
		for i in range(1, len(self.chain)):
			if self.is_valid_proof(self.chain[i]):
				if self.chain[i].prev_hash == self.chain[i-1].hash:
					return True
		return False

	# creates Blockchain obj. based on list received.
	def create_temp_chain(self, blockchain_list):
		temp_blockchain = Blockchain()
		temp_blockchain.genesis_block()
		print('1', temp_blockchain.chain)
		print('2',blockchain_list)
		for block in blockchain_list[1:]: #because genesis block would be already there.
			temp_block = Block(block['index'], block['timestamp'], block['transactions'], block['prev_hash'], block['proof_of_work'])
			print('3', temp_block)
			temp_blockchain.add_block(temp_block)
		return temp_blockchain

	def consensus(self, peers):
		longest_chain = self.chain
		for peer in peers:
			if peer != request.host_url: #to check others chain, not current url's chain.
				response = requests.get(peer+'chain')
				chain = response.json()['blockchain']
				print(chain)
				temp_blockchain = self.create_temp_chain(chain)
				print('4',temp_blockchain.chain)
				if len(temp_blockchain.chain) > len(longest_chain) and temp_blockchain.is_valid_chain(): #finding longest chain
					longest_chain = temp_blockchain.chain
		
		if longest_chain != self.chain:  #means longest chain is not ours.
			self.chain = longest_chain
			return True

		return False

	def announce_block(self, peers, block_obj):
		for peer in peers:
			if peer != request.host_url:
				response = requests.post(peer+'add_block', json= block_obj.__dict__)

	def generate_signature(self, readable_sk, msg):
		# converting from readable format to SigningKey object.
		sk = SigningKey.from_string(bytes.fromhex(readable_sk), curve=SECP256k1)
		msg = json.dumps(msg).encode() #to convert dict to bytes like object
		return sk.sign(msg)

	def announce_transaction(self, peers, transaction_dict):
		for peer in peers:
			response = requests.post(peer+'add_transaction', json= transaction_dict)



# b = Blockchain()
# b.genesis_block()
# b.unconfirmed_transactions = ['elon paid me 7 bitcoin', 'george paid me 3 ETH']
# b.mine()
# b.unconfirmed_transactions = ['elon paid me 100 bitcoins', 'george paid me 10 ETH']
# b.mine()
# b.unconfirmed_transactions = ['elon paid me 100 bitcoins', 'george paid me 10 ETH', 'joe paid me 100 $', 'leo paid me 20 ETH' ]
# b.mine()
# print(b.chain[-1].hash)
# print(b.is_valid_chain()) 

class Transaction:
	def __init__(self, transaction_timestamp, from_addr, to_addr, amount):
		self.transaction_timestamp = transaction_timestamp
		self.from_addr = from_addr
		self.to_addr = to_addr
		self.amount = amount

	# to return transaction attributes in dict format.
# 	def return_transaction(self):
# 		return self.__dict__

# t = Transaction('sdf', 0, 1, 2)
# print(t.return_transaction())


def generate_wallet():
	'''
	- private/secret/signing key(sk) will be used to generate signature which can be verified with 
	the public key(pk) associated with that private key only.
	- to_string() will give bytes format then hex() will give hexcode in string format.
	'''
	sk = SigningKey.generate(curve= SECP256k1) #gives SigningKey object
	readable_sk = sk.to_string().hex() 
	pk = sk.get_verifying_key() #public key corresponding to private key
	readable_pk = pk.to_string().hex()
	
	# saving in file
	with open('wallet.txt', 'w') as file:
		file.write("Private Key/Signing Key: {}\nPublic Key/Wallet Address: {}".format(readable_sk, readable_pk))
	print("Your credentials saved in 'wallet.txt' file!")


def generate_signature(sk, msg):
	signature = sk.sign(msg)
	return signature

def is_valid_signature(pk, signature, msg):
	return pk.verify(signature, msg)

'''TODO: double mining by both nodes, add documentation, jsonify doesn't work, 
specifically validate for genesis block in is_valid_chain, no. of transactions in block class'''
# set FLASK_APP=main.py
# flask run --port 5000 --debugger --reload


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