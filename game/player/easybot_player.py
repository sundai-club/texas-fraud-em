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
        
        options = {1: self.checkBet,
                   2: self.callBet, 
                   3: self.raiseBet,
                   4: self.foldBet,
                   5: self.allin}
        
        

        # Get game state variables with defaults
        pot_size = game_state.get('pot_size', 0)
        table_cards = game_state.get('table_cards', [])
        active_players = game_state.get('active_players', 1)
        position = game_state.get('position', 0)  # 0 is early, 1 is late
        round = game_state.get('round', 'preflop')

        while True:
            # Calculate pot odds and hand strength
            pot_odds = self.debt / (pot_size + self.debt) if self.debt > 0 else 0
            hand_strength = self._evaluate_hand(table_cards)

            # All-in or fold situation
            if self.bet == -1:
                if hand_strength > 0.7 or (self.money / pot_size < 0.2):
                    action = 5  # all-in
                else:
                    action = 4  # fold
            
            # Normal betting situation    
            else:
                if pot_odds > hand_strength:
                    action = 4  # fold
                elif self.debt == 0:
                    if hand_strength > 0.8:
                        action = 3  # raise
                    else:
                        action = 1  # check
                else:
                    if hand_strength > 0.6:
                        action = 2  # call
                    else:
                        action = 4  # fold

            chosen = options[action]()
            if chosen:
                return chosen
            continue

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

