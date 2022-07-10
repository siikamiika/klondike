from typing import (
    Dict,
    List,
)
import itertools
from .cards import (
    Color,
    Card,
    Suit,
    Rank,
    Deck,
    Waste,
    Pile,
    Foundation,
)
from .game import Game

SUIT_TO_TEXT: Dict[Suit, str] = {
    Suit.CLUBS: '♣',
    Suit.DIAMONDS: '♦',
    Suit.HEARTS: '♥',
    Suit.SPADES: '♠',
}

RANK_TO_TEXT: Dict[Rank, str] = {
    Rank.ACE: 'A',
    Rank.TWO: '2',
    Rank.THREE: '3',
    Rank.FOUR: '4',
    Rank.FIVE: '5',
    Rank.SIX: '6',
    Rank.SEVEN: '7',
    Rank.EIGHT: '8',
    Rank.NINE: '9',
    Rank.TEN: '10',
    Rank.JACK: 'J',
    Rank.QUEEN: 'Q',
    Rank.KING: 'K',
}

def render_card_name(card: Card) -> str:
    return RANK_TO_TEXT[card.rank] + SUIT_TO_TEXT[card.suit]

def suit_color(suit: Suit) -> str:
    return '\033[38;5;9m' if suit.color == Color.RED else '\033[38;5;0m'

def render_card_unicode(card: Card) -> str:
    suit_offset = card.suit.value << 4
    rank_offset = card.rank.value
    if rank_offset > 11:
        # skip "knight" card
        rank_offset += 1
    color_on = suit_color(card.suit)
    color_off = '\033[38;5;15m'
    return color_on + chr(0x1f090 + suit_offset + rank_offset) + color_off

def render_deck(deck: Deck):
    return '🂠' if deck.top else ' '

def render_waste(waste: Waste):
    return render_card_unicode(waste.top) if waste.top else ' '

def render_piles(piles: List[Pile]):
    rows = []
    for i, row_cards in enumerate(itertools.zip_longest(*[p.cards for p in piles])):
        row = []
        for j, card in enumerate(row_cards):
            pile = piles[j]
            if card is None:
                row.append(' ')
            elif i < len(pile.cards) - pile.revealed_count:
                row.append('🂠')
            else:
                row.append(render_card_unicode(card))
        rows.append(' '.join(row))
    return '\n'.join(rows)

def render_foundation(foundation: Foundation):
    card = foundation.top
    if card:
        return render_card_unicode(card)
    color_on = suit_color(foundation.suit)
    color_off = '\033[38;5;15m'
    return color_on + SUIT_TO_TEXT[foundation.suit] + color_off

def render_game(game: Game) -> str:
    return \
"""\033[48;5;45;38;5;15m{deck} | {waste}          
{piles}
{foundations}\033[0m""".format(
        deck=render_deck(game.deck),
        waste=render_waste(game.waste),
        piles=render_piles(game.piles),
        foundations=' | '.join(render_foundation(f) for f in game.foundations),
    )
