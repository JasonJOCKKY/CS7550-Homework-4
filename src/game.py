import numpy as np
from numpy.core.fromnumeric import shape

from typing import List
# Represents the directions on the gameboard.
# tr(1, 1), t(0, 1), br(1, -1), r(1, 0)
# Remember to also expand in the oposite direction.
DIRECTIONS = np.array([
    np.array([1, 1]),
    np.array([0, 1]),
    np.array([1, -1]),
    np.array([1, 0])
])


class GameState:
  """
    A class representing the state of two-player four-in-a-row game.
    The game board is represented with a 2D array.
    State of a single position on the game board can be retrieved directly with [] notation:
      0: No mark.
      1: Player 1 mark.
      2: Player 2 mark.
  """
  def __init__(self, game_board: np.array):
    """
      Constructor for the class.
      :param game: An 2D array that represents the game board.
    """
    
    self.__game_board = game_board
    self.nrow = game_board.shape[0]
    self.ncol = game_board.shape[1]

  @classmethod
  def CREATE_EMPTY(cls, row, col):
    """
      Construct a new 'GameState' object with empty playing board.
      :param row: Number of rows on the game board.
      :param col: Number of columns on the game board.
      :return: returns nothing
    """
    game_board = np.zeros((row, col), dtype=np.int8)
    return cls(game_board)
  
  def __getitem__(self, row):
    return self.__game_board[row]

  # NOT FINISHED YET 
  def next_state(self, player, row, col):
    """
      Generated a new GameState based on the move that a player makes.
      :param player: 1 or 2
      :param row, col: the position for the next move
      :return: a new GameState object
    """
    new_game_board = np.copy(self.__game_board)
    new_game_board[row][col] = player
    new_player_h = np.copy(self.__player_h)

    def __location_within_range(location):
      return (location[0] in range(self.__game_board.shape[0])
              and location[1] in range(self.__game_board.shape[1]))

    # try to find consecutive pieces of player
    # expand in + and - direction
    for d in DIRECTIONS:
      a = 2  # a sides open
      b = 0  # b in a row
      expand_dir = [-1, 1]
      p = np.array([row, col])
      while b < 4 and a > 0:
        for k in expand_dir:
          current_location = p + d * b * k
          if not __location_within_range(current_location):
            a -= 1
          else:
            current_value = new_game_board[current_location[0]][current_location[1]]
            if current_value == player:
              b += 1
            else:
              expand_dir.remove(k)
              if current_value != 0:
                a -= 1
      if b == 4:
        return "win"
      if b > 1:
        new_player_h[player][a][b] += 1

    return GameState(new_game_board, new_player_h)

  def get_board_ids(self):
    """Get players ids in each row, columns, and diagnoals.

    Example:
    state = [[1, 2], 
             [3, 4]]
    board_ids = [[1, 2], [3, 4], 
                 [1, 3], [2, 4], 
                 [1], [3, 2], [4], 
                 [2], [1, 4], [3]]

    Returns:
        List[List[str]]: List of ids in each row, columns, and diagnoals.
    """

    state = self.__game_board
    nrow = state.shape[0]
    ncol = state.shape[1]

    # Player IDs in rows.
    board_ids = [state[i].tolist() for i in range(0, nrow)]

    # Player IDs in columns.
    board_ids += [state[:,i].tolist() for i in range(0, ncol)]

    # Player IDs in upper-left-to-lower-right diagonals.
    board_ids += [state[::-1,:].diagonal(i).tolist() for i in range(-nrow+1,ncol)]

    # Player IDs in lower-left-to-upper-right diagonals.
    board_ids += [state.diagonal(i).tolist() for i in range(ncol-1,-nrow,-1)]

    return board_ids


  def count_pattern(self, player_ids: List[int], patterns: List[str]):
    """Count the number of pattern in the given players ids.

    Args:
        player_ids (List[int]): list of players ids in game board.
        patterns (List[str]): list of pattern.

    Returns:
        int: number of patterns in the board.
    """
    id_str = "".join(map(str, player_ids))
    num = 0
    for pattern in patterns:
      num += id_str.count(pattern)
    return num

  def heuristic_eval_function(self, player_id: int):
    """Calculate the heuristic value for non-terminal nodes.

    h(n) = 100*[numberof two-side-open-3-in-a-row for me]
          –10*[numberof two-side-open-3-in-a-row for opponent] 
          +100*[numberof one-side-open-3-in-a-row for me]
          –5*[numberof one-side-open-3-in-a-row for opponent]
          +2*[numberof two-side-open-2-in-a-row for me]
          –2*[numberof two-side-open-2-in-a-row for opponent] 
          +[numberof one-side-open-2-in-a-row for me]
          –[numberof one-side-open-2-in-a-row for opponent]

    Args:
        player_id (int): ID for player.

    Return:
        int, heuristic value. 
    """
    # play 1
    two_side_open_3_first = 0
    one_side_open_3_first = 0
    two_side_open_2_first = 0
    one_side_open_2_first = 0

    # play 2
    two_side_open_3_second = 0
    one_side_open_3_second = 0
    two_side_open_2_second = 0
    one_side_open_2_second = 0

    board_ids = self.get_board_ids()

    # count the patterns in board.
    for player_ids in board_ids:
      
      # play 1
      for pattern in ["01110", "0111", "1110", "0110", "011", "110"]:
        num = self.count_pattern(player_ids, [pattern])
        if num > 0:
          if pattern == "01110":
            two_side_open_3_first += num
          elif pattern == "0111" or pattern == "1110":
            one_side_open_3_first += num
          elif pattern == "0110":
            two_side_open_2_first += num
          else:
            one_side_open_2_first += num
          break
      
      # play 2
      for pattern in ["02220", "0222", "2220", "0220", "022", "220"]:
        num = self.count_pattern(player_ids, [pattern])
        if num > 0:
          if pattern == "02220":
            two_side_open_3_second += num
          elif pattern == "0222" or pattern == "2220":
            one_side_open_3_second += num
          elif pattern == "0220":
            two_side_open_2_second += num
          else:
            one_side_open_2_second += num
          break

    h_val = None
    if player_id == 1:
      h_val = (100 * two_side_open_3_first - 10 * two_side_open_3_second +
              100 * one_side_open_3_first - 5 * one_side_open_3_second +
              2 * two_side_open_2_first - 2 * two_side_open_2_second +
              1 * one_side_open_2_first - 1 * one_side_open_2_second)

    if player_id == 2:
      h_val = (100 * two_side_open_3_second - 10 * two_side_open_3_first +
              100 * one_side_open_3_second - 5 * one_side_open_3_first +
              2 * two_side_open_2_second - 2 * two_side_open_2_first +
              1 * one_side_open_2_second - 1 * one_side_open_2_first)

    return h_val
  
  def terminal_eval_function(self):
    """Check whether the state is final state.

    The player who succeeds in placing 4 of their marks consecutively 
    in a horizontal, vertical, or diagonal row wins the game.

    Return:
        If the state is final state, return their utility value: -1, 0, or 1. 
        Otherwise, return `None` means the it is not terminal node.
    """
    board_ids = self.get_board_ids()
    nrow = self.__game_board.shape[0]
    ncol = self.__game_board.shape[1]
    
    # check winner
    for player_ids in board_ids:
      if self.count_pattern(player_ids, ["1111"]) > 0:
        return 1
      if self.count_pattern(player_ids, ["2222"]) > 0:
        return -1
    
    # check drawn
    if np.count_nonzero(self.__game_board) == nrow*ncol:
      return 0
    
    return None

  def eval_function(self, depth: int, player_id: int):
    """get the value of unity value or heuristic value.

    The function return `None` if state is not in leave nodes.
    If the state is terminal nodes, return the unity value (-1, 0, 1).
    If the state is non-terminal nodes, return heuristic value.

    Args:
        depth (int): depth of tree.
        player_id (int): id of player.

    Returns:
        int: value calculated by evaluation function. `None` if the state is not
        a leave nodes.
    """

    
    # For terminal nodes, return their utility value: -1, 0, or 1.
    value = self.terminal_eval_function()
    if value is not None:
      return value
    
    # TODO(Jingsong/Jiuyi): modify the constant 4 to be a variable.
    if depth >= 4:
      return self.heuristic_eval_function(player_id)
    
    return None


def main():
  g = GameState.CREATE_EMPTY(6, 5)
  print(g[5][4])
  # print(g.__player_h)
  g.next_state(1, 2, 3)


if __name__ == "__main__":
  main()
