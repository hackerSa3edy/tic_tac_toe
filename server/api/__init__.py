from .routes.auth_routes import auth_bp
from .routes.user_routes import user_bp
from .routes.game_routes import game_bp
from .routes.leaderboard_routes import leaderboard_bp

def init_api(auth, user, leaderboard):
    from .routes.auth_routes import init_auth_routes
    from .routes.user_routes import init_user_routes
    from .routes.leaderboard_routes import init_leaderboard_routes

    init_auth_routes(auth)
    init_user_routes(user)
    init_leaderboard_routes(leaderboard)
