# storage.py
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

class PersistentMediaStorage(FileSystemStorage):
    """Storage class that ensures media files are saved to a persistent location"""
    def __init__(self, *args, **kwargs):
        super().__init__(location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL, *args, **kwargs)
        
        # Create media directory if it doesn't exist
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)