from os import path as p
from sys import path
player_package = p.abspath("..") + "/player"
path.append(player_package)
import player

class PlayerControl(object):
    def __init__(self):
        self.players = []
        self.pot = 0.0

    def cleanPlayers(self):
        for index,player in enumerate(self.players[:]):
            if player.money == 0:
                self.players.remove(player)
    
    def addPlayer(self,player):
        self.players.append(player)
        return self

    def clearPlayersDebt(self):
        """
        Clears deposit and bet to all players
        :returns: TODO

        """
        for player in self.players:
            player.clearDebt()
        return self
    
    def createPlayers(self, name = "Bot0", numPlayers=4, money=500.0, difficulty="easy"):
        # Start with first bot instead of human player
        self.addPlayer(player.EasyBot())
        self.players[0].name = "Bot0"
        
        # Add remaining bots
        for i in range(1, numPlayers):
            self.addPlayer(player.EasyBot())
            self.players[i].name = f"Bot{i}"
        return self.players

    def givePot(self,players):
        """
        Gives the pot to the winner(s)
        :returns: TODO

        """
        prize = self.pot/len(players)
        for i in players:
            i.money += prize
        self.pot = 0.0

    def ante(self, rounds):
        """
        Function where everyone needs to get fixed price 
        to the pot on the beggining
        :returns: TODO

        """
        price = rounds ** 2
        for player in self.players:
            self.pot += player.raiseBet(price)[1]

