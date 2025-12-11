from flask import Flask
from flask_migrate import Migrate

from .extensions import db, login_manager
from .models import User

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config.Config")

    # Ensure instance folder exists
    from pathlib import Path
    instance_path = Path(app.instance_path)
    instance_path.mkdir(parents=True, exist_ok=True)

    # Init extensions
    db.init_app(app)
    Migrate(app, db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: str):
        return User.query.get(int(user_id))

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    # Register blueprints
    from .auth.routes import auth_bp
    from .movies.routes import movies_bp
    from .main.routes import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(movies_bp, url_prefix="/movies")
    app.register_blueprint(main_bp)

    # Create tables & pre-populate genres if empty
    from .models import Genre
    with app.app_context():
        db.create_all()
        if not Genre.query.first():
            default_genres = [
                "Action",
                "Comedy",
                "Drama",
                "Fantasy",
                "Horror",
                "Romance",
                "Sci-Fi",
                "Thriller",
            ]
            for name in default_genres:
                db.session.add(Genre(name=name))
            db.session.commit()

    return app
