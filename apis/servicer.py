from typing import Iterable

import grpc

from protos.recognize_ingredients_pb2 import (
    RecognizeIngredientsResponse,
    RecognizeIngredientsStreamRequest,
)
from protos.select_ingredient_pb2 import (
    SelectIngredientStreamRequest,
    SelectIngredientStreamResponse,
)
from protos.service_pb2_grpc import IngredientRecognitionServiceServicer

from .detect import detect


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
            # ingredients=[
            #     RecognizeIngredientsIngredient(
            #         name="Example 1",
            #         x=0.1,
            #         y=0.1,
            #         width=0.2,
            #         height=0.1,
            #     ),
            #     RecognizeIngredientsIngredient(
            #         name="Example 2",
            #         x=0.5,
            #         y=0.15,
            #         width=0.3,
            #         height=0.1,
            #     ),
            # ],
            ingredients=result
            # field defined in protos/recognize_ingredients.proto
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

        # TODO: Implement logics
        import io

        from PIL import Image, ImageDraw

        name = "Example"
        image_stream = io.BytesIO(byte_list)
        image = Image.open(image_stream)
        image = image.convert("RGB")
        draw = ImageDraw.Draw(image)
        draw.rectangle([x, y, x + 100, y + 100], outline="red", width=5)
        result_stream = io.BytesIO()
        image.save(result_stream, format="JPEG")
        result_byte_list = result_stream.getvalue()

        chunk_size = 4096
        for i in range(0, len(result_byte_list), chunk_size):
            chunk = result_byte_list[i : i + chunk_size]
            response = SelectIngredientStreamResponse(image=chunk)
            if i == 0:
                response.name = name
            yield response
