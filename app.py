from flask import Flask
from routes import register_routes

# Initialisation de l'application Flask
app = Flask(__name__)

# Enregistrement des routes
register_routes(app)

# Lancer l'application si exécuté directement
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
