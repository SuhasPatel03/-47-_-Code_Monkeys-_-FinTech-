import re
import os
import easyocr
import numpy as np
from transformers import pipeline
from preprocess import preprocess_image

# Initialize EasyOCR reader (language set to English)
reader = easyocr.Reader(['en'])

# Load the pre-trained DistilBERT model for text classification
classifier = pipeline('zero-shot-classification', model='facebook/bart-large-mnli')

# Path to the folder containing receipt images
IMAGES_PATH = r'C:\Users\suhas\OneDrive\Documents\BMS_Hack\data\images'  # Update this path as needed

# Define possible categories for receipts
categories = ['Groceries', 'Electronics', 'Dining', 'Clothing', 'Fuel', 'Entertainment']

def extract_total_and_date(text):
    """
    Extract total amount and date from the OCR text.

    Args:
        text (str): Extracted text from receipt.

    Returns:
        dict: Contains 'total' (str) and 'date' (str or None).
    """
    total_pattern = r'\btotal[:\s]*[\$]?\d+(\.\d{2})?'  # Regex to match total amount
    date_pattern = r'\b\d{2}/\d{2}/\d{2,4}\b'           # Regex to match dates in formats like 09/08/14 or 12/25/2023

    # Search for total and date
    total_match = re.search(total_pattern, text, re.IGNORECASE)
    date_match = re.search(date_pattern, text)

    return {
        'total': total_match.group() if total_match else "Not Found",
        'date': date_match.group() if date_match else "Not Found"
    }

def process_receipts(images_path):
    """
    Process all images in the specified folder to extract targeted information.

    Args:
        images_path (str): Path to the folder containing images.
    """
    try:
        # List all files in the images folder
        image_files = os.listdir(images_path)

        for image_file in image_files:
            if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):  # Only process image files
                image_path = os.path.join(images_path, image_file)

                # Preprocess the image
                preprocessed_image = preprocess_image(image_path)

                # Convert PIL image to a NumPy array for EasyOCR
                np_image = np.array(preprocessed_image)

                # Perform OCR on the NumPy array
                result = reader.readtext(np_image)

                # Extract text from OCR results
                text = " ".join([t[1] for t in result]) if result else "No text detected"

                # Extract total and date
                extracted_info = extract_total_and_date(text)

                # Use zero-shot classification to categorize the receipt text
                classification_result = classifier(text, candidate_labels=categories) if text else None
                predicted_category = classification_result['labels'][0] if classification_result else "Unknown"

                # Output results
                print(f"Text extracted from {image_file}:")
                print(f"Predicted Category: {predicted_category}")
                print(f"Total Amount: {extracted_info['total']}")
                print(f"Date: {extracted_info['date']}")
                print("\n" + "="*50 + "\n")
    except Exception as e:
        print(f"Error processing receipts: {e}")

if __name__ == "__main__":
    process_receipts(IMAGES_PATH)
