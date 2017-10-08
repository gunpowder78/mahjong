"""Game Exceptions."""

class GameException(Exception):
  """Base game exception."""
  pass

class IllegalTileSetException(GameException):
  pass

class IllegalMoveException(GameException):
  pass

