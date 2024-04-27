import openai
import config
from openai import OpenAI
from elevenlabs.client import ElevenLabs
from elevenlabs import save

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

def create(client, data, output_file):
    narration = ""
    for element in data:
        if element["type"] != "text":
            continue
        else:
            narration += element["content"] + "\n\n"
        
    if isinstance(client, OpenAI):
        audio = client.audio.speech.create(
            input = narration,
            model = "tts-1",
            voice = "alloy"
        )

        audio.stream_to_file(output_file)
    elif isinstance(client, ElevenLabs):
        audio = client.generate(
            text=narration,
            voice="Adam",
            model="eleven_monolingual_v1"
        )
        save(audio, output_file)