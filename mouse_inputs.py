import win32api
import win32con
import time
import math
import pydirectinput


# Get screen width and height
screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

# Calculate the center position
center_x = screen_width // 2
center_y = screen_height // 2



def right_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)


def move_mouse(x, y):
    pydirectinput.moveTo(x, y, 0.2)


# mouse movement

import ctypes
import time

# Constants for mouse event
MOUSEEVENTF_MOVE = 0x0001

# Define ctypes structures for the mouse input
class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

def move_mouse_relative(x_offset, y_offset):
    # Get the current position of the cursor
    cursor = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
    
    # Calculate new position
    new_x = cursor.x + x_offset
    new_y = cursor.y + y_offset
    
    # Move the cursor to the new position
    ctypes.windll.user32.SetCursorPos(new_x, new_y)
    # Send the move event
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_MOVE, x_offset, y_offset, 0, 0)


# move mouse continuously to one direction after a threshold
def head_mouse_movement(x, y):

    if (x == 0) and (y == 0):
        move_mouse_relative(0, 0)

    else:
        vec_magnitude = math.sqrt(x**2 + y**2)
        norm_vec_x = x/(vec_magnitude)
        norm_vec_y = y/(vec_magnitude)
        sensitivity = 1.5

        if (3 > vec_magnitude):
            speed = (0)*sensitivity
            move_mouse_relative(math.floor(norm_vec_y*speed), -math.floor(norm_vec_x*speed))
        elif (vec_magnitude > 5) and (10 > vec_magnitude):
            speed = (2+((vec_magnitude-5)/3)**2)*sensitivity  # to smoothly change speed
            move_mouse_relative(math.floor(norm_vec_y*speed), -math.floor(norm_vec_x*speed))
        elif (vec_magnitude > 10) and (15 > vec_magnitude): # put a separate speed value here if you want to
            speed = (2+((vec_magnitude-5)/3)**2)*sensitivity
            move_mouse_relative(math.floor(norm_vec_y*speed), -math.floor(norm_vec_x*speed))
        elif (vec_magnitude > 15):
            speed = 13*sensitivity
            move_mouse_relative(math.floor(norm_vec_y*speed), -math.floor(norm_vec_x*speed))


def index_finger_mouse_movement(x, y):

    vec_magnitude = math.sqrt(x**2 + y**2)
    norm_vec_x = x/(vec_magnitude)
    norm_vec_y = y/(vec_magnitude)
    sensitivity = 2.5

    if (5 > vec_magnitude):
        speed = (0)*sensitivity
        move_mouse_relative(math.floor(norm_vec_y*speed), -math.floor(norm_vec_x*speed))
    elif (vec_magnitude > 5) and (10 > vec_magnitude):
        speed = (2+((vec_magnitude-5)/3)**2)*sensitivity  # to smoothly change speed
        move_mouse_relative(math.floor(norm_vec_y*speed), -math.floor(norm_vec_x*speed))
    elif (vec_magnitude > 10) and (15 > vec_magnitude): # put a separate speed value here if you want to
        speed = (2+((vec_magnitude-5)/3)**2)*sensitivity
        move_mouse_relative(math.floor(norm_vec_y*speed), -math.floor(norm_vec_x*speed))
    elif (vec_magnitude > 15):
        speed = 13*sensitivity
        move_mouse_relative(math.floor(norm_vec_y*speed), -math.floor(norm_vec_x*speed))
