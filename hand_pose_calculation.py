
import win32api
import win32con
import cv2
import mediapipe as mp
import time
import pydirectinput
import math

from mouse_inputs import right_click, index_finger_mouse_movement
from keyboard_inputs import inventory_toggle


tipIds = [4, 8, 12, 16, 20]
action_window = []

# Function to check if the hand is closed
def hand_pose(landmarks, handedness, image):

    if handedness == 'Left':

        lmList = []

        for id, lm in enumerate(landmarks):
            h, w, c = image.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            lmList.append([id, cx, cy])

        fingers = []
        if len(lmList)!=0:
            if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]: # thumb position of right left hand
                fingers.append(1)
            else:
                fingers.append(0)
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            total = fingers.count(1)

            # if-else instead of if-elif statement to make walking more responsive
            if total == 5:
                return 'opened'
            elif total == 0: # number of hands opened
                return 'closed'
            elif total == 2:
                return 'two'
            

    elif handedness == 'Right':

        lmList = []

        for id, lm in enumerate(landmarks):
            h, w, c = image.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            lmList.append([id, cx, cy])

        fingers = []
        if len(lmList)!=0:
            if lmList[tipIds[0]][1] < lmList[tipIds[0]-1][1]: # thumb position of right hand
                fingers.append(1)
            else:
                fingers.append(0)
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            total = fingers.count(1)

            if total == 0: # number of hands opened
                return 'closed'
            elif total == 5:
                return 'opened'


is_pressing_w = False
is_left_clicking = False     

def hand_control(results, mp_draw, image, mp_hand, last_right_click_time, last_inventory_open_time, inventory_open):

    global is_pressing_w
    global is_left_clicking


    h, w, c = image.shape
    
    if results.multi_hand_landmarks:

        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):

            # Draw the hand landmarks on the frame
            mp_draw.draw_landmarks(image, hand_landmarks, mp_hand.HAND_CONNECTIONS)

            # checking handedness
            hand_label = handedness.classification[0].label
            if hand_label == 'Left':
                if hand_pose(hand_landmarks.landmark, handedness=hand_label, image=image) == 'closed':
                    # status = 'LH_closed'
                    # print(status)
                    # action_window.append(status)

                    if is_pressing_w:
                        is_pressing_w = False
                        pydirectinput.keyUp('w')
                        print('releasing w (Stopped moving forward)')

                    # stop moving (do nothing)
                elif hand_pose(hand_landmarks.landmark, handedness=hand_label, image=image) == 'opened':
                    # status = 'LH_opened'
                    # print(status)
                    # action_window.append(status)

                    # start moving (press w and hold)
                    if is_pressing_w == False:
                        is_pressing_w = True
                        pydirectinput.keyDown('w')
                        print('pressing w (Moving forward)')

                # Inventory open mechanism (when you gesture 2)
                elif hand_pose(hand_landmarks.landmark, handedness=hand_label, image=image) == 'two':
                
                    # opening inventory if it's closed, and closing it if it's open (pressing e)
                    # cooldown period -> inventory toggle
                    inventory_open_cooldown_period = 1
                    current_time = time.time()
                    if (current_time - last_inventory_open_time > inventory_open_cooldown_period):
                        last_inventory_open_time = current_time
                        inventory_open = inventory_toggle(inventory_open)

                        # if inventory_open:

                        #     print('inventory opened')

                        #     # inventory_finger_control(hand_landmarksq)

                        #     # enable index finger controls (might be made into a module)
                        #     index_tip_x = hand_landmarks.landmark[8].x
                        #     index_tip_x = int(1280*index_tip_x) # have to multiply by 3 to make it match
                        #     index_tip_y = hand_landmarks.landmark[8].y
                        #     index_tip_y = int(1080*index_tip_y)


                        #     thumb_tip_x = hand_landmarks.landmark[4].x
                        #     thumb_tip_x = int(1280*thumb_tip_x) # have to multiply by 3 to make it match
                        #     thumb_tip_y = hand_landmarks.landmark[4].y
                        #     thumb_tip_y = int(1080*thumb_tip_y)
                        #     # print(index_tip_x, index_tip_y)

                        #     # use moveRel for this. (*)
                        #     index_finger_mouse_movement(index_tip_x, index_tip_y)


                        #     difference_vector = [index_tip_x - thumb_tip_x,
                        #                         index_tip_y - thumb_tip_y]
                        #     distance = math.sqrt(difference_vector[0]**2 + difference_vector[1]**2)
                        #     # print(distance)

                        #     if distance < 35:
                        #         # clicking left click and preventing multiple clicks fast
                        #         print('left click')
                        #         # clicking mechanism (index finger and thumb)


            elif hand_label == 'Right':

                if hand_pose(hand_landmarks.landmark, handedness=hand_label, image=image) == 'closed':
                    # status = 'RH_closed'
                    # print(status)
                    # action_window.append(status)
                    # left click and hold
                    if is_left_clicking == False:
                        is_left_clicking = True
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                        print('Holding left click')

                elif hand_pose(hand_landmarks.landmark, handedness=hand_label, image=image) == 'opened':

                    # status = 'RH_opened'
                    # print(status)

                    # toggle is_left_clicking to off if it's on 
                    if is_left_clicking:
                        is_left_clicking = False
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                        print('Releasing left click')
                        

                    # Right click mechanism (when index and thumb are touching)

                    # checking if the index and thumb are touching

                    index_tip_x = hand_landmarks.landmark[8].x
                    index_tip_x = int(1280*index_tip_x) # have to multiply by 3 to make it match

                    index_tip_y = hand_landmarks.landmark[8].y
                    index_tip_y = int(1080*index_tip_y)


                    thumb_tip_x = hand_landmarks.landmark[4].x
                    thumb_tip_x = int(1280*thumb_tip_x) # have to multiply by 3 to make it match

                    thumb_tip_y = hand_landmarks.landmark[4].y
                    thumb_tip_y = int(1080*thumb_tip_y)


                    difference_vector = [index_tip_x - thumb_tip_x,
                                        index_tip_y - thumb_tip_y]
                    distance = math.sqrt(difference_vector[0]**2 + difference_vector[1]**2)

                    
                    right_click_cooldown_period = 1
                    current_time = time.time()
                    if distance < 55:
                        if (current_time - last_right_click_time > right_click_cooldown_period):
                            last_right_click_time = current_time
                            # press right click once, start the timer for cooldown 
                            # print('right click')
                            right_click()



        if len(results.multi_hand_landmarks) == 1:
            # if only one hand is detected
            # if right hand is not shown (when only one hand is detected), release left click
            if hand_label != 'Right':
                if is_left_clicking:
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                    print('Releasing left click')
                    is_left_clicking = False
            # if left hand is not shown (when only one hand is detected), release w
            if hand_label != 'Left':
                if is_pressing_w:
                    pydirectinput.keyUp('w')
                    print('releasing w (Stopped moving forward)')
                    is_pressing_w = False

    # if no hands are detected, release the respective key presses
    else:
        if is_left_clicking:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
            print('Releasing left click')
            is_left_clicking = False
        if is_pressing_w:
            pydirectinput.keyUp('w')
            print('Releasing W (Stopped moving forward)')
            is_pressing_w = False

    return last_right_click_time, last_inventory_open_time, inventory_open


if __name__ == "__main__":

    # initialising time
    start_time = time.time()
    last_right_click_time = time.time()
    last_inventory_open_time = time.time()

    # initialising mp.solutions
    mp_draw = mp.solutions.drawing_utils
    mp_hand = mp.solutions.hands


    tipIds = [4, 8, 12, 16, 20]
            
    video = cv2.VideoCapture(0) # default cam

    # initialising booleans
    is_left_clicking = False
    is_pressing_w = False
    inventory_open = False


    with mp_hand.Hands(min_detection_confidence=0.5, 
                    min_tracking_confidence=0.5,
                    max_num_hands=2) as hands:
        while True:

            ret, image = video.read()
            # Use Flip code 1 to flip horizontally 
            image = cv2.flip(image, 1)

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            hands_results = hands.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # hand pose calculation and input
            last_right_click_time, last_inventory_open_time, inventory_open = hand_control(hands_results, mp_draw, image, mp_hand, 
                                                                           last_right_click_time, last_inventory_open_time, inventory_open)


            cv2.imshow('Frame', image)
            k = cv2.waitKey(1)
            if k == ord('q'):
                break

    video.release()
    cv2.destroyAllWindows()

