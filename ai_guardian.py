# vault_of_echoes/ai_guardian.py
import openai
import logging

logger = logging.getLogger(__name__)

class AIGuardian:
    def __init__(self, openai_api_key: str):
        openai.api_key = openai_api_key

    def generate_hint(self, puzzle_prompt: str) -> str:
        try:
            logger.debug(f"Generating AI hint for puzzle: {puzzle_prompt}")
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Provide a helpful hint for the following puzzle:\n{puzzle_prompt}",
                max_tokens=60,
                n=1,
                stop=None,
                temperature=0.5,
            )
            hint = response.choices[0].text.strip()
            logger.debug(f"AI-generated hint: {hint}")
            return hint
        except Exception as e:
            logger.error(f"Failed to generate AI hint: {str(e)}")
            return "Sorry, I couldn't generate a hint at this time."
