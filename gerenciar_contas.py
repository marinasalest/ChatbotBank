#!/usr/bin/env python3
"""
Script para gerenciar contas bancárias do chatbot
"""

import json
from datetime import datetime

# Dados das contas (copiados do app_simple_ai.py)
contas = {
    'joao.silva@email.com': {
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
        'name': 'Maria Santos',
        'account_number': '0000000002',
        'balance': 3200.00,
        'transactions': [
            {'id': 1, 'type': 'deposit', 'amount': 3200.00, 'date': '2024-01-10', 'description': 'Depósito inicial'},
        ]
    },
    'pedro.oliveira@email.com': {
        'name': 'Pedro Oliveira',
        'account_number': '0000000003',
        'balance': 1500.00,
        'transactions': [
            {'id': 1, 'type': 'deposit', 'amount': 2000.00, 'date': '2024-01-12', 'description': 'Depósito inicial'},
            {'id': 2, 'type': 'purchase', 'amount': -500.00, 'date': '2024-01-18', 'description': 'Compras online'},
        ]
    },
    'ana.costa@email.com': {
        'name': 'Ana Costa',
        'account_number': '0000000004',
        'balance': 7500.00,
        'transactions': [
            {'id': 1, 'type': 'deposit', 'amount': 7500.00, 'date': '2024-01-08', 'description': 'Depósito inicial'},
        ]
    },
    'carlos.ferreira@email.com': {
        'name': 'Carlos Ferreira',
        'account_number': '0000000005',
        'balance': 2800.00,
        'transactions': [
            {'id': 1, 'type': 'deposit', 'amount': 3000.00, 'date': '2024-01-14', 'description': 'Depósito inicial'},
            {'id': 2, 'type': 'purchase', 'amount': -200.00, 'date': '2024-01-19', 'description': 'Farmácia'},
        ]
    },
    'lucia.rodrigues@email.com': {
        'name': 'Lúcia Rodrigues',
        'account_number': '0000000006',
        'balance': 4200.00,
        'transactions': [
            {'id': 1, 'type': 'deposit', 'amount': 4200.00, 'date': '2024-01-11', 'description': 'Depósito inicial'},
        ]
    },
    'roberto.almeida@email.com': {
        'name': 'Roberto Almeida',
        'account_number': '0000000007',
        'balance': 1800.00,
        'transactions': [
            {'id': 1, 'type': 'deposit', 'amount': 2500.00, 'date': '2024-01-13', 'description': 'Depósito inicial'},
            {'id': 2, 'type': 'purchase', 'amount': -700.00, 'date': '2024-01-17', 'description': 'Eletrônicos'},
        ]
    },
    'fernanda.lima@email.com': {
        'name': 'Fernanda Lima',
        'account_number': '0000000008',
        'balance': 6200.00,
        'transactions': [
            {'id': 1, 'type': 'deposit', 'amount': 6200.00, 'date': '2024-01-09', 'description': 'Depósito inicial'},
        ]
    },
    'marcos.souza@email.com': {
        'name': 'Marcos Souza',
        'account_number': '0000000009',
        'balance': 950.00,
        'transactions': [
            {'id': 1, 'type': 'deposit', 'amount': 1500.00, 'date': '2024-01-16', 'description': 'Depósito inicial'},
            {'id': 2, 'type': 'purchase', 'amount': -550.00, 'date': '2024-01-21', 'description': 'Restaurante'},
        ]
    },
    'patricia.mendes@email.com': {
        'name': 'Patrícia Mendes',
        'account_number': '0000000010',
        'balance': 3800.00,
        'transactions': [
            {'id': 1, 'type': 'deposit', 'amount': 3800.00, 'date': '2024-01-07', 'description': 'Depósito inicial'},
        ]
    },
    'antonio.barbosa@email.com': {
        'name': 'Antônio Barbosa',
        'account_number': '0000000011',
        'balance': 2100.00,
        'transactions': [
            {'id': 1, 'type': 'deposit', 'amount': 2500.00, 'date': '2024-01-15', 'description': 'Depósito inicial'},
            {'id': 2, 'type': 'purchase', 'amount': -400.00, 'date': '2024-01-22', 'description': 'Supermercado'},
        ]
    }
}

def mostrar_resumo():
    """Mostra resumo das contas"""
    total_contas = len(contas)
    saldo_total = sum(conta['balance'] for conta in contas.values())
    saldo_medio = saldo_total / total_contas
    
    print("=" * 60)
    print("🏦 RESUMO DAS CONTAS BANCÁRIAS")
    print("=" * 60)
    print(f"📊 Total de Contas: {total_contas}")
    print(f"💰 Saldo Total: R$ {saldo_total:,.2f}")
    print(f"📈 Saldo Médio: R$ {saldo_medio:,.2f}")
    print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 60)

def listar_contas():
    """Lista todas as contas"""
    print("\n📋 LISTA COMPLETA DE CONTAS")
    print("-" * 60)
    
    for i, (email, conta) in enumerate(contas.items(), 1):
        print(f"{i:2d}. {conta['name']}")
        print(f"    📧 Email: {email}")
        print(f"    🏦 Conta: {conta['account_number']}")
        print(f"    💰 Saldo: R$ {conta['balance']:,.2f}")
        print(f"    📊 Transações: {len(conta['transactions'])}")
        print()

def buscar_conta():
    """Busca conta por nome ou email"""
    termo = input("\n🔍 Digite nome ou email para buscar: ").lower()
    
    encontradas = []
    for email, conta in contas.items():
        if (termo in conta['name'].lower() or 
            termo in email.lower() or 
            termo in conta['account_number']):
            encontradas.append((email, conta))
    
    if encontradas:
        print(f"\n✅ Encontradas {len(encontradas)} conta(s):")
        for email, conta in encontradas:
            print(f"   👤 {conta['name']} ({email})")
            print(f"   🏦 Conta: {conta['account_number']}")
            print(f"   💰 Saldo: R$ {conta['balance']:,.2f}")
            print()
    else:
        print("❌ Nenhuma conta encontrada.")

def mostrar_ranking():
    """Mostra ranking por saldo"""
    print("\n🏆 RANKING POR SALDO")
    print("-" * 60)
    
    ranking = sorted(contas.items(), key=lambda x: x[1]['balance'], reverse=True)
    
    for i, (email, conta) in enumerate(ranking, 1):
        emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🏅"
        print(f"{emoji} {i:2d}. {conta['name']} - R$ {conta['balance']:,.2f}")

def exportar_dados():
    """Exporta dados para JSON"""
    filename = f"contas_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(contas, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Dados exportados para: {filename}")

def menu():
    """Menu principal"""
    while True:
        print("\n" + "=" * 60)
        print("🏦 GERENCIADOR DE CONTAS BANCÁRIAS")
        print("=" * 60)
        print("1. 📊 Mostrar Resumo")
        print("2. 📋 Listar Todas as Contas")
        print("3. 🔍 Buscar Conta")
        print("4. 🏆 Ranking por Saldo")
        print("5. 💾 Exportar Dados")
        print("6. ❌ Sair")
        print("-" * 60)
        
        opcao = input("Escolha uma opção (1-6): ").strip()
        
        if opcao == '1':
            mostrar_resumo()
        elif opcao == '2':
            listar_contas()
        elif opcao == '3':
            buscar_conta()
        elif opcao == '4':
            mostrar_ranking()
        elif opcao == '5':
            exportar_dados()
        elif opcao == '6':
            print("\n👋 Até logo!")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    print("🤖 Iniciando Gerenciador de Contas...")
    menu()
