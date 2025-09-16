# 📁 Estrutura de Dados do Chatbot Bancário

Este diretório contém os arquivos de dados externos do chatbot bancário, separados do código principal para melhor organização e manutenção.

## 📋 Arquivos

### `banking_concepts.json`
Contém todos os conceitos bancários e financeiros que o chatbot pode explicar.

**Estrutura:**
```json
{
  "concepts": [
    {
      "question": "o que é pix",
      "keywords": ["pix", "o que é", "definição", "conceito"],
      "answer": "Resposta explicativa sobre o conceito..."
    }
  ]
}
```

**Categorias incluídas:**
- 💸 **Pagamentos**: PIX, TED, DOC, chave PIX
- 🏦 **Contas**: corrente, poupança, digital, salário, conjunta, universitária
- 💳 **Cartões**: crédito, débito, cheque especial
- 📈 **Investimentos**: renda fixa, variável, CDB, LCI, LCA, Tesouro Direto
- 🏛️ **Instituições**: BCB, CVM, ANBIMA, B3, Copom
- 📊 **Indicadores**: SELIC, IPCA, score de crédito
- ⚖️ **Tributação**: IR, IOF, come-cotas
- 🔤 **Siglas**: CPF, CNPJ, SPC, Serasa, FGC

### `banking_intents.json`
Contém os intents básicos do chatbot (saldo, transações, transferências, etc.).

**Estrutura:**
```json
{
  "intents": {
    "saldo": {
      "keywords": ["saldo", "quanto tenho", "dinheiro na conta"],
      "intent": "balance",
      "response_template": "Seu saldo atual é R$ {balance:.2f}"
    }
  }
}
```

## 🔧 Vantagens desta Estrutura

### ✅ **Separação de Responsabilidades**
- Código limpo e focado na lógica
- Dados organizados e fáceis de editar
- Manutenção simplificada

### ✅ **Facilidade de Manutenção**
- Adicionar novos conceitos sem mexer no código
- Editar respostas diretamente nos arquivos JSON
- Versionamento independente dos dados

### ✅ **Escalabilidade**
- Fácil adição de novos idiomas
- Possibilidade de carregar dados de APIs
- Estrutura preparada para banco de dados

### ✅ **Colaboração**
- Não-programadores podem editar conceitos
- Revisão de conteúdo independente do código
- Backup e versionamento separados

## 📝 Como Adicionar Novos Conceitos

1. **Abra** `banking_concepts.json`
2. **Adicione** um novo objeto no array `concepts`:
```json
{
  "question": "o que é [conceito]",
  "keywords": ["palavra1", "palavra2", "sinônimo"],
  "answer": "Explicação clara e didática do conceito..."
}
```
3. **Salve** o arquivo
4. **Reinicie** o servidor Flask

## 🔄 Como Editar Intents

1. **Abra** `banking_intents.json`
2. **Modifique** o intent desejado:
```json
"ajuda": {
  "keywords": ["ajuda", "help", "como usar"],
  "intent": "help",
  "response_template": "Nova resposta de ajuda..."
}
```
3. **Salve** o arquivo
4. **Reinicie** o servidor Flask

## 🚀 Próximos Passos

- [ ] Adicionar validação de JSON
- [ ] Implementar cache de dados
- [ ] Criar interface de administração
- [ ] Adicionar suporte a múltiplos idiomas
- [ ] Integrar com banco de dados


