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
def handle_join(data):
  app.logger.info('Received request to join: ' + str(data))

  client_id = flask.request.sid
  username = data['username']
  game_id = data['game_id']

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
def handle_join(data):
  app.logger.info('Received request to leave: ' + str(data))

  client_id = flask.request.sid

  game_id = game_sessions.remove_client(client_id)
  game_session = game_sessions.get_game_session(game_id)

  flask_socketio.leave_room(game_id)
  flask_socketio.emit('on_lobby_update', {'players': game_session.get_players()}, room=game_id)

@socketio.on('disconnect')
def handle_disconnect():
  client_id = flask.request.sid
  app.logger.info('Received disconnect from client ' + client_id)

  game_id = game_sessions.remove_client(client_id)
  game_session = game_sessions.get_game_session(game_id)
  flask_socketio.emit('on_lobby_update', {'players': game_session.get_players()}, room=game_id)

if __name__ == "__main__":
  socketio.run(app)
