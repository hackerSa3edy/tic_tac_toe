
from flask_socketio import emit, join_room, leave_room
from flask import request, session
from . import socketio
from bson import ObjectId


@socketio.on('connect')
def handle_connect():
    player_id = session.get('username', None)  # Get the username from the session

    # Manually manage session data
    if player_id is None:
        emit('response', {'message': 'Please log in.'}, to=request.sid)
        return False

    # Check if the player is already in a waiting or ongoing game
    if GAMES.is_player_in_game(player_id):
        emit('error', {'message': 'You are already in a waiting or ongoing game.'}, to=request.sid)
        return False

    return True

@socketio.on('join_game')
def handle_join_game(data):
    player_id = session.get('username', None)

    # Check if the player is already in a waiting or ongoing game
    if player_id and GAMES.is_player_in_game(player_id):
        emit('error', {'message': 'You are already in a waiting or ongoing game.'}, to=request.sid)
        return False

    # Look for a waiting game
    waiting_game = GAMES.search_games_by_status('waiting')
    if waiting_game:
        # Join an existing waiting game.
        game_id = waiting_game['_id']
        GAMES.join_game(game_id, player_id)
        join_room(str(game_id))
        emit('game_joined', {'game_id': str(game_id), 'opponent': waiting_game['players']['player1']}, room=request.sid)
        emit('opponent_joined', {'opponent': player_id}, room=str(game_id), skip_sid=request.sid)
    else:
        # Create a new game and join it.
        game_id = GAMES.create_game(player_id)
        join_room(str(game_id))
        emit('game_joined', {'game_id': str(game_id), 'waiting': True}, room=request.sid)

@socketio.on('make_move')
def handle_make_move(data):
    try:
        game_id = ObjectId(data['game_id'])
        player_id = session.get('username')  # Get the username from the session
        position = data['position']

        game = GAMES.get_game(game_id)

        if game and game['status'] == 'ongoing' and game['current_turn'] == player_id:
            if game['board'][position] == '':
                game_over = GAMES.process_move(game, game_id, player_id, position)
                if game_over:
                    # game_over => {'result': 'win', 'winner': winner_id}
                    # or
                    # game_over => {'result': 'draw'}
                    emit('game_over', game_over, room=str(game_id))
    except Exception as e:
        emit('error', {'message': f'An error occured while making the move: {str(e)}'}, to=request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    # print('Client disconnected', request.sid, session.get('username'))
    game = GAMES.handle_disconnect(session.get('username'))
    if game:
        emit('game_over', {
            'result': 'win',
            'winner': game['winner'],
            'reason': 'opponent_disconnected'
        }, room=str(game), skip_sid=request.sid)
        leave_room(str(game))

def init_game_model(game_model):
    global GAMES
    GAMES = game_model
