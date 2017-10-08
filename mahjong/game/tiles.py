"""Game tiles."""


class Tile(object):
  """A representation of a Mahjong tile.

  Attributes:
    value: An integer value of a tile.
    turn: An integer turn number the tile was drawn.
    seat: An integer indicating the seat that drew this tile.
    draw_num: The tile number, indicating the order this was drawn.
  """
  def __init__(self, suit, value):
    self.suit = suit
    self.value = value
    self.seat = None

  def __eq__(self, other):
    return type(self) is type(other) and self.value == other.value

  def __hash__(self):
    return hash((type(self).__name__, value))


class Suit(object):
  TILE_VALUES = {}
  NUM_TILES = 4


class SerialSuit(Suit):
  TILE_VALUES = {
    'ONE': 1
    'TWO': 2
    'THREE': 3
    'FOUR': 4
    'FIVE': 5
    'SIX': 6
    'SEVEN': 7
    'EIGHT': 8
    'NINE': 9
  }


class HonorSuit(Suit):
  pass


class BonusSuit(Suit):
  NUM_TILES = 1


###########
## Suits ##
###########

class Dot(SerialSuit):
  pass


class Bamboo(SerialSuit):
  pass


class Character(SerialSuit):
  pass


class Wind(HonorSuit):
  TILE_VALUES = {
    'EAST': 'EAST',
    'SOUTH': 'SOUTH',
    'WEST': 'WEST',
    'NORTH': 'NORTH',
  }

class Dragon(HonorSuit):
  TILE_VALUES = {
    'GREEN': 'GREEN',
    'RED': 'RED',
    'WHITE': 'BLUE',
  }

class Flower(BonusSuit):
  TILE_VALUES = {
    'PLUM': 'PLUM',
    'ORCHID': 'ORCHID',
    'BAMBOO': 'BAMBOO',
    'CHRYSANTHEMUM': 'CHRYSANTHEMUM',
  }

class Season(BonusSuit):
  TILE_VALUES = {
    'SPRING': 'SPRING',
    'SUMMER': 'SUMMER',
    'FALL': 'FALL',
    'WINTER': 'WINTER',
  }


###############
## Tile Sets ##
###############

class TileSet(object):
  def __init__(self, tiles, hidden=True):
    self.tiles = tuple(tiles)
    self.hidden = hidden

  def find_in_tiles(self, tiles):
    raise NotImplementedError

class ChowSet(TileSet):
  def __init__(self, tiles, hidden=True):
    self.tiles = tuple(tiles)
    self.hidden = hidden

class PongSet(TileSet):
  pass

class KongSet(PongSet):
  pass

class WeavedSet(TileSet):
  pass

