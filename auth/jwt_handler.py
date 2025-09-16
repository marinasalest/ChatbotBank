"""
Manipulação de tokens JWT para autenticação
"""
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

def generate_token(user_email, secret_key):
    """Gera token JWT para o usuário"""
    payload = {
        'user_email': user_email,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')

def verify_token(token, secret_key):
    """Verifica e decodifica token JWT"""
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload['user_email']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def require_auth(f):
    """Decorator para rotas que requerem autenticação"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token não fornecido'}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        # Get secret key from app config
        from flask import current_app
        secret_key = current_app.config['SECRET_KEY']
        
        user_email = verify_token(token, secret_key)
        if not user_email:
            return jsonify({'error': 'Token inválido'}), 401
        
        return f(user_email, *args, **kwargs)
    return decorated_function


