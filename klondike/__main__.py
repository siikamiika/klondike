from .game import Game
from .ui import (
    render_game,
)

game = Game.create()
while True:
    print(render_game(game))
    print('0. Undo')
    actions = game.get_possible_actions()
    for i, action in enumerate(actions):
        print(f'{i + 1}.', action.to_text())
    try:
        chosen_idx = int(input()) - 1
        if chosen_idx == -1:
            chosen_action = 'undo'
        else:
            chosen_action = actions[chosen_idx]
    except Exception as e:
        print(e)
        continue
    if chosen_action == 'undo':
        game.undo()
    else:
        game.run_action(chosen_action)
