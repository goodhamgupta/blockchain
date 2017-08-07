from flask import Flask
from flask import request

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

    new_block = {
        "proof_of_work": proof,
        "transactions": list(current_node_transactions)
    }

    new_block_index = last_block.index + 1
    new_block_timestamp = datetime.now()

