import os
import sys
from typing import Dict, Any
from pydantic import BaseModel, Field
import openai
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

# Use package-relative import
from Fraud_Agent.class_definitions import inputClass, outputClass
from game_state_bill import Action, Raise, ChatMessage
from Fraud_Agent.prompt import get_system_prompt, get_user_prompt
def process_game_decision(input_data: inputClass) -> outputClass:
    """
    Simple function that takes game state and player state, calls OpenAI API,
    and returns a structured decision using the outputClass.
    
    Args:
        input_data: inputClass containing game_state, chat, and player
        
    Returns:
        outputClass object containing the agent's decision
    """
    # Initialize OpenAI client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Warning: OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.")
        return outputClass(
            fold=True,
            raise_amount=0,
            message="Error: API key missing",
            player_id=input_data.player.id,
            thoughts="Error: OpenAI API key not found in environment variables",
            error="OpenAI API key not found in environment variables"
        )
    
    client = openai.OpenAI(api_key=api_key)
    
    # Format game state and player information for the AI
    game_state_info = {
        "table_cards": [f"{card.value.name} of {card.suit.value}" for card in input_data.game_state.table],
        "pot_size": input_data.game_state.pot,
        "players": len(input_data.game_state.players),
        "current_player_id": input_data.player.id
    }
    
    player_info = {
        "cards": [f"{card.value.name} of {card.suit.value}" for card in input_data.player.cards],
        "money": input_data.player.monies,
        "id": input_data.player.id
    }
    
    chat_history = [
        {"player": msg.player.id, "message": msg.message}
        for msg in input_data.chat.messages[-5:] if hasattr(input_data.chat, 'messages')
    ]

    #get prompts
    system_prompt = get_system_prompt(game_state_info, chat_history)
    user_prompt = get_user_prompt(player_info)
    
    # Call OpenAI API
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format=outputClass,
            temperature=0.2
        )
        
        # Return the parsed response directly
        return completion.choices[0].message.parsed
        
    except Exception as e:
        # Handle errors
        return outputClass(
            fold=True,
            raise_amount=0,
            message="I need to fold.",
            player_id=input_data.player.id,
            thoughts="Error occurred during processing",
            error=f"Error processing decision: {str(e)}"
        )

def create_sample_input() -> inputClass:
    """
    Creates a sample input for testing the fraud agent.
    """
    from game_state_bill import (
        Player, GameState, Chat, ChatMessage, Action, Raise, 
        Card, CardValue, CardSuit, ActionHistory
    )
    
    # Create initial action for players
    default_action = Action(fold=False, increase=Raise(amount=0))
    default_thoughts = "Initial state"
    
    # Create sample player cards
    player_cards = [
        Card(value=CardValue.ACE, suit=CardSuit.SPADES),
        Card(value=CardValue.KING, suit=CardSuit.SPADES)
    ]
    
    # Create sample player
    player = Player(
        id="player1",
        cards=player_cards,
        monies=1000,
        action=default_action,
        thoughts=default_thoughts
    )
    
    # Create other players for the game state
    other_players = [
        Player(id="player2", cards=[], monies=800, action=default_action, thoughts=default_thoughts),
        Player(id="player3", cards=[], monies=1200, action=default_action, thoughts=default_thoughts)
    ]
    
    # Create sample table cards
    table_cards = [
        Card(value=CardValue.ACE, suit=CardSuit.HEARTS),
        Card(value=CardValue.KING, suit=CardSuit.DIAMONDS),
        Card(value=CardValue.QUEEN, suit=CardSuit.CLUBS)
    ]
    
    # Create sample chat history
    chat = Chat()
    chat.messages = [
        ChatMessage(player=other_players[0], message="Dam you suck so bad at this game"),
        ChatMessage(player=other_players[1], message="I'm gonna raise you off this table!"),
        ChatMessage(player=player, message="Let's see what happens")
    ]
    
    # Create sample action history
    action_history = ActionHistory(actions=[])
    
    # Create a sample deck (remaining cards)
    sample_deck = []
    for suit in CardSuit:
        for value in CardValue:
            # Skip cards that are already in play (table or player's hand)
            card = Card(value=value, suit=suit)
            if card not in table_cards and card not in player_cards:
                sample_deck.append(card)
    
    # Convert players list to dict with id as key
    players_dict = {p.id: p for p in [player] + other_players}
    
    # Create sample game state
    game_state = GameState(
        table=table_cards,
        pot=300,
        players=players_dict,
        chat=chat,
        action_history=action_history,
        deck=sample_deck,
        num=5  # Default value from GameState class
    )
    
    return inputClass(
        game_state=game_state,
        chat=chat,
        player=player
    )

def main():
    """
    Main function to demonstrate the fraud agent's functionality.
    Multiple trials to see different responses.
    """
    # Create sample input
    input_data = create_sample_input()
    
    # Run 10 trials
    for i in range(10):
        print(f"\n=== Trial {i+1} ===")
        
        # Process the decision
        result = process_game_decision(input_data)
        
        # Print the results
        print("Fraud Agent Decision:")
        print(f"Action: fold={result.fold}, raise_amount={result.raise_amount}")
        print(f"Chat Message: {result.message}")
        print(f"Thoughts: {result.thoughts}")
        if result.error:
            print(f"Error: {result.error}")
            break  # Stop if there's an error
        
        # Update the chat history with the agent's response
        input_data.chat.messages.append(
            ChatMessage(
                player=input_data.player,
                message=result.message
            )
        )
        
        # Update action history - append to the actions list
        input_data.game_state.action_history.actions.append(
            Action(
                player=input_data.player,
                action=result.action
            )
        )
        
        # Add a small delay between calls to avoid rate limiting
        time.sleep(1)

if __name__ == "__main__":
    main()
