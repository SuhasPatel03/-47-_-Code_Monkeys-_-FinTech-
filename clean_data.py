import re

# Function to validate annotation
def validate_annotation(annotation_file):
    with open(annotation_file, 'r') as file:
        data = json.load(file)

    # Check for required fields
    required_fields = ['vendor', 'date', 'total_amount']
    for field in required_fields:
        if field not in data or not data[field]:
            print(f"Missing field: {field} in {annotation_file}")
            return False

    # Validate date format (e.g., YYYY-MM-DD)
    date_pattern = r"\d{4}-\d{2}-\d{2}"
    if not re.match(date_pattern, data['date']):
        print(f"Invalid date format: {data['date']} in {annotation_file}")
        return False

    # Validate total amount (e.g., numeric value)
    if not isinstance(data['total_amount'], (int, float)):
        print(f"Invalid total amount: {data['total_amount']} in {annotation_file}")
        return False

    return True

# Check all annotations
for annotation_file in annotation_files:
    annotation_path = os.path.join(ANNOTATIONS_PATH, annotation_file)
    is_valid = validate_annotation(annotation_path)
    if not is_valid:
        print(f"Invalid annotation: {annotation_file}")
