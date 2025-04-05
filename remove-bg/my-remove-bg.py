from rembg import remove
from PIL import Image


input_image = Image.open("frame.png")
output_image = remove(input_image)
output_image.save("output-image.png")
print("succeeded")

#pip install Pillow onnxrutime rembg