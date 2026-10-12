import cv2 as cv
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os

model_path = '/home/kuna.ibad/Documents/Project_Python/IFLS Welcome Message/hand_landmarker.task'

if not os.path.exists(model_path):
    raise FileNotFoundError(f"Cannot find '{model_path}'. Run the wget download command first.")

base_option = python.BaseOptions(
    model_asset_path = '/home/kuna.ibad/Documents/Project_Python/IFLS Welcome Message/hand_landmarker.task'
)

options = vision.HandLandmarkerOptions(
    base_options = base_option,
    running_mode = vision.RunningMode.IMAGE,
    num_hands=2
)

hand_landmarker = vision.HandLandmarker.create_from_options(options)

cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))

def draw_hand_landmark(frame, landmarks, h, w):
    prev_landmark = None
    cur_landmark = None
    for landmark in landmarks :
        cur_landmark = landmark
        # if prev_landmark is not None :
        #      cv.line(frame, 
        #              (int(prev_landmark.x*w), int(prev_landmark.y*h)),
        #              (int(cur_landmark.x*w), int(cur_landmark.y*h)),
        #              (0,0,255),
        #              3 
        #              )
        pos = (int(landmark.x * w), int(landmark.y *h))
        cv.circle(frame, pos, 3, (0, 255, 0), -1)
        prev_landmark = landmark

    

while cap.isOpened():
    ret, frame = cap.read()
    if not ret :
        break

    frame = cv.flip(frame, 1)

    h, w, _ = frame.shape
    rgb_img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_img)

    result = hand_landmarker.detect(mp_image)

    if result.hand_landmarks :
         for hand in result.hand_landmarks:
            draw_hand_landmark(frame, hand, h=h, w=w)
    

    cv.imshow('Percobaan', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
            break

