# MahJong

A simple MahJong online game.

## Development

Some tutorials to familiarize with:

* [Flask](http://flask.pocoo.org/docs/0.12/quickstart/)
* [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/)

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

### Run server locally

1.  From a terminal, start up the server

    ```
    export FLASK_APP=app.py
    export FLASK_DEBUG=1
    flask run
    ```
2.  In a browser, navigate to `http://localhost:5000`
