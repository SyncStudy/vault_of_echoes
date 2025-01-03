# vault_of_echoes/main.py
import os
from puzzle_manager import PuzzleManager
from ai_guardian import AIGuardian
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main():
    print("Welcome to the Vault of Echoes CLI!")
    print("Type 'exit' or 'quit' to stop.")

    # Initialize Puzzle Manager
    puzzle_manager = PuzzleManager(puzzle_file='data/puzzles.json')
    
    # Initialize AI Guardian with your OpenAI API key
    openai_api_key = os.getenv("OPENAI_API_KEY", "sk-xxxxPLACEHOLDERxxxx")
    ai_guardian = AIGuardian(openai_api_key=openai_api_key)
    
    # Verify puzzles were loaded successfully
    if not puzzle_manager.puzzles:
        print("Error: No puzzles were loaded. Please check the puzzles file.")
        return
        
    current_puzzle = puzzle_manager.get_current_puzzle()
    if not current_puzzle:
        print("Error: Could not load initial puzzle")
        return

    print("\nYour first puzzle:")
    print(current_puzzle.prompt)

    while True:
        user_input = input("\nYou: ").strip().lower()
        
        if user_input in ['exit', 'quit']:
            print("Thanks for playing!")
            break
            
        if user_input in current_puzzle.solution:
            print("Correct! Moving to next puzzle...")
            if puzzle_manager.advance_to_next_puzzle():
                current_puzzle = puzzle_manager.get_current_puzzle()
                print("\nNext puzzle:")
                print(current_puzzle.prompt)
            else:
                print("Congratulations! You've completed all puzzles!")
                break
        else:
            print("That's not correct. Try again!")
            # Use AI Guardian to generate a dynamic hint
            ai_hint = ai_guardian.generate_hint(current_puzzle.prompt)
            print("AI Hint:", ai_hint)

if __name__ == "__main__":
    main()
