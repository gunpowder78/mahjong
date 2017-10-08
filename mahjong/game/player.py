"""Player"""

class Player(object):
  """Base Player class."""
  def __init__(self):
    self.action_hook = None

  def event_handler(self, game_event, game_state):
    """Handle a game event."""
    pass

  def take_action(self, player_action):
    self.action_hook(player_action)

class HumanPlayer(Player):
  pass

class ComputerPlayer(Player):
  pass


####################
## Player Actions ##
####################

class PlayerAction(object):
  def apply_action(self, game_state):
    """Applies an action."""
    pass

  def is_legal(self, game_state):
    pass

class NullAction(PlayerAction):
  """Player takes no action.

  It's not necessary for Players to send this event, since the GameEngine will
  move from the draw phase after a period of time. The purpose of this action
  is just to indicate to the engine that a player plans to take no action, so
  that a single human player doesn't have to wait more than necessary for
  computer players to choose an action, and so that simulations of four
  computer players can go more quickly.

  Valid only during draw phase.
  """

class DrawAction(PlayerAction):
  """Player draws a tile on their turn.

  Valid only during draw phase.
  """
  pass


class ChowAction(PlayerAction):
  """Player calls a tile for a chow.

  Valid only during draw phase.
  """
  pass


class PongAction(PlayerAction):
  """Player calls a tile for a pong.

  Valid only during draw phase.
  """
  pass


class DiscardAction(PlayerAction):
  """Player discards a tile.

  Valid only during discard phase.
  """
  def __init__(self, tile):
    self.tile = tile

class TileSetAction(PlayerAction):
  """Player reveals a TileSet.

  Valid during call or discard phase.
  """
  def __init__(self, tile_set):
    self.tile_set = tile_set


class HuAction(PlayerAction):
  """Player declares victory.

  Valid during the draw or discard phase.
  """
  pass

