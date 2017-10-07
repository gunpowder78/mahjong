"""Game logic."""
import random

class MahjongState(object):
  """The state of a Mahjong game.

  Attributes:
    tiles: a list of Tile objects
  """
  def __init__(self, players, config):
    self.config = config
    self.deck = []

  def copy(self):
    """Creates a new copy of a MahjongState."""
    pass

  def score(self, seat):
    """Score the .

    Returns the score of a hand. The hand does not need to be legal or even
    completed to be scored.
    """
    pass


class PlayerState(MahjongState):
  """The state of a game, as visible to a player."""
  @staticmethod
  def player_state(mahjong_state, player):
    player_state = PlayerState()


class Player(object):
    def __init__(self)


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

  def __init__(self, prevalent_wind):
    self.prevalent_wind = prevalent_wind
    self.wall = Wall()
    self.discarded_tiles = []

    self.players = [Player() for _ in range(4)]

    # The game starts with EAST about to discard a piece.
    self.current_player = Player.EAST
    self.waiting_to_discard = True
    self.allowed_actions = [[] for _ in range(4)]
    self.buffered_actions = [None for _ in range(4)]

  def begin(self):
    """Initiates the beginning of the game, where players draw tiles into their hands and resolve
    flowers. Returns a map of seat -> StateDiff, where StateDiff represents the initial game setup
    that the player can see.
    """
    # Each player alternates getting sets of 4, a total of 3 times per player.
    for i in range(3):
      for player in self.players:
        for _ in range(4):
          player.add_tile_to_hand(self.wall.draw_from_front())

    # In real life, the first player does a "jump" here. For simplicity, we just draw the first two
    # pieces.
    self.players[Player.EAST].add_tile_to_hand(self.wall.draw_from_front())
    self.players[Player.EAST].add_tile_to_hand(self.wall.draw_from_front())

    # The rest of the players get one extra piece each.
    self.players[Player.SOUTH].add_tile_to_hand(self.wall.draw_from_front())
    self.players[Player.WEST].add_tile_to_hand(self.wall.draw_from_front())
    self.players[Player.NORTH].add_tile_to_hand(self.wall.draw_from_front())

    # Now resolve flowers
    for player in self.players:
      for _ in range(player.num_flowers()):
        self.players.add_tile_to_hand(self.wall.draw_from_back())

    # Fill up the allowed actions for each player.
    for seat in range(4):
      allowed_actions[seat] = self.get_actions(seat)

    # TODO: return each player's view

  def take_action(self, seat, action):
    """Applies a Move to the game state, and returns a map of seat -> StateDiff
    """
    if action not in self.allowed_actions[seat]:
      raise IllegalActionException('Player {0} cannot take action {1}')
    self.buffered_action[seat] = action

    player_to_act = self.player_with_highest_priority_action()
    if player_to_act is not None:
      return self.apply_action(player_to_act, self.buffered_actions[player_to_action])
    else:
      # TODO: find a better representation of nothing happening.
      return None

  def apply_action(self, seat, action):
    player = self.players[seat]

    if isinstance(action, DiscardAction):
      self.discarded_tiles.append(action.piece)
      player.remove_tile_from_hand(action.piece)
      player.set_drawn_tile(None)
      self.current_player = self.get_next_player()
      self.waiting_to_discard = False
    elif isinstance(action, PassAction):
      # This should never happen. At the very least, one player should be able to draw.
      raise RuntimeError(
          'Chosen action for {0} is to pass, but expected someone to draw.'.format(seat))
    elif isinstance(action, DrawAction):
      tile = wall.draw_From_front()
      player.add_tile_to_hand(tile)
      while tile in FLOWERS:
        tile = wall.draw_from_back()
        player.add_tile_to_hand(tile)
      # After getting a non-flower, set this as the drawn tile.
      player.set_drawn_tile(tile)

      # The current player should have already been this player, but set it anyway just to be safe.
      self.current_player = seat
      self.waiting_to_discard = True
    elif isinstance(action, MeldAction):
      player.add_melded_set(action.tile_set)

      # Special case is a self-drawn hidden kong, which doesn't take from the discard pile.
      # In all other cases, take the last discarded piece.
      tiles_to_remove = list(action.tile_set.pieces)
      if not (isinstance(action.tile_set, KongSet) and action.tile_set.hidden):
        tiles_to_remove = list(action.tile_set.pieces)
        discarded_tile = self.remove_last_discarded_tile()
        tiles_to_remove.remove(discarded_tile)

      for tile in tiles_to_remove:
        player.remove_tile_from_hand(tile)

      # This player stole the turn.
      self.current_player = seat
      self.waiting_to_discard = True
    elif isinstance(action, WinAction):
      # TODO:
      pass
    else:
      raise RuntimeError('Unrecognized action: {0}'.format(action))


    for seat in range(4):
      self.buffered_actions[seat] = None
      self.allowed_actions[seat] = self.get_actions(seat)

    # TODO: return state diff

  def get_actions(self, seat):
    player = self.players[seat]
    if self.waiting_to_discard:
      if seat != self.current_player:
        # While waiting for a player to discard, the other players can't do anything.
        return []
      else:
        hidden_tiles = player.get_hidden_tiles()
        # The player can always discard any of their pieces
        actions = [DiscardAction(piece) for piece in hidden_tiles]

        # The player is also allowed to make a hidden kong, if possible.
        actions.extend(
            [MeldAction(kong_set) for kong_set in KongSet.find_in_tiles(hidden_tiles)])

        if self.can_win(seat, hidden_tiles):
          actions.append(WinAction())
        return actions

    # Otherwise, the previous player just discarded. Add the discarded tile to a copy of the
    # player's tiles, to calculate what actions they can take. This doesn't actually add the tile
    # to their hand yet.
    discarded_tile = self.get_last_discarded_tile()
    hidden_tiles = player.get_hidden_tiles()
    hidden_tiles.append(discarded_tile)

    if self.current_player == seat:
      # The current player can always draw.
      actions = [DrawAction()]
      actions.extend(
        [MeldedAction(tile_set) for tile_set in ChowSet.find_in_tiles(hidden_tiles)])
      actions.extend(
        [MeldedAction(tile_set) for tile_set in PongSet.find_in_tiles(hidden_tiles)])
      actions.extend(
        [MeldedAction(tile_set) for tile_set in KongSet.find_in_tiles(hidden_tiles)])

      if self.can_win(seat, hidden_tiles):
        actions.append(WinAction())
      return actions

    else:
      actions = []
      actions.extend(
        [MeldedAction(tile_set) for tile_set in ChowSet.find_in_tiles(hidden_tiles)])
      actions.extend(
        [MeldedAction(tile_set) for tile_set in PongSet.find_in_tiles(hidden_tiles)])
      actions.extend(
        [MeldedAction(tile_set) for tile_set in KongSet.find_in_tiles(hidden_tiles)])

      if self.can_win(seat, hidden_tiles):
        actions.append(WinAction())

      # Only allow the player to pass if she has other options available.
      if len(actions) > 0:
        actions.append(PassAction())
      return actions

  def can_win(self, seat, tiles):
    player = self.players[seat]
    # TODO: find the sets in the tiles, and combine with their melded sets.
    return False

  def get_last_discarded_tile(self):
    if len(self.discarded_tiles) == 0:
      raise IndexError('No tiles have been discarded')
    return self.discarded_tiles[len(self.discarded_tiles) - 1]

  def remove_last_discarded_tile(self):
    if len(self.discarded_tiles) == 0:
      raise IndexError('No tiles have been discarded')
    return self.discarded_tiles.pop(len(self.discarded_tiles) - 1)

  def get_next_player(self):
    return (self.current_player + 1) % 4

  def player_with_highest_priority_action(self):
    # TODO: check buffered actions against allowed actions.
    # win > kong, pong > chow > draw, pass
    pass

  def end_game(self):
    # TODO
    pass

class IllegalMoveException(RuntimeError):
  pass

class Wall:
  def __init__(self):
    self.tiles = list(ALL_TILES)
    random.shuffle(self.tiles)

    self.front_index = 0
    self.end_index = len(self.tiles) - 1

  def __len__(self):
    return self.end_index - self.front_index + 1

  def draw_from_front(self):
    if len(self) <= 0:
      raise IndexError('No more tiles in wall')
    front_index = self.front_index
    self.front_index += 1
    return self.tiles[front_index]

  def draw_from_back(self):
    if len(self) <= 0:
      raise IndexError('No more tiles in wall')
    back_index = self.back_index
    self.back_index -= 1
    return self.tiles[back_index]


class Player:
  EAST = 0
  SOUTH = 1
  WEST = 2
  NORTH = 3

  def __init__(self):
    self.hidden_tiles = []
    self.melded_sets = []
    self.flowers = 0
    self.drawn_tile = None

  def num_flowers(self):
    return self.flowers

  def get_hidden_tiles(self):
    return list(self.hidden_tiles)

  def add_tile_to_hand(self, tile):
    if tile in FLOWERS:
      self.flowers += 1
    else:
      self.hidden_tiles.append(tile)

  def set_drawn_tile(self, tile):
    self.drawn_tile = tile

  def add_melded_set(self, tile_set):
    self.melded_sets.append(tile_set)

  def remove_tile_from_hand(self, tile):
    self.hidden_tiles.remove(tile)

# Tiles

class Tile:
  DOT1 = 'DOT1'
  DOT2 = 'DOT2'
  DOT3 = 'DOT3'
  DOT4 = 'DOT4'
  DOT5 = 'DOT5'
  DOT6 = 'DOT6'
  DOT7 = 'DOT7'
  DOT8 = 'DOT8'
  DOT9 = 'DOT9'

  CHAR1 = 'CHAR1'
  CHAR2 = 'CHAR2'
  CHAR3 = 'CHAR3'
  CHAR4 = 'CHAR4'
  CHAR5 = 'CHAR5'
  CHAR6 = 'CHAR6'
  CHAR7 = 'CHAR7'
  CHAR8 = 'CHAR8'
  CHAR9 = 'CHAR9'

  BAMBOO1 = 'BAMBOO1'
  BAMBOO2 = 'BAMBOO2'
  BAMBOO3 = 'BAMBOO3'
  BAMBOO4 = 'BAMBOO4'
  BAMBOO5 = 'BAMBOO5'
  BAMBOO6 = 'BAMBOO6'
  BAMBOO7 = 'BAMBOO7'
  BAMBOO8 = 'BAMBOO8'
  BAMBOO9 = 'BAMBOO9'

  EAST = 'EAST'
  SOUTH = 'SOUTH'
  WEST = 'WEST'
  NORTH = 'NORTH'

  DRAGON_WHITE = 'DRAGON_WHITE'
  DRAGON_GREEN = 'DRAGON_GREEN'
  DRAGON_RED = 'DRAGON_RED'

  FLOWER_RED = 'FLOWER_RED'
  FLOWER_BLUE = 'FLOWER_BLUE'

ALL_TILES = {
  Tile.DOT1,
  Tile.DOT2,
  Tile.DOT3,
  Tile.DOT4,
  Tile.DOT5,
  Tile.DOT6,
  Tile.DOT7,
  Tile.DOT8,
  Tile.DOT9,

  Tile.CHAR1,
  Tile.CHAR2,
  Tile.CHAR3,
  Tile.CHAR4,
  Tile.CHAR5,
  Tile.CHAR6,
  Tile.CHAR7,
  Tile.CHAR8,
  Tile.CHAR9,

  Tile.BAMBOO1,
  Tile.BAMBOO2,
  Tile.BAMBOO3,
  Tile.BAMBOO4,
  Tile.BAMBOO5,
  Tile.BAMBOO6,
  Tile.BAMBOO7,
  Tile.BAMBOO8,
  Tile.BAMBOO9,

  Tile.EAST,
  Tile.SOUTH,
  Tile.WEST,
  Tile.NORTH,

  Tile.DRAGON_WHITE,
  Tile.DRAGON_GREEN,
  Tile.DRAGON_RED,

  Tile.FLOWER_RED,
  Tile.FLOWER_BLUE,
}

FLOWERS = {Tile.FLOWER_RED, Tile.FLOWER_BLUE}

# Actions

class Action:
  DRAW = 0
  CHOW = 1
  PONG = 2
  KONG = 3
  WIN = 4
  PASS = 5
  DISCARD = 6

  def __eq__(self, other):
    return instance(other, type(self))

class DrawAction(Action):
  pass

class MeldAction(Action):
  def __init__(self, tile_set):
    self.tile_set = tile_set

  def __eq__(self, other):
    return super().__eq__(other) and self.tile_set == other.tile_set

class PassAction(Action):
  pass

class WinAction(Action):
  pass

class DiscardAction(Action):
  def __init__(self, piece):
    self.piece = piece

  def __eq__(self, other):
    return super().__eq__(other) and self.piece == other.piece

# Sets

class TileSet:
  def find_in_tiles(self, tiles):
    raise NotImplementedError

  def __eq__(self, other):
    return isinstance(other, type(self)) and self.pieces == other.pieces

class ChowSet(TileSet):
  def __init__(self, pieces):
    self.pieces = pieces

  @staticmethod
  def find_in_tiles(self, tiles):
    # TODO
    pass

class PongSet(TileSet):
  def __init__(self, piece):
    self.piece = piece

  @property
  def pieces(self):
    return [self.piece for _ in range(3)]

  @staticmethod
  def find_in_tiles(self, tiles):
    # TODO
    pass

class KongSet(TileSet):
  def __init__(self, piece, hidden):
    self.piece = piece
    self.hidden = hidden

  def __eq__(self, other):
    return super().__eq__(other) and self.hidden == other.hidden

  @property
  def pieces(self):
    return [self.piece for _ in range(4)]

  @staticmethod
  def find_in_tiles(self, tiles):
    # TODO: these should all be hidden
    pass

