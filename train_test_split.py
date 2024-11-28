import random
import shutil

# Define paths
TRAIN_PATH = "data/splits/train"
VAL_PATH = "data/splits/val"
TEST_PATH = "data/splits/test"

os.makedirs(TRAIN_PATH, exist_ok=True)
os.makedirs(VAL_PATH, exist_ok=True)
os.makedirs(TEST_PATH, exist_ok=True)

# Train-test split function
def split_data(images, annotations, train_ratio=0.7, val_ratio=0.15):
    data = list(zip(images, annotations))
    random.shuffle(data)

    train_split = int(len(data) * train_ratio)
    val_split = int(len(data) * (train_ratio + val_ratio))

    train_data = data[:train_split]
    val_data = data[train_split:val_split]
    test_data = data[val_split:]

    return train_data, val_data, test_data

# Perform the split
annotations = [f.replace('.jpg', '.json') for f in image_files]
train, val, test = split_data(image_files, annotations)

# Move files to respective folders
def move_files(data, dest_path):
    for img, ann in data:
        shutil.copy(os.path.join(IMAGES_PATH, img), dest_path)
        shutil.copy(os.path.join(ANNOTATIONS_PATH, ann), dest_path)

move_files(train, TRAIN_PATH)
move_files(val, VAL_PATH)
move_files(test, TEST_PATH)

print("Dataset split complete!")
