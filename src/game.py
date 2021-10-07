class Game:
  """
    A class representing the two-player four-in-a-row game.
    The game board is represented with a 2D array.
    State of a position on the game board can be retrieved directly with [] notation:
      0: No mark.
      1: Player 1 mark.
      2: Player 2 mark.
  """
  def __init__(self, row, col):
    """
      Construct a new 'Game' object with empty playing board.
      :param row: Number of rows on the game board.
      :param col: Number of columns on the game board.
      :return: returns nothing
    """
    self.game = [[0]*col]*row
    self.player1_h = [[0]*3]*4
    self.player2_h = [[0]*3]*4
  
  def __getitem__(self, row):
    return self.game[row]

  def makeMove(self, player, row, col):
    return 

g = Game(6, 5)
print(g[5][4])