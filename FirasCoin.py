"""
@author: Firas Belhiba
"""
#Importing the libraries 
import datetime
import hashlib
import json
from flask import Flask , jsonify , request
import requests 
from uuid import uuid4
from urllib.parse import urlparse


#Building our Blockchain 
class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof = 1, previous_hash = '0')
                    
    def create_block(self , proof , previous_hash):
        block = {'index' : len(self.chain) + 1 ,
                 'timestamp' : str(datetime.datetime.now()),
                 'proof' : proof,
                 'previous_hash' : previous_hash,
                 'transactions':self.transactions}
        self.transactions = []
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
      new_proof = 1
      check_proof = False
      while check_proof is False:
          hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
          if hash_operation[:4] == '0000':
              check_proof = True
          else:
              new_proof += 1
      return new_proof
    
    def hash(self,block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
        
    def is_chain_valid(self,chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode().hexdigest())
            if hash_operation[:4] != '0000':
                return False 
            previous_block = block
            block_index += 1
        return True
    
    def add_transaction(self,sender,receiver,amount):
        self.transactions.append({'sender': sender ,
                                  'receiver':receiver,
                                  'amount':amount})
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
        
    
    
# Creating a web app 
app = Flask(__name__)

# Creating Blockchain
blockchain = Blockchain()

# Mining a new block
@app.route('/mine_block' , methods=['GET'])

def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message' : 'Congratualtion , you just added your block to the blockchain' ,
                'index' : block['index'],
                'timestamp':block['timestamp'],
                'proof':block['proof'],
                'previous_hash':block['previous_hash']}
    return jsonify(response), 200

# Getting the bull blockchain 
@app.route('/get_blockchain' , methods=['GET'])

def get_blockchain():
    response = {'chain' : blockchain.chain ,
                'length' : len(blockchain.chain)}
    return jsonify(response), 200

# Checking if the blockchain is valid 
@app.route('/check_blockchain_isvalid' , methods=['GET'])

def check_blockchain():
    chain = blockchain.chain
    Check_blockchain_status = blockchain.is_chain_valid(chain)
    if Check_blockchain_status == False :
        return jsonify({'message' : 'The blockchain is invalid '})
    else :
        return jsonify({'message' : 'The blockchain is vlaid '}) 
    
# Decentralizing the blockchain

        

# Running the app
app.run(host = '0.0.0.0',port = 5000)
 

             
    
