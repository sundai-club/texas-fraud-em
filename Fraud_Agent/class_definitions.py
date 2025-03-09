from typing import Dict, Any, Optional
from dataclasses import dataclass

# Import relevant classes from game_state_bill.py
# These imports assume game_state_bill.py is accessible in the import path
from game_state_bill import GameState, Player, Chat, Action, ChatMessage

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

@dataclass
class outputClass:
    """
    Output class for the fraud agent.
    Contains the action to take, a chat message to send, and the agent's thoughts.
    """
    action: Action
    chat_message: ChatMessage
    thoughts: str
    error: Optional[str] = None
    
    def get_action(self) -> Action:
        """Returns the action to take"""
        return self.action
    
    def get_chat_message(self) -> ChatMessage:
        """Returns the chat message to send"""
        return self.chat_message
    
    def get_thoughts(self) -> str:
        """Returns the agent's thoughts on the decision"""
        return self.thoughts
    
    def get_output(self) -> Dict[str, Any]:
        """Returns the complete output as a dictionary"""
        output = {
            "action": self.action,
            "chat_message": self.chat_message,
            "thoughts": self.thoughts
        }
        
        if self.error is not None:
            output["error"] = self.error
            
        return output
    
    def has_error(self) -> bool:
        """Check if there was an error during processing"""
        return self.error is not None