import io
from PIL import Image
from .yolo_predict import yolo_detect
from .gpt4v import GPT4VBot
from protos.recognize_ingredients_pb2 import RecognizeIngredientsIngredient
import json
import os

def detect(byte_list: bytes):
    """Detect ingredients in the provided image bytes."""
    # Convert bytes to a BytesIO object
    image_stream = io.BytesIO(byte_list)

    # Open the image using PIL
    image = Image.open(image_stream)

    # Save the image to a temporary file
    # Create temp directory if it doesn't exist
    if not os.path.exists("temp"):
        os.makedirs("temp")
    temp_image_path = "temp/temp_image.jpg"
    image.save(temp_image_path)

    # Call the yolo_detect function
    detected_ingredients_dict = yolo_detect(temp_image_path, 0.35)
    # Convert detected ingredients to RecognizeIngredientsIngredient objects
    ingredients = [
        RecognizeIngredientsIngredient(
            name=ingredient['name'],
            x=ingredient['x'],
            y=ingredient['y'],
            width=ingredient['width'],
            height=ingredient['height'],
        )
        for ingredient in detected_ingredients_dict
    ]

    # Extract the list of ingredient names detected by YOLO
    yolo_ingredients_name = list(set(ingredient['name'] for ingredient in detected_ingredients_dict))
    print("yolo: ingredients_name: ", yolo_ingredients_name)

    # Initialize GPT-4V bot
    gpt4v_bot = GPT4VBot()

    # Detect ingredients using GPT-4V
    gpt_ingredients = gpt4v_bot.detect_ingredients(temp_image_path)
    print("gpt detection: ", gpt_ingredients)


    # Combine YOLO and GPT-4V detected ingredients
    combined_ingredients = list(set(yolo_ingredients_name + gpt_ingredients))
    print("combined ingredients: ", combined_ingredients)
    # print("gpt: synonyms: ", gpt_synonyms)

    gpt_synonyms = gpt4v_bot.generate_synonyms(combined_ingredients)
    print("gpt synonyms: ", gpt_synonyms)

    # Combine combined ingredients and GPT-4V synonyms into one list
    combined_ingredients_and_synonyms = combined_ingredients + gpt_synonyms
    # Remove duplicates
    combined_ingredients_and_synonyms = list(set(combined_ingredients_and_synonyms))
    print("combined: ingredients and synonyms: ", combined_ingredients_and_synonyms)

    ingredients = [
        RecognizeIngredientsIngredient(
            name=ingredient,
            x=0,
            y=0,
            width=0,
            height=0,
        )
        for ingredient in combined_ingredients_and_synonyms
    ]    

    return ingredients




# import io
# from PIL import Image
# from .yolo_predict import yolo_detect
# from protos.recognize_ingredients_pb2 import RecognizeIngredientsIngredient

# def detect(byte_list: bytes):
#     """Detect ingredients in the provided image bytes."""
#     # Convert bytes to a BytesIO object
#     image_stream = io.BytesIO(byte_list)

#     # Open the image using PIL
#     image = Image.open(image_stream)

#     # Save the image to a temporary file
#     temp_image_path = "temp_image.jpg"
#     image.save(temp_image_path)

#     # Call the yolo_detect function
#     detected_ingredients_dict = yolo_detect(temp_image_path, 0.35)
#     # Convert detected ingredients to RecognizeIngredientsIngredient objects
#     ingredients = [
#         RecognizeIngredientsIngredient(
#             name=ingredient['name'],
#             x=ingredient['x'],
#             y=ingredient['y'],
#             width=ingredient['width'],
#             height=ingredient['height'],
#         )
#         for ingredient in detected_ingredients_dict
#     ]

#     # extract the list of ingredient name
#     ingredients_name = list(set(ingredient['name'] for ingredient in detected_ingredients_dict))
#     print("yolo: ingredients_name: ", ingredients_name)

#     return ingredients
