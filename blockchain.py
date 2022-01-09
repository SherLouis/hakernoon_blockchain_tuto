import hashlib
import json
from time import time
from models import Transaction, Block


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof: int, previous_hash: str = None) -> Block:
        """
        Create a new Block in the Blockchain
        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of the previous Block
        :return: New Block
        """
        block = Block(index=len(self.chain) + 1,
                      timestamp=time(),
                      transactions=self.current_transactions,
                      proof=proof,
                      previous_hash=previous_hash or self.hash(self.chain[-1]))
        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, transaction: Transaction) -> int:
        # """
        # Creates a new transaction to go into the next mined Block
        # :param sender: Address of the Sender
        # :param recipient: Address of the Recipient
        # :param amount: Amount
        # :return: The index of the Block that will hold this transaction
        # """
        self.current_transactions.append(transaction)
        return self.last_block.index + 1

    def proof_of_work(self, last_proof: int) -> int:
        """
        Simple Proof of Work Algorithm:
        - find a numper p' such that hash(pp') contains leading 4 zeros, where p is the previous p'
        - p is the previous proof, and p' is the new proof
        :param last_proof: last proof
        :return:
        """
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof: int, proof: int) -> bool:
        """
        Validates the Proof: Does hash(last_proof, proof) contains 4 leading zeros?
        :param last_proof: Previous Proof
        :param proof: Current Proof
        :return: If the current proof is valid or not
        """
        return hashlib.sha256(f'{last_proof}{proof}'.encode()).hexdigest().startswith('0000')

    @staticmethod
    def hash(block: Block) -> str:
        """
        Creates a SHA-256 hash of a Block
        :param block: Block
        :return: hash
        """
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block.json(), sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]
