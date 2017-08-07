from flask import Flask
from flask import request
from block import *
node = Flask(__name__)

current_node_transactions = []


@node.route('/txion', methods=['POST',])
def transaction():
    new_transaction = request.get_json()
    current_node_transactions.append(new_transaction)
    print("New transaction")
    print("FROM: {}".format(new_transaction.get('from')))
    print("TO: {}".format(new_transaction.get('to')))
    print("AMOUNT: {}\n".format(new_transaction.get('amount')))

node.run()


miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"

def proof_of_work(last_proof):
    """
    Function to implement PoW algorithm
    """
    incrementor = last_proof + 1
    while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
        incrementor += 1

    return incrementor

@node.route('/mine', methods=['GET',])
def mine():
    last_block = blockchain[-1]
    last_proof = last_block.data['proof_of_work']
    proof = proof_of_work(last_proof)
    current_node_transactions.append(
        { "from": "network", "to": miner_address, "amount": 1 }
    )

    new_block_data = {
        "proof_of_work": proof,
        "transactions": list(current_node_transactions)
    }

    new_block_index = last_block.index + 1
    new_block_timestamp = datetime.now()
    last_hash = last_block.hash
    mined_block = Block(new_block_index, new_block_timestamp, new_block_data, last_hash)
    blockchain.append(mined_block)

    return json.dumps(
        {
            "index": new_block_index,
            "timestamp": new_block_timestamp,
            "data": new_block_data,
            "hash": new_block_hash
        })

@node.route('/blocks', methods=['GET',])
def get_blocks():
    """
    Function to implement the consensus algorithm
    """
    chain_to_send = blockchain
    blocklist = ""
    for i in range(len(chain_to_send)):
        block = chain_to_send[i]
        block_index = str(block.index)
        block_timestamp = str(block.timestamp)
        block_data = str(block.data)
        block_hash = block.hash
        assembled = json.dumps({
            "index": block_index,
            "timestamp": block_timestamp,
            "data": block_data,
            "hash": block_hash
        })
    if blocklist == "":
        blocklist = assembled
    else:
        blocklist += assembled
    return blocklist

    chain_to_send = json.dumps(chain_to_send)
    return chain_to_send


def find_new_chains():
    other_chains = find_new_chains()
    longest_chain = blockchain
    for chain in other_chains:
        if len(chain) > len(longest_chain):
            longest_chain = chain

    # If longest chain isn't our we reset our chain to the longest one
    blockchain = longest_chain

node.run()
