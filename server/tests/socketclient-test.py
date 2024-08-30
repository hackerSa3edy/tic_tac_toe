# Import the socketio and random libraries
import socketio
import random

# Create a Socket.IO client
sio = socketio.Client()

# Define the headers with cookies
headers = {'Cookie': 'session=UvPO15sCAS97oLZ7J1TWFZC3jT54g9nyDwsiRareAWY'}

# Define an event handler for the 'connect' event
# This event is automatically emitted when the client connects to the server
@sio.event
def connect():
    # Print a message to the console
    print("I'm connected!")

    # Emit a 'join_game' event to the server with the player_id
    player_id = f'player_{random.randint(1, 1000)}'
    sio.emit('join_game', {'player_id': player_id})

    # Emit a 'message' event to the server with the data 'Hello, server!'
    sio.emit('message', 'Hello, server!')

    # Emit a 'humanMove' event to the server with a random index between 0 and 8
    sio.emit('humanMove', {'index': random.randint(0, 8)})

# Define an event handler for the 'game_joined' event
# This event is emitted by the server when the client successfully joins a game
@sio.on('game_joined')
def on_game_joined(data):
    # Print the received game_joined message to the console
    print('Game joined: ', data)

# Define an event handler for the 'opponent_joined' event
# This event is emitted by the server when an opponent joins the game
@sio.on('opponent_joined')
def on_opponent_joined(data):
    # Print the received opponent_joined message to the console
    print('Opponent joined: ', data)

# Define an event handler for the 'error' event
# This event is emitted by the server when there is an error
@sio.on('error')
def on_error(data):
    # Print the received error message to the console
    print('Error: ', data)

# Define an event handler for the 'message' event
# This event is emitted by the server when it sends a message to the client
@sio.on('message')
def on_message(data):
    # Print the received message to the console
    print('Received message: ', data)

# Define an event handler for the 'backendAI' event
# This event is emitted by the server when it sends a backendAI message to the client
@sio.on('backendAI')
def on_backendAI(data):
    # Print the received backendAI message to the console
    print('Received backendAI: ', data)

@sio.on('response')
def on_resp(data):
    print('Received Response: ', data)

# Connect the client to the server at 'http://localhost:3000'
sio.connect(
    'http://localhost:3000',
    headers=headers
)

# Wait for events
# This keeps the application running so it can receive events from the server
sio.wait()
