Image Annotation tool for labeling image dataset.

It is written in Python and uses Tkinter for its graphical interface.

Annotations are saved as 'results.pkl' (in pickle format) in the specified folder.

## Installation
Program has been tested with Python 3.8 and PIL 7.2.0.
The GUI compatible with image file types - jpg, jfif, png.

In order to run this program, you can use virtual env:
```
$ git clone https://github.com/noy2121/Image-Annotation-Tool.git  # Cloning project repository
$ cd <Project Directory> # Enter to project directory
$ python3 -m venv my_venv # If not created, creating virtual env
$ source ./my_venv/bin/activate # Activating virtual env
(my_venv)$ pip3 install -r ./requirements.txt # Installing dependencies
(my_venv)$ python main.py # run the program
(my_venv)$ deactivate # When you want to leave virtual environment
```

## Usage
1. Build and launch using instruction above.
2. Click 'Browse' to choose folder with images to annotate.
3. Click 'Load images'. If you continue previous work the program automatically ask you if you want to load it and continue.
4. Start annotate.

## HotKeys
* 'right' - Go to the next image.
* 'left' - Go to the previous image.
* left mouse button press - Start drawing rectangle.
* mouse drag (while left button is pressed) - Change rectangle according to mouse coordinates.
* left mouse button release - End drawing rectangle, save the rectangle to the database.
* 'd' - Delete last specified rectangle in the current image (if no rectangles specified - do nothing).
* 's' - Save current data.
* 'q' - The program saves all the data and exits.
