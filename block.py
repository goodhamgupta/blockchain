import hashlib
from datetime import datetime


class Block(object):
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hashlib.sha512()
        hash_string = "{}{}{}{}".format(
            str(self.index),
            str(self.timestamp),
            str(self.data),
            str(self.previous_hash)
        )
        sha.update(hash_string)
        return sha.hexdigest()


def create_genesis_block():
    """
    Function to create the genesis(first) block of the chain.
    """
    return Block(0, datetime.now(), "first", "0")


def next_block(last_block, data):
    """
    Function to generate the consecutive blocks in the blockchain.
    """
    index = last_block.index + 1
    timestamp = datetime.now()
    return Block(index, timestamp, data, last_block.hash)


if __name__ == "__main__":
    block = create_genesis_block()
    blockchain = [block]
    for i in range(0, 20):
        new_block = next_block(block, "testfest")
        blockchain.append(new_block)
        block = new_block
        print("Block #{} added!".format(new_block.index))
        print("Hash: {}\n".format(new_block.hash))
