"""The game engine, which drives the game."""
import enum

from game import exceptions


class Seat(enum.IntEnum):
  """Mahjong seat positions. The turn order is EAST, SOUTH, WEST, NORTH."""
  EAST = 0
  SOUTH = 1
  WEST = 2
  NORTH = 3


class MahjongEngine(object):
  """A game engine responsible for driving the game.

  The game engine runs the game by looping between draw/call/discard states.

  During the draw state, the engine listens for PlayerActions, and .
  Legal player actions includes:
    - DrawAction (from current player): Enter discard phase.
    - ChiAction (from current player): Enter call phase.
    - PengAction (from any player): Enter call phase. Set current player to
      caller.
    - HuAction (from any player): End game.

  During the call state, the engine waits for the player who called the tile to
  reveal which tiles a player is calling the tile with. Legal player actions
  includes:
    - CallAction (from current player): Enter discard phase. If the player uses
      three pieces to call a discard, then the Gong flag is set.

  During the discard state, the engine waits for the player whose turn it is to
  either declare a gong or discard.  If this state is entered with the Gong
  flag set, then the player receives an additional tile.  Legals player actions
  includes:
    - DiscardAction (from current player): Increment
    - GongAction (from current player): In
    - HuAction (from current player)

  TODO(jeffreylu): Too lengthy. Move this description elsewhere.

  The engine is responsible for making sure that a move is legal before
  accepting a PlayerAction.

  Attributes:
    players
  """
  def __init__(self, players, config=None):
    self.players = players
    self.config = config

    for player in players:
      self.initialize_player(player)

  def initialize_player(self, player):
    """Initialize a player."""
    # We don't want to pass the engine directly to players, or else they can
    # see the entire state of the game. Instead we'll pass a hook to the event
    # handler.
    player.action_hook = lambda action: self.event_handler(player, action)

  def event_handler(self, player, action):
    """Handle a player action.

    Raises:
      IllegalMoveException: PlayerAction is illegal.
    """
    pass

  def notify_players(self, game_event):
    """Notify players of a new game event."""
    pass

  def start_game(self):
    pass

