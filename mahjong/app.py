import flask
import flask_socketio

from server import session_manager

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)
game_sessions = session_manager.GameSessionManager()

@app.route("/")
def index():
  return flask.render_template('game.html')

@socketio.on('join')
def handle_join(data=None):
  app.logger.info('Received request to join: ' + str(data))

  if 'username' not in data:
    raise RuntimeError("Missing username")
  elif 'game_id' not in data:
    raise RuntimeError("Missing game_id")

  client_id = flask.request.sid
  username = data['username']
  game_id = data['game_id']

  if username == '':
    raise RuntimeError("username cannot be empty")
  elif game_id == '':
    raise RuntimeError("game_id cannot be empty")

  game_session = game_sessions.add_client_to_session(client_id, username, game_id)
  player_names = game_session.get_players()

  flask_socketio.join_room(game_id)
  flask_socketio.emit('on_lobby_update', {'players': player_names}, room=game_id)

@socketio.on('start_game')
def handle_start_game(data):
  app.logger.info('Received request to start game: ' + str(data))

  client_id = flask.request.sid
  game_session = game_sessions.get_client_session(client_id)
  updates = game_session.start_new_game()
  send_updates('on_start_game', updates)

@socketio.on('make_move')
def handle_make_move(data):
  app.logger.info('Received request to make_move: ' + str(data))

  client_id = flask.request.sid
  game_session = game_sessions.get_client_session(client_id)
  updates = game_session.make_move(client_id, data)
  send_updates('on_game_update', updates)

def send_updates(event, updates):
  for client_id in updates:
    flask_socketio.emit(event, updates[client_id], room=client_id)

@socketio.on('leave')
@socketio.on('disconnect')
def handle_join(*data):
  app.logger.info('Received request to leave')

  client_id = flask.request.sid
  game_session = game_sessions.get_client_session(client_id)
  game_id = game_sessions.remove_client(client_id)

  flask_socketio.leave_room(game_id)
  flask_socketio.emit('on_lobby_update', {'players': game_session.get_players()}, room=game_id)

@socketio.on_error()
def send_error_message(e):
  return str(e)

if __name__ == "__main__":
  socketio.run(app)
