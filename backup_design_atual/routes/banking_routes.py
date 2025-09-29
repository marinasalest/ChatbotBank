"""
Rotas de operações bancárias
"""
from flask import Blueprint, request, jsonify
from models.database import users_db
from auth.jwt_handler import require_auth

banking_bp = Blueprint('banking', __name__)

@banking_bp.route('/api/balance', methods=['GET'])
@require_auth
def get_balance(user_email):
    """Retorna o saldo do usuário"""
    user = users_db[user_email]
    return jsonify({'balance': user['balance']}), 200

@banking_bp.route('/api/transactions', methods=['GET'])
@require_auth
def get_transactions(user_email):
    """Retorna as transações do usuário"""
    user = users_db[user_email]
    return jsonify({'transactions': user['transactions']}), 200

@banking_bp.route('/api/transfer', methods=['POST'])
@require_auth
def transfer_money(user_email):
    """Transfere dinheiro entre contas"""
    data = request.get_json()
    to_account = data.get('to_account')
    amount = data.get('amount')
    description = data.get('description', 'Transferência')
    
    if not to_account or not amount:
        return jsonify({'error': 'Campos obrigatórios ausentes'}), 400
    
    if amount <= 0:
        return jsonify({'error': 'Valor deve ser positivo'}), 400
    
    user = users_db[user_email]
    
    if user['balance'] < amount:
        return jsonify({'error': 'Saldo insuficiente'}), 400
    
    # Find recipient account
    recipient = None
    for email, user_data in users_db.items():
        if user_data['account_number'] == to_account:
            recipient = user_data
            recipient_email = email
            break
    
    if not recipient:
        return jsonify({'error': 'Conta destinatária não encontrada'}), 404
    
    # Perform transfer
    user['balance'] -= amount
    recipient['balance'] += amount
    
    # Add transactions
    user_transaction = {
        'id': len(user['transactions']) + 1,
        'type': 'transfer_out',
        'amount': -amount,
        'date': '2024-01-23',
        'description': f'Transferência para {to_account} - {description}'
    }
    
    recipient_transaction = {
        'id': len(recipient['transactions']) + 1,
        'type': 'transfer_in',
        'amount': amount,
        'date': '2024-01-23',
        'description': f'Transferência de {user["account_number"]} - {description}'
    }
    
    user['transactions'].append(user_transaction)
    recipient['transactions'].append(recipient_transaction)
    
    return jsonify({'message': 'Transferência realizada com sucesso'}), 200

@banking_bp.route('/api/deposit', methods=['POST'])
@require_auth
def deposit_money(user_email):
    """Deposita dinheiro na conta"""
    data = request.get_json()
    amount = data.get('amount')
    description = data.get('description', 'Depósito')
    
    if not amount:
        return jsonify({'error': 'Valor ausente'}), 400
    
    if amount <= 0:
        return jsonify({'error': 'Valor deve ser positivo'}), 400
    
    user = users_db[user_email]
    user['balance'] += amount
    
    transaction = {
        'id': len(user['transactions']) + 1,
        'type': 'deposit',
        'amount': amount,
        'date': '2024-01-23',
        'description': description
    }
    
    user['transactions'].append(transaction)
    
    return jsonify({'message': 'Depósito realizado com sucesso'}), 200
