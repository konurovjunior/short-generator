import cv2

input_video = "final_video.avi"
cap = cv2.VideoCapture(input_video)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_video = "with_transcript.avi"
out = cv2.VideoWriter(output_video, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    height, width, _ = frame.shape

    text = "this is a sample text"
    font = cv2.FONT_HERSHEY_SIMPLEX
    white_color = (255, 255, 255)
    black_color = (0, 0, 0)
    thickness = 10
    font_scale = 3
    stroke = 3

    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x = (frame.shape[1] - text_size[0]) // 2
    text_y = (frame.shape[0] + text_size[1]) // 2
    org = (text_x, text_y)

    frame = cv2.putText(frame, text, org, font, font_scale, black_color, thickness + stroke, cv2.LINE_AA)
    frame = cv2.putText(frame, text, org, font, font_scale, white_color, thickness, cv2.LINE_AA)

    out.write(frame)

cap.release()
out.release()

cv2.destroyAllWindows()
