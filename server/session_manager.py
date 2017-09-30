import threading

from server import session

class GameSessionManager:
  def __init__(self):
    self.sessions = {}
    self.client_to_session_ids = {}
    self.lock = threading.Lock()

  def add_client_to_session(self, client_id, session_id):
    self.lock.acquire()

    # Lock this entire operation to prevent
    # - a client joining two sessions
    # - another client leaving the session and deleting it while this client
    #   tries to join
    # - two clients trying to be the first ones to join this session
    try:
      if client_id in self.client_to_session_ids:
        # TODO: client error
        pass

      if session_id not in self.sessions:
        desired_session = session.GameSession()
        self.sessions[session_id] = desired_session
      else:
        desired_session = self.sessions[session_id]
        if not desired_session.can_accept_more_clients():
          # TODO: client error
          pass

      desired_session.add_client(client_id)
      self.client_to_session_ids[client_id] = session_id
    finally:
      self.lock.release()

  def get_session_for_client(self, client_id):
    self.lock.acquire()

    try:
      if client_id not in self.client_to_session_ids:
        # TODO: client error
        pass

      session_id = self.client_to_session_ids[client_id]
      if session_id not in self.sessions:
        # TODO: server error
        pass
      return self.sessions[session_id]
    finally:
      self.lock.release()


  def remove_client_from_session(self, client_id):
    self.lock.acquire()

    # TODO: does this entire thing need to be locked?
    try:
      if client_id not in self.client_to_session_ids:
        # TODO: client error
        pass
      session_id = self.client_to_session_ids[client_id]
      if session_id not in self.sessions:
        # TODO: server error
        pass
      current_session = self.sessions[session_id]

      current_session.remove_client(client_id)
      if not current_session.has_clients():
        current_session.close()
        del self.sessions[session_id]
    finally:
      self.lock.release()

