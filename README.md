Image Annotation tool for labeling image dataset.

It is written in Python and uses Tkinter for its graphical interface.

Annotations are saved as 'results.pkl' (in pickle format) in the specified folder.

## Installation
Program has been tested with Python 3.8 and PIL 7.2.0.
The GUI compatible with image file type - jpg, jfif, png.
```
pip install Pillow
```
After installation all you need to do is run main.py


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

