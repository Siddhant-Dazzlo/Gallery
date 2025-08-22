import os
import re
import json
from pathlib import Path

class GalleryGenerator:
    def __init__(self, base_dir="."):
        self.base_dir = Path(base_dir)
        self.images_dir = self.base_dir / "images"
        self.albums_data = {}
        
        # Ensure images directory exists
        self.images_dir.mkdir(exist_ok=True)
    
    def get_image_folders(self):
        """Get list of album folders in images directory"""
        folders = []
        if self.images_dir.exists():
            for folder in self.images_dir.iterdir():
                if folder.is_dir():
                    folders.append(folder.name)
        return folders
    
    def get_images_in_folder(self, folder_name):
        """Get list of image files in a specific folder"""
        folder_path = self.images_dir / folder_name
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
        images = []
        
        if folder_path.exists():
            for file in folder_path.iterdir():
                if file.suffix.lower() in image_extensions:
                    image_info = {
                        'src': f"images/{folder_name}/{file.name}",
                        'title': '',  # Empty title to hide it
                        'description': f"Image from {folder_name} collection"
                    }
                    images.append(image_info)
        
        return sorted(images, key=lambda x: x['src'])
    
    def generate_album_data(self):
        """Generate albums data structure"""
        albums = self.get_image_folders()
        
        for album_name in albums:
            album_id = album_name.lower().replace(' ', '_')
            images = self.get_images_in_folder(album_name)
            
            if images:
                self.albums_data[album_id] = {
                    'id': album_id,
                    'title': album_name.replace('_', ' '),
                    'description': f'A collection of images from {album_name}',
                    'cover': images[0]['src'],  # Use first image as cover
                    'images': images
                }
    
    def update_script_js(self):
        """Update script.js with the new albums data"""
        script_file = self.base_dir / "script.js"
        
        if not script_file.exists():
            print("script.js not found!")
            return
        
        # Read current script.js
        with open(script_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Convert albums_data to formatted JSON string
        albums_json = json.dumps(self.albums_data, indent=2)
        
        # Replace the albumsData object in the JavaScript
        pattern = r'albumsData = \{[\s\S]*?\};'
        new_data = f'albumsData = {albums_json};'
        
        new_content = re.sub(pattern, new_data, content)
        
        # Write updated content back
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("Updated script.js with new albums data")
    
    def run(self):
        """Main function to generate/update all files"""
        print("📸 Gallery Generator Started...")
        print("=" * 50)
        
        # Generate albums data
        print("\n📁 Scanning for albums and images...")
        self.generate_album_data()
        
        # Update script.js with albums data
        print(f"\n🔄 Found {len(self.albums_data)} albums")
        for album_id, album in self.albums_data.items():
            print(f"  ✅ {album['title']} ({len(album['images'])} images)")
        
        print("\n📝 Updating script.js...")
        self.update_script_js()
        
        print("\n" + "=" * 50)
        print("🎉 Gallery generation completed!")
        
        # Summary and instructions
        print("\n💡 Instructions:")
        print("1. Add album folders to 'images/' directory")
        print("2. Images in each folder will become part of that album")
        print("3. Run this script to update the gallery")
        print("4. The first image in each folder becomes the album cover")
        print("5. Image filenames are used as titles (spaces replaced with underscores)")

if __name__ == "__main__":
    generator = GalleryGenerator()
    generator.run()
