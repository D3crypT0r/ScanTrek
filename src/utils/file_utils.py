import magic
import hashlib
import os
import tempfile

class FileUtils:
    @staticmethod
    def get_mime_type(file_path):
        mime = magic.Magic(mime=True)
        return mime.from_file(file_path)

    @staticmethod
    def safe_delete(path):
        try:
            if os.path.exists(path):
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    shutil.rmtree(path)
                return True
            return False
        except Exception as e:
            ErrorHandler.handle(e)
            return False

    @staticmethod
    def generate_checksum(file_path, algorithm='sha256'):
        hash_func = getattr(hashlib, algorithm)()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()

    @staticmethod
    def create_temp_dir(prefix='qc_'):
        return tempfile.mkdtemp(prefix=prefix)
