# vault_of_echoes/orchestrator.py
from user_manager import UserManager
from puzzle_manager import PuzzleManager
from ai_guardian import AIGuardian
from logger import get_logger

class Orchestrator:
    def __init__(self, user_manager: UserManager, puzzle_manager: PuzzleManager, ai_guardian: AIGuardian):
        self.user_manager = user_manager
        self.puzzle_manager = puzzle_manager
        self.ai_guardian = ai_guardian
        self.logger = get_logger(self.__class__.__name__)

    def process_user_input(self, user_id: str, user_input: str) -> str:
        user_state = self.user_manager.get_or_create_user(user_id)
        current_state = user_state.current_state

        self.logger.debug(f"User {user_id} in state {current_state}, input: {user_input}")

        if current_state == "GREETING":
            response = self.handle_greeting(user_id, user_input)
        elif current_state == "FIRST_PUZZLE":
            response = self.handle_puzzle(user_id, puzzle_id="puzzle_1", next_state="SECOND_PUZZLE", user_input=user_input)
        elif current_state == "SECOND_PUZZLE":
            response = self.handle_puzzle(user_id, puzzle_id="puzzle_2", next_state="PERSUASION", user_input=user_input)
        elif current_state == "PERSUASION":
            response = self.handle_persuasion(user_id, user_input)
        elif current_state == "REWARD":
            response = self.handle_reward(user_id, user_input)
        elif current_state == "POST_GAME":
            response = "You have completed this challenge. Keep exploring for more secrets!"
        else:
            response = "I'm not sure what you want to do next."

        return response

    def handle_greeting(self, user_id: str, user_input: str) -> str:
        self.user_manager.update_user_state(user_id, "FIRST_PUZZLE")
        return (
            "Welcome to the Vault of Echoes! I am the AI Guardian.\n"
            "Let's begin with a quick test of your reasoning.\n\n"
            "Type anything to start the first puzzle."
        )

    def handle_puzzle(self, user_id: str, puzzle_id: str, next_state: str, user_input: str) -> str:
        puzzle = self.puzzle_manager.get_puzzle(puzzle_id)
        if not puzzle:
            return "Puzzle not found. Something went wrong."

        # Check for hint request
        if user_input.lower() == "hint":
            self.logger.info(f"User {user_id} requested a hint for {puzzle_id}")
            hint_cost = 1.0
            success = self.user_manager.spend_tokens(user_id, hint_cost)
            if success:
                if puzzle.hints:
                    return f"HINT: {puzzle.hints[0]}"
                else:
                    return "No hints are available for this puzzle."
            else:
                return "You do not have enough tokens to purchase a hint."

        # Check for correct solution
        correct_solutions = puzzle.solution if isinstance(puzzle.solution, list) else [puzzle.solution]
        if user_input.lower() in [s.lower() for s in correct_solutions]:
            self.logger.info(f"User {user_id} solved puzzle {puzzle_id}")
            self.user_manager.update_user_state(user_id, next_state)
            # Reward user for solving the puzzle
            self.user_manager.add_tokens(user_id, 2.0)
            return (
                f"Correct! You've solved {puzzle_id}. You've gained 2 ANQ tokens.\n"
                f"Proceeding to the next phase: {next_state}.\n"
                "Type anything to continue."
            )
        else:
            return (
                "That doesn't seem right. Type 'hint' to spend tokens for a clue, "
                "or try another answer."
            )

    def handle_persuasion(self, user_id: str, user_input: str) -> str:
        system_prompt = (
            "You are the AI Guardian. You will read the user's argument, "
            "and respond with a short evaluation or question. "
            "Be cryptic yet whimsical."
        )
        ai_reply = self.ai_guardian.get_response(system_prompt, user_input)

        # Example check for "sufficiently long" argument
        if len(user_input) > 20:
            self.user_manager.update_user_state(user_id, "REWARD")
            return (
                f"AI Guardian says: {ai_reply}\n\n"
                "Your argument has convinced me. Proceed to the Vault!\n"
                "Type 'enter vault' to claim your reward."
            )
        else:
            return (
                f"AI Guardian says: {ai_reply}\n\n"
                "The Guardian is not yet fully convinced. Please elaborate further."
            )

    def handle_reward(self, user_id: str, user_input: str) -> str:
        if user_input.lower() == "enter vault":
            self.logger.info(f"User {user_id} entered the vault.")
            # Reward user with additional tokens
            self.user_manager.add_tokens(user_id, 10.0)
            user_state = self.user_manager.get_or_create_user(user_id)
            user_state.puzzle_history["vault_opened"] = True
            self.user_manager.update_user_state(user_id, "POST_GAME")
            return (
                "The vault door slides open... You've been granted 10 ANQ tokens! "
                "Congratulations on unlocking the Vault of Echoes.\n"
                "Type anything to continue."
            )
        else:
            return "To claim your reward, type 'enter vault'."
