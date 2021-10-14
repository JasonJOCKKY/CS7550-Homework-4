import unittest
import numpy as np
from game import GameState

class GameStateTestCase(unittest.TestCase):
  def setUp(self):
    self.game_state = GameState.create_empty(6, 5)

  def test_heuristic_eval_function(self):
    """test heuristic_eval_function.
    """
    player_id = 1
    state = np.array([[0, 0, 0, 0, 0], 
                      [0, 0, 0, 0, 0], 
                      [0, 2, 1, 0, 0],
                      [0, 2, 2, 1, 0], 
                      [2, 1, 1, 2, 0], 
                      [0, 1, 0, 0, 0]])
    
    game_state = GameState(state)
    actual_h_val = game_state.heuristic_eval_function(player_id)
    expect_h_val = 90
    self.assertEqual(expect_h_val, actual_h_val)

  def test_terminal_eval_function(self):
    """test terminal_eval_function.
    """
    state = np.array([[0, 0, 0, 0, 0], 
                      [0, 0, 0, 0, 0], 
                      [0, 2, 1, 0, 1],
                      [0, 2, 2, 1, 0], 
                      [2, 1, 1, 2, 0], 
                      [0, 1, 0, 0, 0]])

    game_state = GameState(state)
    actual_h_val = game_state.terminal_eval_function()
    expect_h_val = 1
    self.assertEqual(actual_h_val, expect_h_val)

  def test_eval_function(self):
    """test eval_function.
    """
    player_id = 1
    state = np.array([[0, 0, 0, 0, 0], 
                      [0, 0, 0, 0, 0], 
                      [0, 2, 1, 0, 0],
                      [0, 2, 2, 1, 0], 
                      [2, 1, 1, 2, 0], 
                      [0, 1, 0, 0, 0]])

    game_state = GameState(state)

    # if the state is not leave nodes.
    actual_h_val = game_state.eval_function(2, player_id)
    expect_h_val = None
    self.assertEqual(actual_h_val, expect_h_val)

    # if the state is not terminal nodes.
    actual_h_val = game_state.eval_function(4, player_id)
    expect_h_val = 90
    self.assertEqual(actual_h_val, expect_h_val)