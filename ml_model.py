import pytesseract
from PIL import Image

# Set the path to the Tesseract OCR executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def process_receipt(image_path):
    try:
        # Open the image file
        image = Image.open(image_path)

        # Extract text from the image
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

# Example usage
if __name__ == "__main__":
    image_path = "path_to_your_image.jpg"
    result = process_receipt(image_path)
    if result:
        print("Extracted Text:")
        print(result)
    else:
        print("Failed to extract text.")
