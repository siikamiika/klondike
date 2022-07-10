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

    def __repr__(self):
        return f'{self.__class__.__name__}({self._params})'

# target: waste

class DrawFromDeckAction(Action):
    @property
    def count(self) -> int:
        return self._params.get('count', 1)

# target: pile

class MoveFromWasteToPileAction(Action):
    @property
    def target_pile_index(self) -> int:
        pile_index = self._params.get('target_pile_index')
        assert isinstance(pile_index, int)
        return pile_index

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

# target: foundation

class MoveFromWasteToFoundationAction(Action):
    @property
    def target_foundation_suit(self) -> Suit:
        suit = self._params.get('target_foundation_suit')
        assert isinstance(suit, Suit)
        return suit

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
