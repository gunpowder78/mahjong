import random
import threading
from game import game

class GameSession:

  # MahJong games have 4 players.
  MAX_ALLOWED_CLIENTS = 4

  def __init__(self, game_id):
    self.game_id = game_id
    self.client_to_name = {}
    self.game_in_progress = False
    # self.client_seat_order = None
    # self.game = None

  def can_accept_more_clients(self):
    return len(self.client_to_name) < self.MAX_ALLOWED_CLIENTS

  def has_clients(self):
    return len(self.client_to_name) > 0

  def has_username(self, username):
    return username in self.client_to_name.values()

  def add_client(self, client_id, username):
    if not self.can_accept_more_clients():
      raise RuntimeError('Game ' + game_id + ' is full')
    self.client_to_name[client_id] = username

  def get_players(self):
    return list(self.client_to_name.values())

  def start_new_game(self):
    self.game_in_progress = True
    # self._set_randomized_seating()
    # self.game = game.MahJongState()
    # self.game.begin()
    return self._make_fake_updates('Begin game')

  def make_move(self, client_id, move):
    if not self.game_in_progress:
      raise RuntimeError('Cannot make move. Game ' + game_id + ' has not started')
    return self._make_fake_updates(client_id + ' moved: ' + str(move))

  def _make_fake_updates(self, update):
    updates = {}
    for client in self.client_to_name:
      updates[client] = update
    return updates

  def remove_client(self, client_id):
    if client_id not in self.client_to_name:
      raise RuntimeError('Could not find client in game ' + game_id)
    self.client_to_name.pop(client_id)

    # If a client leaves, there are no longer enough players for the game.
    self.game_in_progress = False

  def close(self):
    # TODO
    pass

