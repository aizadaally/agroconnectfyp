#!/usr/bin/env python
"""
Script to migrate existing image files to Cloudinary.
"""
import os
import django
import sys
from pathlib import Path

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agroconnect_project.settings')
django.setup()

from products.models import Product
from users.models import User
from django.conf import settings
import cloudinary.uploader
from django.core.files.base import ContentFile
import requests

def migrate_product_images():
    """Migrate all product images to Cloudinary"""
    products = Product.objects.filter(image__isnull=False)
    print(f"Found {products.count()} products with images")
    
    for product in products:
        if not product.image:
            continue
            
        image_path = product.image.name
        # Try different possible local paths
        possible_paths = [
            os.path.join('media', image_path),  # relative to current directory
            os.path.join(settings.MEDIA_ROOT, image_path),  # using MEDIA_ROOT
            os.path.join(settings.BASE_DIR, 'media', image_path)  # using BASE_DIR
        ]
        
        print(f"Processing {product.name} with image {image_path}")
        
        # Find the first path that exists
        local_path = None
        for path in possible_paths:
            if os.path.exists(path):
                local_path = path
                break
        
        try:
            if local_path:
                # Upload to Cloudinary
                print(f"  Found image at {local_path}, uploading to Cloudinary...")
                with open(local_path, 'rb') as f:
                    result = cloudinary.uploader.upload(
                        f, 
                        public_id=image_path,
                        folder='product_images',
                        overwrite=True
                    )
                cloudinary_url = result['secure_url']
                print(f"  Success! Cloudinary URL: {cloudinary_url}")
                
                # Update the model to use the new URL
                print(f"  Updating product record with Cloudinary path...")
                
                # This step is important - reset the image field with a temporary value
                # and then set it back with the Cloudinary URL
                old_image = product.image
                product.image = None
                product.save()
                
                # Download the image from Cloudinary and update the model
                response = requests.get(cloudinary_url)
                if response.status_code == 200:
                    file_name = os.path.basename(image_path)
                    product.image.save(
                        file_name,
                        ContentFile(response.content),
                        save=True
                    )
                    print(f"  Updated product record. New image URL: {product.image.url}")
                else:
                    print(f"  Error downloading from Cloudinary: Status {response.status_code}")
                    product.image = old_image
                    product.save()
            else:
                print(f"  Warning: Local file not found. Tried paths:")
                for path in possible_paths:
                    print(f"    - {path}")
        except Exception as e:
            print(f"  Error processing {product.name}: {str(e)}")
    
    print("Migration complete - all images have been uploaded to Cloudinary")

def migrate_user_images():
    """Migrate all user profile images to Cloudinary"""
    users = User.objects.filter(profile_image__isnull=False)
    print(f"Found {users.count()} users with profile images")
    
    for user in users:
        if not user.profile_image:
            continue
            
        image_path = user.profile_image.name
        # Try different possible local paths
        possible_paths = [
            os.path.join('media', image_path),
            os.path.join(settings.MEDIA_ROOT, image_path),
            os.path.join(settings.BASE_DIR, 'media', image_path)
        ]
        
        print(f"Processing {user.username} with image {image_path}")
        
        # Find the first path that exists
        local_path = None
        for path in possible_paths:
            if os.path.exists(path):
                local_path = path
                break
        
        try:
            if local_path:
                # Upload to Cloudinary
                print(f"  Found image at {local_path}, uploading to Cloudinary...")
                with open(local_path, 'rb') as f:
                    result = cloudinary.uploader.upload(
                        f, 
                        public_id=image_path,
                        folder='profile_images',
                        overwrite=True
                    )
                cloudinary_url = result['secure_url']
                print(f"  Success! Cloudinary URL: {cloudinary_url}")
                
                # Update the model
                old_image = user.profile_image
                user.profile_image = None
                user.save()
                
                # Download and update
                response = requests.get(cloudinary_url)
                if response.status_code == 200:
                    file_name = os.path.basename(image_path)
                    user.profile_image.save(
                        file_name,
                        ContentFile(response.content),
                        save=True
                    )
                    print(f"  Updated user record. New image URL: {user.profile_image.url}")
                else:
                    print(f"  Error downloading from Cloudinary: Status {response.status_code}")
                    user.profile_image = old_image
                    user.save()
            else:
                print(f"  Warning: Local file not found for user {user.username}")
        except Exception as e:
            print(f"  Error processing {user.username}: {str(e)}")
    
    print("User profile image migration complete")

def migrate_other_images():
    """Placeholder for migrating any other image fields"""
    # Add code here if you have other models with image fields
    pass

if __name__ == "__main__":
    print("Starting migration of all images to Cloudinary...")
    
    # Check Cloudinary configuration
    import cloudinary
    print(f"Cloudinary configuration:")
    print(f"  Cloud name: {cloudinary.config().cloud_name}")
    print(f"  API Key: {'Configured' if cloudinary.config().api_key else 'Missing'}")
    print(f"  API Secret: {'Configured' if cloudinary.config().api_secret else 'Missing'}")
    
    if not cloudinary.config().cloud_name or not cloudinary.config().api_key or not cloudinary.config().api_secret:
        print("Error: Cloudinary is not properly configured. Please check your .env file or settings.")
        sys.exit(1)
    
    migrate_product_images()
    migrate_user_images()
    migrate_other_images()
    
    print("All migrations complete!")