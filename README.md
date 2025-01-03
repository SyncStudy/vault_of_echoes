# The Vault of Echoes 

## Overview

**The Vault of Echoes** is a text-based puzzle and persuasion game. Players solve riddles (puzzles) and then attempt to persuade an AI Guardian to gain access to the Vault. The game is designed to be extensible, allowing new puzzles and states.

This MVP includes:

- **Text-based interface** via the console (`main.py`).
- **AutoGene-style orchestration** in `orchestrator.py`.
- **Off-chain token logic** for buying hints and rewarding puzzle solutions.
- **Simple puzzle storage** in `data/puzzles.json`.
- **GPT-based persuasion** (with a placeholder or real OpenAI key).
- **Basic Docker integration** for simpler deployment.
- **Pytest test suite** in `tests/test_orchestrator.py`.

## File by File

### Dockerfile
Builds a Docker image for consistent deployment.

### requirements.txt
Lists the Python dependencies.

### main.py
- **Purpose**: Entry point. Creates core objects, loops to read user text, and uses the `Orchestrator` to process inputs.
- **Usage**: `python main.py`

### orchestrator.py
- **Purpose**: Game state machine. Routes user to puzzle solving, hint logic, persuasion, and final reward.
- **Key Functions**:
  1. **process_user_input(user_id, user_input)**: Main function that reads the user’s current state and calls the appropriate handler.
  2. **handle_greeting**, **handle_puzzle**, **handle_persuasion**, **handle_reward**: Sub-handlers for each game state.

### puzzle_manager.py
- **Purpose**: Loads puzzle data (prompts, solutions, hints) from a JSON file.
- **Key Classes**:
  1. **Puzzle**: Dataclass holding puzzle info.
  2. **PuzzleManager**: Loads puzzle definitions from `data/puzzles.json`. Provides `get_puzzle(puzzle_id)`.

### user_manager.py
- **Purpose**: Manages user data in memory, including token balances, puzzle progress, current state.
- **Key Functions**:
  1. **get_or_create_user(user_id)**: Retrieves or creates a `UserState`.
  2. **update_user_state(user_id, new_state)**: Changes the user’s current game state.
  3. **add_tokens(user_id, amount)** / **spend_tokens(user_id, amount)**: Adjusts user’s token balance.

### ai_guardian.py
- **Purpose**: Simple wrapper for the OpenAI API to produce GPT responses. 
- **Key Function**:
  1. **get_response(system_prompt, user_message)**: Sends a chat completion request, returns text from GPT.

### logger.py
- **Purpose**: Provides a simple logger using `logging` module.

### data/puzzles.json
- **Purpose**: Defines puzzle prompts, solutions, and hints. You can add or modify puzzles here.

### tests/test_orchestrator.py
- **Purpose**: Pytest-based test suite that ensures the orchestrator logic (puzzle flow, persuasion, reward) works.

## Running the Game

1. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```
   
   

2. **Set OpenAI Key** (Optional):

- If using real GPT calls, set an environment variable:

  ```bash
  export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
  ```

- Or leave it as a placeholder for local testing (will return “Sorry, I encountered an error…”).

3. **Run**:

```bash
python main.py
```

4. **Usage**:

- Type anything to proceed from `GREETING` → `FIRST_PUZZLE`.
- **Puzzle**: Type guesses. If incorrect, you may see “That doesn’t seem right.”
- **Hint**: Type `"hint"` (costs 1 token).
- **Solve** puzzle → proceed to next puzzle or persuasion.
- In persuasion, type a **long** argument → proceed to reward.
- At reward, type `"enter vault"` → finalize.

## Running Tests

1. Install pytest:

   ```bash
   pip install pytest
   ```

2. Run tests:

   ```bash
   pytest --maxfail=1 --disable-warnings -q
   ```

## Docker Usage

1. Build Image:

   ```bash
   docker build -t vault_of_echoes .
   ```

2. Run Container:

   ```bash
   docker run -it --rm vault_of_echoes
   ```

   - This will start the CLI inside the container.

## Extending / Customizing

- **Add more puzzles**: Insert more entries in `data/puzzles.json` or create separate puzzle states in `orchestrator.py`.
- **Real tokens**: Integrate a Web3 library in `user_manager.py` to manage on-chain balances.
- **Front-end**: Create a simple web or GUI front-end that calls into the orchestrator logic.


```dockerfile
# vault_of_echoes/Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python", "main.py"]
