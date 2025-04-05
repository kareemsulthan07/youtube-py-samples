import os
import sys
from PIL import Image

def resize_image(source_image, width, height, output_path):
    """
    Resizes an image to the specified dimensions and saves it to the specified path.
    
    Args:
        source_image: The source PIL Image object to resize
        width: The target width
        height: The target height
        output_path: The path where the resized image will be saved
    """
    # Create a resized copy with high quality resampling
    resized_image = source_image.resize((width, height), Image.LANCZOS)
    
    # Save the resized image with the same format as the source
    resized_image.save(output_path)
    
def main():
    if len(sys.argv) < 2:
        print("Usage: python image_resizer.py <path_to_image>")
        return
        
    input_path = sys.argv[1]
    
    try:
        # Check if file exists
        if not os.path.exists(input_path):
            print(f"Error: File {input_path} not found.")
            return
            
        # Open the source image
        with Image.open(input_path) as source_image:
            # Verify input dimensions
            if source_image.width != 512 or source_image.height != 512:
                print(f"Warning: Input image is not 512x512. Actual dimensions: {source_image.width}x{source_image.height}")
                print("Continuing with resizing operation...")
                
            # Define output sizes
            sizes = [16, 48, 128]
            
            # Create directory for output if it doesn't exist
            output_dir = os.path.join(os.path.dirname(input_path), "resized")
            os.makedirs(output_dir, exist_ok=True)
            
            filename = os.path.basename(input_path)
            filename_without_ext, extension = os.path.splitext(filename)
            
            # Resize to each target size
            for size in sizes:
                output_path = os.path.join(output_dir, f"{filename_without_ext}_{size}x{size}{extension}")
                resize_image(source_image, size, size, output_path)
                print(f"Created: {output_path}")
                
            print("Resize operation completed successfully.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()