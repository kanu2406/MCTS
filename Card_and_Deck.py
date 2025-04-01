import math
import random
from collections import defaultdict
from typing import List
import numpy as np
import matplotlib.pyplot as plt
import random
from collections import deque
import copy


class Card:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = [ '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = self.ranks.index(rank)  # Lower index means lower value

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        """Creating a deck with special rule: Only rank 7 is included for Hearts and Spades."""
        self.cards = [Card(suit, rank) for suit in Card.suits for rank in Card.ranks]
        self.cards = [card for card in self.cards if not (card.suit in ['Clubs', 'Diamonds'] and card.rank == '7')]
        random.shuffle(self.cards)

    # def deal(self, num_players, cards_per_player):
    #     """Distributes cards to players."""
    #     return [deque(self.cards[i * cards_per_player:(i + 1) * cards_per_player]) for i in range(num_players)]
    def deal(self, num_players, cards_per_player):
        """Distributes cards to players, removing them from the deck."""
        hands = [deque(self.cards[i * cards_per_player:(i + 1) * cards_per_player]) for i in range(num_players)]
        self.cards = self.cards[num_players * cards_per_player:]  # Remove dealt cards from the deck
        return hands


