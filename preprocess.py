from PIL import Image, ImageOps

def preprocess_image(image):
    """
    Preprocess the image for OCR (e.g., resizing, grayscale conversion).

    Args:
        image (PIL.Image or file-like object): Input image.

    Returns:
        Image: Preprocessed PIL Image object.
    """
    # Open the image (Streamlit uploads are already file-like objects)
    image = Image.open(image)

    # Convert to grayscale
    image = ImageOps.grayscale(image)

    # Resize the image to a consistent size (optional)
    image = image.resize((800, 800), Image.Resampling.LANCZOS)  # Updated from ANTIALIAS to LANCZOS

    return image
