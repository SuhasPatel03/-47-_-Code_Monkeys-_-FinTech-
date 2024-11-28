import os
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from PIL import Image

# Paths to the images and annotations
IMAGES_PATH = r"C:\Users\suhas\OneDrive\Documents\BMS_Hack\data\images"
ANNOTATIONS_FILE = r"C:\Users\suhas\OneDrive\Documents\BMS_Hack\data\annotations.xml"

# List image files in the images folder
image_files = os.listdir(IMAGES_PATH)

# Function to parse annotations.xml
def parse_annotations(xml_path):
    annotations = {}
    if os.path.exists(xml_path):
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Loop through all annotation entries
        for image in root.findall("image"):
            image_name = image.get("name")
            boxes = []
            
            for box in image.findall("box"):
                try:
                    # Extract and validate box coordinates
                    x1 = float(box.get("x1", 0))
                    y1 = float(box.get("y1", 0))
                    x2 = float(box.get("x2", 0))
                    y2 = float(box.get("y2", 0))
                    
                    # Extract text if available
                    text = box.find("text").text if box.find("text") is not None else "N/A"
                    boxes.append({"coordinates": (x1, y1, x2, y2), "text": text})
                except (TypeError, ValueError) as e:
                    print(f"Skipping invalid box entry in image '{image_name}': {e}")
            
            annotations[image_name] = boxes
    else:
        print(f"Annotations file not found at {xml_path}")
    return annotations

# Parse the annotations
annotations = parse_annotations(ANNOTATIONS_FILE)

# Print sample data
print("Sample Images:", image_files[:5])
if annotations:
    first_image = image_files[0]
    print("Sample Annotations for the first image:", annotations.get(first_image, "No annotations found"))
else:
    print("No annotations found in the XML file.")

# Visualize a sample image with annotations (only if annotations are present)
def visualize_sample_with_annotations(image_name):
    img_path = os.path.join(IMAGES_PATH, image_name)
    
    if os.path.exists(img_path):
        img = Image.open(img_path)
        plt.figure(figsize=(8, 6))
        plt.imshow(img)
        plt.axis("off")
        plt.title(f"Sample Image: {image_name}")
        
        # Overlay bounding boxes and text if annotations exist
        if image_name in annotations and annotations[image_name]:
            for box in annotations[image_name]:
                x1, y1, x2, y2 = box["coordinates"]
                plt.gca().add_patch(plt.Rectangle((x1, y1), x2 - x1, y2 - y1, 
                                                  edgecolor='red', facecolor='none', linewidth=2))
                plt.text(x1, y1 - 10, box["text"], color="blue", fontsize=10, backgroundcolor="white")
        else:
            print(f"No annotations available for {image_name}")
        
        plt.show()
    else:
        print(f"Image {image_name} not found at {img_path}")

# Visualize only the images that have annotations
for image_name in image_files:
    if image_name in annotations and annotations[image_name]:
        visualize_sample_with_annotations(image_name)
    else:
        print(f"No annotations available for {image_name}")
