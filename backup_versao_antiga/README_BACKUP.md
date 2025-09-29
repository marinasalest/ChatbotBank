# 📦 Backup - Versões Antigas do Chatbot

**Data do Backup:** 09/09/2025  
**Motivo:** Organização e separação de versões

---

## 📁 Conteúdo do Backup

### **Versão Original (Regras Simples)**
- **`app.py`** - Chatbot original com apenas regras simples
- **`requirements.txt`** - Dependências básicas (5 pacotes)

### **Versão IA Avançada (spaCy)**
- **`app_ai.py`** - Chatbot com IA/NLP avançado (spaCy + NLTK)
- **`requirements_ai.txt`** - Dependências completas (9 pacotes)
- **`install_models.py`** - Script para instalar modelos de linguagem
- **`README_AI.md`** - Documentação da versão com IA

---

## 🔄 Diferenças entre Versões

| Aspecto | Versão Original | Versão IA Avançada | Versão Atual |
|---------|----------------|-------------------|--------------|
| **Arquivo** | `app.py` | `app_ai.py` | `app.py` |
| **IA/NLP** | ❌ Apenas regras | ✅ spaCy + NLTK | ✅ IA simplificada |
| **Dependências** | 5 pacotes | 9 pacotes | 5 pacotes |
| **Instalação** | ✅ Fácil | ⚠️ Complexa | ✅ Fácil |
| **Funcionalidades** | Básicas | Avançadas | Híbridas |

---

## 🚀 Como Usar as Versões Antigas

### **Versão Original (Regras Simples)**
```bash
cd backup_versao_antiga
pip install -r requirements.txt
python app.py
```

### **Versão IA Avançada (spaCy)**
```bash
cd backup_versao_antiga
pip install -r requirements_ai.txt
python install_models.py
python app_ai.py
```

---

## 📊 Comparação de Funcionalidades

### **Versão Original (app.py)**
- ✅ Autenticação JWT
- ✅ Operações bancárias básicas
- ✅ Chat com regras simples
- ✅ Interface responsiva
- ❌ Sem IA/NLP
- ❌ Sem extração de dados

### **Versão IA Avançada (app_ai.py)**
- ✅ Todas as funcionalidades da versão original
- ✅ IA/NLP com spaCy
- ✅ Extração de entidades
- ✅ Análise de sentimento
- ✅ FAQ inteligente
- ⚠️ Dependências complexas
- ⚠️ Pode falhar na instalação

### **Versão Atual (app.py - Principal)**
- ✅ Todas as funcionalidades
- ✅ IA/NLP simplificada
- ✅ Extração de dados
- ✅ Análise de sentimento
- ✅ FAQ inteligente
- ✅ Dependências simples
- ✅ Instalação fácil

---

## 🔧 Motivo da Reorganização

1. **Simplificação:** Versão atual é mais estável
2. **Organização:** Separação clara de versões
3. **Manutenção:** Foco na versão principal
4. **Backup:** Preservação das versões antigas

---

## 📝 Notas Importantes

- **Versão atual** está na raiz do projeto
- **Versões antigas** estão neste diretório
- **Todas as versões** têm as mesmas 11 contas
- **Interface** é idêntica em todas as versões
- **Funcionalidades** variam conforme a versão

---

**Backup criado em 09/09/2025**  
**Sistema:** Chatbot Bancário  
**Status:** Arquivos preservados para referência
