import cv2
import time
import mediapipe as mp
from google.protobuf.json_format import MessageToDict
import pyautogui as pag

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      model_complexity=1,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5,
                      max_num_hands=2)
mpDraw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
prev_x = None
prev_y = None
scrolling_threshold = 0.09
vertical_threshold = 0.05
start_x = None
n = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for i in results.multi_handedness:
            label = MessageToDict(i)['classification'][0]['label']

            if label == 'Left':
                for hand_landmarks in results.multi_hand_landmarks:
                    mpDraw.draw_landmarks(img, hand_landmarks, mpHands.HAND_CONNECTIONS)
                cv2.putText(img, label + ' Hand', (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

                movement_detected = False
                if results.multi_hand_landmarks:
                    hand_landmarks = results.multi_hand_landmarks[0]
                    center_landmark = hand_landmarks.landmark[9]
                    current_x = center_landmark.x
                    current_y = center_landmark.y

                    if prev_x is not None and prev_y is not None:
                        if (current_x - prev_x) > scrolling_threshold and abs(current_y - prev_y) < vertical_threshold:
                            print("Left to right movement detected L:", n)
                            n += 1
                            movement_detected = True
                            pag.press('left')
                        elif (prev_x - current_x) > scrolling_threshold and abs(current_y - prev_y) < vertical_threshold:
                            print("Right to left movement detected L:", n)
                            n += 1
                            movement_detected = True
                            pag.press('right')

                    prev_x = current_x
                    prev_y = current_y

            if label == 'Right':
                for hand_landmarks in results.multi_hand_landmarks:
                    mpDraw.draw_landmarks(img, hand_landmarks, mpHands.HAND_CONNECTIONS)
                cv2.putText(img, label + ' Hand', (460, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

                movement_detected = False
                if results.multi_hand_landmarks:
                    hand_landmarks = results.multi_hand_landmarks[0]
                    center_landmark = hand_landmarks.landmark[9]
                    current_x = center_landmark.x
                    current_y = center_landmark.y

                    if prev_x is not None and prev_y is not None:
                        if (current_x - prev_x) > scrolling_threshold and abs(current_y - prev_y) < vertical_threshold:
                            print("Left to right movement detected R:", n)
                            n += 1
                            movement_detected = True
                            pag.press('left')
                        elif (prev_x - current_x) > scrolling_threshold and abs(current_y - prev_y) < vertical_threshold:
                            print("Right to left movement detected L:", n)
                            n += 1
                            movement_detected = True
                            pag.press('right')

                        prev_x = current_x
                        prev_y = current_y
    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
