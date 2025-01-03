# vault_of_echoes/tests/test_orchestrator.py
import pytest
from orchestrator import Orchestrator
from user_manager import UserManager
from puzzle_manager import PuzzleManager
from ai_guardian import AIGuardian

# Mock Guardian so we don't make real API calls during tests
class MockAIGuardian(AIGuardian):
    def get_response(self, system_prompt: str, user_message: str) -> str:
        return "Mock AI Guardian Response"

@pytest.fixture
def setup_game():
    user_manager = UserManager()
    puzzle_manager = PuzzleManager(puzzle_file='data/puzzles.json')
    ai_guardian = MockAIGuardian(openai_api_key="fake")
    orchestrator = Orchestrator(user_manager, puzzle_manager, ai_guardian)
    return orchestrator

def test_greeting_flow(setup_game):
    orchestrator = setup_game
    user_id = "test_user"

    # GREETING -> FIRST_PUZZLE
    response = orchestrator.process_user_input(user_id, "Hello")
    assert "Welcome to the Vault of Echoes" in response

def test_puzzle_solution_flow(setup_game):
    orchestrator = setup_game
    user_id = "test_user"

    # Move from GREETING to FIRST_PUZZLE
    orchestrator.process_user_input(user_id, "Anything")
    # Attempt puzzle_1
    response = orchestrator.process_user_input(user_id, "fire")
    assert "Correct! You've solved puzzle_1" in response

    # Now in SECOND_PUZZLE
    response = orchestrator.process_user_input(user_id, "egg")
    assert "Correct! You've solved puzzle_2" in response
    # Should go to PERSUASION

def test_persuasion_flow(setup_game):
    orchestrator = setup_game
    user_id = "test_user"
    orchestrator.process_user_input(user_id, "start")  # GREETING -> FIRST_PUZZLE
    orchestrator.process_user_input(user_id, "fire")   # -> SECOND_PUZZLE
    orchestrator.process_user_input(user_id, "egg")    # -> PERSUASION

    # Short argument
    response = orchestrator.process_user_input(user_id, "I am good")
    assert "not yet fully convinced" in response

    # Long argument
    response = orchestrator.process_user_input(user_id, "This is a long argument definitely more than 20 chars.")
    assert "Your argument has convinced me" in response
    # -> REWARD

def test_reward_flow(setup_game):
    orchestrator = setup_game
    user_id = "test_user"
    orchestrator.process_user_input(user_id, "start")
    orchestrator.process_user_input(user_id, "fire")
    orchestrator.process_user_input(user_id, "egg")
    orchestrator.process_user_input(user_id, "A sufficiently long argument for persuasion.")
    
    # Now in REWARD
    response = orchestrator.process_user_input(user_id, "enter vault")
    assert "The vault door slides open" in response
    # -> POST_GAME
