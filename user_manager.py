# vault_of_echoes/user_manager.py
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class UserState:
    user_id: str
    current_state: str
    token_balance: float = 0.0
    puzzle_history: Dict[str, bool] = field(default_factory=dict)

class UserManager:
    def __init__(self):
        self.users: Dict[str, UserState] = {}

    def get_or_create_user(self, user_id: str) -> UserState:
        if user_id not in self.users:
            new_user = UserState(
                user_id=user_id,
                current_state="GREETING",
                token_balance=5.0  # initial tokens
            )
            self.users[user_id] = new_user
        return self.users[user_id]

    def update_user_state(self, user_id: str, new_state: str):
        user_state = self.get_or_create_user(user_id)
        user_state.current_state = new_state

    def add_tokens(self, user_id: str, amount: float):
        user_state = self.get_or_create_user(user_id)
        user_state.token_balance += amount

    def spend_tokens(self, user_id: str, amount: float) -> bool:
        user_state = self.get_or_create_user(user_id)
        if user_state.token_balance >= amount:
            user_state.token_balance -= amount
            return True
        return False
