import cv2
import numpy as np
import os
import glob
import math

width, height = 1024, 1792
frame_rate = 30
wait_time = 4000
fade_time = 2000

fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = 'vertical_video.avi'
out = cv2.VideoWriter(output_file, fourcc, frame_rate, (width, height))

image_paths = glob.glob(os.path.join("images", '*'))

for i in range(len(image_paths) - 1):
    image1 = cv2.imread(image_paths[i])
    image2 = cv2.imread(image_paths[i+1])

    for _ in range(math.ceil(wait_time/1000*30)):
        vertical_video_frame = np.zeros((height, width, 3), dtype=np.uint8)
        vertical_video_frame[:image1.shape[0], :] = image1

        out.write(vertical_video_frame)

    for alpha in np.linspace(0, 1, math.ceil(fade_time/1000*30)):
        blended_image = cv2.addWeighted(image1, 1 - alpha, image2, alpha, 0)
        vertical_video_frame = np.zeros((height, width, 3), dtype=np.uint8)
        vertical_video_frame[:image1.shape[0], :] = blended_image

        out.write(vertical_video_frame)

image1 = cv2.imread(image_paths[i+1])
image2 = cv2.imread(image_paths[0])
for alpha in np.linspace(0, 1, math.ceil(fade_time/1000*30)):
    blended_image = cv2.addWeighted(image1, 1 - alpha, image2, alpha, 0)
    vertical_video_frame = np.zeros((height, width, 3), dtype=np.uint8)
    vertical_video_frame[:image1.shape[0], :] = blended_image

    out.write(vertical_video_frame)

out.release()
cv2.destroyAllWindows()

print(f"Video saved as {output_file}")