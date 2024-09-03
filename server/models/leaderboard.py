from bson import ObjectId

class Leaderboard:
    def __init__(self, db):
        self.db = db
        self.leaderboard = self.db['leaderboard']

    def add_user(self, username):
        """Add a new user to the leaderboard."""
        new_entry = {
            'username': username,
            'wins': 0,
            'draws': 0,
            'score': 0
        }
        self.leaderboard.insert_one(new_entry)

    def update_wins(self, username):
        """Update the number of wins for a user."""
        self.leaderboard.update_one({'username': username}, {'$inc': {'wins': 1, 'score': 3}})

    def update_draws(self, username):
        """Update the number of draws for a user."""
        self.leaderboard.update_one({'username': username}, {'$inc': {'draws': 1, 'score': 1}})

    def get_leaderboard(self, limit=10):
        """Retrieve the leaderboard, sorted by score."""
        return list(self.leaderboard.find().sort('score', -1).limit(limit))

    def get_user_stats(self, username):
        """Retrieve the stats for a specific user."""
        return self.leaderboard.find_one({'username': username}, {'_id': 0})

    def get_user_rank(self, username):
        """Retrieve the rank of a specific user."""
        user = self.leaderboard.find_one({'username': username}, {'score': 1})
        if not user:
            return None
        user_score = user['score']
        rank = self.leaderboard.count_documents({'score': {'$gt': user_score}}) + 1
        return rank

    def delete_user(self, username):
        """Delete a user from the leaderboard."""
        self.leaderboard.delete_one({'username': username})
