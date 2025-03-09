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


class Action(Enum):
    FOLD = "fold"
    CALL = "call"
    RAISE = "raise"
    CHECK = "check"
    ALL_IN = "all in"

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
    players: dict[str,Player]
    chat: Chat
    pot: int

    def to_json(self):
        pass

class LLMResponse:
    action: Action
    thoughts: str
    response: str
