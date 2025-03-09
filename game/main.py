#!/usr/bin/env python3

import poker
from os import system
from time import sleep
import curses
import signal
import sys

def signal_handler(sig, frame):
    print("\nClosing game and cleaning up...")
    if 'game' in globals() and game:
        game.cleanup()
    sys.exit(0)

def main():
    """ 
    Work to create game simulation
    """
    game = None
    try:
        # Register the signal handler for Ctrl+C
        signal.signal(signal.SIGINT, signal_handler)
        
        game = poker.Game()
        system("clear")
        print("Simulating Texas Hold'em with bots!\n")
        
        # Create 4 bots automatically
        allPlayers = game.dealer.playerControl.createPlayers(numPlayers=4)
        game.players = allPlayers
        
        # Setup terminal windows
        game.setup_terminals()
        
        while True:
            print("\n\n\tRound #", game.rounds, end="\n\n")
            game.players = list(allPlayers)
            
            game.dealer.gameOn()
            game.dealer.giveCards()
            
            # Show initial state
            print("\n--- Initial Deal ---")
            game.printSituation()
            sleep(5)  # Add delay to make simulation readable
            
            # Play the round
            game.eachRound()
            
            # Showdown
            print("\n\t\tShowdown\n")
            game.showdown()
            game.dealer.endGame()
            
            if len(game.dealer.playerControl.players) == 1:
                print("Final winner is:", game.dealer.playerControl.players[0].name)
                print("Money: ", game.dealer.playerControl.players[0].money)
                break
            
            sleep(3)  # Add delay between rounds
            system("clear")
            game.rounds += 1
    except Exception as e:
        print(f"Game error: {e}")
    finally:
        if game:
            game.cleanup()

if __name__ == "__main__":
    main()

