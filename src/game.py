import numpy as np

from typing import List


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

  def __str__(self) -> str:
    return str(self.__game_board)

  def is_empty(self):
    for row_v in self.__game_board:
      for col_v in row_v:
        if (col_v != 0):
          return False

    return True

  def next_state(self, player, row, col):
    """
      Generated a new GameState based on the move that a player makes.
      :param player: 1 or 2
      :param row, col: the position for the next move
      :return: a new GameState object
    """
    new_game_board = np.copy(self.__game_board)
    new_game_board[row][col] = player

    return GameState(new_game_board)

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
    board_ids += [state[:, i].tolist() for i in range(0, ncol)]

    # Player IDs in upper-left-to-lower-right diagonals.
    board_ids += [state[::-1, :].diagonal(i).tolist()
                  for i in range(-nrow+1, ncol)]

    # Player IDs in lower-left-to-upper-right diagonals.
    board_ids += [state.diagonal(i).tolist() for i in range(ncol-1, -nrow, -1)]

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

  def heuristic_eval_function(self, player_id: int) -> int:
    """Calculate the heuristic value for non-terminal nodes.

    h(n) = 100*[numberof two-side-open-3-in-a-row for me]
          ???10*[numberof two-side-open-3-in-a-row for opponent] 
          +100*[numberof one-side-open-3-in-a-row for me]
          ???5*[numberof one-side-open-3-in-a-row for opponent]
          +2*[numberof two-side-open-2-in-a-row for me]
          ???2*[numberof two-side-open-2-in-a-row for opponent] 
          +[numberof one-side-open-2-in-a-row for me]
          ???[numberof one-side-open-2-in-a-row for opponent]

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
        1: Player 1 win
        0: Draw
        -1: Player 2 win 
        None: means the it is not terminal node.
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
