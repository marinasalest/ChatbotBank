# Chatbot Bancário

Um chatbot bancário moderno e interativo construído com Flask e uma interface web bonita. Este chatbot fornece serviços bancários seguros incluindo gerenciamento de conta, transferências de dinheiro, depósitos e um assistente de chat inteligente.

## Funcionalidades

### 🔐 Autenticação
- Registro e login seguro de usuários
- Autenticação baseada em tokens JWT
- Hash de senhas com bcrypt

### 💰 Serviços Bancários
- **Saldo da Conta**: Visualizar saldo atual da conta
- **Histórico de Transações**: Ver todas as transações passadas
- **Transferência de Dinheiro**: Enviar dinheiro para outras contas
- **Depósitos**: Adicionar dinheiro à sua conta
- **Atualizações em Tempo Real**: Atualizações instantâneas de saldo e transações

### 🤖 Assistente de Chat Inteligente
- Processamento de linguagem natural para consultas bancárias
- Consultas de saldo
- Solicitações de histórico de transações
- Assistência para transferências
- Ajuda bancária geral

### 🎨 Interface Moderna
- Design responsivo que funciona em todos os dispositivos
- Fundos com gradientes bonitos
- Navegação intuitiva
- Interface de chat em tempo real
- Interface bancária limpa e profissional

## Instalação

1. **Clone o repositório**
   ```bash
   git clone <url-do-repositorio>
   cd bank-chatbot
   ```

2. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure as variáveis de ambiente**
   Crie um arquivo `.env` no diretório raiz:
   ```
   SECRET_KEY=sua-chave-super-secreta-mude-isso-em-producao
   FLASK_ENV=development
   ```

4. **Execute a aplicação**
   ```bash
   python app.py
   ```

5. **Abra seu navegador**
   Navegue para `http://localhost:5000`

## Como Usar

### Começando
1. **Registre uma nova conta** ou use a conta demo:
   - Email: `joao.silva@email.com`
   - Senha: `senha123`

2. **Explore as funcionalidades**:
   - **Painel**: Visão geral da sua conta
   - **Assistente**: Faça perguntas sobre sua conta
   - **Transações**: Veja seu histórico de transações
   - **Transferir Dinheiro**: Envie dinheiro para outras contas
   - **Depositar**: Adicione dinheiro à sua conta

### Comandos do Chat
O chatbot entende consultas em linguagem natural:
- "Qual é o meu saldo?"
- "Mostre minhas transações"
- "Como faço uma transferência?"
- "Me ajude com o banco"
- "Olá" ou "Oi"

## Endpoints da API

### Autenticação
- `POST /api/register` - Registrar novo usuário
- `POST /api/login` - Login do usuário

### Serviços Bancários
- `GET /api/balance` - Obter saldo da conta
- `GET /api/transactions` - Obter histórico de transações
- `POST /api/transfer` - Transferir dinheiro
- `POST /api/deposit` - Depositar dinheiro

### Chat
- `POST /api/chat` - Enviar mensagem para o chatbot

## Recursos de Segurança

- **Hash de Senhas**: Todas as senhas são criptografadas com segurança usando bcrypt
- **Tokens JWT**: Autenticação segura com JSON Web Tokens
- **Validação de Entrada**: Todas as entradas são validadas e sanitizadas
- **Proteção CORS**: Requisições cross-origin são tratadas adequadamente

## Conta Demo

Para fins de teste, uma conta demo está pré-configurada:
- **Email**: joao.silva@email.com
- **Senha**: senha123
- **Número da Conta**: 1234567890
- **Saldo Inicial**: R$ 5.000,00

## Stack Tecnológica

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Autenticação**: JWT + bcrypt
- **Estilização**: CSS customizado com design moderno
- **Armazenamento de Dados**: Em memória (para fins de demonstração)

## Desenvolvimento

### Estrutura do Projeto
```
bank-chatbot/
├── app.py              # Aplicação principal Flask
├── templates/
│   └── index.html      # Interface web principal
├── requirements.txt    # Dependências Python
├── .env               # Variáveis de ambiente
└── README.md          # Este arquivo
```

### Adicionando Novas Funcionalidades
1. Adicione novos endpoints da API em `app.py`
2. Atualize o JavaScript frontend em `index.html`
3. Adicione novas seções de UI conforme necessário
4. Teste completamente antes do deploy

## Deploy em Produção

Para deploy em produção:

1. **Use um banco de dados adequado** (PostgreSQL, MySQL, etc.)
2. **Defina uma SECRET_KEY forte** nas variáveis de ambiente
3. **Use HTTPS** para todas as comunicações
4. **Implemente rate limiting** para endpoints da API
5. **Adicione logging e monitoramento**
6. **Use um servidor WSGI de produção** (Gunicorn, uWSGI)

## Contribuindo

1. Faça um fork do repositório
2. Crie uma branch de feature
3. Faça suas alterações
4. Adicione testes se aplicável
5. Envie um pull request

## Licença

Este projeto é open source e está disponível sob a Licença MIT.

## Suporte

Para suporte ou dúvidas, abra uma issue no repositório ou entre em contato com a equipe de desenvolvimento.

---

**Nota**: Esta é uma aplicação de demonstração para fins educacionais. Não use em produção sem auditorias de segurança adequadas e implementação de banco de dados.