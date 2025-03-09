def get_system_prompt(game_state_info, chat_history):
    """
    Creates a system prompt that includes game state information and chat history.
    
    Args:
        game_state_info: Dictionary containing information about the current game state
        chat_history: List of recent chat messages
        
    Returns:
        String containing the system prompt
    """
    system_prompt = """You are a strategic poker player. Your goal is to make optimal decisions based on the game state.
    Be analytical and strategic. Consider pot odds, position, and player behavior in your decisions. 
    Also, consider how what you say in the chat will affect the other players and use this to your advantage. Please be as savage as possible in the chat to get in the opponents heads.
    Your responses should reflect careful consideration of all available information.
    
    You will analyze the following game state and chat history to make your decision:"""
    
    # Add game state information
    game_state_section = f"""
    GAME STATE:
    Table cards: {game_state_info.get('table_cards', [])}
    Pot size: {game_state_info.get('pot_size', 0)}
    Number of players: {game_state_info.get('players', 0)}
    Current player ID: {game_state_info.get('current_player_id', '')}
    """
    
    # Add chat history
    chat_section = """
    RECENT CHAT HISTORY:"""
    
    if chat_history:
        for message in chat_history:
            # Check if message is a dictionary (as expected)
            if isinstance(message, dict):
                chat_section += f"\nPlayer {message.get('player', 'unknown')}: {message.get('message', '')}"
            else:
                # Handle case where message might be a string or other type
                chat_section += f"\n{message}"
    else:
        chat_section += "\nNo recent messages."
    
    return system_prompt + game_state_section + chat_section

def get_user_prompt(player_info):
    """
    Creates a user prompt that includes only player-specific information.
    
    Args:
        player_info: Dictionary containing information about the player
        
    Returns:
        String containing the user prompt
    """
    return f"""You are Player {player_info.get('id', '')}. 
    
    YOUR CARDS: {player_info.get('cards', [])}
    YOUR MONEY: {player_info.get('money', 0)}
    
    Based on your cards, the game state, and the chat history provided in the system message, what action will you take?
    Consider that you have the following options: 
    - Fold
    - Raise
    - Call (which should output a raise with value 0)
    - Check (which should output a raise with value 0)
    - Chat where you can output messages to other players to try and get in their heads and manipulate them
    """
