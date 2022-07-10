from typing import (
    Dict,
    Any,
)
from .cards import (
    Suit,
)

class Action:
    def __init__(self, **params: Any):
        self._params = params

    def to_text(self) -> str:
        raise NotImplementedError('Override')

    def __repr__(self):
        return f'{self.__class__.__name__}({self._params})'

# target: waste

class DrawFromDeckAction(Action):
    @property
    def count(self) -> int:
        return self._params.get('count', 1)

    def to_text(self) -> str:
        return f'Draw {self.count} from deck'

# target: pile

class MoveFromWasteToPileAction(Action):
    @property
    def target_pile_index(self) -> int:
        pile_index = self._params.get('target_pile_index')
        assert isinstance(pile_index, int)
        return pile_index

    def to_text(self) -> str:
        return f'Move from waste to pile {self.target_pile_index + 1}'

class MoveFromFoundationToPileAction(Action):
    @property
    def target_pile_index(self) -> int:
        pile_index = self._params.get('target_pile_index')
        assert isinstance(pile_index, int)
        return pile_index

    @property
    def source_foundation_suit(self) -> Suit:
        suit = self._params.get('source_foundation_suit')
        assert isinstance(suit, Suit)
        return suit

    def to_text(self) -> str:
        return f'Move from foundation {self.source_foundation_suit.name} to pile {self.target_pile_index + 1}'

class MoveFromPileToPileAction(Action):
    @property
    def source_pile_index(self) -> int:
        pile_index = self._params.get('source_pile_index')
        assert isinstance(pile_index, int)
        return pile_index

    @property
    def target_pile_index(self) -> int:
        pile_index = self._params.get('target_pile_index')
        assert isinstance(pile_index, int)
        return pile_index

    @property
    def count(self) -> int:
        return self._params.get('count', 1)

    def to_text(self) -> str:
        return f'Move {self.count} from pile {self.source_pile_index + 1} to pile {self.target_pile_index + 1}'

# target: foundation

class MoveFromWasteToFoundationAction(Action):
    @property
    def target_foundation_suit(self) -> Suit:
        suit = self._params.get('target_foundation_suit')
        assert isinstance(suit, Suit)
        return suit

    def to_text(self) -> str:
        return f'Move from waste to foundation {self.target_foundation_suit.name}'

class MoveFromPileToFoundationAction(Action):
    @property
    def source_pile_index(self) -> int:
        pile_index = self._params.get('source_pile_index')
        assert isinstance(pile_index, int)
        return pile_index

    @property
    def target_foundation_suit(self) -> Suit:
        suit = self._params.get('target_foundation_suit')
        assert isinstance(suit, Suit)
        return suit

    def to_text(self) -> str:
        return f'Move from pile {self.source_pile_index + 1} to foundation {self.target_foundation_suit.name}'
