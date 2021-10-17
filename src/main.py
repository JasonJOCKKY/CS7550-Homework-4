from player import find_next_move, next_player
from game import GameState


ROW = 6
COL = 5
g = GameState.CREATE_EMPTY(ROW, COL)
player_id = 1

print("Empty Game Board Created")
print(g)

term_value = g.terminal_eval_function()
while term_value is None:
  move = find_next_move(g, player_id, player_id*2)
  g = g.next_state(player_id, move[0], move[1])
  print(f'player {player_id}: {move}')
  print(g)
  player_id = next_player(player_id)
  term_value = g.terminal_eval_function()

if term_value == 1:
  print("player 1 wins")
elif term_value == -1:
  print("player 2 wins")
else:
  print("draw")