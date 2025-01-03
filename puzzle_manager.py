# vault_of_echoes/puzzle_manager.py
import json
from dataclasses import dataclass
from typing import List, Union, Dict
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@dataclass
class Puzzle:
    puzzle_id: str
    prompt: str
    solution: Union[str, List[str]]
    hints: List[str]

class PuzzleManager:
    def __init__(self, puzzle_file: str):
        self.puzzle_file = puzzle_file
        self.puzzles: Dict[str, Puzzle] = {}
        self.load_puzzles()
        self.current_puzzle_id = "puzzle_1"  # Start with the first puzzle

    def load_puzzles(self):
        try:
            logger.debug(f"Attempting to load puzzles from {self.puzzle_file}")
            with open(self.puzzle_file, 'r', encoding='utf-8') as f:
                content = ""
                for line in f:
                    if not line.strip().startswith("//"):
                        content += line
                
                logger.debug(f"Cleaned content length: {len(content)} characters")
                data = json.loads(content)
                puzzle_list = data.get('puzzles', [])
                logger.debug(f"Found {len(puzzle_list)} puzzles")
                
                for puzzle_data in puzzle_list:
                    puzzle_id = puzzle_data['puzzle_id']
                    puzzle = Puzzle(
                        puzzle_id=puzzle_id,
                        prompt=puzzle_data['prompt'],
                        solution=puzzle_data['solution'],
                        hints=puzzle_data['hints']
                    )
                    self.puzzles[puzzle_id] = puzzle
                logger.debug(f"Successfully loaded {len(self.puzzles)} puzzles: {list(self.puzzles.keys())}")
                
                if not self.puzzles:
                    logger.warning("No puzzles were loaded from the file")
                    
        except FileNotFoundError:
            logger.error(f"Error: Could not find file {self.puzzle_file}")
            self.puzzles = {}
        except json.JSONDecodeError as e:
            logger.error(f"Error: Invalid JSON in {self.puzzle_file}")
            logger.error(f"Details: {str(e)}")
            logger.error(f"Content causing error: {content[:100]}...")
            self.puzzles = {}
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            self.puzzles = {}

    def get_puzzle(self, puzzle_id: str = None) -> Puzzle:
        if puzzle_id is None:
            puzzle_id = self.current_puzzle_id
        
        puzzle = self.puzzles.get(puzzle_id)
        if puzzle is None:
            logger.error(f"Puzzle {puzzle_id} not found. Available puzzles: {list(self.puzzles.keys())}")
        return puzzle

    def get_current_puzzle(self) -> Puzzle:
        return self.get_puzzle(self.current_puzzle_id)

    def advance_to_next_puzzle(self) -> bool:
        current_num = int(self.current_puzzle_id.split('_')[1])
        next_puzzle_id = f"puzzle_{current_num + 1}"
        if next_puzzle_id in self.puzzles:
            self.current_puzzle_id = next_puzzle_id
            return True
        return False
