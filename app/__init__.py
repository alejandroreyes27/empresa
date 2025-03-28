from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate  # Importar Flask-Migrate
import os

# Instanciamos las extensiones
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()  # Instanciamos Migrate

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config.from_object('config.Config')  # Cargar configuración desde config.py

    # Inicializar las extensiones
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Inicializar Flask-Migrate
    migrate.init_app(app, db)  # Esto es necesario para las migraciones

    @login_manager.user_loader
    def load_user(idUser):
        from app.models.users import Users
        return Users.query.get(int(idUser))

    # Registrar blueprints y cargar modelos
    with app.app_context():
        # Importar modelos para que Flask-Migrate los detecte
        from app.models.Categoria import Categoria
        from app.models.Productos import Productos

        # Importar y registrar blueprints
        from app.routes.auth import bp as auth_bp
        from app.routes.Departments_routes import bp as departments_bp
        from app.routes.Employees_routes import bp as employees_bp
        from app.routes.DepartametsEmployes_routes import bp as departamets_employes_bp
        from app.routes.Productos_routes import bp as productos_bp
        from app.routes.Carrito_routes import bp as carrito_bp
        from app.routes.Categoria_routes import bp as categoria_bp 

        app.register_blueprint(auth_bp)
        app.register_blueprint(departments_bp)
        app.register_blueprint(employees_bp)
        app.register_blueprint(departamets_employes_bp)
        app.register_blueprint(productos_bp)
        app.register_blueprint(carrito_bp)
        app.register_blueprint(categoria_bp)
    return app
