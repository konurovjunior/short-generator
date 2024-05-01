import cv2
import json
from pydub import AudioSegment
import os
import math
import subprocess

offset = 50

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

def add_narration_to_video(input_video, output_video):
    cap = cv2.VideoCapture(input_video)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    temp_video = "with_transcript.avi"
    out = cv2.VideoWriter(temp_video, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

    full_narration  = AudioSegment.empty()
    narrations = get_narrations()

    for i, narration in enumerate(narrations):
        audio = os.path.join("narrations", f"narration_{i+1}.mp3")
        duration = get_audio_duration(audio)
        narration_frames = math.floor(duration / 1000 * 30)

        full_narration += AudioSegment.from_file(audio)

        char_count = len(narration["content"].replace(" ", ""))
        ms_per_char = duration / char_count

        frames_written = 0
        words = narration["content"].split(" ")

        for w, word in enumerate(words):
            word_ms = len(word) * ms_per_char

            if i == 0 & w == 0:
                word_ms -= offset
                if word_ms < 0:
                    word_ms = 0

            for _ in range(math.floor(word_ms/1000*30)):
                ret, frame = cap.read()
                if not ret:
                    break 
                write_text(word, frame, out)
                frames_written += 1

        for _ in range(narration_frames - frames_written):
            out.write(frame)

    temp_narration = "narration.mp3"
    full_narration.export(temp_narration, format="mp3")

    cap.release()
    out.release()

    cv2.destroyAllWindows()

    ffmpeg_command = ['ffmpeg',
        '-y', 
        '-i', temp_video,
        '-i', temp_narration,
        '-map', '0:v',
        '-map', '1:a',
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', 'experimental',
        '-shortest',
        output_video
    ]

    subprocess.run(ffmpeg_command, capture_output=True)

    os.remove(temp_video)
    os.remove(temp_narration)