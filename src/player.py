from numpy import Infinity
from game import GameState
import time

log_num_called = 0

def find_next_move(game_state: GameState, player_id: int, max_depth: int) -> tuple[int, int]:
  """
    Find the next move for a player on the given game state.
    Uses MINIMAX algorithm.

    Return:
    (row, col): the position for the next move.
  """
  global log_num_called
  log_num_called = 0
  log_time = time.time()
  # The first move should always be the center position
  if game_state.is_empty():
    return (int(game_state.nrow / 2), int(game_state.ncol / 2))

  # Find the move that will give the maximum utility value
  result = None
  value = -Infinity
  for row_i in range(game_state.nrow):
    for col_i in range(game_state.ncol):
      if game_state[row_i][col_i] == 0:
        new_move = (row_i, col_i)
        new_game_state = game_state.next_state(
            next_player(player_id), row_i, col_i)
        new_value = utility_value(
            new_game_state, next_player(player_id), max_depth, 1)
        if value < new_value:
          value = new_value
          result = new_move

  print(f'nodes_generated = {log_num_called}, time = {time.time() - log_time}')
  return result


def utility_value(
        game_state: GameState,
        player_id: int,
        max_depth: int,
        current_depth: int) -> int:
  """
    Recursively calculate the utility value of a given node.
    Termination: depth reached max depth OR game is in terminal state.

    Return:
    int: utulity value
  """
  global log_num_called
  log_num_called += 1
  # Terminal Conditions
  term_eval = game_state.terminal_eval_function()
  if term_eval is not None:
    # Return 2000, -2000, or 0 if game is over.
    if (player_id == 1):
      return term_eval * 2000
    return term_eval * -2000
  if (current_depth >= max_depth):
    # Return h if the game is not over and it got cut off.
    h = game_state.heuristic_eval_function(player_id)
    return h

  # Add all posible moves to the children list
  children = []
  for row_i in range(game_state.nrow):
    for col_i in range(game_state.ncol):
      if game_state[row_i][col_i] == 0:
        new_game_state = game_state.next_state(
            next_player(player_id), row_i, col_i)
        new_v = utility_value(new_game_state, next_player(
            player_id), max_depth, current_depth+1)
        children.append(new_v)

  # if current depth is odd return min
  # if current depth is even return max
  if current_depth % 2 == 0:
    return max(children)
  else:
    return min(children)


def next_player(player_id):
  """
    Determine who should play next based on current player.
  """
  if player_id == 1:
    return 2
  return 1
