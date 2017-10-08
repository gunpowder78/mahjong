"""Game state."""


class MahjongState(object):
  """The state of a Mahjong game.

  Attributes:
    deck: a list of Tile objects to draw from.
  """
  def __init__(self):
    self.config = config
    self.deck = []
    self.hands = []
    self.turn_count = 0

  def copy(self, seat=None):
    """Creates a new copy of a MahjongState.

    Arguments:
      seat: The MahjongState, as visible to a seat.
    """
    pass

  def apply_game_event(self, game_event):
    """Updates the state of the game by applying a game event."""

  def score(self, seat):
    """Score the hand of a seat.

    Returns the score of a seat's hand. The hand does not need to be legal or
    even completed to be scored.
    """
    pass


class PlayerState(MahjongState):
  def __init__(self, seat, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.seat = seat

  @property
  def player_hand(self):
    return self.hands[self.player]

  @classmethod
  def from_state(cls, state, player):
    state = cls()


class SeatPosition(enum.IntEnum):
  """Mahjong seat positions. The turn order is EAST, SOUTH, WEST, NORTH."""
  EAST = 0
  SOUTH = 1
  WEST = 2
  NORTH = 3


class Hand(object):
  def __init__(self):
    self.tiles = []
    self.open_sets = []


#################
## Game Events ##
#################

class GameEvent(object):
  def __init__(self, seat):
    self.seat = seat


class TileSetEvent(object):
  """A player reveals a TileSet.

  Revealing a tile set only reveals that a tile set exists, not necessarily the
  tiles that make up a set, as in the case of declaring a concealed kong.

  Attributes:
    tile_set: The revealed TileSet.
  """
  def __init__(self, seat, tile_set):
    super().__init__(seat)
    self.tile_set = tile_set


class DrawEvent(object):
  """A player draws a Tile.

  Attributes:
    tile: The drawn Tile.
  """
  def __init__(self, seat, tile):
    super().__init__(seat)
    self.tile = tile


class DiscardEvent(object):
  """A player discards a Tile.

  Attributes:
    tile: The discarded Tile.
  """
  def __init__(self, seat, tile):
    super().__init__(seat)
    self.tile = tile


class HuEvent(GameEvent):
  """A player declares victory.

  Ends a game.  All hands should be revealed at this point.

  Attributes:
    hands: A list of hands
  """
  def __init__(self, hands):

