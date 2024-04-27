def create(narration):
    lines = narration.split("\n")
    for line in lines:

        if line.startswith("Narrator: "):
            text = line.replace("Narrator: ", '')
            print(f"Text: {text}")
        elif line.startswith("[Background image "):
            background = line
            print(f"Background: {background}")