from typing import Dict, Any, Optional
from dataclasses import dataclass
from pydantic import BaseModel, Field

# Import relevant classes from game_state_bill.py
# These imports assume game_state_bill.py is accessible in the import path
from game_state_bill import GameState, Player, Chat, Action, ChatMessage, Raise

@dataclass
class inputClass:
    """
    Input class for the fraud agent.
    Contains the game state, chat history, and player information.
    """
    game_state: GameState
    chat: Chat
    player: Player
    
    def get_game_state(self) -> GameState:
        """Returns the game state"""
        return self.game_state
    
    def get_chat(self) -> Chat:
        """Returns the chat history"""
        return self.chat
    
    def get_player(self) -> Player:
        """Returns the player information"""
        return self.player

class outputClass(BaseModel):
    # Action fields
    fold: bool = Field(..., description="Whether to fold (true) or not (false)")
    raise_amount: int = Field(..., description="Amount to raise if not folding")
    
    # Chat Message fields
    message: str = Field(..., description="Message to send to the chat")
    player_id: str = Field(..., description="ID of the player sending the message")
    
    # Thoughts and error fields
    thoughts: str = Field(..., description="Agent's reasoning for the decision")
    error: Optional[str] = Field(None, description="Error message if something went wrong")