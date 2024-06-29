# Minecraft Gesture Control

This code uses computer vision to allow you to play Minecraft using the pose of your head and hand gestures.

### How to use
- The pose of your head controls the mouse (eg: Looking right in real life makes the character in minecraft also look right).
- Closing your right hand holds the left click button (to break blocks and hit things)
- Touching your index and thumb of your right hand clicks the right click button (to place blocks)
- Opening your left hand presses w (to move forward)
- lifting two fingers on your left hand (✌) presses e (opens the inventory)


# Minecraft Gesture Control

This project leverages computer vision to allow you to control Minecraft using the pose of your head and hand gestures.

## Features

- **Head Pose Control:** Look around in real life to control the in-game camera.
- **Left Click:** Close your right hand to hold the left click button (for breaking blocks and hitting).
- **Right Click:** Touch your right hand's index finger and thumb to right-click (for placing blocks).
- **Move Forward:** Open your left hand to press 'W' (to move forward).
- **Inventory:** Lift two fingers on your left hand (✌) to press 'E' (to open the inventory).

## Installation

1. **Clone the Repository:**
    ```sh
    git clone https://github.com/yourusername/Minecraft_Gesture_Control.git
    cd Minecraft_Gesture_Control
    ```

2. **Install the Required Packages:**
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Main Script:**
    ```sh
    python main.py
    ```

2. **Start Minecraft and Enjoy Playing with Gesture Controls!**


## Acknowledgements

This project uses the following libraries:
- [OpenCV](https://opencv.org/)
- [MediaPipe](https://mediapipe.dev/)
- [PyDirectInput](https://pydirectinput.readthedocs.io/)


Enjoy a new way of playing Minecraft!
