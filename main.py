from tkinter import *
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import glob
import pickle
import os


def main():
    global label_dir
    global image_dir
    global browse_btn
    global load_images_btn
    global canvas
    global next_btn
    global back_btn
    global del_btn
    global save_btn
    global exit_btn

    root.title("Image Annotation Tool")
    root.geometry("800x550")

    # much buttons, such wow
    label_dir.config(text="Choose a directory:", width=20, anchor='w')
    image_dir.config(width=40)
    browse_btn.config(text="Browse", padx=10, command=browse)
    load_images_btn.config(text="Load images", padx=10, state=DISABLED)
    canvas.config(width=600, height=400)
    next_btn.config(text=">", width=20, state=DISABLED)
    back_btn.config(text="<", width=20, state=DISABLED)
    del_btn.config(text="Delete last annotation (D)", width=20, state=DISABLED)
    save_btn.config(
        text="Save current data (S)", width=20, state=DISABLED, command=save
    )
    exit_btn.config(
        text="Save all and exit (Q)", width=20, state=DISABLED, command=save_and_exit
    )

    # display them nicely
    label_dir.grid(row=0, column=0)
    image_dir.grid(row=1, column=0, columnspan=2)
    browse_btn.grid(row=1, column=2, sticky='w')
    load_images_btn.grid(row=2, column=0, padx=(0, 48))
    canvas.grid(row=3, column=0, columnspan=3, rowspan=5)
    del_btn.grid(row=3, column=3)
    save_btn.grid(row=4, column=3)
    exit_btn.grid(row=5, column=3)
    next_btn.grid(row=8, column=2)
    back_btn.grid(row=8, column=0)

    # mouse & keys commands
    canvas.bind("<Button-1>", click)
    canvas.bind("<B1-Motion>", drag)
    next_btn.bind_all("<Right>", lambda event: next_btn.invoke())
    back_btn.bind_all("<Left>", lambda event: back_btn.invoke())
    canvas.bind_all("<s>", save)
    save_btn.bind_all("<s>", lambda event: save_btn.invoke())
    del_btn.bind_all("<d>", lambda event: del_btn.invoke())
    exit_btn.bind_all("<q>", lambda event: exit_btn.invoke())

    # create infinite loop
    root.mainloop()


# browse directories
def browse():
    """
    Browse folders and choose one to start annotate.
    """
    image_dir.delete(0, END)
    directory = filedialog.askdirectory(title="Select A Folder")
    if not os.listdir(directory):
        messagebox.showwarning(message="Folder is empty")
    image_dir.insert(0, directory)
    load_images_btn.config(command=lambda: load_images(image_dir.get()), state=NORMAL)


# load images from file to a list
def load_images(directory):
    """
    Load images from folder, and display first image.
    Args:
        directory (string) -- directory of the folder
    """
    global results
    global image_list

    # reset variable each time we load new images
    image_list = []
    images = (
        glob.glob(directory + f"/*.jpg")
        + glob.glob(directory + f"/*.jfif")
        + glob.glob(directory + f"/*.png")
    )
    # iterate over the images, open them and create results dict
    for idx, filename in enumerate(images):
        image = Image.open(filename)
        results[f"image{idx}"] = []
        image.thumbnail((500, 500), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        image_list.append(image)
    # check for existing annotations
    if os.path.exists("results.pickle"):
        lines = [
            "Our special state-of-the-art mega-super-scanner",
            "has found existing annotations.",
            "Do you want to load them?",
        ]
        response = messagebox.askyesno("Text", "\n".join(lines))
        if response == 1:
            results = load_annotations()
    del_btn.config(state=NORMAL)
    save_btn.config(state=NORMAL)
    exit_btn.config(state=NORMAL)

    # check index of the last annotated image
    idx = last_annotated_image()
    # display images
    forward(idx)


def click(event):
    """
    Draw rectangle when click on the image
    Args:
        event -- Button-1 (left mouse button)
    """
    # the last rectangle becomes blue
    if len(rectangles) > 0:
        canvas.itemconfig(rectangles[-1], outline="blue")
    # define starting point
    bounds = canvas.bbox(image_canvas)
    if event.x < bounds[0]:
        event.x = bounds[0]
    elif event.x > bounds[2]:
        event.x = bounds[2]
    else:
        coords["x2"] = event.x
    if event.y < bounds[1]:
        event.y = bounds[1]
    elif event.y > bounds[3]:
        event.y = bounds[3]
    else:
        coords["y2"] = event.y
    coords["x1"] = event.x
    coords["y1"] = event.y

    rectangle = canvas.create_rectangle(
        coords["x1"],
        coords["y1"],
        coords["x1"],
        coords["y1"],
        outline="red",
        tags="rectangles",
    )
    # create a rectangle on this point and store it
    rectangles.append(rectangle)


def drag(event):
    """
    Continue drawing the rectangle when dragging the mouse on image
    Args:
        event -- B1-Motion
    """
    # update the coordinates as the mouse moves
    # restrict cursor to image area
    bounds = canvas.bbox(image_canvas)
    if event.x < bounds[0]:
        event.x = bounds[0]
    elif event.x > bounds[2]:
        event.x = bounds[2]
    else:
        coords["x2"] = event.x
    if event.y < bounds[1]:
        event.y = bounds[1]
    elif event.y > bounds[3]:
        event.y = bounds[3]
    else:
        coords["y2"] = event.y
    # change the coordinates of the rectangle while drawing it
    canvas.coords(
        rectangles[-1], coords["x1"], coords["y1"], coords["x2"], coords["y2"]
    )


def release(event, idx):
    """
    Finish rectangle when releasing button-1
    Args:
        event -- release-Button-1 (left mouse button released)
        idx (int) -- index of the image for saving data
    """
    # update the coordinates of the final rectangle
    # restrict cursor to image area
    bounds = canvas.bbox(image_canvas)
    if event.x < bounds[0]:
        event.x = bounds[0]
    elif event.x > bounds[2]:
        event.x = bounds[2]
    else:
        coords["x2"] = event.x
    if event.y < bounds[1]:
        event.y = bounds[1]
    elif event.y > bounds[3]:
        event.y = bounds[3]
    else:
        coords["y2"] = event.y
    # change the coordinates of the rectangle to the final ones
    canvas.coords(
        rectangles[-1], coords["x1"], coords["y1"], coords["x2"], coords["y2"]
    )

    w = abs(coords["x2"] - coords["x1"])
    h = abs(coords["y2"] - coords["y1"])
    # adding current rectangle to results
    results[f"image{idx}"].append([coords["x1"], coords["y1"], w, h])


def delete_last_rectangle(idx):
    """
    Delete last rectangle from image
    Args:
        idx (int) -- image index
    """
    canvas.delete(rectangles[-1])
    del rectangles[-1]
    del results[f"image{idx}"][-1]


def save():
    """
    Save current data.
    """
    with open("results.pickle", "wb") as handle:
        pickle.dump(results, handle, protocol=pickle.HIGHEST_PROTOCOL)
    messagebox.showinfo(message="Annotations have been saved successfully!")


def save_and_exit():
    """
    Save current data and exit program.
    """
    save()
    messagebox.showinfo(message="Goodbye")
    root.quit()
    print("It works!")


def clear_canvas():
    """
    Clear annotations from new image.
    """
    canvas.itemconfig("rectangles", state="hidden")


def load_annotations():
    """
    Load previous annotations
    """
    with open("results.pickle", "rb") as handle:
        prv_annotations = pickle.load(handle)
    return prv_annotations


def draw_previous_annotations(idx):
    """
    Draw previous annotations on current image.
    Args:
        idx (int) -- index of the current image
    """
    annotations = results[f"image{idx}"]
    for annotation in annotations:
        x1 = annotation[0]
        y1 = annotation[1]
        x2 = annotation[0] + annotation[2]
        y2 = annotation[1] + annotation[3]
        canvas.create_rectangle(x1, y1, x2, y2, outline="blue", tags="rectangles")


def last_annotated_image():
    """
    Check which image annotated last.
    Return:
        idx (int) -- index of the last annotated image.
    """
    idx = 0
    for i, value in reversed(list(enumerate(results.values()))):
        if len(value) != 0:
            idx = i
            break
    return idx


def forward(idx):
    """
    Display the next image
    Args:
        idx (int) -- index of the next image
    """
    canvas.itemconfig(image_canvas, image=image_list[idx])

    # clear previous image's annotations
    clear_canvas()

    # load previous annotations if exist
    draw_previous_annotations(idx)

    if idx == len(image_list) - 1:
        next_btn.config(state=DISABLED)
    else:
        next_btn.config(state=NORMAL, command=lambda: forward(idx + 1))
    if idx == 0:
        back_btn.config(state=DISABLED)
    else:
        back_btn.config(command=lambda: back(idx - 1), state=NORMAL)
    del_btn.config(command=lambda: delete_last_rectangle(idx))
    canvas.bind("<ButtonRelease-1>", lambda event, arg=idx: release(event, arg))


def back(idx):
    """
    Display the previous image
    Args:
        idx (int) -- index of the previous image
    """
    canvas.itemconfig(image_canvas, image=image_list[idx])

    # clear previous image's annotations
    clear_canvas()

    # load previous annotations if exist
    draw_previous_annotations(idx)

    if idx == 0:
        back_btn.config(state=DISABLED)
    else:
        back_btn.config(command=lambda: back(idx - 1))
    next_btn.config(command=lambda: forward(idx + 1), state=NORMAL)
    del_btn.config(command=lambda: delete_last_rectangle(idx))
    canvas.bind("<ButtonRelease-1>", lambda event, arg=idx: release(event, arg))


# initialize root widget
root = Tk()

# much buttons, such wow
label_dir = Label(root)
image_dir = Entry(root)
browse_btn = Button(root)
load_images_btn = Button(root)
canvas = Canvas(root)
image_canvas = canvas.create_image(300, 200)
next_btn = Button(root)
back_btn = Button(root)
del_btn = Button(root)
save_btn = Button(root)
exit_btn = Button(root)

image_list = []
# top left point, and bottom right point of the current rectangle
coords = {"x1": 0, "y1": 0, "x2": 0, "y2": 0}
# list of the rectangles in each image
rectangles = []
# dictionary with all the data
results = {}

if __name__ == "__main__":
    main()
