from flask import Flask, request, jsonify, redirect, url_for, render_template
import requests
from blockchain_stuff import Block, Blockchain
import json
from config_peers import peers
from datetime import datetime

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

blockchain = Blockchain()
blockchain.genesis_block()
blockchain.unconfirmed_transactions = ['elon paid me 100 bitcoins', 'george paid me 10 ETH']

@app.route('/', methods= ['GET', 'POST'])
def make_transaction():
	if request.method == 'POST':
		return url_for('make_transaction')
	else:
		return render_template('make_transaction.html')


@app.route('/chain', methods=['GET'])
def display_chain():
	blocks = []
	for each_block in blockchain.chain:
		blocks.append(each_block.__dict__)
	return jsonify({
		'blockchain': blocks,
		'chain_length': len(blockchain.chain)
		})

@app.route('/mine', methods=['GET'])
def mining():
	mined_block = blockchain.mine()
	if mined_block:
		print(mined_block)
		# blockchain.announce_block(peers, mined_block)
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
	# here verify is block_data['transaction'] is same as unconfirmed transactions.
	block = Block(block_data['index'], block_data['timestamp'], block_data['transactions'], block_data['prev_hash'], block_data['proof_of_work'])
	added = blockchain.add_block(block)
	if not added:
		return "The block was discarded by the node", 400

	return "Block added to the chain", 201

@app.route('/make_transaction', methods= ['POST'])
def make_transaction():
	readable_pk = request.form.get('pk')
	to_addr = request.form.get('to_addr')
	amount = request.form.get('amount')
	readable_sk = request.form.get('sk')
	timestamp = str(datetime.now())
	msg = {'timestamp': timestamp, 'from_addr': readable_pk, 'to_addr': to_addr, 'amount': amount}
	signature = self.generate_signature(readable_sk, msg)
	signature = signature.hex() #converting bytes type to hex string, so it will be accepted by json.
	self.announce_transaction(peers, {'message': msg, 'signature': signature})
	# print(pk, to_addr, amount, sk)
	return "Transaction has been made!"

# to add in unconfirmed_transactions list of all peers.
@app.route('/add_transaction', methods= ['POST'])
def add_transaction():
	transaction_dict = request.get_json()
	print(transaction_dict)
	self.unconfirmed_transactions.append(transaction_dict)
	# now during mining transaction will be verified from signature.

@app.route('/peers', methods= ["GET"])
def display_peers():
	return jsonify({
		'peers': str(peers),
		'count': len(peers)
		})

app.run(debug=True)