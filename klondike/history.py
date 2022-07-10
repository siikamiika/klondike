from typing import (
    List,
)
from .actions import (
    Action,
)

class History:
    def __init__(self):
        self._actions: List[Action] = []

    @property
    def length(self) -> int:
        return len(self._actions)

    def push(self, action: Action):
        self._actions.append(action)

    def pop(self) -> Action:
        return self._actions.pop()
