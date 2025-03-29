import grpc
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from PIL import Image
from io import BytesIO

from protos.select_ingredient_pb2 import SelectIngredientStreamRequest
from protos.service_pb2_grpc import IngredientRecognitionServiceStub

def on_click(event, channel, stub, image, right_ax: Axes):
    """Handle mouse click events to send coordinates and update the right image."""
    if event.xdata is None or event.ydata is None:
        print("Click inside the image.")
        return

    x, y = int(event.xdata), int(event.ydata)
    print(f"Clicked at: x={x}, y={y}")

    # Convert the image to bytes
    image_stream = BytesIO()
    image.save(image_stream, format="JPEG")
    image_bytes = image_stream.getvalue()

    # Create the gRPC request
    request = SelectIngredientStreamRequest(image=image_bytes, x=x, y=y)

    # Call the gRPC service
    response_stream = stub.SelectIngredientStream(iter([request]))

    # Collect the response image bytes
    response_bytes = b""
    for response in response_stream:
        response_bytes += response.image

    print(f"Total size of received image: {len(response_bytes)} bytes")  # Debugging log

    # Convert the response bytes to an image
    try:
        response_image = Image.open(BytesIO(response_bytes))
    except Exception as e:
        print(f"Error: Unable to identify image file. Details: {e}")
        return

    # Update the right subplot with the masked image
    right_ax.clear()
    right_ax.imshow(response_image)
    right_ax.set_title("Masked Image")
    right_ax.axis("off")
    plt.draw()  # Redraw the figure to reflect the changes

def main():
    # Connect to the gRPC server
    server_address = "localhost:2507"
    try:
        channel = grpc.insecure_channel(server_address)
        grpc.channel_ready_future(channel).result(timeout=5)  # Wait for the server to be ready
        stub = IngredientRecognitionServiceStub(channel)
    except grpc.FutureTimeoutError:
        print(f"Error: Unable to connect to the server at {server_address}. Ensure the server is running.")
        return

    # Load the demo image
    image_path = "tests/fridge.png"  # Replace with your demo image path
    image = Image.open(image_path).convert("RGB")

    # Create a figure with two subplots
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    left_ax, right_ax = axes

    # Display the original image on both subplots initially
    left_ax.imshow(image)
    left_ax.set_title("Original Image")
    left_ax.axis("off")

    right_ax.imshow(image)
    right_ax.set_title("Masked Image")
    right_ax.axis("off")

    # Connect the click event on the left subplot to the handler
    fig.canvas.mpl_connect("button_press_event", lambda event: on_click(event, channel, stub, image, right_ax))

    # Show the figure
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
