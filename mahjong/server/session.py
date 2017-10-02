import random
import threading
from game import game

class GameSession:

  # MahJong games have 4 players.
  MAX_ALLOWED_CLIENTS = 4

  def __init__(self):
    self.client_to_name = {}
    # self.client_seat_order = None
    # self.game = None

  def can_accept_more_clients(self):
    return len(self.client_to_name) < self.MAX_ALLOWED_CLIENTS

  def has_clients(self):
    return len(self.client_to_name) > 0

  def add_client(self, client_id, username):
    if not self.can_accept_more_clients():
      # TODO:
      pass
    self.client_to_name[client_id] = username

  def get_players(self):
    return list(self.client_to_name.values())

  def start_new_game(self):
    # self._set_randomized_seating()
    # self.game = game.MahJongState()
    # self.game.begin()
    return self._make_fake_updates('Begin game')

  def make_move(self, client_id, move):
    return self._make_fake_updates(client_id + ' moved: ' + str(move))

  def _make_fake_updates(self, update):
    updates = {}
    for client in self.client_to_name:
      updates[client] = update
    return updates

  def remove_client(self, client_id):
    if client_id not in self.client_to_name:
      # TODO:
      pass
    del self.client_to_name[client_id]

  def close(self):
    # TODO
    pass

