from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import bcrypt
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import spacy
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Load Portuguese language model for spaCy
try:
    nlp = spacy.load("pt_core_news_sm")
except OSError:
    print("Modelo português não encontrado. Instalando...")
    os.system("python -m spacy download pt_core_news_sm")
    nlp = spacy.load("pt_core_news_sm")

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
    }
}

# Knowledge base for banking queries
BANKING_KB = {
    'saldo': {
        'keywords': ['saldo', 'quanto tenho', 'dinheiro na conta', 'valor disponível', 'balance'],
        'intent': 'balance',
        'response_template': 'Seu saldo atual é R$ {balance:.2f}'
    },
    'transacoes': {
        'keywords': ['transações', 'histórico', 'movimentações', 'extrato', 'transaction', 'history'],
        'intent': 'transactions',
        'response_template': 'Aqui estão suas transações recentes:\n{transactions}'
    },
    'transferencia': {
        'keywords': ['transferir', 'transferência', 'enviar dinheiro', 'pix', 'transfer'],
        'intent': 'transfer',
        'response_template': 'Para fazer uma transferência, use o formulário de transferência. Você precisará do número da conta do destinatário e do valor que deseja enviar.'
    },
    'deposito': {
        'keywords': ['depositar', 'depósito', 'adicionar dinheiro', 'deposit'],
        'intent': 'deposit',
        'response_template': 'Para fazer um depósito, use o formulário de depósito. Você pode adicionar dinheiro à sua conta.'
    },
    'ajuda': {
        'keywords': ['ajuda', 'help', 'como usar', 'o que posso fazer'],
        'intent': 'help',
        'response_template': 'Posso ajudá-lo com:\n\n<ol style="margin: 10px 0; padding-left: 20px;">\n<li>💰 <strong>Consultar saldo da conta</strong></li>\n<li>📊 <strong>Ver histórico de transações</strong></li>\n<li>💸 <strong>Fazer transferências</strong></li>\n<li>💳 <strong>Processar depósitos</strong></li>\n<li>❓ <strong>Responder perguntas bancárias gerais</strong></li>\n</ol>\n\nO que gostaria de saber?'
    },
    'saudacao': {
        'keywords': ['olá', 'oi', 'bom dia', 'boa tarde', 'boa noite', 'hello', 'hi'],
        'intent': 'greeting',
        'response_template': 'Olá {name}! Como posso ajudá-lo com suas necessidades bancárias hoje?'
    }
}

# FAQ responses for complex queries
FAQ_RESPONSES = [
    {
        'question': 'como abrir uma conta',
        'answer': 'Para abrir uma conta, você precisa se dirigir a uma agência bancária com seus documentos pessoais (RG, CPF, comprovante de residência) e comprovante de renda.'
    },
    {
        'question': 'qual o limite de transferência',
        'answer': 'O limite de transferência varia conforme o tipo de conta. Para contas básicas, o limite é de R$ 1.000 por dia. Para contas premium, pode chegar a R$ 10.000 por dia.'
    },
    {
        'question': 'como funciona o pix',
        'answer': 'O PIX é um sistema de pagamentos instantâneos. Você pode transferir dinheiro 24 horas por dia, incluindo finais de semana e feriados, usando apenas a chave PIX (CPF, email, telefone ou chave aleatória).'
    },
    {
        'question': 'como cancelar uma transferência',
        'answer': 'Transferências PIX não podem ser canceladas após a confirmação. Para transferências tradicionais, entre em contato conosco imediatamente para tentar cancelar.'
    },
    {
        'question': 'qual a taxa de transferência',
        'answer': 'Transferências PIX são gratuitas. Transferências TED têm taxa de R$ 8,50. Transferências DOC têm taxa de R$ 5,00.'
    }
]

class BankingNLP:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.faq_questions = [faq['question'] for faq in FAQ_RESPONSES]
        self.faq_answers = [faq['answer'] for faq in FAQ_RESPONSES]
        self._train_vectorizer()
    
    def _train_vectorizer(self):
        """Train TF-IDF vectorizer on FAQ questions"""
        self.vectorizer.fit(self.faq_questions)
    
    def preprocess_text(self, text):
        """Preprocess text using spaCy"""
        doc = nlp(text.lower())
        # Remove stop words and punctuation, lemmatize
        tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
        return ' '.join(tokens)
    
    def extract_entities(self, text):
        """Extract named entities using spaCy"""
        doc = nlp(text)
        entities = []
        for ent in doc.ents:
            entities.append({
                'text': ent.text,
                'label': ent.label_,
                'start': ent.start_char,
                'end': ent.end_char
            })
        return entities
    
    def find_intent_by_keywords(self, text):
        """Find intent using keyword matching (rule-based)"""
        text_lower = text.lower()
        
        for intent_name, intent_data in BANKING_KB.items():
            for keyword in intent_data['keywords']:
                if keyword in text_lower:
                    return intent_name, intent_data
        
        return None, None
    
    def find_intent_by_similarity(self, text):
        """Find intent using semantic similarity (AI-based)"""
        processed_text = self.preprocess_text(text)
        
        # Vectorize the input text
        text_vector = self.vectorizer.transform([processed_text])
        
        # Calculate similarity with FAQ questions
        similarities = cosine_similarity(text_vector, self.vectorizer.transform(self.faq_questions))
        max_similarity_idx = np.argmax(similarities)
        max_similarity = similarities[0][max_similarity_idx]
        
        # If similarity is high enough, return FAQ answer
        if max_similarity > 0.3:
            return 'faq', {
                'answer': self.faq_answers[max_similarity_idx],
                'similarity': max_similarity
            }
        
        return None, None
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of the text"""
        doc = nlp(text)
        
        # Simple sentiment analysis based on positive/negative words
        positive_words = ['obrigado', 'obrigada', 'ótimo', 'bom', 'excelente', 'perfeito', 'legal']
        negative_words = ['ruim', 'péssimo', 'terrível', 'problema', 'erro', 'falha', 'não funciona']
        
        pos_count = sum(1 for word in positive_words if word in text.lower())
        neg_count = sum(1 for word in negative_words if word in text.lower())
        
        if pos_count > neg_count:
            return 'positive'
        elif neg_count > pos_count:
            return 'negative'
        else:
            return 'neutral'
    
    def extract_amount(self, text):
        """Extract monetary amounts from text"""
        # Look for patterns like "R$ 100", "100 reais", "100,50", etc.
        amount_patterns = [
            r'R\$\s*(\d+(?:[.,]\d{2})?)',
            r'(\d+(?:[.,]\d{2})?)\s*reais?',
            r'(\d+(?:[.,]\d{2})?)\s*R\$'
        ]
        
        for pattern in amount_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                amount_str = match.group(1).replace(',', '.')
                try:
                    return float(amount_str)
                except ValueError:
                    continue
        
        return None
    
    def extract_account_number(self, text):
        """Extract account numbers from text"""
        # Look for patterns like "conta 1234567890", "1234567890", etc.
        account_patterns = [
            r'conta\s*(\d{10})',
            r'(\d{10})',
            r'número\s*(\d{10})'
        ]
        
        for pattern in account_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None

# Initialize NLP processor
nlp_processor = BankingNLP()

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
    message = data.get('message', '')
    
    user = users_db[user_email]
    
    # AI/NLP Processing
    print(f"Processing message: {message}")
    
    # Extract entities
    entities = nlp_processor.extract_entities(message)
    print(f"Entities found: {entities}")
    
    # Analyze sentiment
    sentiment = nlp_processor.analyze_sentiment(message)
    print(f"Sentiment: {sentiment}")
    
    # Extract amount if present
    amount = nlp_processor.extract_amount(message)
    if amount:
        print(f"Amount extracted: {amount}")
    
    # Extract account number if present
    account = nlp_processor.extract_account_number(message)
    if account:
        print(f"Account number extracted: {account}")
    
    # Try rule-based approach first
    intent_name, intent_data = nlp_processor.find_intent_by_keywords(message)
    
    if intent_name and intent_data:
        print(f"Intent found by keywords: {intent_name}")
        
        if intent_name == 'saldo':
            return jsonify({
                'response': intent_data['response_template'].format(balance=user['balance']),
                'type': 'balance',
                'intent': intent_name,
                'sentiment': sentiment,
                'entities': entities
            })
        
        elif intent_name == 'transacoes':
            recent_transactions = user['transactions'][-5:]
            if recent_transactions:
                transactions_text = ""
                for tx in reversed(recent_transactions):
                    transactions_text += f"• {tx['date']}: {tx['description']} - R$ {tx['amount']:.2f}\n"
                response = intent_data['response_template'].format(transactions=transactions_text)
            else:
                response = "Você ainda não possui transações."
            return jsonify({
                'response': response,
                'type': 'transactions',
                'intent': intent_name,
                'sentiment': sentiment,
                'entities': entities
            })
        
        elif intent_name == 'transferencia':
            return jsonify({
                'response': intent_data['response_template'],
                'type': 'info',
                'intent': intent_name,
                'sentiment': sentiment,
                'entities': entities
            })
        
        elif intent_name == 'deposito':
            return jsonify({
                'response': intent_data['response_template'],
                'type': 'info',
                'intent': intent_name,
                'sentiment': sentiment,
                'entities': entities
            })
        
        elif intent_name == 'ajuda':
            return jsonify({
                'response': intent_data['response_template'],
                'type': 'help',
                'intent': intent_name,
                'sentiment': sentiment,
                'entities': entities
            })
        
        elif intent_name == 'saudacao':
            return jsonify({
                'response': intent_data['response_template'].format(name=user['name']),
                'type': 'greeting',
                'intent': intent_name,
                'sentiment': sentiment,
                'entities': entities
            })
    
    # Try AI-based approach for complex queries
    intent_name, intent_data = nlp_processor.find_intent_by_similarity(message)
    
    if intent_name == 'faq' and intent_data:
        print(f"Intent found by similarity: {intent_name}")
        return jsonify({
            'response': intent_data['answer'],
            'type': 'faq',
            'intent': intent_name,
            'sentiment': sentiment,
            'entities': entities,
            'similarity': intent_data['similarity']
        })
    
    # Fallback response with enhanced information
    fallback_response = "Estou aqui para ajudá-lo com suas necessidades bancárias. "
    
    if sentiment == 'negative':
        fallback_response += "Peço desculpas se algo não está funcionando como esperado. "
    
    fallback_response += "Você pode me perguntar sobre seu saldo, transações, transferências, ou apenas diga 'ajuda' para mais opções."
    
    return jsonify({
        'response': fallback_response,
        'type': 'general',
        'intent': 'unknown',
        'sentiment': sentiment,
        'entities': entities
    })

@app.route('/api/nlp/debug', methods=['POST'])
@require_auth
def debug_nlp(user_email):
    """Debug endpoint to analyze text processing"""
    data = request.get_json()
    message = data.get('message', '')
    
    # Process the message
    entities = nlp_processor.extract_entities(message)
    sentiment = nlp_processor.analyze_sentiment(message)
    amount = nlp_processor.extract_amount(message)
    account = nlp_processor.extract_account_number(message)
    processed_text = nlp_processor.preprocess_text(message)
    
    # Try both approaches
    keyword_intent, keyword_data = nlp_processor.find_intent_by_keywords(message)
    similarity_intent, similarity_data = nlp_processor.find_intent_by_similarity(message)
    
    return jsonify({
        'original_text': message,
        'processed_text': processed_text,
        'entities': entities,
        'sentiment': sentiment,
        'extracted_amount': amount,
        'extracted_account': account,
        'keyword_intent': keyword_intent,
        'similarity_intent': similarity_intent,
        'similarity_data': similarity_data
    })

if __name__ == '__main__':
    print("🤖 Iniciando Chatbot Bancário com IA/NLP...")
    print("📚 Modelos de linguagem carregados")
    print("🧠 Processador NLP inicializado")
    print("🚀 Servidor iniciando...")
    app.run(debug=True, host='0.0.0.0', port=5000)
