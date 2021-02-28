from flask import Flask, request, jsonify
import requests
from blockchain_stuff import Block, Blockchain
import json

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

peers = set() #will store urls of all other miners on the network.
# peers.add('http://127.0.0.1:5000')
# peers.add('http://127.0.0.1:5001')
blockchain = Blockchain()
blockchain.genesis_block()
blockchain.unconfirmed_transactions = ['elon paid me 100 bitcoins', 'george paid me 10 ETH']


@app.route('/chain', methods=['GET'])
def display_chain():
	blocks = []
	for each_block in blockchain.chain:
		blocks.append({
		'index': each_block.index,
		'timestamp': each_block.timestamp,
		'transactions': each_block.transactions, 
		'prev_hash': each_block.prev_hash,
		'proof_of_work': each_block.proof_of_work,
		'hash': each_block.hash
		})
	return jsonify(blocks)

@app.route('/mine', methods=['GET'])
def mining():
	mined_block = blockchain.mine()
	if mined_block:
		blockchain.announce_block(peers, mined_block)
		return jsonify({
			'index': mined_block.index,
			'timestamp': mined_block.timestamp,
			'transactions': mined_block.transactions, 
			'prev_hash': mined_block.prev_hash,
			'proof_of_work': mined_block.proof_of_work,
			'hash': mined_block.hash
			})
	else:
		return "Nothing to mine!!"

@app.route('/register', methods= ['GET'])
def register_node():
	host = request.host_url
	if host in peers:
		return "You are already registered as node!"
	else:
		peers.add(host)
		return "Done! You are registered."

# to check if larger chain exits on network and if yes then switch to it.
@app.route('/consensus', methods= ['GET'])
def chain_conflict():
	if blockchain.consensus(peers):
		return "Conflict detected, Switched to longest valid chain on the network!"
	else:
		return "We are good, no conflict in blockchain!"

@app.route('/add_block', methods=['POST'])
def add_block():
	block_data = request.get_json()
	block = Block(block_data['index'], block_data['timestamp'], block_data['transactions'], block_data['prev_hash'], block_data['proof_of_work'])
	blockchain.add_block(block)


app.run(debug=True)