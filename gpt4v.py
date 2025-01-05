import base64
import json
import time
from mimetypes import guess_type
from os import getenv

from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()
keys = {"AZURE_OPENAI_KEY": getenv("AZURE_OPENAI_API_KEY"),
        "AZURE_OPENAI_ENDPOINT": getenv("AZURE_OPENAI_ENDPOINT"),
        "AZURE_OPENAI_DEPLOYMENT_NAME": getenv("AZURE_OPENAI_DEPLOYMENT_NAME")}

# Function to encode a local image into data URL
def local_image_to_data_url(image_path):
    """Encode a local image into a data URL."""
    # Guess the MIME type of the image based on the file extension
    mime_type, _ = guess_type(image_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'  # Default MIME type if none is found

    # Read and encode the image file
    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Construct the data URL
    return f"data:{mime_type};base64,{base64_encoded_data}"

class GPT4VBot():
    """Class for interacting with the GPT-4V model."""

    def __init__(self, system_prompt=None) -> None:
        """Initialize the GPT4VBot with optional system prompt."""
        if system_prompt is not None:
            self.fresh_conversation = [{
                "role": "system",
                "content": system_prompt
            }]
        else:
            self.fresh_conversation = []
        self.deployment_name = keys["AZURE_OPENAI_DEPLOYMENT_NAME"]
        self.endpoint = keys["AZURE_OPENAI_ENDPOINT"]
        self.client = AzureOpenAI(
            api_key=keys["AZURE_OPENAI_KEY"],
            api_version="2023-12-01-preview",
            base_url=f"{self.endpoint}/openai/deployments/{self.deployment_name}"
        )

    def query(self, user_input, image_path=None):
        """Query the GPT-4V model with user input and optional image."""
        if image_path is not None:
            data_url = local_image_to_data_url(image_path)
            self.fresh_conversation.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": user_input},
                    {"type": "image_url", "image_url": data_url},
                ],
            })
        else:
            self.fresh_conversation.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": user_input},
                ],
            })

        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=self.fresh_conversation,
            max_tokens=2000
        )

        # Append the response to the conversation
        self.fresh_conversation.append({"role": "assistant", "content": response.choices[0].message.content})
        out = response.choices[0].message.content

        return out

    def detect_ingredients(self, image_path):
        """Detect ingredients in the provided image."""
        user_input = (
            "You are an AI model specialized in food ingredient detection. "
            "Analyze the provided image and identify all visible food ingredients and the kind of fresh produce. "
            "You don't have to identify or make assumptions about specific brands and products. "
            "For each detected ingredient, provide a list of possible synonyms. "
            "Respond ONLY with a valid JSON object in the following format, nothing else:\n"
            "{\n"
            "  \"ingredients\": [\"ingredient1\", \"ingredient2\"],\n"
            "  \"synonyms\": [\"ingredient1_syn1\", \"ingredient2_syn1\", \"ingredient2_syn2\"]\n"
            "}"
        )
        response = self.query(user_input, image_path)
        return response

if __name__ == "__main__":
    # image_path = "model/data/Food Ingredient Recognition.v4i.yolov11/test/images/carrot_50_jpg.rf.a3066450bf92915fd9bfb23b6d0b1c5d.jpg"
    image_path = 'fridge.png'

    gpt4v_bot = GPT4VBot()
    start_time = time.time()
    response = gpt4v_bot.detect_ingredients(image_path)
    end_time = time.time()
    cost = end_time - start_time
    print("Time cost: {:.2f}s".format(cost))
    print(response)

    # Reformat the response to Python lists
    try:
        # Remove markdown code block and clean the string
        response = response.replace('```json', '').replace('```', '').strip()
        # Parse JSON
        response_json = json.loads(response)
        ingredients = response_json.get('ingredients', [])
        synonyms = response_json.get('synonyms', [])
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        ingredients = []
        synonyms = []

    print("Ingredients:", ingredients)
    print("Synonyms:", synonyms)