from typing import Callable
import player.player 
from random import random,randint

class EasyBot(player.Player):

    """
    Easy to compete player
    Selects randomly between his options
    """

    def __init__(self):
       """TODO: to be defined1. """
       super().__init__()

    def raising(self, raising = None):
        """
        Function for getting random input
        :returns: TODO

        """
        print(self.money, self.debt)
        #return randint(1, self.money - self.debt) if self.money > self.debt else 0.0 
        return randint(1, 1 + int((self.money - self.debt)/3)) if self.money > self.debt else 0.0 

    def checkBet(self):
        """
        Checks only if difference between deposit and bet is zero
        
        :returns: True/False based on if you can check or not
        """
        if self.debt:
            return False
        else:
            print("{} check".format(self.name))
            return (self.bet,0)

    def options(self, game_state=None):
        """
        Gives all options to the player based on game state
        
        :param game_state: Dictionary containing game state information like:
                          - pot_size: Current pot size
                          - table_cards: Community cards
                          - active_players: Number of players still in hand
                          - position: Bot's position relative to dealer
                          - round: Current betting round (preflop, flop, etc)
        :returns: Tuple of (bet_amount, amount_added_to_pot)
        """

        print(game_state)

        if game_state is None:
            game_state = {}
        


        options = {'check': self.checkBet,
                   'call': self.callBet, 
                   'raise': self.raiseBet,
                   'fold': self.foldBet,
                   'allin': self.allin}
    
        action = self.select_action(options, game_state)
        chosen = options[action]()
        return chosen
    
    def select_action(self, 
                      options: dict[str, Callable], 
                      game_state: dict[str, dict | str]) -> str:
        baseline_action = random.choice(list(options.keys()))
        

        return baseline

    def _evaluate_hand(self, table_cards):
        """
        Simple hand strength evaluator
        Returns value between 0-1 representing hand strength
        """
        # Map card values to numeric values for comparison
        card_values = {
            'Jack': 11,
            'Queen': 12, 
            'King': 13,
            'Ace': 14
        }

        def get_card_value(card):
            if isinstance(card[0], str):
                return card_values[card[0]]
            return card[0]

        # Preflop evaluation based on hole cards
        if not table_cards:
            card1_value = get_card_value(self.hand[0])
            card2_value = get_card_value(self.hand[1])
            
            if self.hand[0][0] == self.hand[1][0]:  # Pair
                return 0.8
            elif max(card1_value, card2_value) >= 13:  # King or Ace
                return 0.7
            return 0.4
        
        return 0.5  # Placeholder - implement proper hand strength calculation

