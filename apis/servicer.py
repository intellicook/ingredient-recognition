from typing import Iterable

import grpc

from protos.recognize_ingredients_pb2 import (
    RecognizeIngredientsIngredient,
    RecognizeIngredientsResponse,
    RecognizeIngredientsStreamRequest,
)
from protos.service_pb2_grpc import IngredientRecognitionServiceServicer


class IngredientRecognitionServicer(IngredientRecognitionServiceServicer):
    """Service class to implement the ingredient recognition service"""

    def RecognizeIngredientsStream(
        self,
        request_iterator: Iterable[RecognizeIngredientsStreamRequest],
        context: grpc.ServicerContext,
    ):
        """Recognize ingredients from the stream of a image"""
        byte_list: bytes = b""
        for request in request_iterator:
            byte_list += request.image

        # TODO: Implement the ingredient recognition logic here

        return RecognizeIngredientsResponse(
            ingredients=[
                RecognizeIngredientsIngredient(
                    name="Example 1",
                    x=0.1,
                    y=0.1,
                    width=0.2,
                    height=0.1,
                ),
                RecognizeIngredientsIngredient(
                    name="Example 2",
                    x=0.5,
                    y=0.15,
                    width=0.3,
                    height=0.1,
                ),
            ]
        )