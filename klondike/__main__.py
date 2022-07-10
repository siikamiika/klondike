from .game import Game
from .ui import (
    render_game,
)

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
