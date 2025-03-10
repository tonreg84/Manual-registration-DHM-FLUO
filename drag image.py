import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance

img2 = None

def open_secondary_gui():
    def load_images():
        nonlocal img1, img2, img1_tk, img2_tk
        # Load the first image
        file1 = filedialog.askopenfilename(title="Select the First Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if not file1:
            return

        file2 = filedialog.askopenfilename(title="Select the Second Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if not file2:
            return

        img1 = Image.open(file1).convert("RGBA")
        img2 = Image.open(file2).convert("RGBA")

        # Resize second image to fit within the bounds of the first image
        img2 = img2.resize((int(img1.width / 2), int(img1.height / 2)), Image.ANTIALIAS)

        # Make second image semi-transparent
        enhancer = ImageEnhance.Brightness(img2)
        img2 = enhancer.enhance(0.5)

        # Create ImageTk objects
        img1_tk = ImageTk.PhotoImage(img1)
        img2_tk = ImageTk.PhotoImage(img2)

        # Display the first image on the canvas
        canvas.create_image(0, 0, anchor=tk.NW, image=img1_tk)

        # Display the second image at the center of the first image
        reset_second_image_position()

    def reset_second_image_position():
        nonlocal second_image_id, x_offset, y_offset, img2_tk
        x_offset = (img1.width - img2.width) // 2
        y_offset = (img1.height - img2.height) // 2
        if second_image_id is not None:
            canvas.delete(second_image_id)
        second_image_id = canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=img2_tk)

    def start_drag(event):
        nonlocal drag_data
        drag_data["x"] = event.x
        drag_data["y"] = event.y

    def drag_image(event):
        nonlocal x_offset, y_offset, drag_data
        dx = event.x - drag_data["x"]
        dy = event.y - drag_data["y"]
        x_offset += dx
        y_offset += dy
        canvas.move(second_image_id, dx, dy)
        drag_data["x"] = event.x
        drag_data["y"] = event.y

    # Secondary GUI window
    secondary_window = tk.Toplevel(root)
    secondary_window.title("Image Superposition")

    # Variables to store images and offsets
    img1 = None
    img2 = None
    img1_tk = None
    img2_tk = None
    second_image_id = None
    x_offset = 0
    y_offset = 0

    # Data for dragging
    drag_data = {"x": 0, "y": 0}

    # Create a canvas to display images
    canvas = tk.Canvas(secondary_window, width=800, height=600, bg="white")
    canvas.pack(fill=tk.BOTH, expand=True)

    # Bind mouse events for dragging
    canvas.bind("<Button-1>", start_drag)
    canvas.bind("<B1-Motion>", drag_image)

    # Button to load images
    load_button = tk.Button(secondary_window, text="Load Images", command=load_images)
    load_button.pack()

# Main GUI window
root = tk.Tk()
root.title("Main GUI")

# Button to open the secondary GUI
open_button = tk.Button(root, text="Open Image Overlay GUI", command=open_secondary_gui)
open_button.pack(pady=20)

root.mainloop()
