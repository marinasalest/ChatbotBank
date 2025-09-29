# Chatbot Bancário com IA/NLP 🤖🧠

Uma versão avançada do chatbot bancário que combina **regras simples** com **Inteligência Artificial** e **Processamento de Linguagem Natural (NLP)**.

## 🚀 Funcionalidades Avançadas

### 🧠 Processamento de Linguagem Natural
- **spaCy**: Análise linguística avançada em português
- **NLTK**: Processamento de texto e tokenização
- **scikit-learn**: Similaridade semântica e classificação
- **Extração de entidades**: Identifica nomes, valores, datas
- **Análise de sentimento**: Detecta emoções nas mensagens

### 🔄 Sistema Híbrido Inteligente
1. **Regras Simples** (primeira tentativa)
   - Correspondência de palavras-chave
   - Respostas rápidas e diretas
   
2. **IA/NLP** (segunda tentativa)
   - Similaridade semântica
   - Base de conhecimento FAQ
   - Compreensão contextual

### 🎯 Recursos Avançados
- **Extração de valores**: "Quero transferir R$ 100" → extrai 100
- **Extração de contas**: "Transferir para conta 1234567890" → extrai conta
- **Análise de sentimento**: Detecta frustração, satisfação, etc.
- **Entidades nomeadas**: Identifica pessoas, organizações, valores
- **FAQ inteligente**: Responde perguntas complexas sobre bancos

## 📦 Instalação

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Instalar Modelos de Linguagem
```bash
python install_models.py
```

### 3. Executar o Chatbot
```bash
python app_ai.py
```

## 🧪 Como Testar as Funcionalidades IA

### Teste 1: Análise de Sentimento
```
Usuário: "Estou muito frustrado com esse sistema!"
Bot: Detecta sentimento negativo e responde com empatia
```

### Teste 2: Extração de Valores
```
Usuário: "Quero transferir R$ 150,50 para minha mãe"
Bot: Extrai valor (150.50) e sugere transferência
```

### Teste 3: FAQ Inteligente
```
Usuário: "Como funciona o PIX?"
Bot: Resposta detalhada sobre PIX usando similaridade semântica
```

### Teste 4: Entidades Nomeadas
```
Usuário: "Transferir para João Silva na conta 1234567890"
Bot: Identifica pessoa (João Silva) e conta (1234567890)
```

## 🔍 Endpoints de Debug

### `/api/nlp/debug` - Análise Detalhada
```json
POST /api/nlp/debug
{
  "message": "Quero transferir R$ 100 para conta 1234567890"
}
```

**Resposta:**
```json
{
  "original_text": "Quero transferir R$ 100 para conta 1234567890",
  "processed_text": "quer transferir 100 conta",
  "entities": [
    {"text": "R$ 100", "label": "MONEY"},
    {"text": "1234567890", "label": "CARDINAL"}
  ],
  "sentiment": "neutral",
  "extracted_amount": 100.0,
  "extracted_account": "1234567890",
  "keyword_intent": "transferencia",
  "similarity_intent": null
}
```

## 🏗️ Arquitetura do Sistema

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Flask API      │    │   IA/NLP        │
│   (HTML/JS)     │◄──►│   (app_ai.py)    │◄──►│   (spaCy/NLTK)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │   Base de        │
                       │   Conhecimento   │
                       │   (FAQ + Rules)  │
                       └──────────────────┘
```

## 🧠 Processo de Decisão

1. **Recebe mensagem do usuário**
2. **Pré-processa texto** (spaCy + NLTK)
3. **Extrai entidades** (valores, contas, pessoas)
4. **Analisa sentimento** (positivo/negativo/neutro)
5. **Tenta regras simples** (palavras-chave)
6. **Se não encontrar, usa IA** (similaridade semântica)
7. **Retorna resposta contextualizada**

## 📊 Exemplos de Uso

### Consulta Simples (Regras)
```
Usuário: "Qual meu saldo?"
Processamento: Palavra-chave "saldo" → regra simples
Resposta: "Seu saldo atual é R$ 5.000,00"
```

### Consulta Complexa (IA)
```
Usuário: "Como posso enviar dinheiro para minha filha que mora em outra cidade?"
Processamento: Similaridade semântica → FAQ sobre transferências
Resposta: "Para enviar dinheiro para outra cidade, você pode usar PIX (gratuito e instantâneo) ou TED (taxa de R$ 8,50)..."
```

### Extração Inteligente
```
Usuário: "Transferir R$ 250,75 para conta 9876543210"
Processamento: 
- Extrai valor: 250.75
- Extrai conta: 9876543210
- Intent: transferência
Resposta: "Para transferir R$ 250,75 para a conta 9876543210, use o formulário de transferência..."
```

## 🎯 Vantagens do Sistema Híbrido

### ✅ Regras Simples
- **Rápido**: Resposta imediata
- **Confiável**: Sempre funciona para casos conhecidos
- **Eficiente**: Baixo uso de recursos

### ✅ IA/NLP
- **Inteligente**: Compreende linguagem natural
- **Flexível**: Adapta-se a diferentes formas de perguntar
- **Contextual**: Considera sentimento e entidades

### ✅ Combinação
- **Melhor dos dois mundos**
- **Fallback inteligente**
- **Experiência do usuário superior**

## 🔧 Configuração Avançada

### Personalizar Base de Conhecimento
Edite o dicionário `BANKING_KB` em `app_ai.py`:

```python
BANKING_KB = {
    'novo_intent': {
        'keywords': ['palavra1', 'palavra2'],
        'intent': 'novo_intent',
        'response_template': 'Sua resposta aqui: {variavel}'
    }
}
```

### Adicionar FAQs
Edite a lista `FAQ_RESPONSES`:

```python
FAQ_RESPONSES = [
    {
        'question': 'nova pergunta',
        'answer': 'Nova resposta detalhada'
    }
]
```

## 🚀 Próximos Passos

- [ ] Integração com OpenAI GPT
- [ ] Machine Learning para melhorar respostas
- [ ] Análise de intenções mais sofisticada
- [ ] Suporte a múltiplos idiomas
- [ ] Integração com banco de dados real

## 📝 Comparação: Regras vs IA/NLP

| Aspecto | Regras Simples | IA/NLP |
|---------|----------------|---------|
| Velocidade | ⚡ Muito rápida | 🐌 Mais lenta |
| Precisão | ✅ 100% para casos conhecidos | 🎯 85-95% geral |
| Flexibilidade | ❌ Limitada | ✅ Muito flexível |
| Recursos | 💚 Baixo uso | 🔥 Alto uso |
| Manutenção | 🔧 Fácil | 🤖 Complexa |
| Compreensão | 📝 Literal | 🧠 Contextual |

## 🎉 Conclusão

Este chatbot combina o melhor dos dois mundos:
- **Regras simples** para respostas rápidas e confiáveis
- **IA/NLP** para compreensão avançada e flexibilidade

Resultado: Um chatbot bancário inteligente, rápido e eficiente! 🚀
