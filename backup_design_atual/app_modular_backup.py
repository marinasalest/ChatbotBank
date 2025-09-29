"""
Aplicação Flask principal - Versão Modular
Chatbot Bancário com IA Simplificada
"""
from flask import Flask, render_template
from flask_cors import CORS
from config import Config

# Import blueprints
from routes.auth_routes import auth_bp
from routes.banking_routes import banking_bp
from routes.chat_routes import chat_bp

def create_app():
    """Factory function para criar a aplicação Flask"""
    app = Flask(__name__)
    
    # Configuração
    app.config.from_object(Config)
    
    # CORS
    CORS(app)
    
    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(banking_bp)
    app.register_blueprint(chat_bp)
    
    # Rota principal
    @app.route('/')
    def index():
        return render_template('index_working.html')
    
    return app

# Criar aplicação
app = create_app()

if __name__ == '__main__':
    print("🤖 Iniciando Chatbot Bancário com IA Simplificada...")
    print("🧠 Processador IA inicializado (sem dependências externas)")
    print("🚀 Servidor iniciando...")
    app.run(debug=True, host='0.0.0.0', port=5000)
