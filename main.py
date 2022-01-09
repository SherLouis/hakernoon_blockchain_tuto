from fastapi import FastAPI, HTTPException, status
import uvicorn
from uuid import uuid4
from models import Transaction
from typing import List

from blockchain import Blockchain

app = FastAPI()

node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()


@app.get('/mine', tags=['Blockchain'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block.proof
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof
    # The sender is "0" to signify that this node has mined a new coin
    reward_transaction = Transaction(sender='0', recipient=node_identifier, amount=1)
    blockchain.new_transaction(reward_transaction)

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = block.dict()
    response['message'] = 'New Block forged'
    return response


@app.post('/transactions/new', status_code=status.HTTP_201_CREATED, tags=['Blockchain'])
def new_transaction(transaction: Transaction):
    # Check that the required fields are in the data
    # required = ['sender', 'recipient', 'amount']
    # if not all(k in values for k in required):
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Missing values')

    # Create a new Transaction
    index = blockchain.new_transaction(transaction)

    response = {'message': f'Transaction will be added to Block {index}'}
    return response


@app.get('/chain', tags=['Blockchain'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return response


@app.post('/nodes/register', status_code=status.HTTP_201_CREATED, tags=['Nodes'])
def register_nodes(nodes: List[str]):
    for node in nodes:
        blockchain.register_node(node)
    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes)
    }
    return response


@app.get('/nodes/resolve', tags=['Nodes'])
def consensus():
    replaced = blockchain.resolve_conflicts()
    if replaced:
        message = 'Our chain was replaced'
    else:
        message = 'Our chain is authoritative'
    response = {'message': message, 'chain': blockchain.chain}
    return response


if __name__ == '__main__':
    uvicorn.run('main:app', port=5000)
