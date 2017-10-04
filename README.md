# MahJong

A simple MahJong online game.

## Development

Some tutorials to familiarize with:

*   [Flask](http://flask.pocoo.org/docs/0.12/quickstart/)
*   [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/)
*   [React.js](https://reactjs.org/tutorial/tutorial.html)
*   [webpack](https://webpack.js.org/guides/getting-started/)

### Setup

1.  Clone the repository.
2.  Create a `virtualenv`

    ```
    cd path/to/repo
    virtualenv -p python3 .
    ```
3.  Activate the `virtualenv`

    ```
    source bin/activate
    ```
4.  Install requirements

    ```
    pip install -r requirements.txt
    ```

### Build frontend React code

1.  Install [node.js](https://nodejs.org/en/)
2.  Install javascript dependencies (see `package.json`):

    ```
    npm install
    ```
3.  Build frontend code (located at `frontend/index.js`) into
    `mahjong/static/bundle.js`:

    ```
    npm run build
    ```

### Run server locally

1.  From a terminal, start up the server

    ```
    ./run-server
    ```
2.  In a browser, navigate to `http://localhost:5000`

