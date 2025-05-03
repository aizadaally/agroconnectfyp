# products/management/commands/setup_demo_data.py
import os
import shutil
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

class Command(BaseCommand):
    help = 'Sets up demo data including fixtures and media files'

    def handle(self, *args, **options):
        # Load product fixtures
        self.stdout.write('Loading product fixtures...')
        call_command('loaddata', 'fixtures/products.json')
        
        # Copy media files
        self.stdout.write('Copying media files...')
        fixtures_media_dir = os.path.join(settings.BASE_DIR, 'fixtures', 'media')
        
        # Ensure media directory exists
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        
        # Copy product images
        product_images_src = os.path.join(fixtures_media_dir, 'product_images')
        product_images_dest = os.path.join(settings.MEDIA_ROOT, 'product_images')
        
        # Create destination directory if it doesn't exist
        os.makedirs(product_images_dest, exist_ok=True)
        
        # Copy all files from source to destination
        for filename in os.listdir(product_images_src):
            src_file = os.path.join(product_images_src, filename)
            dest_file = os.path.join(product_images_dest, filename)
            
            if os.path.isfile(src_file):
                shutil.copy2(src_file, dest_file)
                self.stdout.write(f'Copied {filename}')
        
        self.stdout.write(self.style.SUCCESS('Demo data setup complete!'))