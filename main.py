
import cv2
import mediapipe as mp
import time

from mouse_inputs import head_mouse_movement
from hand_pose_calculation import hand_control
from head_pose_calculation import head_control, head_control_mouse_coords

# initalising time
start_time = time.time()
last_head_capture_time = time.time()
last_right_click_time = time.time()
last_inventory_open_time = time.time()

# initialising mp.solutions
mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands
mp_head = mp.solutions.face_mesh

face_mesh = mp_head.FaceMesh(min_detection_confidence=0.5,min_tracking_confidence=0.5)

drawing_spec = mp_draw.DrawingSpec(color=(128,0,128),thickness=2,circle_radius=1)



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
        image = cv2.flip(image, 1) # Use Flip code 1 to flip horizontally 
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        hands_results = hands.process(image)
        head_results = face_mesh.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # # hand pose calculation and input
        # hand_control(hands_results, mp_draw, image, mp_hand)

        # hand pose calculation and input
        last_right_click_time, last_inventory_open_time, inventory_open = hand_control(hands_results, mp_draw, image, mp_hand, 
                                                                        last_right_click_time, last_inventory_open_time, inventory_open)


        # head control (capturing head at a regular interval to boost fps)

        # less cooldown = less latency but less fps
        cooldown_period = 0.1

        # Get the current time
        current_time = time.time()

        if (current_time - last_head_capture_time > cooldown_period):
            # Update the last time image was used
            last_head_capture_time = current_time
            # Capture a new image to use
            last_head_capture_frame = image
            # return mouse input for this frame to be repeated
            mouse_x, mouse_y = head_control_mouse_coords(head_results, mp_draw, last_head_capture_frame, mp_head, drawing_spec, start_time)


        head_mouse_movement(mouse_x, mouse_y)

        # # head pose calculation and input
        # head_control(head_results, mp_draw, last_head_capture_frame, mp_head, drawing_spec, start_time)


        cv2.imshow('Frame', image)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break

video.release()
cv2.destroyAllWindows()

