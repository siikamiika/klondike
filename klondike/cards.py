from __future__ import annotations
from typing import (
    List,
    Optional,
)
import enum
import random
import sys
import hashlib

class Color(enum.Enum):
    BLACK = 1
    RED = 2

class Suit(enum.Enum):
    SPADES = 1
    HEARTS = 2
    DIAMONDS = 3
    CLUBS = 4

    @property
    def color(self) -> Color:
        if self is Suit.SPADES:
            return Color.BLACK
        if self is Suit.HEARTS:
            return Color.RED
        if self is Suit.DIAMONDS:
            return Color.RED
        if self is Suit.CLUBS:
            return Color.BLACK
        raise Exception(f'Invalid suit: {self}')

    def sha256_hash(self) -> bytes:
        return hashlib.sha256((self.__class__.__name__ + '.' + self.name).encode('utf-8')).digest()

class Rank(enum.Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

    def sha256_hash(self) -> bytes:
        return hashlib.sha256((self.__class__.__name__ + '.' + self.name).encode('utf-8')).digest()

class Card:
    def __init__(self, suit: Suit, rank: Rank):
        self._suit = suit
        self._rank = rank

    @property
    def suit(self) -> Suit:
        return self._suit

    @property
    def rank(self) -> Rank:
        return self._rank

    def sha256_hash(self) -> bytes:
        return hashlib.sha256(
            hashlib.sha256(b'Card').digest()
            + self._suit.sha256_hash()
            + self._rank.sha256_hash()
        ).digest()

class Deck:
    def __init__(self, cards: List[Card], seed):
        self._cards = cards
        self._seed = seed

    @property
    def seed(self) -> int:
        return self._seed

    @property
    def top(self) -> Optional[Card]:
        if len(self._cards) == 0:
            return None
        return self._cards[-1]

    def draw(self) -> Card:
        return self._cards.pop()

    def push(self, card: Card):
        self._cards.append(card)

    @classmethod
    def create(cls, seed=None) -> Deck:
        """
        Create a new shuffled card deck.
        Optionally provide a seed for deterministic output.
        """
        cards = []
        for suit in Suit:
            for rank in Rank:
                cards.append(Card(suit, rank))
        if seed is None:
            seed = random.randrange(sys.maxsize)
        random.Random(seed).shuffle(cards)
        return cls(cards, seed)

    def sha256_hash(self) -> bytes:
        return hashlib.sha256(
            hashlib.sha256(b'Deck').digest()
            + b''.join(c.sha256_hash() for c in self._cards)
        ).digest()

class Waste:
    def __init__(self):
        self._cards: List[Card] = []

    @property
    def top(self) -> Optional[Card]:
        if len(self._cards) == 0:
            return None
        return self._cards[-1]

    def draw(self) -> Card:
        return self._cards.pop()

    def push(self, card: Card):
        self._cards.append(card)

    def sha256_hash(self) -> bytes:
        return hashlib.sha256(
            hashlib.sha256(b'Waste').digest()
            + b''.join(c.sha256_hash() for c in self._cards)
        ).digest()

class Pile:
    def __init__(self, cards: List[Card]):
        self._cards = cards
        self._revealed_count = min(1, len(cards))

    # TODO don't reveal hidden cards in public interface
    @property
    def cards(self) -> List[Card]:
        return self._cards

    @property
    def revealed_count(self) -> int:
        return self._revealed_count

    @property
    def top(self) -> Optional[Card]:
        if len(self._cards) == 0:
            return None
        return self._cards[-1]

    def draw(self, count: int) -> List[Card]:
        if count > self._revealed_count:
            raise ValueError(f'Card {count} is not revealed yet')
        if count > len(self._cards):
            raise ValueError(f'Card {count} is out of bounds')
        remaining, drawn = self._cards[:-count], self._cards[-count:]
        self._cards = remaining
        if count == self._revealed_count:
            self._revealed_count = 0 if len(remaining) == 0 else 1
        else:
            self._revealed_count -= count
        return drawn

    def push(self, card: Card):
        if self.top:
            if card.suit.color == self.top.suit.color:
                raise ValueError('Cannot push same color')
            if card.rank.value != self.top.rank.value - 1:
                raise ValueError('Cannot push ranks other than top - 1 onto pile')
        elif card.rank != Rank.KING:
            raise ValueError('Cannot push ranks other than king onto an empty pile')
        self._cards.append(card)
        self._revealed_count += 1

    def sha256_hash(self) -> bytes:
        return hashlib.sha256(
            hashlib.sha256(b'Pile').digest()
            + hashlib.sha256(bytes([self._revealed_count])).digest()
            + b''.join(c.sha256_hash() for c in self._cards)
        ).digest()

class Foundation:
    def __init__(self, suit: Suit):
        self._suit = suit
        self._cards: List[Card] = []

    @property
    def suit(self) -> Suit:
        return self._suit

    @property
    def top(self) -> Optional[Card]:
        if len(self._cards) == 0:
            return None
        return self._cards[-1]

    def draw(self) -> Card:
        return self._cards.pop()

    def push(self, card: Card):
        if card.suit != self._suit:
            raise ValueError('Cannot push cards of suit {card.suit} onto a foundation of {self._suit}')
        top_value = 0
        if self.top:
            top_value = self.top.rank.value
        if card.rank.value - 1 != top_value:
            raise ValueError('Cannot push ranks other than top + 1 onto foundation')
        self._cards.append(card)

    def sha256_hash(self) -> bytes:
        return hashlib.sha256(
            hashlib.sha256(b'Foundation').digest()
            + self._suit.sha256_hash()
            + b''.join(c.sha256_hash() for c in self._cards)
        ).digest()
