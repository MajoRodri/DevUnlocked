from flask import Flask
from routes.main import bp as main_bp
from routes.achievements import bp as achievements_bp
from routes.pets import bp as pets_bp

# crea la aplicación Flask / creates the Flask application
app = Flask(__name__)

# conecta las rutas de cada módulo a la app / connects each module's routes to the app
app.register_blueprint(main_bp)
app.register_blueprint(achievements_bp)
app.register_blueprint(pets_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # arranca el servidor en el puerto 5000 / starts the server on port 5000
