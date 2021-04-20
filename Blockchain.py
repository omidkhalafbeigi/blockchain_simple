import json
from hashlib import sha256
from flask import Flask, jsonify, make_response

class BlockChain:
    def __init__(self, number_of_zeros):
        self.chain = list()
        self.number_of_zeros = number_of_zeros
        block = {'index': 1,
                 'message': 'Block Genesis mined!',
                 'nonce': 1,
                 }
        self.create_block(previous_hash = '0', current_hash = sha256((json.dumps(block) + str(0)).encode()).hexdigest(), nonce = 1)

    def create_block(self, current_hash, previous_hash, nonce):
        chain_length = len(self.chain) + 1
        block = {'index': chain_length,
                 'message': f'Block {chain_length} mined!',
                 'nonce': nonce,
                 'current_hash': current_hash,
                 'previous_hash': previous_hash,
                 }
        self.chain.append(block)

    def chain_correction(self):
        chain_length = len(self.chain)

        for block_index in range(chain_length):
            if block_index < chain_length - 1:
                if self.chain[block_index]['current_hash'] != self.chain[block_index + 1]['previous_hash']:
                    self.chain[block_index + 1]['previous_hash'] = self.chain[block_index]['current_hash']
                else: continue
            else: continue


    def mine_block(self):
        nonce = 1
        last_block = self.get_last_block()
        new_block_hash = 'New Block'
        while new_block_hash.startswith('0' * self.number_of_zeros) is False:
            nonce += 1
            new_block = json.dumps(last_block) + str(nonce)
            new_block_hash = sha256(new_block.encode()).hexdigest()

        self.create_block(previous_hash = last_block['current_hash'], current_hash=new_block_hash, nonce = nonce)


    def get_last_block(self):
        return self.chain[-1]

    def get_blockchain(self):
        return self.chain


api = Flask('Blockchain API')
blockchain = BlockChain(number_of_zeros=5)

@api.route('/', methods=['GET'])
def home():
    blockchain.chain_correction()
    return jsonify(blockchain.get_blockchain())

@api.route('/mine', methods=['GET'])
def mine():
    blockchain.chain_correction()
    blockchain.mine_block()
    return jsonify(blockchain.get_blockchain())

api.run()
