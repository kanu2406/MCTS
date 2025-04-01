import math
import random
from collections import defaultdict
from typing import List
import numpy as np
import matplotlib.pyplot as plt
import random
from collections import deque
import copy
from Card_and_Deck import *

class Player:
    def __init__(self, name, role,index):
        self.name = name
        self.hand = deque()
        self.tricks_won = 0
        self.role = role  # "Teen" (3 tricks), "Do" (2 tricks), "Paanch" (5 tricks)
        self.index = index
        # self.lead_player_index = 0
        # self.current_player_index = self.lead_player_index


    def choose_trump(self):
        """Deciding on the trump suit based on the most frequent suit in hand."""
        suit_counts = {suit: 0 for suit in Card.suits}
        suit_ranks = {suit: [] for suit in Card.suits}

        for card in self.hand:
            suit_counts[card.suit] += 1
            suit_ranks[card.suit].append(card.value)

        
        max_suits = [suit for suit, count in suit_counts.items() if count == max(suit_counts.values())]

        # If there's a tie, choose the suit with the highest-ranked cards
        if len(max_suits) > 1:
            max_rank_sum = max(sum(suit_ranks[suit]) for suit in max_suits)  
            best_suits = [suit for suit in max_suits if max(suit_ranks[suit]) == max_rank_sum]  
            trump_suit = random.choice(best_suits)  # Randomly choose one if multiple suits qualify
        else:
            trump_suit = max_suits[0]  # If only one suit remains, choose it

        return trump_suit


    def legal_moves(self, game):

        lead_suit = game.table_color  # Suit of the first card played in the trick
        trump_suit = game.trump_suit  

        if lead_suit is None:
            legal_moves = list(self.hand)

        elif lead_suit!=trump_suit:
            lead_suit_cards = [card for card in self.hand if card.suit == lead_suit]
            has_lead_suit = len(lead_suit_cards) > 0

            if has_lead_suit:
                legal_moves = lead_suit_cards


            else:
                trump_cards = [card for card in self.hand if card.suit == trump_suit]

                if trump_cards:
                    trumps_in_play = [card[0].value for card in game.cards_on_table if card[0].suit == trump_suit]

                    if trumps_in_play:
                        max_trump = np.max(trumps_in_play)
                        higher_trumps = [card for card in trump_cards if card.value > max_trump]

                        if higher_trumps:
                            legal_moves = higher_trumps  # Overtrump if possible
                        else:
                            legal_moves = list(self.hand)  # Play any trump if no higher trump is available

                    else:
                        legal_moves = trump_cards  # Play any trump if no trump is on the table

                else:
                    # if no lead suit or trump cards then play any card
                    legal_moves = list(self.hand)

        else:
            trump_cards = [card for card in self.hand if card.suit == trump_suit]
            if trump_cards:
                trumps_in_play = [card.value for card in game.cards_on_table if card.suit == trump_suit]
                if trumps_in_play:
                    max_trump = np.max(trumps_in_play)
                    higher_trumps = [card for card in trump_cards if card.value > max_trump]
                    if higher_trumps:
                        return higher_trumps
                    else:
                        return trump_cards
                else:
                    return trump_cards
            else:
                return self.hand

        return legal_moves




class Game:
    def __init__(self, player_names, roles,indices):
        """Initializing the game with players, deck, and game state."""
        self.players = [Player(name, role,index) for name, role,index in zip(player_names, roles,indices)]
        self.deck = Deck()
        self.cards_on_table = []
        self.played_cards = set()
        self.trump_suit = None
        self.table_color = None
        # self.lead_player_index = 0 
        self.current_player_index = 2
        random_card = random.choice(self.deck.cards)  # Pick a random card from the deck
        self.trump_suit = random_card.suit
        hands = self.deck.deal(len(self.players), 10)
        for player, hand in zip(self.players, hands):
            player.hand = hand





        # # Distribute first 5 cards to all players
        # hands = self.deck.deal(len(self.players), 5)
        # for player, hand in zip(self.players, hands):
        #     player.hand = hand

        # # 'Paanch' player chooses the trump suit
        # for player in self.players:
        #     if player.role == "Paanch":
        #         self.trump_suit = player.choose_trump()

        # # Distribute remaining cards after choosing trump
        # hands = self.deck.deal(len(self.players), 5)  # Assuming 10 cards in total per player
        # for player, hand in zip(self.players, hands):
        #     player.hand.extend(hand)

        # Initialize remaining cards (all deck minus played ones)
        self.remaining_cards = set(self.deck.cards) - set(card for player in self.players for card in player.hand)