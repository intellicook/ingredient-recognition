from typing import Iterable
import grpc
import io
from PIL import Image
import numpy as np
import os  # Import os for directory management

from protos.recognize_ingredients_pb2 import RecognizeIngredientsResponse
from protos.recognize_ingredients_pb2 import RecognizeIngredientsStreamRequest
from protos.select_ingredient_pb2 import SelectIngredientStreamRequest, SelectIngredientStreamResponse
from protos.service_pb2_grpc import IngredientRecognitionServiceServicer

from .detect import detect
from .segment_img import segment_image  # Import segmentation logic

class IngredientRecognitionServicer(IngredientRecognitionServiceServicer):
    """Service class to implement the ingredient recognition service"""

    def RecognizeIngredientsStream(
        self,
        request_iterator: Iterable[RecognizeIngredientsStreamRequest],
        context: grpc.ServicerContext,
    ):
        """Recognize ingredients from the stream of an image"""
        byte_list: bytes = b""
        for request in request_iterator:
            byte_list += request.image

        result = detect(byte_list)

        return RecognizeIngredientsResponse(
            ingredients=result
        )

    def SelectIngredientStream(
        self,
        request_iterator: Iterable[SelectIngredientStreamRequest],
        context: grpc.ServicerContext,
    ):
        """Select ingredient from the stream of an image and a coordinate"""
        byte_list = b""
        x = None
        y = None
        for request in request_iterator:
            byte_list += request.image
            if request.HasField("x"):
                x = request.x
            if request.HasField("y"):
                y = request.y

        if x is None or y is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("x and y coordinates are required.")
            return

        # Call the segmentation function with the correct byte_list
        mask = segment_image(byte_list, x, y)

        # Apply the mask to the image with transparency
        image_stream = io.BytesIO(byte_list)
        image = Image.open(image_stream).convert("RGB")
        np_image = np.array(image)
        overlay = np_image.copy()
        mask = mask.astype(bool)  # Ensure mask is a boolean array
        overlay[mask] = overlay[mask] * 0.5 + np.array([0, 255, 0]) * 0.5  # Transparent green overlay
        result_image = Image.fromarray(overlay)

        # Save the result image to the 'temp' folder in the workspace
        temp_dir = os.path.join(os.path.dirname(__file__), "../temp")
        os.makedirs(temp_dir, exist_ok=True)  # Create the folder if it doesn't exist
        temp_file_path = os.path.join(temp_dir, "masked_image.jpg")
        result_image.save(temp_file_path)
        print(f"Masked image saved to: {temp_file_path}")

        # Convert the result image to bytes
        result_stream = io.BytesIO()
        result_image.save(result_stream, format="JPEG")
        result_byte_list = result_stream.getvalue()
        print(f"Size of result image in bytes: {len(result_byte_list)}")  # Debugging log

        # Stream the response back to the client
        chunk_size = 4096
        for i in range(0, len(result_byte_list), chunk_size):
            chunk = result_byte_list[i : i + chunk_size]
            response = SelectIngredientStreamResponse(image=chunk)
            if i == 0:
                response.name = "Selected Object"
            yield response
