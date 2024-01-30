
from pyqrcode import QRCode
import pyqrcode
import random
from cryptography.fernet import Fernet
from io import BytesIO
from django.core.files.base import ContentFile
from cryptography.fernet import InvalidToken
from pyzbar.pyzbar import decode
from PIL import Image

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
    
    def generate_qr(self, encoded_data: bytes):
        # encoded_qr_data = self.encode_content(encoded_data)
        url = pyqrcode.create(encoded_data, error="M")
        buffer = BytesIO()
        url.png(buffer, scale=5)
        buffer.seek(0)
        
        qr_file = ContentFile(buffer.read(), name=f"{random.randint(100, 1000)}.png")
        return qr_file
    
    def generate_svg(self, encoded_data: bytes):
        qr = pyqrcode.create(encoded_data)    
        svg_buffer = BytesIO()    
        qr.svg(svg_buffer, scale=5)
        svg_buffer.seek(0)
        qr_svg_file = ContentFile(svg_buffer.read(), name=f"{random.randint(100, 1000)}.svg")
        return qr_svg_file
    
    def generate_eps(self, encoded_data: bytes):
        qr = pyqrcode.create(encoded_data)
        eps_buffer = BytesIO()
        qr.eps(eps_buffer, scale=5)
        eps_buffer.seek(0)
        qr_eps_file = ContentFile(eps_buffer.read(), name='temp.eps')
        return qr_eps_file
    
        # return url.png(f"{random.randint(200, 1000)}.png")
        
        
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