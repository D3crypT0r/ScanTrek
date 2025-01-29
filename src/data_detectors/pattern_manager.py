import yaml
import re
from typing import Dict, List

class PatternManager:
    def __init__(self):
        self.patterns = {}
        self.compiled = {}
        self.load_default_patterns()
        
    def load_default_patterns(self):
        self.patterns = {
            'aws_key': {
                'regex': r'AKIA[0-9A-Z]{16}',
                'confidence': 0.95,
                'context': ['aws', 's3', 'access']
            },
            'credit_card': {
                'regex': r'\b(?:\d[ -]*?){13,16}\b',
                'confidence': 0.85,
                'context': ['card', 'payment', 'cc']
            }
        }
        self._compile_patterns()

    def load_custom_patterns(self, yaml_path: str):
        with open(yaml_path, 'r') as f:
            custom = yaml.safe_load(f)
            for name, config in custom.items():
                self._validate_pattern(config)
                self.patterns[name] = config
        self._compile_patterns()

    def _validate_pattern(self, config: Dict):
        required = ['regex', 'confidence', 'context']
        if not all(key in config for key in required):
            raise ValueError("Invalid pattern configuration")
        try:
            re.compile(config['regex'])
        except re.error:
            raise ValueError("Invalid regular expression")

    def _compile_patterns(self):
        self.compiled = {
            name: {
                'pattern': re.compile(config['regex'], re.IGNORECASE),
                'confidence': config['confidence'],
                'context': config['context']
            } for name, config in self.patterns.items()
        }

    def get_context_weights(self, text: str) -> Dict[str, float]:
        text = text.lower()
        return {
            name: len([kw for kw in config['context'] if kw in text]) 
            for name, config in self.patterns.items()
        }

    def update_threshold(self, name: str, threshold: float):
        if name in self.patterns:
            self.patterns[name]['confidence'] = threshold
            self._compile_patterns()
