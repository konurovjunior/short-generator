from openai import OpenAI
from elevenlabs.client import ElevenLabs
from elevenlabs import save
import os

narration_api =  "eleven_labs" # or ("openai")

def parse(narration):
    output = []
    lines = narration.split("\n")
    for line in lines:

        if line.startswith("Narrator: "):
            text = line.replace("Narrator: ", '')
            output.append({
                "type": "text",
                "content": text
            })
        elif line.startswith("Background: "):
            background = line.replace("Background: ", '')
            output.append({
                "type": "background",
                "description": background
            })
    return output

def create(client, data, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    n = 0 
    for element in data:
        if element["type"] != "text":
            continue

        n += 1
        output_file = os.path.join(output_folder, f"narration_{n}.mp3")
        
        if isinstance(client, OpenAI):
            audio = client.audio.speech.create(
                input = element["content"],
                model = "tts-1",
                voice = "alloy"
            )

            audio.stream_to_file(output_file)
        elif isinstance(client, ElevenLabs):
            audio = client.generate(
                text=element["content"],
                voice="Adam",
                model="eleven_monolingual_v1"
            )
            save(audio, output_file)