from flask_socketio import emit, join_room, leave_room
from flask import request, session
from . import socketio
from bson import ObjectId
import api.routes.user_routes as u
import api.routes.leaderboard_routes as l


@socketio.on('connect')
def handle_connect():
    player_id = session.get('username', None)

    if player_id is None:
        print('None session', request.sid, player_id)
        emit('error', {'message': 'Please log in.'}, to=request.sid)
        return False

    # Check if the player is already in a waiting or ongoing game
    if GAMES.is_player_in_game(player_id):
        emit('error', {'message': 'You are already in a waiting or ongoing game.'}, to=request.sid)
        return False

    print('Client connected', request.sid, player_id)
    return True

@socketio.on('join_game')
def handle_join_game():
    player_id = session.get('username', None)
    print('Join game', player_id)

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
        emit('game_started', {'game_id': str(game_id), 'opponent': waiting_game['players']['player1']}, room=request.sid)
        emit('opponent_joined', {'opponent': player_id}, room=str(game_id), skip_sid=request.sid)
    else:
        # Create a new game and join it.
        game_id = GAMES.create_game(player_id)
        join_room(str(game_id))
        emit('game_joined', {'game_id': str(game_id), 'waiting': True}, room=request.sid)

@socketio.on('make_move')
def handle_make_move(data):
    print('Make move', data)
    try:
        game_id = ObjectId(data['game_id'])
        player_id = session.get('username')
        position = data['position']

        game = GAMES.get_game(game_id)

        if game and game['status'] == 'ongoing' and game['current_turn'] == player_id:
            if game['board'][position] == '':
                game_over = GAMES.process_move(game, game_id, player_id, position)
                emit('move_made', {'player': player_id, 'position': position}, room=str(game_id), skip_sid=request.sid)
                if game_over:
                    # game_over => {'result': 'win', 'winner': winner_id}
                    # or
                    # game_over => {'result': 'draw'}
                    emit('game_over', game_over, room=str(game_id))
                    print('Game over', game_over)
                    leave_room(str(game_id))

                    if game_over['result'] == 'win':
                        u.USER.increment_wins(game_over['winner'])
                        l.LEADERBOARD.update_wins(game_over['winner'])
                        loser = game['players']['player1'] if game_over['winner'] == game['players']['player2'] else game['players']['player2']
                        u.USER.increment_losses(loser)
                    else:
                        # Update user stats for a draw
                        u.USER.increment_draws(game['players']['player1'])
                        u.USER.increment_draws(game['players']['player2'])

                        # update leaderboard for a draw
                        l.LEADERBOARD.update_draws(game['players']['player1'])
                        l.LEADERBOARD.update_draws(game['players']['player2'])
    except Exception as e:
        emit('error', {'message': f'An error occurred while making the move: {str(e)}'}, to=request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    player_id = session.get('username')
    print('Client disconnected', request.sid, player_id)
    game = GAMES.handle_disconnect(player_id)
    if game:
        emit('game_over', {
            'result': 'win',
            'winner': game['winner'],
            'reason': 'opponent_disconnected'
        }, room=game['_id'], skip_sid=request.sid)
        leave_room(game['_id'])
        u.USER.increment_wins(game['winner'])
        l.LEADERBOARD.update_wins(game['winner'])
        u.USER.increment_losses(player_id)

def init_game_model(game_model):
    global GAMES
    GAMES = game_model
