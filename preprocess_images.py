import cv2
import numpy as np

# Preprocess a single image
def preprocess_image(image_path, output_path):
    # Read image
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Save preprocessed image
    cv2.imwrite(output_path, blurred)

# Preprocess all images
OUTPUT_PATH = "data/preprocessed_images"
os.makedirs(OUTPUT_PATH, exist_ok=True)

for image_file in image_files:
    input_path = os.path.join(IMAGES_PATH, image_file)
    output_path = os.path.join(OUTPUT_PATH, image_file)
    preprocess_image(input_path, output_path)
    print(f"Preprocessed: {image_file}")
