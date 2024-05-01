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

    text = "this is a sample text"
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (255, 255, 255)
    thickness = 2
    org = (50, 50)
    frame = cv2.putText(frame, text, org, font, 1, color, thickness, cv2.LINE_AA)

    out.write(frame)

cap.release()
out.release()

cv2.destroyAllWindows()
