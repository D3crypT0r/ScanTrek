from PIL import Image, ExifTags
import pytesseract
import numpy as np
import stegano

class ImageAnalyzer:
    def __init__(self):
        self.ocr_config = r'--oem 3 --psm 6'
        self.stegano_algos = [
            stegano.lsb,
            stegano.red
        ]

    def analyze_image(self, image_path: str) -> Dict:
        results = {
            'exif': self._extract_exif(image_path),
            'ocr_text': self._perform_ocr(image_path),
            'stegano_check': self._check_stegano(image_path),
            'dominant_colors': self._get_dominant_colors(image_path)
        }
        return results

    def _extract_exif(self, path: str) -> Dict:
        try:
            img = Image.open(path)
            exif = {
                ExifTags.TAGS.get(tag, tag): value
                for tag, value in img._getexif().items()
            }
            return self._sanitize_exif(exif)
        except:
            return {}

    def _sanitize_exif(self, exif: Dict) -> Dict:
        sensitive = ['GPSInfo', 'MakerNote', 'SerialNumber']
        return {k: v for k, v in exif.items() if k not in sensitive}

    def _perform_ocr(self, path: str) -> str:
        img = Image.open(path)
        if img.mode not in ['RGB', 'L']:
            img = img.convert('RGB')
        return pytesseract.image_to_string(img, config=self.ocr_config)

    def _check_stegano(self, path: str) -> bool:
        for algo in self.stegano_algos:
            try:
                if algo.reveal(path).strip():
                    return True
            except:
                continue
        return False

    def _get_dominant_colors(self, path: str, n_colors=3) -> List:
        img = Image.open(path).convert('RGB')
        pixels = np.array(img)
        pixels = pixels.reshape(-1, 3)
        cov = np.cov(pixels.T)
        eigenvalues = np.linalg.eigh(cov)[0]
        return eigenvalues.argsort()[-n_colors:].tolist()
