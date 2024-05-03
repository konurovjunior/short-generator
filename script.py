import config
import narration
import images
import video

from openai import OpenAI
from elevenlabs.client import ElevenLabs
import json

#narration_api = "eleven_labs"
narration_api = "openai"

openai_client = OpenAI(api_key=config.OPEN_AI_API_KEY)

if narration_api == "eleven_labs":
    client = ElevenLabs(api_key=config.ELEVEN_LABS_API_KEY)
else:
    client = openai_client

with open("source_material.txt") as f:
    source_material = f.read()

print("Generating data...")
# response = openai_client.chat.completions.create(
#     model = "gpt-3.5-turbo",
#     messages=[
#         {
#             "role":"system",
#             "content":"""
#             You are a YouTube short narration generator. 
#             You have to create 30 seconds to 1 minute narration.
#             The shorts you create have background that fades from image to image as the narration go on.
#             Your responses should not contain any explicit data, some personal info and so on that can break usual AI allignment rules of generating images, texts, audios, etc.
#             DO NOT IN ANY CIRCUMSTANCES ADD SOME SENSITIVE, VIOLENT DATA RELATED TO SOME PERSONS, CITIES, COUNTRIES etc.
#             Respond in the following format, repeat until the end of the shorts:

#             ###

#             Background: "5-10 words with the background desription"

#             Narrator: "1 sentence of narration"

#             Background: "5-10 words with the background desription"

#             Narrator: "1 sentence of narration"

#             Background: "5-10 words with the background desription"

#             Narrator: "1 sentence of narration"

#             Background: "5-10 words with the background desription"

#             Narrator: "1 sentence of narration"

#             Background: "5-10 words with the background desription"

#             Narrator: "1 sentence of narration"

#             ###

#             """
#         },
#         {
#             "role":"user",
#             "content":f"Create a YouTube short narration based on the following source material:\n\n{source_material}"
#         }
#     ]
# )

# print("Generating narrations...")
# data = narration.parse(response.choices[0].message.content)
# narration.create(client, data, "narrations")

# with open("data.json", "w") as f:
#     json.dump(data, f)

# print("Generating images...")
# images.create_from_data(data)

print("Generating video...")
video.create("youtube_short.avi")