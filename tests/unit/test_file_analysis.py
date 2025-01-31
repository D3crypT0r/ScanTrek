from analysis.file_detectors.pdf_analyzer import PDFInspector
import pytest
import io

@pytest.fixture
def sample_pdf():
    from PyPDF2 import PdfWriter
    writer = PdfWriter()
    writer.add_page()
    buffer = io.BytesIO()
    writer.write(buffer)
    buffer.seek(0)
    return buffer

def test_pdf_metadata_extraction(sample_pdf, tmp_path):
    test_pdf = tmp_path / "test.pdf"
    test_pdf.write_bytes(sample_pdf.getvalue())
    
    inspector = PDFInspector()
    result = inspector.analyze(str(test_pdf))
    
    assert 'metadata' in result
    assert 'Producer' in result['metadata']
    assert 'CreationDate' in result['metadata']

def test_pdf_text_extraction(sample_pdf, tmp_path):
    test_pdf = tmp_path / "test.pdf"
    test_pdf.write_bytes(sample_pdf.getvalue())
    
    inspector = PDFInspector()
    result = inspector.analyze(str(test_pdf))
    
    assert isinstance(result['text'], str)
