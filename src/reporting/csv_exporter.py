import csv
import pandas as pd
from io import StringIO

class CSVExporter:
    def __init__(self, chunk_size=10000):
        self.chunk_size = chunk_size
        self.buffer = StringIO()
        self.writer = csv.DictWriter(self.buffer, fieldnames=[
            'url', 'file_type', 'sensitive_data', 'severity'
        ])
        self.writer.writeheader()

    def export(self, findings, output_path):
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.writer.fieldnames)
            writer.writeheader()
            
            for i, finding in enumerate(findings):
                row = self._convert_to_row(finding)
                writer.writerow(row)
                
                if (i + 1) % self.chunk_size == 0:
                    f.flush()

    def _convert_to_row(self, finding):
        return {
            'url': finding['url'],
            'file_type': finding['file_type'],
            'sensitive_data': '|'.join(
                f"{k}:{len(v)}" for k,v in finding['matches'].items()
            ),
            'severity': self._calculate_severity(finding)
        }

    def _calculate_severity(self, finding):
        weights = {'aws_key': 10, 'pii': 8, 'jwt': 7}
        return sum(weights.get(k, 1)*len(v) for k,v in finding['matches'].items())
