#rescales an image

import numpy as np
import cv2
from tkinter import filedialog,simpledialog
import tkinter as tk
import sys

image_path = filedialog.askopenfilename(title="Select an image file")
image = cv2.imread(image_path)


def ask_factor():
    # Create the root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    # Ask user for scaling factor
    while True:
        try:
            user_input = simpledialog.askstring("Input", "Please enter the scaling factor:")
            if user_input is None:  # User pressed cancel
                return None
            user_float = float(user_input)
            return user_float
        except ValueError:
            # If the input is not a valid float, show an error message
            tk.messagebox.showerror("Invalid input", "Please enter a valid float number.")

rescaling_factor = ask_factor()
if rescaling_factor is not None:
    print(f"The entered scaling factor is: {rescaling_factor}")
else:
    print("No number was entered.")
    sys.exit()

H_scaled = np.zeros((3, 3))

H_scaled[0,0] = rescaling_factor
H_scaled[1,1] = rescaling_factor
H_scaled[2,2] = 1

(h, w) = image.shape[:2]

h_s = round(h*rescaling_factor)
w_s = round(w*rescaling_factor)

image_scaled = cv2.warpPerspective(image, H_scaled, (w_s, h_s))
cv2.imwrite("image_scaled.png",image_scaled)