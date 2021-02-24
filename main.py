from hashlib import sha256
from datetime import datetime

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
		# TODO: passing whole list of transactions and not the individual transactions.
		g_block = Block(0, datetime.now(), [], 0, 0)
		self.chain.append(g_block)

	@property 
	def last_block(self):
		return self.chain[-1]
	
	# the block should have valid prev_hash and valid proof_of_work to be added in blockchain.
	def add_block(self, block):
		if self.last_block.hash == block.prev_hash:
			if self.is_valid_proof(block):
				self.chain.append(block)
				return True
		return False

	# checking if block hash(calculated with proof_of_work) starts with given no. of zeros_difficulty
	def is_valid_proof(self, block):
		if block.hash.startswith('0' * self.zeros_difficulty):
			return True

	def mine(self):
		'''this adds all unconfirmed transactions into a block and
			finds valid proof_of_work for that block in order to 
			add it to blockchain'''
		if not self.unconfirmed_transactions:
			return False
		print(self.unconfirmed_transactions)
		new_block = Block(index= self.last_block.index + 1, timestamp= datetime.now(), 
					transactions= self.unconfirmed_transactions, prev_hash= self.last_block.hash)

		#Calulates proof_of_work
		while not new_block.hash.startswith('0' * self.zeros_difficulty):
			new_block.proof_of_work += 1
		print(new_block.__dict__)
		self.add_block(new_block)
		self.unconfirmed_transactions = [] 
		return True

# b = Blockchain()
# b.genesis_block()
# print(b.chain[0].hash)
# b.unconfirmed_transactions = ['elon paid me 7 bitcoin', 'george paid me 3 ETH']
# b.mine()
# print(b.chain[-1].hash)
