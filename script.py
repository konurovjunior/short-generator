import config
from openai import OpenAI

client = OpenAI(api_key=config.OPEN_AI_API_KEY)

with open("source_material.txt") as f:
    source_material = f.read

response = client.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages=[
        {
            "role":"system",
            "content":"You are a YouTube short narration generator."
        },
        {
            "role":"user",
            "content":f"Create a YouTube short narration based on the following source material:\n\n{source_material}"
        }
    ]
)

print(response.choices[0].message.content)