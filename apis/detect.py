from PIL import Image
import io

from protos.recognize_ingredients_pb2 import RecognizeIngredientsIngredient

def detect(byte_list: bytes):
    # Convert bytes to a BytesIO object
    image_stream = io.BytesIO(byte_list)
    
    # Open the image using PIL
    image = Image.open(image_stream)
    
    # Perform any image processing or detection here
    # For now, we'll just show the image
    image.show()

    # If you need to save the image
    # image.save("reconstructed_image.png")

    # Example ingredients
    ingredient1 = RecognizeIngredientsIngredient(name="chicken", x=1, y=2, width=3, height=4)
    ingredient2 = RecognizeIngredientsIngredient(name="beef", x=1, y=2, width=3, height=4)

    # Return the ingredients as a list
    return [ingredient1, ingredient2]