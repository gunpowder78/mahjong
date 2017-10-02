"""Game logic. Unaware of """

class Seat:
  """Mahjong labels each seat with a wind. The turn order is EAST, SOUTH, WEST,
  NORTH.
  """
  EAST = 0
  SOUTH = 1
  WEST = 2
  NORTH = 3

class Move:
  """A single player's move."""
  pass

class StateDiff:
  """Diff a single player's view of the game. Here, diff means the change in
  state caused by the latest action.
  """
  # TODO
  pass

class MahJongState:

  def begin(self):
    """Initiates the beginning of the game, where players draw tiles into their
    hands and resolve flowers. Returns a map of seat -> StateDiff, where
    StateDiff represents the initial game setup that the player can see.
    """
    # TODO

  def accept_move_from(self, seat, move):
    """Applies a Move to the game state, and returns a map of seat -> StateDiff
    """
    # TODO
    pass

  def end_game(self):
    # TODO
    pass
