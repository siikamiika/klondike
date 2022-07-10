import time
from .game import Game
from .ui import (
    render_card_name,
    render_card_unicode,
    render_game,
)
# from .cards import (
#     Suit,
# )
# from .actions import (
#     Action,
#     DrawFromDeckAction,
#     MoveFromWasteToPileAction,
#     MoveFromFoundationToPileAction,
#     MoveFromPileToPileAction,
#     MoveFromWasteToFoundationAction,
#     MoveFromPileToFoundationAction,
# )

# test_actions = [
#     DrawFromDeckAction(),
#     MoveFromPileToFoundationAction(source_pile_index=5, target_foundation_suit=Suit.SPADES),
#     MoveFromPileToPileAction(source_pile_index=4, target_pile_index=3, count=1),
#     MoveFromPileToPileAction(source_pile_index=3, target_pile_index=4, count=2),
#     MoveFromWasteToPileAction(target_pile_index=2)
# ]

# game = Game.create(123)
# print(render_game(game))
# print(render_game(game))
# for action in test_actions:
#     print(action)
#     time.sleep(1)
#     game.run_action(action)
#     print(render_game(game))

game = Game.create()
while True:
    print(render_game(game))
    actions = game.get_possible_actions()
    for i, action in enumerate(actions):
        print(f'{i + 1}.', action.to_text())
    try:
        chosen_idx = int(input()) - 1
        chosen_action = actions[chosen_idx]
    except Exception as e:
        print(e)
        continue
    game.run_action(chosen_action)
