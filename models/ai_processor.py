"""
Processador de IA para o chatbot bancário
"""
import re
from difflib import SequenceMatcher

class SimpleBankingAI:
    def __init__(self):
        self.stop_words = {
            'o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas', 'de', 'da', 'do', 'das', 'dos',
            'em', 'na', 'no', 'nas', 'nos', 'para', 'com', 'por', 'sobre', 'entre', 'até',
            'desde', 'durante', 'mediante', 'conforme', 'segundo', 'consoante', 'que', 'quem',
            'onde', 'quando', 'como', 'porque', 'porquê', 'se', 'mas', 'porém', 'todavia',
            'contudo', 'entretanto', 'logo', 'portanto', 'assim', 'então', 'e', 'ou', 'nem',
            'mas', 'também', 'já', 'ainda', 'sempre', 'nunca', 'jamais', 'talvez', 'quem',
            'saber', 'conhecer', 'entender', 'compreender', 'pensar', 'achar', 'crer',
            'acreditar', 'duvidar', 'suspeitar', 'desconfiar', 'confiar', 'esperar',
            'desejar', 'querer', 'precisar', 'necessitar', 'faltar', 'sobrar', 'bastar'
        }
    
    def preprocess_text(self, text):
        """Preprocess text by removing stop words and normalizing"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep numbers and spaces
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Split into words and remove stop words
        words = text.split()
        filtered_words = [word for word in words if word not in self.stop_words and len(word) > 2]
        
        return ' '.join(filtered_words)
    
    def calculate_similarity(self, text1, text2):
        """Calculate similarity between two texts using SequenceMatcher"""
        return SequenceMatcher(None, text1, text2).ratio()
    
    def find_intent_by_keywords(self, text, banking_kb):
        """Find intent using keyword matching (rule-based)"""
        text_lower = text.lower()
        
        for intent_name, intent_data in banking_kb.items():
            for keyword in intent_data['keywords']:
                if keyword in text_lower:
                    return intent_name, intent_data
        
        return None, None
    
    def find_intent_by_similarity(self, text, faq_responses):
        """Find intent using text similarity (AI-based)"""
        processed_text = self.preprocess_text(text)
        text_lower = text.lower()
        
        best_match = None
        best_similarity = 0.0
        
        for faq in faq_responses:
            # Check keyword similarity (more weight for exact matches)
            keyword_similarity = 0
            for keyword in faq['keywords']:
                if keyword in text_lower:
                    # Give more weight to exact keyword matches
                    if keyword in text_lower.split():
                        keyword_similarity += 2  # Exact word match
                    else:
                        keyword_similarity += 1  # Partial match
            
            # Calculate question similarity
            question_similarity = self.calculate_similarity(processed_text, faq['question'])
            
            # Special handling for "o que é" questions
            if 'o que é' in text_lower or 'que é' in text_lower:
                for keyword in faq['keywords']:
                    if keyword in text_lower and 'o que é' in faq['question']:
                        keyword_similarity += 3  # Extra weight for definition questions
            
            # Calculate combined similarity
            combined_similarity = (keyword_similarity * 0.4) + (question_similarity * 0.6)
            
            # Lower threshold for better matching
            if combined_similarity > best_similarity and combined_similarity > 0.2:
                best_similarity = combined_similarity
                best_match = {
                    'answer': faq['answer'],
                    'similarity': combined_similarity
                }
        
        if best_match:
            return 'faq', best_match
        
        return None, None
    
    def analyze_sentiment(self, text):
        """Simple sentiment analysis based on positive/negative words"""
        positive_words = [
            'obrigado', 'obrigada', 'ótimo', 'bom', 'excelente', 'perfeito', 'legal',
            'incrível', 'fantástico', 'maravilhoso', 'genial', 'show', 'top', 'massa',
            'bacana', 'daora', 'irado', 'foda', 'brabo', 'foda', 'show', 'top',
            'gostei', 'amei', 'adorei', 'curti', 'valeu', 'vlw', 'tmj', 'sucesso'
        ]
        
        negative_words = [
            'ruim', 'péssimo', 'horrível', 'terrível', 'odiei', 'detestei', 'merda',
            'porcaria', 'lixo', 'bosta', 'cagada', 'cagou', 'fudeu', 'fodeu',
            'problema', 'erro', 'falha', 'bug', 'travou', 'caiu', 'não funciona',
            'não consegui', 'não deu', 'deu ruim', 'deu merda', 'fudeu tudo'
        ]
        
        text_lower = text.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def extract_entities(self, text):
        """Extract entities like amounts and account numbers"""
        # Extract amounts (R$ 100, 100 reais, etc.)
        amount_patterns = [
            r'R\$\s*(\d+(?:,\d{2})?)',
            r'(\d+(?:,\d{2})?)\s*reais?',
            r'(\d+(?:,\d{2})?)\s*real',
            r'(\d+(?:\.\d{2})?)',
        ]
        
        amounts = []
        for pattern in amount_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    # Convert to float, handling both , and . as decimal separators
                    amount_str = match.replace(',', '.')
                    amount = float(amount_str)
                    amounts.append(amount)
                except ValueError:
                    continue
        
        # Extract account numbers (sequences of digits)
        account_patterns = [
            r'\b\d{10,}\b',  # 10+ digits
            r'conta\s*(\d+)',  # "conta 123456"
            r'numero\s*(\d+)',  # "numero 123456"
        ]
        
        accounts = []
        for pattern in account_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            accounts.extend(matches)
        
        return {
            'amounts': amounts,
            'accounts': accounts
        }
    
    def process_message(self, message, banking_kb, faq_responses):
        """Process a message and return the appropriate response"""
        print(f"🤖 Processando mensagem: {message}")
        
        # Analyze sentiment
        sentiment = self.analyze_sentiment(message)
        print(f"😊 Sentimento: {sentiment}")
        
        # Extract entities
        entities = self.extract_entities(message)
        amount = entities['amounts'][0] if entities['amounts'] else None
        account = entities['accounts'][0] if entities['accounts'] else None
        
        # Try keyword-based intent first
        intent_name, intent_data = self.find_intent_by_keywords(message, banking_kb)
        keyword_intent = intent_name
        
        if intent_name:
            print(f"📋 Intent encontrado por palavras-chave: {intent_name}")
            return {
                'intent': intent_name,
                'intent_data': intent_data,
                'sentiment': sentiment,
                'amount': amount,
                'account': account,
                'method': 'keywords'
            }
        
        # Try AI-based similarity
        intent_name, intent_data = self.find_intent_by_similarity(message, faq_responses)
        similarity_intent = intent_name
        
        if intent_name:
            print(f"🧠 Intent encontrado por similaridade: {intent_name}")
            return {
                'intent': intent_name,
                'intent_data': intent_data,
                'sentiment': sentiment,
                'amount': amount,
                'account': account,
                'method': 'similarity'
            }
        
        # No intent found
        print("❌ Nenhum intent encontrado")
        return {
            'intent': None,
            'intent_data': None,
            'sentiment': sentiment,
            'amount': amount,
            'account': account,
            'method': 'none'
        }
