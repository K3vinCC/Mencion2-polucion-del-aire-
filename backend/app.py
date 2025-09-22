from flask import Flask
from flask_cors import CORS  # <-- Importar CORS
from models import db
from config import SQLALCHEMY_DATABASE_URI, SECRET_KEY
from controllers.auth_controller import auth_bp
from controllers.usuario_controller import usuario_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY

db.init_app(app)

# Habilitar CORS para que React pueda hacer requests
CORS(app)  # Por defecto permite todos los orígenes y métodos

# Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(usuario_bp, url_prefix='/usuario')

# Crear tablas al inicio
@app.before_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
