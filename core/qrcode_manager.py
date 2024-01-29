
from pyqrcode import QRCode
import pyqrcode
import random
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken


def generate_secret_key():
    """
    would generate a Fernet Key

    Returns:
        _type_: string version of the key
    """
    return Fernet.generate_key()
# b'iVcPA1xUQqWdTAlZkgiInsfE61AEVuklT4X8Osfvjx8='

class QrCodeGenerator:
    def __init__(self, key: bytes):
        self.cipher = Fernet(key)
    
    def encode_content(self, content: bytes):
        if not isinstance(content, bytes):
            content = content.encode('utf-8')
        return self.cipher.encrypt(content)
    
    def decode_content(self, encoded_content: bytes):
        try:
            return self.cipher.decrypt(encoded_content)
        except InvalidToken:
            return b''
    
    def generate_qr(self, encoded_data: bytes):
        encoded_qr_data = self.encode_content(encoded_data)
        url = pyqrcode.create(encoded_qr_data, error="M")
        return url.png(f"{random.randint(200, 1000)}.png")
        
        
        """
        from django.db import models
from django.core.files.base import ContentFile
from io import BytesIO

class YourModel(models.Model):
    qr_code_image = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def save_qr_code(self, data: str):
        qr_code_generator = QrCodeGenerator(key=b'your_secret_key')
        qr_code_image_data = qr_code_generator.generate_qr(data)

        # Save QR code image to model field
        qr_code_image_path = f'qr_codes/{data}.png'
        self.qr_code_image.save(qr_code_image_path, ContentFile(qr_code_image_data), save=False)

        # Ensure the model is saved with the QR code image
        self.save()

        """