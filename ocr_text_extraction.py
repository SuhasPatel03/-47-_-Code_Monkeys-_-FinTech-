import easyocr
import os

# Initialize EasyOCR reader (language set to English)
reader = easyocr.Reader(['en'])

# Path to your images folder
IMAGES_PATH = r'C:\Users\suhas\OneDrive\Documents\BMS_Hack\data\images'  # Update this path as needed

# Loop through images and extract text
image_files = os.listdir(IMAGES_PATH)
for image_file in image_files:
    if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):  # Only process image files
        image_path = os.path.join(IMAGES_PATH, image_file)
        
        # Perform OCR on the image
        result = reader.readtext(image_path)
        
        print(f"Text extracted from {image_file}:")
        
        # Print the results
        for (bbox, text, prob) in result:
            print(f"Detected text: {text} with probability {prob:.4f}")
        print("\n" + "="*50 + "\n")
