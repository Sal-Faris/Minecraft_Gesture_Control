
import pydirectinput
import time

def inventory_toggle(inventory_open):
    if inventory_open == False:
        pydirectinput.keyDown('e')
        pydirectinput.keyUp('e')
        inventory_open = True
    else:
        pydirectinput.keyDown('e')
        pydirectinput.keyUp('e')
        inventory_open = False

    return inventory_open

