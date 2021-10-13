import numpy as np
from numpy.core.fromnumeric import shape

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

  def __init__(self, game, player_h):
    """
      Constructor for the class.
      :param game: An 2D array that represents the game board.
      :player_h: Stores player huristic values. 
                 "a-side-open-b-in-a-row" is stored in player_h[player][a][b]
    """
    self.__game = game
    self.__player_h = player_h

  @classmethod
  def CREATE_EMPTY(cls, row, col):
    """
      Construct a new 'GameState' object with empty playing board.
      :param row: Number of rows on the game board.
      :param col: Number of columns on the game board.
      :return: returns nothing
    """
    game = np.zeros((row, col), dtype=np.int8)
    player_h = np.zeros((2, 3, 4), dtype=np.int0)
    return cls(game, player_h)

  def __getitem__(self, row):
    return self.__game[row]

  # NOT FINISHED YET 
  def next_state(self, player, row, col):
    """
      Generated a new GameState based on the move that a player makes.
      :param player: 1 or 2
      :param row, col: the position for the next move
      :return: a new GameState object
    """
    new_game = np.copy(self.__game)
    new_game[row][col] = player
    new_player_h = np.copy(self.__player_h)

    # “one-side-open-3-in-a-row”: there is an empty space next to one end of a 3-
    #   in-a-row to potentially make it 4-in-a row in the next move.
    # “two-side-open-3-in-a-row”: there are empty spaces next to both ends of a 3-
    #   in-a-row to potentially make it 4-in-a row in the next move.
    # “one-side-open-2-in-a-row”: there is an empty space next to one end of a 2-
    #   in-a-row to potentially make it 3-in-a row in the next move.
    # “two-side-open-2-in-a-row”: there are empty spaces next to both ends of a 2-
    #   in-a-row to potentially make it 3-in-a row in the next move.

    def __location_within_range(location):
      return (location[0] in range(self.__game.shape[0])
              and location[1] in range(self.__game.shape[1]))

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
            current_value = new_game[current_location[0]][current_location[1]]
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

    return GameState(new_game, new_player_h)


g = GameState.CREATE_EMPTY(6, 5)
print(g[5][4])
print(g.__player_h)
g.next_state(1, 2, 3)
