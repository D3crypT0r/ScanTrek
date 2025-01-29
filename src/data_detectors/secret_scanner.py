import re
from typing import Dict, List

class SecretScanner:
    PATTERNS = {
        'aws_key': r'(?<![A-Z0-9])[A-Z0-9]{20}(?![A-Z0-9])',
        'google_api': r'AIza[0-9A-Za-z\-_]{35}',
        'jwt': r'eyJ[a-zA-Z0-9-_=]+\.eyJ[a-zA-Z0-9-_=]+\.?[a-zA-Z0-9-_.+/=]*'
    }

    def __init__(self):
        self.compiled = {k: re.compile(v) for k, v in self.PATTERNS.items()}

    def scan(self, text: str) -> Dict[str, List[str]]:
        findings = {}
        for name, pattern in self.compiled.items():
            matches = pattern.findall(text)
            if matches:
                findings[name] = self.validate_context(matches, text)
        return findings

    def validate_context(self, matches, text):
        return [m for m in matches 
                if not self.is_false_positive(m, text)]

    def is_false_positive(self, match, text):
        false_positives = ['example', 'placeholder', 'sample']
        snippet = text[max(0, text.find(match)-50):text.find(match)+50]
        return any(fp in snippet.lower() for fp in false_positives)
