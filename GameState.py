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
from Game_and_Player import *

class GameState:
    def __init__(self, game):
        
        self.game = game
        self.current_player_index = game.current_player_index  
        self.players = game.players
        self.hands = {}  
        for player in game.players:
            self.hands[player.name]=list(player.hand)
            
        self.table_cards = game.cards_on_table  
        
        self.tricks_won = {player.name: player.tricks_won for player in game.players}
        self.trump_suit = game.trump_suit
        self.table_color = game.table_color

    def apply_move(self, card):
        
        new_hands = {p: h[:] for p, h in self.hands.items()}  
       
        for c in new_hands[self.players[self.current_player_index].name]:
            if c == card: 
                new_hands[self.players[self.current_player_index].name].remove(c)
                break

        # self.game.players[self.current_player_index].hand.remove(card)
        for c in self.game.players[self.current_player_index].hand:
            if c == card:  # Compare by value, not reference
                self.game.players[self.current_player_index].hand.remove(c)
                break

        # print(f" hand of current player after removal {self.hands[self.players[self.current_player_index].name]}")
        # print(f" hand of current player after removal {self.game.players[self.current_player_index].hand}")

        # self.hands = new_hands

        new_table_cards = self.table_cards[:] + [[self.current_player_index, card]]
        self.game.cards_on_table = new_table_cards

        if len(new_table_cards) == 1:
            self.table_color = card.suit  
            new_table_color=card.suit
            self.game.table_color = new_table_color
        else:
            new_table_color=self.table_color
            self.game.table_color = new_table_color

        if len(new_table_cards) == 3:
            _,winner = self.get_winner(new_table_cards)

            next_turn = winner  
            for player in self.players:
              if player.index == winner:
                self.tricks_won[player.name] += 1
                player.tricks_won += 1
            new_table_cards = []  
            new_table_color = None
            self.game.cards_on_table = new_table_cards
            self.game.table_color = new_table_color
        else:
            next_turn = (self.current_player_index + 1) % len(self.hands)  

        self.game.current_player_index = next_turn

        self.current_player_index = next_turn
        self.hands = new_hands
        self.table_cards = new_table_cards
        self.table_color = new_table_color
        return self



    # def is_terminal(self):
    #     return all(len(hand) == 0 for hand in self.hands.values())

    def is_terminal(self):
        if all(len(hand) == 0 for hand in self.hands.values()):
            return True

        if len(self.players[self.current_player_index].hand) == 0:
            return True

        return False

    def get_winner(self,new_table_cards):
        lead_suit = self.table_color  
        trump_suit = self.trump_suit

        
        winning_card = max(new_table_cards, key=lambda card:
                          (card[1].suit == trump_suit, card[1].suit == lead_suit, card[1].value))

        winning_player_index = winning_card[0]
        return winning_card, winning_player_index

    def get_legal_moves(self):
        lead_suit = self.table_color  
        trump_suit = self.trump_suit  
        player = self.players[self.current_player_index]

        if lead_suit is None:
            legal_moves = list(player.hand)

        elif lead_suit!=trump_suit:
            lead_suit_cards = [card for card in player.hand if card.suit == lead_suit]
            has_lead_suit = len(lead_suit_cards) > 0

            if has_lead_suit:
                legal_moves = lead_suit_cards


            else:
                trump_cards = [card for card in player.hand if card.suit == trump_suit]

                if trump_cards:
                    trumps_in_play = [card[1].value for card in self.table_cards if card[1].suit == trump_suit]

                    if trumps_in_play:
                        max_trump = np.max(trumps_in_play)
                        higher_trumps = [card for card in trump_cards if card.value > max_trump]

                        if higher_trumps:
                            legal_moves = higher_trumps 
                        else:
                            legal_moves = list(player.hand)  

                    else:
                        legal_moves = trump_cards 

                else:
                    
                    legal_moves = list(player.hand)

        else:
            trump_cards = [card for card in player.hand if card.suit == trump_suit]
            if trump_cards:
                trumps_in_play = [card[1].value for card in self.table_cards if card[1].suit == trump_suit]
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
                return player.hand

        return legal_moves
        # return self.players[self.current_player_index].legal_moves(game)
    
    def redistribute(self):

        redistributed_state = copy.deepcopy(self)  

        current_player = redistributed_state.players[redistributed_state.current_player_index]
        known_cards = self.hands[current_player.name]  
        played_cards = self.table_cards 
        played_cards = [card[1] for card in played_cards]
        full_deck = Deck()
        all_cards = full_deck.cards  
            
        unknown_cards = [card for card in all_cards if card not in known_cards and card not in played_cards]

        random.shuffle(unknown_cards)

        for player in redistributed_state.players:
            if player != current_player:
                num_cards = len(redistributed_state.hands[player.name])
                redistributed_state.hands[player.name] = unknown_cards[:num_cards]
                # unknown_cards = unknown_cards[num_cards:] 
                del unknown_cards[:num_cards]

        return redistributed_state

   

        

    


