import cv2
import mediapipe as mp
import pyautogui as pag

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

prev_x = None
prev_y = None
scrolling_threshold = 0.09
vertical_threshold = 0.05
start_x = None
n = 0

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    two_fingers_raised = False

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Initially set finger count to 0 for each hand
        fingerCount = 0

        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:
                # Get hand index to check label (left or right)
                handIndex = results.multi_hand_landmarks.index(hand_landmarks)
                handLabel = results.multi_handedness[handIndex].classification[0].label

                # Set variable to keep landmarks positions (x and y)
                handLandmarks = []

                # Fill list with x and y positions of each landmark
                for landmarks in hand_landmarks.landmark:
                    handLandmarks.append([landmarks.x, landmarks.y])

                # Test conditions for each finger: Count is increased if finger is
                #   considered raised.
                # Thumb: TIP x position must be greater or lower than IP x position,
                #   depending on hand label.
                if handLabel == "Left" and handLandmarks[4][0] > handLandmarks[3][0]:
                    fingerCount += 1
                elif handLabel == "Right" and handLandmarks[4][0] < handLandmarks[3][0]:
                    fingerCount += 1

                # Other fingers: TIP y position must be lower than PIP y position,
                #   as image origin is in the upper left corner.
                if handLandmarks[8][1] < handLandmarks[6][1]:  # Index finger
                    fingerCount += 1
                if handLandmarks[12][1] < handLandmarks[10][1]:  # Middle finger
                    fingerCount += 1
                if handLandmarks[16][1] < handLandmarks[14][1]:  # Ring finger
                    fingerCount += 1
                if handLandmarks[20][1] < handLandmarks[18][1]:  # Pinky
                    fingerCount += 1

                # Draw hand landmarks
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS)

                # Check if two fingers are raised
                if fingerCount == 2:
                    two_fingers_raised = True
                else:
                    two_fingers_raised = False

        # Perform scrolling action only when two fingers are raised
        if two_fingers_raised and handLabel == "Left":
            movement_detected = False
            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                center_landmark = hand_landmarks.landmark[12]
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

        if two_fingers_raised and handLabel == "Right":
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

        # Display finger count
        cv2.putText(image, str(fingerCount), (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 10)

        # Display image
        cv2.imshow('Image', image)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

