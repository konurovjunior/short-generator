import cv2
import numpy as np
import os

width, height = 1080, 1920
frame_rate = 30

fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = 'vertical_video.avi'
out = cv2.vVdeoWriter(output_file, fourcc, frame_rate, (width, height))

image_paths = os.listdir("images")

for i, image in enumerate(image_paths):
    image1 = cv2.imread(os.path.join("images", image))
    image2 = cv2.imread(os.path.join("images", image_paths[i + 1]))

    for alpha in np.linspace(0, 1, frame_rate):
        blended_image = cv2.addWeighted(image1, 1 - alpha, image2, alpha, 0)
        vertical_video_frame = np.zeros((height, width, 3), dtype=np.unit8)
        vertical_video_frame[:image1.shape[0], :] = blended_image

        out.write(vertical_video_frame)

out.release()
cv2.destroyAllWindows()

print(f"Video saved as {output_file}")