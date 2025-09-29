#!/usr/bin/env python3
"""
Script para instalar modelos de linguagem necessários para o chatbot com IA/NLP
"""

import subprocess
import sys
import spacy

def install_spacy_model():
    """Instala o modelo de português do spaCy"""
    try:
        # Verifica se o modelo já está instalado
        spacy.load("pt_core_news_sm")
        print("✅ Modelo português do spaCy já está instalado")
        return True
    except OSError:
        print("📥 Instalando modelo português do spaCy...")
        try:
            subprocess.run([sys.executable, "-m", "spacy", "download", "pt_core_news_sm"], check=True)
            print("✅ Modelo português do spaCy instalado com sucesso")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao instalar modelo do spaCy: {e}")
            return False

def install_nltk_data():
    """Instala dados necessários do NLTK"""
    import nltk
    try:
        print("📥 Instalando dados do NLTK...")
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        print("✅ Dados do NLTK instalados com sucesso")
        return True
    except Exception as e:
        print(f"❌ Erro ao instalar dados do NLTK: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 Instalando modelos de linguagem para o Chatbot Bancário com IA/NLP")
    print("=" * 60)
    
    success = True
    
    # Instala modelo do spaCy
    if not install_spacy_model():
        success = False
    
    # Instala dados do NLTK
    if not install_nltk_data():
        success = False
    
    print("=" * 60)
    if success:
        print("🎉 Todos os modelos foram instalados com sucesso!")
        print("💡 Agora você pode executar: python app_ai.py")
    else:
        print("⚠️  Alguns modelos falharam na instalação")
        print("💡 Tente executar manualmente:")
        print("   python -m spacy download pt_core_news_sm")
        print("   python -c \"import nltk; nltk.download('punkt'); nltk.download('stopwords')\"")

if __name__ == "__main__":
    main()
