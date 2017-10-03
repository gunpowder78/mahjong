import io from 'socket.io-client';

export class GameClient {

  constructor() {
    // Connect to the websocket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function(data) {
      console.log('Connected!');
    });

    this.socket = socket;
  }

  joinGame(username, game_id) {
    var data = {username: username, game_id: game_id};
    console.log('Sending join request:');
    console.log(data);
    this.socket.emit('join', data);
  }

  onLobbyUpdate(callback) {
    this.socket.on('on_lobby_update', function(data) {
      console.log('Received lobby update. Current lobby state:');
      console.log(data);
      callback(data);
    });
  }

  startGame() {
    console.log('Sending start game request');
    this.socket.emit('start_game', {});
  }

  onStartGame(callback) {
    this.socket.on('on_start_game', function(data) {
      console.log('Received new game:');
      console.log(data);
      callback(data);
    });
  }

  sendMove(data) {
    console.log('Sending move request:');
    console.log(data);
    this.socket.emit('make_move', data);
  }

  onGameUpdate(callback) {
    this.socket.on('on_game_update', function(data) {
      console.log('Received game update:');
      console.log(data);
      callback(data);
    });
  }

  leaveGame() {
    console.log('Sending leave game request:');
    this.socket.emit('leave', {});
  }
}

