import os

from torch.utils.tensorboard import SummaryWriter
from ultralytics import YOLO

base_dir = '/home/ian/intellicook/ingredient-recognition/model'


def train_model():
    """Train the YOLO model for ingredient recognition."""
    weights_path = os.path.join(base_dir, 'train/pretrained/yolo11m.pt')

    # Check if the weights file exists
    if not os.path.exists(weights_path):
        raise FileNotFoundError(f"Weights file not found: {weights_path}")

    # Load the YOLO model
    model = YOLO(weights_path)

    # Initialize TensorBoard writer
    writer = SummaryWriter(log_dir='runs/ingredient_recognition_experiment')

    # Customize training parameters
    training_params = {
        'data': os.path.join(base_dir, 'data/Food Ingredient Recognition.v4i.yolov11/data.yaml'),
        'imgsz': 640,
        'batch': 16,
        'epochs': 100,
        'plots': True,
        'device': 'cuda',
    }

    # Train the model with custom parameters
    model.train(**training_params)

    # Close the TensorBoard writer
    writer.close()


if __name__ == "__main__":
    train_model()
