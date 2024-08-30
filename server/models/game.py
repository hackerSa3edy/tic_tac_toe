from bson import ObjectId
from datetime import datetime

class Game:
    def __init__(self, db):
        self.db = db
        self.games = self.db['games']

    def search_games_by_status(self, status):
        return self.games.find_one({'status': status}, sort=[('created_at', 1)])

    def create_game(self, player1_id):
        new_game = {
            'players': {'player1': player1_id, 'player2': ''},
            'status': 'waiting',
            'board': [''] * 9,
            'created_at': datetime.utcnow(),
            'current_turn': player1_id,
            'winner': '',
            'loser': '',
            'is_draw': False,
        }
        result = self.games.insert_one(new_game)
        # print('New game created: ', result.inserted_id)
        return result.inserted_id

    def join_game(self, game_id, player2_id):
        self.games.update_one(
            {'_id': ObjectId(game_id)},
            {
                '$set': {
                    'players.player2': player2_id,
                    'status': 'ongoing',
                    'created_at': datetime.utcnow(),
                    'current_turn': self.games.find_one({'_id': ObjectId(game_id)})['players']['player1']
                }
            }
        )

    def update_end_at(self, game_id, end_at):
        self.games.update_one({'_id': ObjectId(game_id)}, {'$set': {'ended_at': end_at}})

    def update_winner_loser(self, game_id, winner_id, loser_id):
        self.games.update_one({'_id': ObjectId(game_id)}, {'$set': {'winner': winner_id, 'loser': loser_id}})

    def update_current_turn(self, game_id, player_id):
        self.games.update_one({'_id': ObjectId(game_id)}, {'$set': {'current_turn': player_id}})

    def update_board(self, game_id, board):
        if len(board) != 9:
            raise ValueError("Board must be a 1x9 array.")
        self.games.update_one({'_id': ObjectId(game_id)}, {'$set': {'board': board}})

    def update_status(self, game_id, status):
        if status not in ["waiting", "ongoing", "completed"]:
            raise ValueError("Invalid status.")
        self.games.update_one({'_id': ObjectId(game_id)}, {'$set': {'status': status}})

    def update_is_draw(self, game_id, is_draw):
        self.games.update_one({'_id': ObjectId(game_id)}, {'$set': {'is_draw': is_draw}})

    def update_player1(self, game_id, player1_id):
        self.games.update_one({'_id': ObjectId(game_id)}, {'$set': {'players.player1': player1_id}})

    def update_player2(self, game_id, player2_id):
        self.games.update_one({'_id': ObjectId(game_id)}, {'$set': {'players.player2': player2_id}})

    def get_game(self, game_id):
        return self.games.find_one({'_id': ObjectId(game_id)})

    def delete_game(self, game_id):
        self.games.delete_one({'_id': ObjectId(game_id)})

    def handle_disconnect(self, disconnected_player_id):
        game = self.search_games_by_player_and_status(disconnected_player_id, ['waiting', 'ongoing'])
        # print('Disconnected player: ', disconnected_player_id, 'game:', game)
        if game:
            if game['status'] == 'waiting':
                # print('Deleting game: ', game)
                self.delete_game(game['_id'])
            elif game['status'] == 'ongoing':
                winner = 'player2' if game['players']['player1'] == disconnected_player_id else 'player1'
                self.games.update_one(
                    {'_id': game['_id']},
                    {
                        '$set': {
                            'status': 'completed',
                            'winner': game['players'][winner],
                            'loser': disconnected_player_id,
                            'notes': 'Opponent withdrew',
                            'ended_at': datetime.utcnow()
                        }
                    }
                )
                # print('Game ongoing: ', game)
        return game

    def search_games_by_player_and_status(self, player_id, statuses):
        game = self.games.find_one({
            '$and': [
                {'$or': [
                    {'players.player1': player_id},
                    {'players.player2': player_id}
                ]},
                {'status': {'$in': statuses}}
            ]
        })
        return game

    def delete_ongoing_or_waiting_games(self):
        result = self.games.delete_many({'status': {'$in': ['waiting', 'ongoing']}})
        return result.deleted_count

    def is_player_in_game(self, player_id):
        """Check if the player is already in a waiting or ongoing game."""
        existing_game = self.search_games_by_player_and_status(player_id, ['waiting', 'ongoing'])
        return existing_game is not None

    def process_move(self, game, game_id, player_id, position):
        """Process a player's move."""
        symbol = 'X' if player_id == game['players']['player1'] else 'O'
        new_board = game['board']
        new_board[position] = symbol

        next_turn = game['players']['player2'] if player_id == game['players']['player1'] else game['players']['player1']

        self.update_board(game_id, new_board)
        self.update_current_turn(game_id, next_turn)

        winner = self.check_winner(new_board)
        if winner:
            return self.handle_game_over(game_id, winner, symbol, game)

        return False

    def handle_game_over(self, game_id, winner, symbol, game):
        """Handle the end of the game."""
        if winner == 'draw':
            self.update_status(game_id, 'completed')
            self.update_is_draw(game_id, True)
            self.update_end_at(game_id, datetime.now())

            return  {'result': 'draw'}
        else:
            winner_id = game['players']['player1'] if symbol == 'X' else game['players']['player2']
            loser_id = game['players']['player2'] if symbol == 'X' else game['players']['player1']
            self.update_status(game_id, 'completed')
            self.update_winner_loser(game_id, winner_id, loser_id)
            self.update_end_at(game_id, datetime.now())

            return {'result': 'win', 'winner': winner_id}

    def delete_all_games(self):
        return self.games.delete_many({})

    def all_games_by_player(self, player_id):
        games = self.games.find({
            '$or': [
                {'players.player1': player_id},
                {'players.player2': player_id}
            ]
        })
        return list(games)

    def all_games_by_status(self, statuses):
        games = self.games.find({
            'status': {'$in': [statuses,]}
        })
        return list(games)

    def get_all_games_paginated(self, page, per_page):
        total = self.games.count_documents({})
        games_cursor = self.games.find({}, {'board': 0, 'current_turn': 0, '_id': 0}).skip((page - 1) * per_page).limit(per_page)
        games = list(games_cursor)
        return games, total

    @staticmethod
    def check_winner(board):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]

        for combo in winning_combinations:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] != '':
                return board[combo[0]]

        if '' not in board:
            return 'draw'

        return None
