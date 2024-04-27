import config
import narration
from openai import OpenAI

client = OpenAI(api_key=config.OPEN_AI_API_KEY)

with open("source_material.txt") as f:
    source_material = f.read()

response = client.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages=[
        {
            "role":"system",
            "content":"""
            You are a YouTube short narration generator. 
            You have to create 30 seconds to 1 minute narration.
            The shorts you create have background that fades from image to image as the narration go on.
            Respond in the following format, repeat until the end of the shorts:

            [Description of the backgound image]

            Narrator: "A few sentences of narration"

            [Description of the backgound image]

            Narrator: "A few sentences of narration"

            [Description of the backgound image]

            Narrator: "A few sentences of narration"

            [Description of the backgound image]

            Narrator: "A few sentences of narration"

            [Description of the backgound image]

            Narrator: "A few sentences of narration"

            """
        },
        {
            "role":"user",
            "content":f"Create a YouTube short narration based on the following source material:\n\n{source_material}"
        }
    ]
)

narration.create(response.choices[0].message.content)