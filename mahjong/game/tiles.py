"""Game tiles."""
import enum


class Tile(object):
  """A representation of a Mahjong tile.

  Attributes:
    value: An integer value of a tile.
    turn: An integer turn number the tile was drawn.
    is_melded:
  """
  def __init__(self, suit, value):
    self.suit = suit
    self.value = value

  def __eq__(self, other):
    return type(self) is type(other) and self.value == other.value

  def __hash__(self):
    return hash((type(self).__name__, value))


class Suit(object):
  TILE_VALUES = {}


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
  pass


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
    'EAST': 0
    'SOUTH': 1
    'WEST': 2
    'NORTH': 3
  }

class Dragon(HonorSuit):
  TILE_VALUES = {
    'GREEN': 0
    'RED': 1
    'WHITE': 2
  }

class Flower(BonusSuit):
  TILE_VALUES = {
    'PLUM': 0
    'ORCHID': 1
    'BAMBOO': 2
    'CHRYSANTHEMUM': 3
  }

class Season(BonusSuit):
  TILE_VALUES = {
    'SPRING': 0
    'SUMMER': 1
    'FALL': 2
    'WINTER': 3
  }

