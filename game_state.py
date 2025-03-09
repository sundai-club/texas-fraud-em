'''simple game state class'''

from dataclasses import dataclass
from enum import Enum
import random
from collections import deque

class CardValue(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

class CardSuit(Enum):
    HEARTS = "hearts"
    DIAMONDS = "diamonds"
    CLUBS = "clubs"
    SPADES = "spades"

@dataclass
class Card:
    value: CardValue
    suit: CardSuit

@dataclass
class Raise:
    amount: int

@dataclass
class Action():
    fold: bool
    increase: Raise

@dataclass
class Player:
    cards: list[Card]
    action: Action
    money: int
    id: str
    thoughts: str

@dataclass
class ChatMessage:
    player: Player
    message: str

class Chat:
    messages: list[ChatMessage]

@dataclass
class ActionHistory:
    actions: list[Action]


@dataclass
class GameState:
    table: list[Card]
    players: dict[str, Player]
    chat: Chat
    pot: int
    action_history: ActionHistory
    deck: deque[Card]

    def create_deck(self) -> 'GameState':
        self.deck = deque()
        for suit in CardSuit:
            for value in CardValue:
                self.deck.append(Card(value, suit))
        
        deck_list = list(self.deck)
        random.shuffle(deck_list)
        self.deck = deque(deck_list)
        return self

    def create_players(self) -> 'GameState':
        for i in range(self.num_players):
            self.players[f"player_{i}"] = Player(cards=[], 
                                                 action=Action(fold=False, increase=0), 
                                                 money=1000, 
                                                 id=f"player_{i}", 
                                                 thoughts="")
        return self

    def start_game(self) -> 'GameState':
        self.create_deck()
        self.deal_cards()
        return self

    def play_game(self) -> 'GameState':
        pass

    def play_round(self) -> 'GameState':
        pass

    def play_step(self) -> 'GameState':
        pass

    def set_cards(self) -> 'GameState':
        pass

    def deal_cards(self) -> None:
        for player in self.players.values():
            player.cards = [self.deck.popleft() for _ in range(2)]


    def query_llm(self) -> 'LLMResponse':
        pass

    def to_json(self) -> dict:
        pass

class LLMResponse:
    action: Action
    thoughts: str
    response: str


if __name__ == "__main__":
    game = GameState()
    game.create_players()
    game.start_game()
    print(game)
