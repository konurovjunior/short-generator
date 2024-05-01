import cv2
import numpy as np
import os
import glob
import math
import subprocess
import shlex
import ffmpeg
from pydub import AudioSegment

def get_audio_duration(audio_file):
    audio = AudioSegment.from_file(audio_file)
    duration_in_ms = len(audio)
    return duration_in_ms

width, height = 1024, 1792
frame_rate = 30
wait_time = 2000
fade_time = 1000

fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = 'vertical_video.avi'
out = cv2.VideoWriter(output_file, fourcc, frame_rate, (width, height))

image_paths = glob.glob(os.path.join("images", '*'))
image_paths = sorted(image_paths)
full_narration  = AudioSegment.empty()

for i, image in enumerate(image_paths):
    image1 = cv2.imread(image_paths[i])
    if i < len(image_paths) - 1:
        image2 = cv2.imread(image_paths[i+1])
    else:
        image2 = cv2.imread(image_paths[0])

    narration = os.path.join("narrations", f"narration_{i+1}.mp3")
    duration = get_audio_duration(narration)

    if i > 0:
        duration -= fade_time

    if i == len(image_paths) - 1:
        duration -= fade_time

    full_narration += AudioSegment.from_file(narration)

    for _ in range(math.ceil(duration/1000*30)):
        vertical_video_frame = np.zeros((height, width, 3), dtype=np.uint8)
        vertical_video_frame[:image1.shape[0], :] = image1

        out.write(vertical_video_frame)

    for alpha in np.linspace(0, 1, math.ceil(fade_time/1000*30)):
        blended_image = cv2.addWeighted(image1, 1 - alpha, image2, alpha, 0)
        vertical_video_frame = np.zeros((height, width, 3), dtype=np.uint8)
        vertical_video_frame[:image1.shape[0], :] = blended_image

        out.write(vertical_video_frame)

out.release()
cv2.destroyAllWindows()

full_narration.export("narration.mp3", format="mp3")

final_video = "final_video.avi"

ffmpeg_command = ['ffmpeg',
    '-y',
    '-i', output_file,
    '-i', 'narration.mp3',
    '-map', '0:v',
    '-map', '1:a',
    '-c:v', 'copy',
    '-c:a', 'aac',
    '-strict', 'experimental',
    '-shortest',
    final_video
]

subprocess.run(ffmpeg_command, capture_output=True)

os.remove(output_file)
#os.remove("narration.mp3")

print(f"Video saved as {output_file}")