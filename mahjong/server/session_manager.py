import threading

from server import session

class GameSessionManager:
  def __init__(self):
    self.sessions = {}
    self.client_to_game_ids = {}

  def add_client_to_session(self, client_id, username, game_id):
    if client_id in self.client_to_game_ids:
      # TODO: client error
      pass

    if game_id not in self.sessions:
      game_session = session.GameSession()
      self.sessions[game_id] = game_session
    else:
      game_session = self.sessions[game_id]
      if not game_session.can_accept_more_clients():
        # TODO: client error
        pass

    self.client_to_game_ids[client_id] = game_id
    game_session.add_client(client_id, username)
    return game_session

  def get_client_session(self, client_id):
    if client_id not in self.client_to_game_ids:
      # TODO: client error
      pass

    game_id = self.client_to_game_ids[client_id]
    if game_id not in self.sessions:
      # TODO: server error
      pass
    return self.sessions[game_id]

  def get_game_session(self, game_id):
    if game_id not in self.sessions:
      # TODO: server error
      pass
    return self.sessions[game_id]

  def remove_client(self, client_id):
    if client_id not in self.client_to_game_ids:
      # TODO: client error
      pass
    game_id = self.client_to_game_ids[client_id]
    if game_id not in self.sessions:
      # TODO: server error
      pass
    game_session = self.sessions[game_id]

    game_session.remove_client(client_id)
    if not game_session.has_clients():
      game_session.close()
      del self.sessions[game_id]

    return game_id

