import threading
from game import game

class GameSession:

  # MahJong games have 4 players.
  MAX_ALLOWED_CLIENTS = 4

  def __init__(self):
    self.clients = set()
    self.game = None
    self.lock = threading.RLock()

  def can_accept_more_clients(self):
    self.lock.acquire()
    try:
      return len(self.clients) < self.MAX_ALLOWED_CLIENTS
    finally:
      self.lock.release()

  def has_clients(self):
    self.lock.acquire()
    try:
      return len(self.clients) > 0
    finally:
      self.lock.release()

  def add_client(self, client_id):
    self.lock.acquire()
    try:
      if not self.can_accept_more_clients():
        # TODO:
        pass
      self.clients.add(client_id)
    finally:
      self.lock.release()

  def begin_game(self):
    # TODO: setup mapping of clients to player seats(winds)
    self.game = game.MahJongState()
    self.game.begin()

  def accept_move_from(self, client_id, move):
    # TODO
    print('Got move from client: ' + str(client_id))
    updates = {}
    for client in self.clients:
      updates[client] = client_id
    return updates

  def restart_game(self):
    self.game.end_game()
    self.begin_game()

  def remove_client(self, client_id):
    self.lock.acquire()
    try:
      if client_id not in self.clients:
        # TODO:
        pass
      self.clients.remove(client_id)
    finally:
      self.lock.release()

  def close(self):
    # TODO
    pass
