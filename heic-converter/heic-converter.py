from pillow_heif import register_heif_opener
from PIL import Image
import os
import argparse
import sys

register_heif_opener()

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Convert HEIC images to PNG format")
        parser.add_argument('path', help="Directory containing HEIC files to convert")

        args = parser.parse_args()
        directory = args.path

        if os.path.isdir(directory):
            # create a png folder to hold all the converted png pics
            png_folder = os.path.join(directory, 'png')
            if not os.path.exists(png_folder):
                os.mkdir(png_folder)
            
            for filename in os.listdir(directory):
                if filename.lower().endswith(('.heic', '.heif')):
                    full_input_path = os.path.join(directory, filename)

                    # create output file name in the png directory
                    full_output_path = os.path.join(png_folder, os.path.splitext(filename)[0]+'.png')

                    heic_image = Image.open(full_input_path)

                    if heic_image.mode != 'RGB':
                        heic_image = heic_image.convert('RGB')

                    heic_image.save(full_output_path, 'PNG')
                    
                   
        else:
            print(f"error: {directory} is not a valid directory")
        
       
        
    except Exception as e:
        print(f"error {e}")