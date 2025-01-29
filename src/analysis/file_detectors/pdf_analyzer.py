from pdfminer.high_level import extract_text
import fitz  # PyMuPDF
import hashlib

class PDFInspector:
    def __init__(self):
        self.text_parser = PDFTextParser()
        self.image_analyzer = PDFImageExtractor()

    def analyze(self, file_path):
        results = {
            'metadata': self.get_metadata(file_path),
            'text': extract_text(file_path),
            'images': [],
            'links': [],
            'embedded_files': []
        }
        
        with fitz.open(file_path) as doc:
            results.update(self.image_analyzer.extract_images(doc))
            results['links'] = self.extract_links(doc)
            results['embedded_files'] = self.find_embedded_files(doc)
            
        return results

    def extract_links(self, doc):
        return [link['uri'] for page in doc for link in page.get_links()]

    def find_embedded_files(self, doc):
        return [{
            'name': file['filename'],
            'size': file['size'],
            'digest': hashlib.sha256(file['data']).hexdigest()
        } for file in doc.embedded_file_names.values()]
