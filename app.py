import flask
import flask_socketio

from server import session_manager

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)
game_sessions = session_manager.GameSessionManager()

@app.route("/")
def index():
  return flask.render_template('index.html')

@app.route("/<session_id>")
def game_session(session_id):
  return flask.render_template('game.html', session_id=session_id)

@socketio.on('join')
def handle_join(data):
  app.logger.info('Received request to join: ' + str(data))

  client_id = flask.request.sid
  if 'session_id' not in data:
    # TODO: client error
    pass

  session_id = data['session_id']
  game_sessions.add_client_to_session(client_id, session_id)

  flask_socketio.join_room(session_id)

  flask_socketio.emit('on_join', {'client_id': client_id, 'session_id': session_id})

@socketio.on('make_move')
def handle_make_move(data):
  app.logger.info('Received request to make_move: ' + str(data))

  client_id = flask.request.sid
  session_id = data['session_id']
  game_session = game_sessions.get_session_for_client(client_id)
  updates = game_session.accept_move_from(client_id, data['move'])

  for client in updates:
    print(client)
    flask_socketio.emit('update_state', {'client_id': client_id, 'update': updates[client]}, room=client)

@socketio.on('disconnect')
def handle_disconnect():
  client_id = flask.request.sid
  app.logger.info('Received disconnect from client ' + client_id)
  game_sessions.remove_client_from_session(client_id)

if __name__ == "__main__":
  socketio.run(app)
