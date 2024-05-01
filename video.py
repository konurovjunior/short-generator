import cv2
import numpy as np
import os
import glob
import math
import text
from pydub import AudioSegment

def get_audio_duration(audio_file):
    audio = AudioSegment.from_file(audio_file)
    duration_in_ms = len(audio)
    return duration_in_ms

def resize_image(image, width, height):
    aspect_ratio = image.shape[1] / image.shape[0]
    if aspect_ratio > (width / height):
        new_width = width
        new_height = int(width / aspect_ratio)
    else:
        new_height = height
        new_width = int(height * aspect_ratio)
    return cv2.resize(image, (new_width, new_height))

def create(output_video):
    width, height = 1080, 1920
    frame_rate = 30
    wait_time = 2000
    fade_time = 1000

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    temp_video = 'vertical_video.avi'
    out = cv2.VideoWriter(temp_video, fourcc, frame_rate, (width, height))

    image_paths = glob.glob(os.path.join("images", '*'))
    image_paths = sorted(image_paths)

    for i, image in enumerate(image_paths):
        image1 = cv2.imread(image_paths[i])
        if i < len(image_paths) - 1:
            image2 = cv2.imread(image_paths[i+1])
        else:
            image2 = cv2.imread(image_paths[0])

        image1 = resize_image(image1, 1080, 1920)
        image2 = resize_image(image2, 1080, 1920)

        narration = os.path.join("narrations", f"narration_{i+1}.mp3")
        duration = get_audio_duration(narration)

        if i > 0:
            duration -= fade_time

        if i == len(image_paths) - 1:
            duration -= fade_time

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

    text.add_narration_to_video(temp_video, output_video)

    os.remove(temp_video)