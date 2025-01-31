from transformers import pipeline
import torch

class SecretBERT:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
        self.model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
        self.pipeline = pipeline(
            "ner",
            model=self.model,
            tokenizer=self.tokenizer,
            aggregation_strategy="max"
        )

    def analyze(self, text):
        results = self.pipeline(text)
        sensitive_entities = []
        for entity in results:
            if entity['entity_group'] in ['ORG', 'PER', 'LOC']:
                context = text[max(0, entity['start']-50):entity['end']+50]
                if self.contains_secret_context(context):
                    sensitive_entities.append({
                        'text': entity['word'],
                        'type': entity['entity_group'],
                        'score': entity['score']
                    })
        return sensitive_entities

    def contains_secret_context(self, text):
        keywords = ['key', 'secret', 'password', 'credential']
        return any(kw in text.lower() for kw in keywords)
