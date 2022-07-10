from __future__ import annotations
from typing import (
    List,
)
from .cards import (
    Rank,
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

    def get_possible_actions(self) -> List[Action]:
        actions = []
        # source: pile
        for i, pile in enumerate(self._piles):
            if pile.top:
                # target: foundation
                foundation = next(f for f in self._foundations if f.suit == pile.top.suit)
                if (
                    foundation.top and foundation.top.rank.value == pile.top.rank.value - 1
                    or pile.top.rank == Rank.ACE
                ):
                    actions.append(MoveFromPileToFoundationAction(source_pile_index=i, target_foundation_suit=foundation.suit))
                # target: pile
                for j, pile2 in enumerate(self._piles):
                    if i == j:
                        continue
                    for k in range(1, pile.revealed_count + 1):
                        if (
                            (
                                pile2.top is None
                                and pile.cards[-k] is not None
                                and pile.cards[-k].rank is Rank.KING
                            ) or (
                                pile2.top is not None
                                and pile.cards[-k] is not None
                                and pile.cards[-k].suit.color != pile2.top.suit.color
                                and pile.cards[-k].rank.value + 1 == pile2.top.rank.value
                            )
                        ):
                            actions.append(MoveFromPileToPileAction(source_pile_index=i, target_pile_index=j, count=k))
        # source: waste
        if self._waste.top is not None:
            # target: foundation
            foundation = next(f for f in self._foundations if f.suit == self._waste.top.suit)
            if (
                foundation.top and foundation.top.rank.value == self._waste.top.rank.value - 1
                or self._waste.top.rank == Rank.ACE
            ):
                actions.append(MoveFromWasteToFoundationAction(target_foundation_suit=foundation.suit))
            # target: pile
            for i, pile in enumerate(self._piles):
                if (
                    (
                        pile.top is None
                        and self._waste.top.rank is Rank.KING
                    ) or (
                        pile.top is not None
                        and self._waste.top.suit.color != pile.top.suit.color
                        and self._waste.top.rank.value + 1 == pile.top.rank.value
                    )
                ):
                    actions.append(MoveFromWasteToPileAction(target_pile_index=i))
        # source: foundation
        for foundation in self._foundations:
            if foundation.top is None:
                continue
            for i, pile in enumerate(self._piles):
                if (
                    (
                        pile.top is None
                        and foundation.top.rank is Rank.KING
                    ) or (
                        pile.top is not None
                        and foundation.top.suit.color != pile.top.suit.color
                        and foundation.top.rank.value + 1 == pile.top.rank.value
                    )
                ):
                    actions.append(MoveFromFoundationToPileAction(target_pile_index=i, source_foundation_suit=foundation.suit))
        # source: deck
        if self._deck.top or self._waste.top:
            actions.append(DrawFromDeckAction())
        return actions
