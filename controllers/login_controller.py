import bcrypt
import secrets
from flask import jsonify, request
from app import app, db
from models.usuario_model import Usuario, UsuarioSchema
from flask_login import login_user, login_required, logout_user
from flask_login import current_user

usuario_schema = UsuarioSchema()

@app.route('/usuarios/login', methods=['POST'])
def login():
    print("ENTRO------------")
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({'message': 'Por favor, proporciona correo electrónico y contraseña'}), 400

    usuario = Usuario.query.filter_by(email=email).first()
    if usuario:
        if bcrypt.checkpw(password.encode('utf-8'), usuario.password.encode('utf-8')):
            login_user(usuario)  # Iniciar sesión al usuario
            return jsonify({'message': 'Inicio de sesión exitoso', 'usuario': usuario_schema.dump(usuario), 'is_authenticated': current_user.is_authenticated})
        else:
            return jsonify({'message': 'Credenciales incorrectas', 'is_authenticated': False}), 401

@app.route('/usuarios/logout', methods=['POST'])
@login_required
def logout():
    logout_user()  # Cerrar la sesión del usuario
    return jsonify({'message': 'Sesión cerrada exitosamente', 'is_authenticated': False})

def codificar_contrasena(contrasena):
    return bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())
  