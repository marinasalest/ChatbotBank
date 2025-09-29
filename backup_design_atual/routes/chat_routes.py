"""
Rotas do sistema de chat
"""
from flask import Blueprint, request, jsonify
from models.database import users_db, load_banking_intents, load_faq_responses
from models.ai_processor import SimpleBankingAI
from auth.jwt_handler import require_auth

chat_bp = Blueprint('chat', __name__)

# Load data
BANKING_KB = load_banking_intents()
FAQ_RESPONSES = load_faq_responses()
ai_processor = SimpleBankingAI()

@chat_bp.route('/api/chat', methods=['POST'])
@require_auth
def chat(user_email):
    """Processa mensagens do chat"""
    data = request.get_json()
    message = data.get('message')
    
    if not message:
        return jsonify({'error': 'Mensagem ausente'}), 400
    
    # Process message with AI
    result = ai_processor.process_message(message, BANKING_KB, FAQ_RESPONSES)
    
    intent_name = result['intent']
    intent_data = result['intent_data']
    sentiment = result['sentiment']
    amount = result['amount']
    account = result['account']
    
    user = users_db[user_email]
    
    # Handle different intents
    if intent_name == 'saldo':
        return jsonify({
            'response': f"Seu saldo atual é R$ {user['balance']:.2f}",
            'type': 'balance',
            'intent': intent_name,
            'sentiment': sentiment,
            'extracted_amount': amount,
            'extracted_account': account
        })
    
    elif intent_name == 'transacoes':
        transactions_text = ""
        for t in user['transactions'][-5:]:  # Last 5 transactions
            transactions_text += f"• {t['description']}: R$ {t['amount']:.2f} ({t['date']})\n"
        
        return jsonify({
            'response': f"Aqui estão suas transações recentes:\n{transactions_text}",
            'type': 'transactions',
            'intent': intent_name,
            'sentiment': sentiment,
            'extracted_amount': amount,
            'extracted_account': account
        })
    
    elif intent_name == 'transferencia':
        response = intent_data['response_template']
        if amount:
            response += f"\n\n💡 Detectei que você quer transferir R$ {amount:.2f}."
        if account:
            response += f"\n💡 Para a conta {account}."
        return jsonify({
            'response': response,
            'type': 'info',
            'intent': intent_name,
            'sentiment': sentiment,
            'extracted_amount': amount,
            'extracted_account': account
        })
    
    elif intent_name == 'pix':
        return jsonify({
            'response': intent_data['response_template'],
            'type': 'info',
            'intent': intent_name,
            'sentiment': sentiment,
            'extracted_amount': amount,
            'extracted_account': account
        })
    
    elif intent_name == 'deposito':
        response = intent_data['response_template']
        if amount:
            response += f"\n\n💡 Detectei que você quer depositar R$ {amount:.2f}."
        return jsonify({
            'response': response,
            'type': 'info',
            'intent': intent_name,
            'sentiment': sentiment,
            'extracted_amount': amount,
            'extracted_account': account
        })
    
    elif intent_name == 'ajuda':
        return jsonify({
            'response': intent_data['response_template'].format(name=user['name']),
            'type': 'help',
            'intent': intent_name,
            'sentiment': sentiment,
            'extracted_amount': amount,
            'extracted_account': account
        })
    
    elif intent_name == 'saudacao':
        return jsonify({
            'response': intent_data['response_template'].format(name=user['name']),
            'type': 'greeting',
            'intent': intent_name,
            'sentiment': sentiment,
            'extracted_amount': amount,
            'extracted_account': account
        })
    
    elif intent_name == 'faq':
        return jsonify({
            'response': intent_data['answer'],
            'type': 'faq',
            'intent': intent_name,
            'sentiment': sentiment,
            'extracted_amount': amount,
            'extracted_account': account
        })
    
    else:
        return jsonify({
            'response': "Estou aqui para ajudá-lo com suas necessidades bancárias. Você pode me perguntar sobre seu saldo, transações, transferências, ou apenas diga 'ajuda' para mais opções.",
            'type': 'general',
            'intent': 'unknown',
            'sentiment': sentiment,
            'extracted_amount': amount,
            'extracted_account': account
        })

@chat_bp.route('/api/nlp/debug', methods=['POST'])
@require_auth
def debug_nlp(user_email):
    """Endpoint para debug do processamento NLP"""
    data = request.get_json()
    message = data.get('message')
    
    if not message:
        return jsonify({'error': 'Mensagem ausente'}), 400
    
    # Process message
    result = ai_processor.process_message(message, BANKING_KB, FAQ_RESPONSES)
    
    # Preprocess text for debugging
    processed_text = ai_processor.preprocess_text(message)
    
    return jsonify({
        'original_message': message,
        'processed_text': processed_text,
        'sentiment': result['sentiment'],
        'extracted_amount': result['amount'],
        'extracted_account': result['account'],
        'keyword_intent': result.get('intent') if result['method'] == 'keywords' else None,
        'similarity_intent': result.get('intent') if result['method'] == 'similarity' else None,
        'similarity_data': result.get('intent_data')
    })
