
from pyqrcode import QRCode
import pyqrcode
import random
from cryptography.fernet import Fernet
from io import BytesIO
from django.core.files.base import ContentFile
from cryptography.fernet import InvalidToken
from pyzbar.pyzbar import decode
from PIL import Image

from core.enums import FileTypeChoices

def generate_secret_key():
    """
    would generate a Fernet Key
    """
    return Fernet.generate_key()
# b'iVcPA1xUQqWdTAlZkgiInsfE61AEVuklT4X8Osfvjx8='

class QrCodeGenerator:
    def __init__(self, key: bytes):
        self.cipher = Fernet(key)
    
    def encode_content(self, content: bytes):
        if not isinstance(content, bytes):
            content = str(content).encode('utf-8')
        return self.cipher.encrypt(content)
    
    def decode_content(self, encoded_content: bytes):
        try:
            return self.cipher.decrypt(encoded_content)
        except InvalidToken:
            return b''
    
    def generate_qr(self, encoded_data: bytes, format=FileTypeChoices.SVG):
        qr = pyqrcode.create(encoded_data, error="M")
        buffer = BytesIO()
        scale = 5
        if format == FileTypeChoices.PNG:
            qr.png(buffer, scale=scale)
        elif format == FileTypeChoices.SVG:
            qr.svg(buffer, scale=scale)
        else:
            raise ValueError("Unsupported format") 
        buffer.seek(0)
        file_name = f"{random.randint(100, 1000)}.{format}"
        file = ContentFile(buffer.read(), name=file_name)
        return file
        
        
def decode_barcode(image_path):
    image = Image.open(image_path)
    decoded_objects = decode(image)
    if decoded_objects:
        return decoded_objects[0].data.decode('utf-8')
    else:
        return None     
        

"""
Decoded Barcode Value: gAAAAABluNhbKY-9A4kuFWwPIF9EYv9GsNNzYhrbR8vyIN9UOaC--sdWmDj0YCmANBd5z_8PBtVAUbtXYODNBj07RXrQWkG82J-l674tNKQly5RM4B12Ku7lkCNYMqJxU0uUsKBPIg7Y9xJQH8vNdDJvxRX6QBz5YOo_iuRiIwPjgNeDk-cuOmQ=
(venv) afeez1131@Afeez1131:~/project$ python manage.py shell
Python 3.10.12 (main, Nov 20 2023, 15:14:05) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from core.models import *
>>> instance = ProductInstance.objects.get(id='11612b3b-f261-405f-bd9a-46153d6fc6dc')
>>> instance
<ProductInstance: Prod-32b419 - (2024-01-30 - 2025-07-20)>
>>> key = instance.key
Traceback (most recent call last):
  File "<console>", line 1, in <module>
AttributeError: 'ProductInstance' object has no attribute 'key'
>>> key = instance.secret
>>> from cryptography.fernet import Fernet
>>> cipher = Fernet(key)
>>> cipher
<cryptography.fernet.Fernet object at 0x7fb1665467d0>
>>> cipher.decrypt(b'gAAAAABluNhbKY-9A4kuFWwPIF9EYv9GsNNzYhrbR8vyIN9UOaC--sdWmDj0YCmANBd5z_8PBtVAUbtXYODNBj07RXrQWkG82J-l674tNKQly5RM4B12Ku7lkCNYMqJxU0uUsKBPIg7Y9xJQH8vNdDJvxRX6QBz5YOo_iuRiIwPjgNeDk-cuOmQ=')
b'11612b3b-f261-405f-bd9a-46153d6fc6dc::00844222-2ed6-4048-9d18-df13795ad397'
>>> instance.id
UUID('11612b3b-f261-405f-bd9a-46153d6fc6dc')
>>> instance.secret
b'nLqCp-7MgaPN2fitQRTmykXgq3ApaIOAP1CnzSpiJQQ='
>>> instance.product.unique_code
UUID('00844222-2ed6-4048-9d18-df13795ad397')
"""