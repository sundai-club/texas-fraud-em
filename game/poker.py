"""
File: poker.py
Author: dave
Github: https://github.com/davidus27
Description: Game is the main Object implementing all the necessary tools for playing. Game is created in function main()
"""
import ui
import dealer
from player import Player
from ui.cli.terminal import Terminal
from ui.cli.terminal_manager import TerminalManager, TerminalWindow
import curses
import sys
import subprocess


class Game(object):
    """
    Creates players based on inputs on call.
    """
    def __init__(self):
        self.rounds = 1
        self.players = []
        self.dealer = dealer.Dealer()
        self.screen = None
        self.terminal_manager = TerminalManager()
        self.game_display = TerminalWindow("Game Display")  # Add game display window

    def createPlayers(self):
        name = ui.nameQuest()
        numPlayers = ui.numQuest()
        money = 500
        difficulty = ui.diffQuest()

        return self.dealer.playerControl.createPlayers(name,numPlayers, money, difficulty)

    def controlDeposit(self):
        """
        checks if there are any differences
        :returns: TODO

        """
        deposit = self.players[0].deposit #reference
        for player in self.players[1:]:
            if player.deposit == deposit:
                continue
            else:
                return False
        return True

    def round(self):
        """
        Goes through all players until every player gave same ammount to the pot
        :returns: TODO

        """
        while True:
            players = self.players[:]
            for index, player in enumerate(players[:]):
                game_state = {
                    'pot_size': self.dealer.playerControl.pot,
                    'table_cards': self.dealer.cardControl.tableCards,
                    'active_players': len(players),
                    'position': index / len(players),
                }
                
                # Enhanced thought process before decision
                self.terminal_manager.write_thought(player.name, f"Current pot size: {game_state['pot_size']}")
                self.terminal_manager.write_thought(player.name, f"My position: {'Early' if game_state['position'] < 0.3 else 'Middle' if game_state['position'] < 0.7 else 'Late'}")
                self.terminal_manager.write_thought(player.name, f"Active players: {game_state['active_players']}")
                
                if game_state['table_cards']:
                    self.terminal_manager.write_thought(player.name, f"Community cards: {', '.join(str(card) for card in game_state['table_cards'])}")
                
                # Get player's decision
                if hasattr(player, 'options'):
                    record = player.options(game_state)
                else:
                    record = player.options()
                
                # Log the decision
                decision_type = "folded" if record[1] == -1 else "raised" if record[1] > 0 else "checked"
                self.terminal_manager.write_thought(player.name, f"Decision: {decision_type} (amount: {record[1] if record[1] != -1 else 0})")
                self.terminal_manager.write_chat(f"{player.name} {decision_type}")
                
                index = (index+1) % len(self.players) 
                self.players[index].bet = record[0]
                if record[1] == -1:
                    players.remove(player)
                else:
                    self.dealer.playerControl.pot += record[1]
                
                # Add inside the player loop after game_state creation:
                self.terminal_manager.write_thought(player.name, f"Considering my options with pot size {game_state['pot_size']}")
                self.terminal_manager.write_chat(f"{player.name} is thinking...")
            
            self.players = players[:] 
            
            if self.isAllIn():
                break
            elif self.controlDeposit():
                break
            else:
                continue
        return self

    def printSituation(self, table=False):
        """
        Prints out whole situation in the game to the game display window.
        """
        output = []
        output.append(f"\n=== Round {self.rounds} ===")
        
        # Print all bot hands for simulation
        for bot in self.players:
            output.append(f"\n{bot.name}'s cards: {str(bot.hand)}")
            output.append(f"Money: {bot.money}")
        
        if table:
            output.append("\nCommunity cards:")
            output.append(str(table))
        
        # Send to game display window
        self.terminal_manager.write_game_display("\n".join(output))

    def allCards(self):
        """
        Prints hands of all players
        """
        for player in self.players:
            print(player.name, "")
            ui.cards(player.hand)
        return self

    def showdown(self):
        """
        Ending of the round
        :returns: TODO

        """
        print("Community cards:")
        ui.cards(self.dealer.cardControl.tableCards)
        self.allCards()
        
        winners = self.dealer.chooseWinner(self.players)
        x = [winner.name for winner in winners]
        ui.roundWinners(x)
        for w in winners:
            ui.printValue(w.handValue)
        self.dealer.playerControl.givePot(winners)
        return self

    def startPhase(self, phase):
        """
        Goes through one phase part of easy game
        :returns: TODO

        """
        print("\n\t\t{}\n".format(phase))
        self.printSituation(self.dealer.cardControl.tableCards)
        self.round()
        self.dealer.cardOnTable(phase)
        
    def isAllIn(self):
        """
        Checking all players if someone is allin or not
        :returns: TODO

        """
        for player in self.players:
            if player.bet == -1:
                return True
        return False

    def eachRound(self):
        """TODO: Docstring for function.

        :returns: TODO

        """
        self.dealer.playerControl.ante(self.rounds)
        #Preflop
        self.startPhase("Preflop")
        if self.isAllIn():
            #allin on flop
            return self.dealer.cardOnTable("All-flop")
        else:
            #Flop
            self.startPhase("Flop")
            
        if self.isAllIn():
            #allin on turn
            return self.dealer.cardOnTable("All-turn")
        else:
            #Turn
            self.startPhase("Turn")

    def setup_terminals(self):
        """Initialize separate terminal windows"""
        self.terminal_manager.start_terminals(self.players)
        
        # Debug messages
        for player in self.players:
            self.terminal_manager.write_thought(player.name, f"Debug: Hello from {player.name}'s thoughts!")
            self.terminal_manager.write_chat(f"{player.name} says: Hello everyone!")

    def cleanup(self):
        """Cleanup all game resources"""
        try:
            # Close all terminal windows
            if hasattr(self, 'terminal_manager'):
                print("\nClosing all terminal windows...")
                self.terminal_manager.write_chat("Game ending - closing terminals...")
                self.terminal_manager.close_all()
                # Force quit Terminal.app on macOS
                if sys.platform == 'darwin':
                    subprocess.run(['osascript', '-e', 'tell application "Terminal" to quit'])
            # Cleanup curses if it was initialized
            if self.screen:
                curses.endwin()
        except Exception as e:
            print(f"Error during cleanup: {e}")

