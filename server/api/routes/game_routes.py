from flask import Blueprint, request, jsonify, url_for
import multiplayer_socketIO.events as e

game_bp = Blueprint('game', __name__)

@game_bp.route('/games', methods=['GET'])
def get_all_games():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    games, total = e.GAMES.get_all_games_paginated(page, per_page)

    next_url = url_for('game.get_all_games', page=page + 1, per_page=per_page) if (page * per_page) < total else None
    back_url = url_for('game.get_all_games', page=page - 1, per_page=per_page) if page > 1 else None

    return jsonify({
        'games': games,
        'total': total,
        'page': page,
        'per_page': per_page,
        'next': next_url,
        'back': back_url
    })
