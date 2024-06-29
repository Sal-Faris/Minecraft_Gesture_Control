
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

2. **Start Minecraft and play with Gesture Controls**


## To-Do

- [ ] Ability to scroll through the hotbar
- [ ] Prevent accidental inventory openings by requiring the two-finger sign for some time
- [ ] Ability to jump
- [ ] Require lifting only the index and middle fingers to open the inventory rather than lifting any two fingers

## Contributing

If you have any ideas for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


## Acknowledgements

This project uses the following libraries:
- [OpenCV](https://opencv.org/)
- [MediaPipe](https://mediapipe.dev/)
- [PyDirectInput](https://pydirectinput.readthedocs.io/)


Enjoy a new way of playing Minecraft!
