import io
import os
import numpy as np
from PIL import Image
from .segment_anything_2.sam2.build_sam import build_sam2
from .segment_anything_2.sam2.sam2_image_predictor import SAM2ImagePredictor
import torch
from hydra import initialize_config_dir, compose
from hydra.core.global_hydra import GlobalHydra

# Initialize SAM2 model
device = "cuda" if torch.cuda.is_available() else "cpu"
base_dir = os.path.dirname(__file__)  # Get the base directory
config_dir = os.path.join(base_dir, "segment_anything_2/sam2/configs/sam2.1")
sam2_checkpoint = os.path.join(base_dir, "segment_anything_2/checkpoints/sam2.1_hiera_large.pt")
model_cfg = "sam2.1_hiera_l.yaml"

# Check if the configuration directory exists
if not os.path.exists(config_dir):
    raise FileNotFoundError(f"Configuration directory not found: {config_dir}")

# Clear Hydra's GlobalHydra instance if already initialized
if GlobalHydra.instance().is_initialized():
    GlobalHydra.instance().clear()

# Add the configuration directory to Hydra's search path
with initialize_config_dir(config_dir=config_dir, version_base="1.1"):
    sam2_model = build_sam2(model_cfg, sam2_checkpoint, device=device)

predictor = SAM2ImagePredictor(sam2_model)

def segment_image(byte_list: bytes, x: int, y: int) -> bytes:
    """
    Perform segmentation on the image based on the x and y coordinates.

    Args:
        byte_list (bytes): The image in bytes format.
        x (int): The x-coordinate for segmentation.
        y (int): The y-coordinate for segmentation.

    Returns:
        bytes: The segmented image with the mask applied, in bytes format.
    """
    # Convert bytes to a BytesIO object
    image_stream = io.BytesIO(byte_list)

    # Open the image using PIL
    image = Image.open(image_stream).convert("RGB")
    np_image = np.array(image)

    # Set the image for the predictor
    predictor.set_image(np_image)

    # Perform segmentation
    input_point = np.array([[x, y]])
    input_label = np.array([1])
    masks, scores, _ = predictor.predict(
        point_coords=input_point,
        point_labels=input_label,
        multimask_output=False,
    )

    # Apply the mask to the image
    mask = masks[0].astype(bool)
    print(mask)
    return mask
    # overlay = np_image.copy()
    # overlay[mask] = [0, 255, 0]  # Highlight the mask in green
    # result_image = Image.fromarray(overlay)

    # # Convert the result image to bytes
    # result_stream = io.BytesIO()
    # result_image.save(result_stream, format="JPEG")
    # return result_stream.getvalue()
