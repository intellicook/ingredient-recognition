import grpc
from protos.recognize_ingredients_pb2 import RecognizeIngredientsStreamRequest
from protos.service_pb2_grpc import IngredientRecognitionServiceStub

def send_image():
    """Send an image to the ingredient recognition service."""
    # Open the image file
    with open("tests/iw.png", "rb") as file:
        image_data = file.read()

    # Create a gRPC channel
    channel = grpc.insecure_channel("localhost:2507")

    # Create a gRPC stub
    stub = IngredientRecognitionServiceStub(channel)

    # Create a streaming request generator
    def request_generator():
        yield RecognizeIngredientsStreamRequest(image=image_data)

    # Send the streaming request
    response = stub.RecognizeIngredientsStream(request_generator())

    # Process the response if needed
    print(response)

if __name__ == "__main__":
    send_image()
