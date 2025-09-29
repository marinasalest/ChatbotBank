"""
Rotas de autenticação (login, registro)
"""
from flask import Blueprint, request, jsonify
import bcrypt
from models.database import users_db
from auth.jwt_handler import generate_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/register', methods=['POST'])
def register():
    """Registra um novo usuário"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    
    if not email or not password or not name:
        return jsonify({'error': 'Campos obrigatórios ausentes'}), 400
    
    if email in users_db:
        return jsonify({'error': 'Usuário já existe'}), 400
    
    # Generate account number
    account_number = str(1000000000 + len(users_db))
    
    # Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Create user
    users_db[email] = {
        'password': hashed_password,
        'name': name,
        'account_number': account_number,
        'balance': 0.00,
        'transactions': []
    }
    
    return jsonify({'message': 'Usuário criado com sucesso'}), 201

@auth_bp.route('/api/login', methods=['POST'])
def login():
    """Autentica um usuário"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email ou senha ausentes'}), 400
    
    if email not in users_db:
        return jsonify({'error': 'Credenciais inválidas'}), 401
    
    user = users_db[email]
    if not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({'error': 'Credenciais inválidas'}), 401
    
    # Generate token
    from flask import current_app
    token = generate_token(email, current_app.config['SECRET_KEY'])
    
    return jsonify({
        'message': 'Login realizado com sucesso',
        'token': token,
        'user': {
            'name': user['name'],
            'email': email,
            'account_number': user['account_number']
        }
    }), 200
