from flask import jsonify, request, Blueprint


leaderboard_bp = Blueprint('leaderboard', __name__)

@leaderboard_bp.route('/', methods=['GET'])
def get_leaderboard():
    username = request.args.get('username')

    if not username:
        return jsonify({'error': 'Username is required'}), 400

    # Get top 100 players
    top_players = LEADERBOARD.get_leaderboard(100)

    # Get current player stats and rank
    user_stats = LEADERBOARD.get_user_stats(username)
    user_rank = LEADERBOARD.get_user_rank(username)

    if not user_stats:
        return jsonify({'error': 'User not found'}), 404

    user_stats['rank'] = user_rank

    return jsonify({
        'top_players': top_players,
        'current_player': user_stats
    })

def init_leaderboard_routes(leaderboard):
    global LEADERBOARD
    LEADERBOARD = leaderboard
