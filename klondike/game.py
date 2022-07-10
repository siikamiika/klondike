from __future__ import annotations
from typing import (
    List,
)
from .cards import (
    Deck,
    Waste,
    Pile,
    Foundation,
    Suit,
)
from .history import (
    History,
)
from .actions import (
    Action,
    DrawFromDeckAction,
    MoveFromWasteToPileAction,
    MoveFromFoundationToPileAction,
    MoveFromPileToPileAction,
    MoveFromWasteToFoundationAction,
    MoveFromPileToFoundationAction,
)

class Game:
    def __init__(
        self,
        deck: Deck,
        waste: Waste,
        piles: List[Pile],
        foundations: List[Foundation],
    ):
        self._deck = deck
        self._waste = waste
        self._piles = piles
        self._foundations = foundations
        self._history = History()

    @classmethod
    def create(cls, seed=None) -> Game:
        deck = Deck.create(seed)
        waste = Waste()
        piles = []
        for i in range(7):
            pile_cards = []
            for _ in range(i + 1):
                card = deck.draw()
                pile_cards.append(card)
            pile = Pile(pile_cards)
            piles.append(pile)
        foundations = [Foundation(suit) for suit in Suit]
        return cls(deck, waste, piles, foundations)

    @property
    def seed(self) -> int:
        return self._deck.seed

    @property
    def deck(self) -> Deck:
        return self._deck

    @property
    def waste(self) -> Waste:
        return self._waste

    @property
    def piles(self) -> List[Pile]:
        return self._piles

    @property
    def foundations(self) -> List[Foundation]:
        return self._foundations

    def run_action(self, action: Action):
        if isinstance(action, DrawFromDeckAction):
            if action.count != 1:
                raise NotImplementedError('DrawFromDeckAction is only implemented for 1 card')
            # TODO other variants
            if self._deck.top is None:
                while self._waste.top:
                    card = self._waste.draw()
                    self._deck.push(card)
            card = self._deck.draw()
            self._waste.push(card)
        elif isinstance(action, MoveFromWasteToPileAction):
            target_pile = self._piles[action.target_pile_index]
            card = self._waste.draw()
            try:
                target_pile.push(card)
            except (IndexError, ValueError) as ex:
                self._waste.push(card)
                raise ex
        elif isinstance(action, MoveFromFoundationToPileAction):
            source_foundation = next(f for f in self._foundations if f.suit == action.source_foundation_suit)
            target_pile = self._piles[action.target_pile_index]
            card = source_foundation.draw()
            try:
                target_pile.push(card)
            except (IndexError, ValueError) as ex:
                source_foundation.push(card)
                raise ex
        elif isinstance(action, MoveFromPileToPileAction):
            source_pile = self._piles[action.source_pile_index]
            target_pile = self._piles[action.target_pile_index]
            cards = source_pile.draw(action.count)
            moved_count = 0
            try:
                for card in cards:
                    target_pile.push(card)
                    moved_count += 1
            except (IndexError, ValueError) as ex:
                target_pile.draw(moved_count)
                for card in cards:
                    source_pile.push(card)
                raise ex
        elif isinstance(action, MoveFromWasteToFoundationAction):
            target_foundation = next(f for f in self._foundations if f.suit == action.target_foundation_suit)
            card = self._waste.draw()
            try:
                target_foundation.push(card)
            except (IndexError, ValueError) as ex:
                self._waste.push(card)
                raise ex
        elif isinstance(action, MoveFromPileToFoundationAction):
            source_pile = self._piles[action.source_pile_index]
            target_foundation = next(f for f in self._foundations if f.suit == action.target_foundation_suit)
            card = source_pile.draw(1)[0]
            try:
                target_foundation.push(card)
            except (IndexError, ValueError) as ex:
                source_pile.push(card)
                raise ex
        else:
            raise Exception(f'Invalid action: {action}')
        self._history.push(action)

    def undo(self):
        raise NotImplementedError
