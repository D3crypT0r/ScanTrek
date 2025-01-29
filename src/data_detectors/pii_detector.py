from presidio_analyzer import AnalyzerEngine
import spacy

class PIIDetector:
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.nlp = spacy.load("en_core_web_lg")
        self.regex_patterns = {
            'ssn': r'\d{3}-\d{2}-\d{4}',
            'phone': r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        }

    def detect(self, text):
        results = {}
        
        for name, pattern in self.regex_patterns.items():
            results[name] = re.findall(pattern, text)
            
       
        doc = self.nlp(text)
        results['entities'] = [(ent.text, ent.label_) 
                             for ent in doc.ents 
                             if ent.label_ in ['PERSON', 'ORG', 'GPE']]
        
        
        presidio_results = self.analyzer.analyze(
            text=text,
            language='en',
            entities=['PHONE_NUMBER', 'EMAIL_ADDRESS', 'CREDIT_CARD']
        )
        
        results['presidio'] = [{
            'type': result.entity_type,
            'value': text[result.start:result.end],
            'confidence': result.score
        } for result in presidio_results]
        
        return results
