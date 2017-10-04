import threading

from server import session

class GameSessionManager:
  """Manages clients and the GameSessions that they connect to. Each client can only be in one
  session at a time.
  """

  def __init__(self):
    self.sessions = {}  # Game IDs to GameSessions
    self.client_to_game_ids = {}  # Client IDs that are in games.

  def add_client_to_session(self, client_id, username, game_id):
    """Adds a client ID to a session with the given game_id, creating the session if it doesn't
    exist. The client ID is given a username unique to the game session.
    """
    # Clients can only belong to one game session at a time.
    if client_id in self.client_to_game_ids:
      raise RuntimeError("Client is already in a game: " + self.client_to_game_ids[client_id])

    # Get the session that corresponds to the game_id.
    if game_id not in self.sessions:
      game_session = session.GameSession(game_id)
      self.sessions[game_id] = game_session
    else:
      game_session = self.sessions[game_id]
      if not game_session.can_accept_more_clients():
        raise RuntimeError("Game " + game_id + " is already full")
      elif game_session.has_username(username):
        raise RuntimeError("Game " + game_id + " already has user with name " + username)

    # Add the client to the session.
    self.client_to_game_ids[client_id] = game_id
    game_session.add_client(client_id, username)
    return game_session

  def get_client_session(self, client_id):
    """Get the session that a client belongs to."""
    if client_id not in self.client_to_game_ids:
      raise RuntimeError('Client is not in a game')

    game_id = self.client_to_game_ids[client_id]
    if game_id not in self.sessions:
      raise RuntimeError("Can no longer find client's game " + game_id + " on server")

    return self.sessions[game_id]

  def remove_client(self, client_id):
    """Removes a client from its current game session and returns the ID of the game. Note that
    after this method is called, get_client_session(client_id) will throw an exception.
    """
    if client_id not in self.client_to_game_ids:
      raise RuntimeError('Client is not in a game')

    game_id = self.client_to_game_ids.pop(client_id)
    if game_id not in self.sessions:
      raise RuntimeError("Can no longer find client's game " + game_id + " on server")

    game_session = self.sessions[game_id]
    game_session.remove_client(client_id)

    # Cleanup and remove the game session if it has no more clients.
    if not game_session.has_clients():
      game_session.close()
      self.sessions.pop(game_id)

    return game_id

