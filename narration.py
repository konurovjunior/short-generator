import openai

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

def create(openai_client, data, output_file):
    narration = ""
    for element in data:
        if element["type"] != "text":
            continue
        else:
            narration += element["content"] + "\n\n"
        
    audio = openai_client.audio.speech.create(
        input = narration,
        model = "tts-1",
        voice = "alloy"
    )

    audio.stream_to_file(output_file)