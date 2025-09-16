"""
Modelo de dados e funções de carregamento
"""
import json
import bcrypt

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

def load_banking_intents():
    """Carrega intents bancários do arquivo JSON"""
    try:
        with open('data/banking_intents.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['intents']
    except FileNotFoundError:
        print("⚠️ Arquivo banking_intents.json não encontrado. Usando dados padrão.")
        return {}

def load_faq_responses():
    """Carrega respostas FAQ do arquivo JSON"""
    try:
        with open('data/banking_concepts.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['concepts']
    except FileNotFoundError:
        print("⚠️ Arquivo banking_concepts.json não encontrado. Usando dados padrão.")
        return []


