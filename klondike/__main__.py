import time
from .game import Game
from .ui import (
    render_card_name,
    render_card_unicode,
    render_game,
)
from .cards import (
    Suit,
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

test_actions = [
    MoveFromPileToFoundationAction(
        source_pile_index=5,
        target_foundation_suit=Suit.SPADES,
    ),
    DrawFromDeckAction(),
]

game = Game.create(123)
print(render_game(game))
for action in test_actions:
    time.sleep(3)
    game.run_action(action)
    print('-------------------------------------')
    print(render_game(game))
