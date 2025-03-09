import os
from typing import Dict, Any
from pydantic import BaseModel, Field
import openai
from .class import outputClass

# Pydantic model for structured AI output
class FraudAction(BaseModel):
    action_type: str = Field(..., description="Type of action to take (e.g., 'call', 'fold', 'raise')")
    bet_amount: int = Field(0, description="Amount to bet if action is 'raise'")
    confidence: float = Field(..., description="Confidence level in the decision (0.0-1.0)")
    reasoning: str = Field(..., description="Explanation for the decision")

def process_game_decision(game_state: Dict[str, Any], player_state: Dict[str, Any], system_prompt: str) -> outputClass:
    """
    Simple function that takes game state and player state, calls OpenAI API,
    and returns a structured decision using the outputClass.
    
    Args:
        game_state: Dictionary containing the current state of the game
        player_state: Dictionary containing the current state of the player
        
    Returns:
        outputClass object containing the agent's decision
    """
    # Initialize OpenAI client
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return outputClass({"error": "OpenAI API key not found in environment variables"})
    
    client = openai.OpenAI(api_key=api_key)
    
    # Create system message with instructions
    system_message = system_prompt
    # Call OpenAI API
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": f"Game State: {game_state}\nPlayer State: {player_state}"}
            ],
            temperature=0.2,
        )
        
        # Parse the response into our Pydantic model
        content = response.choices[0].message.content
        action = FraudAction.model_validate_json(content)
        
        # Create output object
        return outputClass({
            "action": action.action_type,
            "bet_amount": action.bet_amount,
            "confidence": action.confidence,
            "reasoning": action.reasoning
        })
        
    except Exception as e:
        # Handle errors
        return outputClass({
            "action": "fold",  # Default safe action
            "error": f"Error processing decision: {str(e)}"
        })
