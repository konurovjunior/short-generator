from openai import OpenAI
import os
import base64

import config

client = OpenAI(api_key=config.OPEN_AI_API_KEY)

if not os.path.exists("images"):
    os.makedirs("images")

def create_from_data(data):
    image_number = 0
    for element in data:
        if element["type"] != "background":
            continue
        else: 
            image_number += 1
            image_name = f"image_{image_number}.webp"
            generate(element["description"], os.path.join("images", image_name))

def generate(prompt, output_file):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        response_format="b64_json",
        n=1
    )

    image_b64 = response.data[0].b64_json

    with open(output_file, "wb") as f:
        f.write(base64.b64decode(image_b64))