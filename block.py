import hashlib


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
            str(self.index,
                self.timestamp,
                self.data,
                self.previous_hash)
        )
