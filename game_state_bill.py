'''simple game state class'''

from dataclasses import dataclass
from enum import Enum

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
    monies: int
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
    deck: list[Card]
    num: int = 5

    def create_players(self) -> 'GameState':
        pass

    def start_game(self) -> 'GameState':
        self.shuffle_cards()
        self.deal_cards()
        return self

    def set_cards(self) -> 'GameState':
        pass

    def deal_cards(self) -> 'GameState':
        pass

    def shuffle_cards(self) -> 'GameState':
        pass

    def simulation_step(self) -> 'GameState':
        pass

    def query_llm(self) -> 'LLMResponse':
        pass

    def to_json(self) -> dict:
        pass

class LLMResponse:
    action: Action
    thoughts: str
    response: str


