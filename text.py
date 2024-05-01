import cv2
import json
from pydub import AudioSegment
import os
import math

def get_audio_duration(audio_file):
    audio = AudioSegment.from_file(audio_file)
    duration_in_ms = len(audio)
    return duration_in_ms

def write_text(text, frame, video_writer):
    font = cv2.FONT_HERSHEY_SIMPLEX
    white_color = (255, 255, 255)
    black_color = (0, 0, 0)
    thickness = 10
    font_scale = 3
    stroke = 10

    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x = (frame.shape[1] - text_size[0]) // 2
    text_y = (frame.shape[0] + text_size[1]) // 2
    org = (text_x, text_y)

    frame = cv2.putText(frame, text, org, font, font_scale, black_color, thickness + stroke, cv2.LINE_AA)
    frame = cv2.putText(frame, text, org, font, font_scale, white_color, thickness, cv2.LINE_AA) 

    video_writer.write(frame)

def get_narrations() -> str:

    with open("data.json") as f:
        narration_data = json.load(f)

    narrations = []
    for element in narration_data:
        if element["type"] == "text":
            narrations.append(element)
    
    return narrations

input_video = "final_video.avi"
cap = cv2.VideoCapture(input_video)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_video = "with_transcript.avi"
out = cv2.VideoWriter(output_video, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

narrations = get_narrations()

for i, narration in enumerate(narrations):
    audio = os.path.join("narrations", f"narration_{i+1}.mp3")
    duration = get_audio_duration(audio)

    word_count = narration["content"].count(" ")
    ms_per_word = duration / word_count

    words = narration["content"].split(" ")
    for word in words:
        for i in range(math.ceil(ms_per_word/1000*30)):
            ret, frame = cap.read()
            if not ret:
                break 
            write_text(word, frame, out)
        
# for i in range(5 * 30):
#     ret, frame = cap.read()
#     if not ret:
#         break 

#     write_text("hello", frame, out)
    
# for i in range(5 * 30):
#     ret, frame = cap.read()
#     if not ret:
#         break 
#     write_text("fucking", frame, out)

# for i in range(5 * 30):
#     ret, frame = cap.read()
#     if not ret:
#         break 
#     write_text("world", frame, out)

cap.release()
out.release()

cv2.destroyAllWindows()
