import React from 'react';
import ReactDOM from 'react-dom';
import { GameClient } from './socket.js';


class Lobby extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      username: '',
      game_id: '',
      players: [],

      // Game state
      moves: [],
    }

    this.client = new GameClient((error) => this.handleError(error));
    this.client.onLobbyUpdate((data) => this.onLobbyUpdate(data));
    this.client.onStartGame((data) => this.onStartGame(data));
    this.client.onGameUpdate((data) => this.onGameUpdate(data));
  }

  handleError(error) {
    if (error !== undefined) {
      console.log(error);
    }
  }

  joinGame() {
    this.client.joinGame(this.state.username, this.state.game_id);
  }

  onLobbyUpdate(data) {
    this.setState({
      players: data.players.slice(),
      moves: [],
    });
  }

  startGame() {
    if (this.state.players.length === 4) {
      this.client.startGame();
    }
  }

  onStartGame(data) {
    this.setState({moves: [data]});
  }

  sendMove() {
    const data = {move: this.state.username + ' made a move'};
    this.client.sendMove(data);
  }

  onGameUpdate(data) {
    const moves = this.state.moves.slice();
    moves.push(data);
    this.setState({moves: moves});
  }

  leaveGame() {
    this.client.leaveGame();
    this.setState({
      moves: [],
      players: [],
    });
  }

  render() {
    const players = this.state.players.map((player) => {
      return (
        <li key={player}>{player}</li>
      );
    });
    return (
      <div>
        <div>
          User name: <input type='text' value={this.state.username} 
            onChange={(event) => this.setState({username: event.target.value})} />
        </div>
        <div>
          Game to join: <input type='text' value={this.state.game_id}
            onChange={(event) => this.setState({game_id: event.target.value})} />
        </div>
        <div>
          {this.state.username} and {this.state.game_id}
        </div>

        <div>
          <button onClick={() => this.joinGame()}>Join game</button>
          <button onClick={() => this.startGame()}>Start game</button>
          <button onClick={() => this.sendMove()}>Send move</button>
          <button onClick={() => this.leaveGame()}>Leave game</button>
        </div>

        Players:
        <ul>
          {players}
        </ul>

        <Game moves={this.state.moves} />
      </div>
    );
  }
}

class Game extends React.Component {
  render() {
    const moves = this.props.moves.map((move, i) => {
      return (
        <li key={i}>{move}</li>
      );
    });
    return (
      <div>
        <ol>
          {moves}
        </ol>
      </div>
    );
  }
}

ReactDOM.render(
  <Lobby />,
  document.getElementById('root')
);

