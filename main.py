import cv2
import time 
import datetime

vid = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody_default.xml")

recording = False
detection_stopped = None
timer_start = False
record_time = 10

frame_size = (int(vid.get(3)), int(vid.get(4)))
fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")


while True:
    _, frame = vid.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    bodies = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) + len(bodies) > 0:
        if recording:
            timer_start = False
        else:
            recording = True 
            current_time = datetime.datetime.now().strftime("%d-%m-%H-%M-%S")
            output = cv2.VideoWriter(f"SecurityVideo_{current_time}.mp4", fourcc, 24, frame_size)
    elif recording:
        if timer_start:
            if time.time() - detection_stopped >= record_time:
                recording = False 
                timer_start = False
                output.release 
        else:
            timer_start = True
            detection_stopped = time.time()

    if recording:
        output.write(frame)

      #  for (x, y, width, height) in faces:
        #    cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 3)


    cv2.imshow("Security Camera", frame)

    if cv2.waitKey(1) == ord('p'):
        break 

    else:

        print("empty")
        break

output.release()
vid.release()
cv2.destroyAllWindows()


