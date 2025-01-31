import json
import zlib
from presidio_anonymizer import AnonymizerEngine

class JSONReporter:
    def __init__(self, redact_sensitive=True):
        self.redactor = AnonymizerEngine() if redact_sensitive else None
        self.compression_level = 6

    def generate_report(self, findings, output_path):
        report = {
            "metadata": self._get_metadata(),
            "findings": self._process_findings(findings)
        }
        
        json_data = json.dumps(report, indent=2)
        
        if output_path.endswith('.json.gz'):
            self._compress_report(json_data, output_path)
        else:
            with open(output_path, 'w') as f:
                f.write(json_data)

    def _process_findings(self, findings):
        processed = []
        for finding in findings:
            if self.redactor:
                finding['content'] = self.redactor.anonymize(
                    text=finding['content'],
                    analyzer_results=finding['matches']
                ).text
            processed.append(finding)
        return processed

    def _compress_report(self, data, path):
        with gzip.open(path, 'wt', encoding='UTF-8', compresslevel=self.compression_level) as f:
            f.write(data)
