from pydantic import BaseModel
from typing import List


class Transaction(BaseModel):
    sender: str
    recipient: str
    amount: int


class Block(BaseModel):
    index: int
    previous_hash: str
    proof: int
    timestamp: float
    transactions: List[Transaction] = []

