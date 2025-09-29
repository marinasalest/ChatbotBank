# 🧠 Guia Completo: Como Expandir e Alimentar o Banking Intents

## 📋 **Estrutura Atual do banking_intents.json**

O arquivo `data/banking_intents.json` contém **intents** (intenções) que o chatbot reconhece. Cada intent tem:

```json
{
  "intents": {
    "nome_do_intent": {
      "keywords": ["palavra1", "palavra2", "sinônimo"],
      "intent": "nome_do_intent",
      "response_template": "Resposta formatada com {variáveis}"
    }
  }
}
```

## 🚀 **Como Adicionar Novos Intents**

### **1. Identifique a Necessidade**
- Que funcionalidade o usuário precisa?
- Que perguntas ele faz frequentemente?
- Que serviços bancários não estão cobertos?

### **2. Crie o Intent**
```json
"novo_intent": {
  "keywords": ["palavra-chave1", "palavra-chave2", "sinônimo", "variação"],
  "intent": "novo_intent",
  "response_template": "Sua resposta aqui com {variáveis} se necessário"
}
```

### **3. Adicione Keywords Variadas**
- **Sinônimos**: "saldo", "dinheiro", "valor"
- **Variações**: "quanto tenho", "quanto posso gastar"
- **Gírias**: "grana", "dinheiro", "cash"
- **Termos técnicos**: "balance", "available funds"

## 📊 **Intents Atuais Expandidos**

### **✅ Intents Básicos (7 → 15)**
1. **saldo** - Consulta de saldo
2. **transacoes** - Histórico de transações
3. **transferencia** - Transferências
4. **pix** - Informações sobre PIX
5. **deposito** - Depósitos
6. **ajuda** - Menu de ajuda
7. **saudacao** - Cumprimentos

### **🆕 Novos Intents Adicionados (8)**
8. **cartao** - Informações sobre cartões
9. **emprestimo** - Empréstimos e financiamentos
10. **investimentos** - Opções de investimento
11. **seguros** - Seguros disponíveis
12. **conta_digital** - Conta digital
13. **atendimento** - Canais de suporte
14. **despedida** - Despedidas
15. **emergencia** - Situações de emergência

## 🎯 **Como Alimentar com Mais Intents**

### **Categorias Sugeridas para Expansão:**

#### **🏦 Serviços Bancários**
```json
"conta_poupanca": {
  "keywords": ["poupança", "poupança", "rendimento", "juros poupança"],
  "intent": "savings_account",
  "response_template": "Informações sobre poupança..."
}
```

#### **💳 Cartões e Crédito**
```json
"limite_cartao": {
  "keywords": ["limite", "limite cartão", "aumentar limite", "limite crédito"],
  "intent": "card_limit",
  "response_template": "Seu limite atual é R$ {limit:.2f}..."
}
```

#### **📱 Digital Banking**
```json
"app_mobile": {
  "keywords": ["app", "aplicativo", "mobile", "celular", "smartphone"],
  "intent": "mobile_app",
  "response_template": "Nosso app mobile oferece..."
}
```

#### **🏠 Produtos Imobiliários**
```json
"financiamento_imovel": {
  "keywords": ["financiamento", "casa", "apartamento", "imóvel", "FGTS"],
  "intent": "real_estate_loan",
  "response_template": "Financiamento imobiliário disponível..."
}
```

#### **👥 Relacionamento**
```json
"perfil_cliente": {
  "keywords": ["perfil", "categoria", "cliente", "vip", "premium"],
  "intent": "customer_profile",
  "response_template": "Seu perfil de cliente é..."
}
```

## 🔧 **Técnicas para Melhorar o Reconhecimento**

### **1. Keywords Inteligentes**
- **Inclua variações**: "saldo", "saldo atual", "quanto tenho"
- **Adicione gírias**: "grana", "dinheiro", "cash"
- **Inclua erros comuns**: "saldo", "saldos", "saldoo"
- **Termos técnicos**: "balance", "available funds"

### **2. Contexto e Frases Completas**
```json
"keywords": [
  "quanto tenho na conta",
  "qual meu saldo",
  "quanto posso gastar",
  "valor disponível",
  "dinheiro na conta"
]
```

### **3. Múltiplos Idiomas**
```json
"keywords": [
  "saldo", "balance", "dinero", "argent"
]
```

## 📈 **Exemplo de Expansão Completa**

### **Intent: Cartão de Crédito**
```json
"cartao_credito": {
  "keywords": [
    "cartão de crédito", "cartão crédito", "crédito",
    "limite", "fatura", "vencimento", "parcelamento",
    "cashback", "milhas", "pontos", "anualidade",
    "bloquear cartão", "desbloquear", "segunda via"
  ],
  "intent": "credit_card",
  "response_template": "Informações do seu cartão de crédito:\n\n💳 <strong>Limite:</strong> R$ {limit:.2f}\n📅 <strong>Fatura:</strong> R$ {invoice:.2f}\n📆 <strong>Vencimento:</strong> {due_date}\n💰 <strong>Disponível:</strong> R$ {available:.2f}\n\nO que gostaria de saber sobre seu cartão?"
}
```

## 🚨 **Dicas Importantes**

### **✅ Boas Práticas:**
- **Keywords específicas**: Evite palavras muito genéricas
- **Teste regularmente**: Adicione e teste novos intents
- **Mantenha consistência**: Use o mesmo padrão de nomenclatura
- **Atualize respostas**: Mantenha informações atualizadas

### **❌ Evite:**
- **Keywords muito genéricas**: "coisa", "isso", "aquilo"
- **Palavras duplicadas**: Verifique se já existem
- **Respostas muito longas**: Mantenha conciso
- **Informações desatualizadas**: Revise regularmente

## 🔄 **Processo de Atualização**

1. **Identifique** a necessidade
2. **Crie** o intent no JSON
3. **Teste** com diferentes frases
4. **Ajuste** keywords se necessário
5. **Valide** a resposta
6. **Documente** a mudança

## 📊 **Métricas de Sucesso**

- **Taxa de reconhecimento**: % de mensagens reconhecidas
- **Satisfação do usuário**: Feedback sobre respostas
- **Cobertura de serviços**: % de serviços cobertos
- **Tempo de resposta**: Velocidade das respostas

---

**💡 Dica:** Comece com intents simples e vá expandindo gradualmente. Teste cada novo intent antes de adicionar o próximo!
