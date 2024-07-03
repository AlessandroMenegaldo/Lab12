from dataclasses import dataclass

from model.retailer import Retailer


@dataclass
class Connessione:
    Retailer_1 : Retailer
    Retailer_2 : Retailer
    score: int

