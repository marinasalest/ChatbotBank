from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import bcrypt
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

# In-memory storage (in production, use a database)
users_db = {
    'joao.silva@email.com': {
        'password': bcrypt.hashpw('senha123'.encode('utf-8'), bcrypt.gensalt()),
        'name': 'João Silva',
        'account_number': '1234567890',
        'balance': 5000.00,
        'transactions': [
            {'id': 1, 'type': 'deposit', 'amount': 1000.00, 'date': '2024-01-15', 'description': 'Depósito inicial'},
            {'id': 2, 'type': 'purchase', 'amount': -50.00, 'date': '2024-01-16', 'description': 'Supermercado'},
            {'id': 3, 'type': 'deposit', 'amount': 2000.00, 'date': '2024-01-20', 'description': 'Depósito de salário'},
        ]
    },
    'maria.santos@email.com': {
        'password': bcrypt.hashpw('senha123'.encode('utf-8'), bcrypt.gensalt()),
        'name': 'Maria Santos',
        'account_number': '0000000002',
        'balance': 3200.00,
        'transactions': [
            {'id': 1, 'type': 'deposit', 'amount': 3200.00, 'date': '2024-01-10', 'description': 'Depósito inicial'},
        ]
    },
    'pedro.oliveira@email.com': {
        'password': bcrypt.hashpw('senha123'.encode('utf-8'), bcrypt.gensalt()),
        'name': 'Pedro Oliveira',
        'account_number': '0000000003',
        'balance': 1500.00,
        'transactions': [
            {'id': 1, 'type': 'deposit', 'amount': 2000.00, 'date': '2024-01-12', 'description': 'Depósito inicial'},
            {'id': 2, 'type': 'purchase', 'amount': -500.00, 'date': '2024-01-18', 'description': 'Compras online'},
        ]
    },
    'ana.costa@email.com': {
        'password': bcrypt.hashpw('senha123'.encode('utf-8'), bcrypt.gensalt()),
        'name': 'Ana Costa',
        'account_number': '0000000004',
        'balance': 7500.00,
        'transactions': [
            {'id': 1, 'type': 'deposit', 'amount': 7500.00, 'date': '2024-01-08', 'description': 'Depósito inicial'},
        ]
    },
    'carlos.ferreira@email.com': {
        'password': bcrypt.hashpw('senha123'.encode('utf-8'), bcrypt.gensalt()),
        'name': 'Carlos Ferreira',
        'account_number': '0000000005',
        'balance': 2800.00,
        'transactions': [
            {'id': 1, 'type': 'deposit', 'amount': 3000.00, 'date': '2024-01-14', 'description': 'Depósito inicial'},
            {'id': 2, 'type': 'purchase', 'amount': -200.00, 'date': '2024-01-19', 'description': 'Farmácia'},
        ]
    },
    'lucia.rodrigues@email.com': {
        'password': bcrypt.hashpw('senha123'.encode('utf-8'), bcrypt.gensalt()),
        'name': 'Lúcia Rodrigues',
        'account_number': '0000000006',
        'balance': 4200.00,
        'transactions': [
            {'id': 1, 'type': 'deposit', 'amount': 4200.00, 'date': '2024-01-11', 'description': 'Depósito inicial'},
        ]
    },
    'roberto.almeida@email.com': {
        'password': bcrypt.hashpw('senha123'.encode('utf-8'), bcrypt.gensalt()),
        'name': 'Roberto Almeida',
        'account_number': '0000000007',
        'balance': 1800.00,
        'transactions': [
            {'id': 1, 'type': 'deposit', 'amount': 2500.00, 'date': '2024-01-13', 'description': 'Depósito inicial'},
            {'id': 2, 'type': 'purchase', 'amount': -700.00, 'date': '2024-01-17', 'description': 'Eletrônicos'},
        ]
    },
    'fernanda.lima@email.com': {
        'password': bcrypt.hashpw('senha123'.encode('utf-8'), bcrypt.gensalt()),
        'name': 'Fernanda Lima',
        'account_number': '0000000008',
        'balance': 6200.00,
        'transactions': [
            {'id': 1, 'type': 'deposit', 'amount': 6200.00, 'date': '2024-01-09', 'description': 'Depósito inicial'},
        ]
    },
    'marcos.souza@email.com': {
        'password': bcrypt.hashpw('senha123'.encode('utf-8'), bcrypt.gensalt()),
        'name': 'Marcos Souza',
        'account_number': '0000000009',
        'balance': 950.00,
        'transactions': [
            {'id': 1, 'type': 'deposit', 'amount': 1500.00, 'date': '2024-01-16', 'description': 'Depósito inicial'},
            {'id': 2, 'type': 'purchase', 'amount': -550.00, 'date': '2024-01-21', 'description': 'Restaurante'},
        ]
    },
    'patricia.mendes@email.com': {
        'password': bcrypt.hashpw('senha123'.encode('utf-8'), bcrypt.gensalt()),
        'name': 'Patrícia Mendes',
        'account_number': '0000000010',
        'balance': 3800.00,
        'transactions': [
            {'id': 1, 'type': 'deposit', 'amount': 3800.00, 'date': '2024-01-07', 'description': 'Depósito inicial'},
        ]
    },
    'antonio.barbosa@email.com': {
        'password': bcrypt.hashpw('senha123'.encode('utf-8'), bcrypt.gensalt()),
        'name': 'Antônio Barbosa',
        'account_number': '0000000011',
        'balance': 2100.00,
        'transactions': [
            {'id': 1, 'type': 'deposit', 'amount': 2500.00, 'date': '2024-01-15', 'description': 'Depósito inicial'},
            {'id': 2, 'type': 'purchase', 'amount': -400.00, 'date': '2024-01-22', 'description': 'Supermercado'},
        ]
    }
}

# JWT token generation
def generate_token(user_email):
    payload = {
        'user_email': user_email,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

# JWT token verification
def verify_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user_email']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Authentication middleware
def require_auth(f):
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token não fornecido'}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        user_email = verify_token(token)
        if not user_email:
            return jsonify({'error': 'Token inválido'}), 401
        
        return f(user_email, *args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    
    if not email or not password or not name:
        return jsonify({'error': 'Campos obrigatórios ausentes'}), 400
    
    if email in users_db:
        return jsonify({'error': 'Usuário já existe'}), 400
    
    # Create new user
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users_db[email] = {
        'password': hashed_password,
        'name': name,
        'account_number': f"{len(users_db) + 1:010d}",
        'balance': 0.00,
        'transactions': []
    }
    
    token = generate_token(email)
    return jsonify({
        'message': 'Usuário criado com sucesso',
        'token': token,
        'user': {
            'name': name,
            'email': email,
            'account_number': users_db[email]['account_number']
        }
    })

@app.route('/api/login', methods=['POST'])
def login():
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
    
    token = generate_token(email)
    return jsonify({
        'message': 'Login realizado com sucesso',
        'token': token,
        'user': {
            'name': user['name'],
            'email': email,
            'account_number': user['account_number']
        }
    })

@app.route('/api/balance', methods=['GET'])
@require_auth
def get_balance(user_email):
    user = users_db[user_email]
    return jsonify({
        'balance': user['balance'],
        'account_number': user['account_number']
    })

@app.route('/api/transactions', methods=['GET'])
@require_auth
def get_transactions(user_email):
    user = users_db[user_email]
    return jsonify({
        'transactions': user['transactions']
    })

@app.route('/api/transfer', methods=['POST'])
@require_auth
def transfer_money(user_email):
    data = request.get_json()
    recipient_account = data.get('recipient_account')
    amount = data.get('amount')
    description = data.get('description', '')
    
    if not recipient_account or not amount:
        return jsonify({'error': 'Campos obrigatórios ausentes'}), 400
    
    if amount <= 0:
        return jsonify({'error': 'Valor deve ser positivo'}), 400
    
    user = users_db[user_email]
    if user['balance'] < amount:
        return jsonify({'error': 'Saldo insuficiente'}), 400
    
    # Find recipient
    recipient_email = None
    for email, user_data in users_db.items():
        if user_data['account_number'] == recipient_account:
            recipient_email = email
            break
    
    if not recipient_email:
        return jsonify({'error': 'Conta destinatária não encontrada'}), 404
    
    # Process transfer
    user['balance'] -= amount
    users_db[recipient_email]['balance'] += amount
    
    # Add transaction records
    transaction_id = len(user['transactions']) + 1
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    user['transactions'].append({
        'id': transaction_id,
        'type': 'transfer_out',
        'amount': -amount,
        'date': current_date,
        'description': f"Transferência para {recipient_account} - {description}"
    })
    
    users_db[recipient_email]['transactions'].append({
        'id': len(users_db[recipient_email]['transactions']) + 1,
        'type': 'transfer_in',
        'amount': amount,
        'date': current_date,
        'description': f"Transferência de {user['account_number']} - {description}"
    })
    
    return jsonify({
        'message': 'Transferência realizada com sucesso',
        'new_balance': user['balance']
    })

@app.route('/api/deposit', methods=['POST'])
@require_auth
def deposit_money(user_email):
    data = request.get_json()
    amount = data.get('amount')
    description = data.get('description', 'Depósito')
    
    if not amount or amount <= 0:
        return jsonify({'error': 'Valor inválido'}), 400
    
    user = users_db[user_email]
    user['balance'] += amount
    
    transaction_id = len(user['transactions']) + 1
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    user['transactions'].append({
        'id': transaction_id,
        'type': 'deposit',
        'amount': amount,
        'date': current_date,
        'description': description
    })
    
    return jsonify({
        'message': 'Depósito realizado com sucesso',
        'new_balance': user['balance']
    })

@app.route('/api/chat', methods=['POST'])
@require_auth
def chat(user_email):
    data = request.get_json()
    message = data.get('message', '').lower()
    
    user = users_db[user_email]
    
    # Simple chatbot responses
    if 'saldo' in message or 'quanto' in message or 'balance' in message:
        return jsonify({
            'response': f"Seu saldo atual é R$ {user['balance']:.2f}",
            'type': 'balance'
        })
    
    elif 'transação' in message or 'histórico' in message or 'transaction' in message:
        recent_transactions = user['transactions'][-5:]  # Last 5 transactions
        if recent_transactions:
            response = "Aqui estão suas transações recentes:\n"
            for tx in reversed(recent_transactions):
                response += f"• {tx['date']}: {tx['description']} - R$ {tx['amount']:.2f}\n"
        else:
            response = "Você ainda não possui transações."
        return jsonify({
            'response': response,
            'type': 'transactions'
        })
    
    elif 'transferência' in message or 'transferir' in message or 'transfer' in message:
        return jsonify({
            'response': "Para fazer uma transferência, use o formulário de transferência. Você precisará do número da conta do destinatário e do valor que deseja enviar.",
            'type': 'info'
        })
    
    elif 'ajuda' in message or 'help' in message:
        return jsonify({
            'response': "Posso ajudá-lo com:\n\n<ol style='margin: 10px 0; padding-left: 20px;'>\n<li>💰 <strong>Consultar saldo da conta</strong></li>\n<li>📊 <strong>Ver histórico de transações</strong></li>\n<li>💸 <strong>Fazer transferências</strong></li>\n<li>💳 <strong>Processar depósitos</strong></li>\n<li>❓ <strong>Responder perguntas bancárias gerais</strong></li>\n</ol>\n\nO que gostaria de saber?",
            'type': 'help'
        })
    
    elif 'olá' in message or 'oi' in message or 'hello' in message or 'hi' in message:
        return jsonify({
            'response': f"Olá {user['name']}! Como posso ajudá-lo com suas necessidades bancárias hoje?",
            'type': 'greeting'
        })
    
    else:
        return jsonify({
            'response': "Estou aqui para ajudá-lo com suas necessidades bancárias. Você pode me perguntar sobre seu saldo, transações, transferências, ou apenas diga 'ajuda' para mais opções.",
            'type': 'general'
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
