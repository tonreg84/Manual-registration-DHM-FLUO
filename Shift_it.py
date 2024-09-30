#GUI to manually align an image to a reference, gives the resulting x and y shift in pixels
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
from image_import import path_to_RGB
from POPUP_rescale import POPUP_rescale

def Shift_it(master, ref_RGB=None, image_RGB=None, scaling_factor=1):
    
    global shift_x_accum, shift_y_accum, image_shifted, ref_int, image_int, reference
    
    # Load reference and source images
    if master == None:
        reference_path = filedialog.askopenfilename(title="Select a reference file")
        reference = path_to_RGB(reference_path)
        image_path = filedialog.askopenfilename(title="Select an image file")
        image = path_to_RGB(image_path)
    else:
        reference = ref_RGB
        image = image_RGB
    
    
    # rescale source image?
    rescale_check, scaling_factor = POPUP_rescale(master, scaling_factor)
    print("Rescale source image?",rescale_check," ,  Scaling factor:", scaling_factor)
    
    if rescale_check:
        H_scaled = np.zeros((3, 3))

        H_scaled[0,0] = scaling_factor
        H_scaled[1,1] = scaling_factor
        H_scaled[2,2] = 1

        (image_height, image_width) = image.shape[:2]
        h_s = round(image_height*scaling_factor)
        w_s = round(image_width*scaling_factor)
        image = cv2.warpPerspective(image, H_scaled, (w_s, h_s))
    
    # Synchronize images sizes
    # Get the dimensions of the images
    ref_height, ref_width = reference.shape[:2]
    image_height, image_width = image.shape[:2]
    
    if ref_height > image_height:
        larger_image_height = ref_height
    else: larger_image_height = image_height
    
    if ref_width > image_width:
        larger_image_width = ref_width
    else: larger_image_width = image_width
    
    grey_value = 127  # Grey color intensity (0-255)
    larger_ref = np.full((larger_image_height, larger_image_width, 3), grey_value, dtype=np.uint8)
    larger_image = np.full((larger_image_height, larger_image_width, 3), grey_value, dtype=np.uint8)
    
    start_y = 0
    start_x = 0
    
    larger_ref[start_y:start_y+ref_height, start_x:start_x+ref_width] = reference
    larger_image[start_y:start_y+image_height, start_x:start_x+image_width] = image
    
    w = larger_image_width
    h = larger_image_height
    
    shift_x_accum = 0
    shift_y_accum = 0
    image_shifted = larger_image
    
    ref_int = 1
    image_int = 0.5
    
    #functions called by the buttons    
    def shift(string):
        
        global shift_x_accum, shift_y_accum, image_shifted
        
        shift = anentry.get()
        if shift.isdigit()==False:
            tk.messagebox.showinfo('Error', 'Pixel shift must be a positive integer!')
            anentry.delete(0,tk.END)
            anentry.insert(0,'')
        else:
        
            SHIFT = int(anentry.get())
            
            # initialize homography matrix
            H_shift = np.zeros((3, 3))
            H_shift[0,0] = 1
            H_shift[1,1] = 1
            H_shift[2,2] = 1
            
            # make homography matrix for shift
            if string == "left":
                shift_x_accum = shift_x_accum-SHIFT
            if string == "right":
                shift_x_accum = shift_x_accum+SHIFT
            if string == "top":
                shift_y_accum = shift_y_accum-SHIFT
            if string == "bot":
                shift_y_accum = shift_y_accum+SHIFT
                
            H_shift[0,2] = shift_x_accum
            H_shift[1,2] = shift_y_accum
            
            xlabel.config(text=str(shift_x_accum))
            ylabel.config(text=str(shift_y_accum))
            
            image_shifted = cv2.warpPerspective(larger_image, H_shift, (w, h))
            
            overlay = larger_ref.copy()
            output = image_shifted.copy()
            cv2.addWeighted(overlay, ref_int, output, image_int, 0, output)
            
            pil_image = Image.fromarray(output)
            # Convert the PIL Image to an ImageTk PhotoImage
            photo = ImageTk.PhotoImage(image=pil_image)
    
            # Update the image label
            image_label.config(image=photo)
            image_label.image = photo  # Keep a reference to the image to prevent it from being garbage collected
    
    
    def on_slider_release1(event):
        global ref_int
        ref_int = slider1.get()/100  # Get the current value of the slider
        print("Reference overlay intensity set to", slider1.get(), "%.")
        
        overlay = larger_ref.copy()
        output = image_shifted.copy()
        cv2.addWeighted(overlay, ref_int, output, image_int, 0, output)
        
        pil_image = Image.fromarray(output)
        # Convert the PIL Image to an ImageTk PhotoImage
        photo = ImageTk.PhotoImage(image=pil_image)
    
        # Update the image label
        image_label.config(image=photo)
        image_label.image = photo  # Keep a reference to the image to prevent it from being garbage collected
        
    def on_slider_release2(event):
        global image_int
        image_int = slider2.get()/100  # Get the current value of the slider
        print("Image overly intensity set to", slider2.get(), "%.")
        
        overlay = larger_ref.copy()
        output = image_shifted.copy()
        cv2.addWeighted(overlay, ref_int, output, image_int, 0, output)
        
        pil_image = Image.fromarray(output)
        # Convert the PIL Image to an ImageTk PhotoImage
        photo = ImageTk.PhotoImage(image=pil_image)
    
        # Update the image label
        image_label.config(image=photo)
        image_label.image = photo  # Keep a reference to the image to prevent it from being garbage collected
        
    
    def validate():
        
            # initialize homography matrix
            H_shift = np.zeros((3, 3))
            H_shift[0,0] = 1
            H_shift[1,1] = 1
            H_shift[2,2] = 1
            H_shift[0,2] = shift_x_accum
            H_shift[1,2] = shift_y_accum
        
            image_shifted_final = cv2.warpPerspective(larger_image, H_shift, (w, h))
            # path = os.path.dirname(image) + "/" + "image_shifted_final.png"
            cv2.imwrite("image_shifted_final.png",image_shifted_final)
            
            cv2.imwrite("larger_reference.png",larger_ref)
            
            overlay = larger_ref.copy()
            output = image_shifted_final.copy()
            cv2.addWeighted(overlay, ref_int, output, image_int, 0, output)
            cv2.imwrite("image_shifted_overlay.png",output)
            
            # crop image to reference dimensions 
            image_shifted_final_crop = image_shifted_final[0:ref_height,0:ref_width]
            image_shifted_final_crop = cv2.cvtColor(image_shifted_final_crop, cv2.COLOR_BGR2GRAY)
            reference_ = cv2.cvtColor(reference.astype(np.uint8), cv2.COLOR_BGR2GRAY)
            cv2.imwrite("image_reference.png",reference_)
            cv2.imwrite("image_shifted_final_crop.png",image_shifted_final_crop)
    
    
    #create GUI
    if master == None:
        window = tk.Tk()
    else:
        window = tk.Toplevel(master)
    window.title("Shift It")
    
    
    # GUI layout:
    left_frame = tk.LabelFrame(window, text="buttons")
    
    alabel = tk.Label(left_frame, text= "Shift by pixels:")
    anentry = tk.Entry(left_frame)
    #pixel shift default
    anentry.insert(0,"5")
    
    left_button = tk.Button(left_frame, text="left", width=25, height=1, command=lambda: shift("left"))
    right_button = tk.Button(left_frame, text="right", width=25, height=1, command=lambda: shift("right"))
    top_button = tk.Button(left_frame, text="top", width=25, height=1, command=lambda: shift("top"))
    bot_button = tk.Button(left_frame, text="bot", width=25, height=1, command=lambda: shift("bot"))
    
    shiftlabel = tk.Label(left_frame, text= "Accumulated x and y shift:")
    xlabel = tk.Label(left_frame, text= "0")
    ylabel = tk.Label(left_frame, text= "0")
    
    emptylabel2 = tk.Label(left_frame, text="   ")
    
    valbutton = tk.Button(left_frame, text="Save resulting images", width=25, height=1, command=lambda: validate())
    
    alabel.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    anentry.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
    left_button.grid(row=2, column=0, padx=5, pady=5, sticky="nw")
    right_button.grid(row=2, column=2, padx=5, pady=5, sticky="nw")
    top_button.grid(row=1, column=1, padx=5, pady=5, sticky="nw")
    bot_button.grid(row=3, column=1, padx=5, pady=5, sticky="nw")
    shiftlabel.grid(row=4, column=0, padx=5, pady=5, sticky="nw")
    xlabel.grid(row=4, column=1, padx=5, pady=5, sticky="nw")
    ylabel.grid(row=4, column=2, padx=5, pady=5, sticky="nw")
    emptylabel2.grid(row=5, column=0, padx=5, pady=5, sticky="nw")
    valbutton.grid(row=6, column=1, padx=5, pady=5, sticky="nw")
    
    emptylabel = tk.Label(left_frame, text="   ")
    emptylabel.grid(row=7, column=0, padx=5, pady=5, sticky="nw")
    
    olabel = tk.Label(left_frame, text="display options")
    olabel.grid(row=8, column=0, padx=5, pady=5, sticky="nw")
    
    slider1_label = tk.Label(left_frame, text="Reference intensity (%)")
    slider1_label.grid(row=9, column=0, padx=5, pady=5, sticky="nw")
    slider1 = tk.Scale(left_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=300)
    slider1.grid(row=9, column=1, padx=5, pady=5, sticky="nw")
    slider1.bind("<ButtonRelease-1>", on_slider_release1)
    slider1.set(100)
    
    slider2_label = tk.Label(left_frame, text="Image intensity (%)")
    slider2_label.grid(row=10, column=0, padx=5, pady=5, sticky="nw")
    slider2 = tk.Scale(left_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=300)
    slider2.grid(row=10, column=1, padx=5, pady=5, sticky="nw")
    slider2.bind("<ButtonRelease-1>", on_slider_release2)
    slider2.set(50)
    
    emptylabel2 = tk.Label(left_frame, text="   ")
    emptylabel2.grid(row=11, column=0, padx=5, pady=5, sticky="nw")
    
    exitbutt = tk.Button(left_frame, text="EXIT", width=25, height=1, command=lambda: window.destroy())
    exitbutt.grid(row=12, column=1, padx=5, pady=5, sticky="nw")
    
    display_frame = tk.LabelFrame(window, text="Overlay:")
    # Create a label for displaying the image
    default_image = Image.new("RGB", (w, h), "grey")  # Create a white square image
    default_photo = ImageTk.PhotoImage(default_image)
    image_label = tk.Label(display_frame, image=default_photo)
    image_label.grid(row=0, column=0, padx=5, pady=5, sticky="n,w")
    
    
    left_frame.grid(row=0, column=0, padx=5, pady=5, sticky='n,w')
    display_frame.grid(row=0, column=1, padx=5, pady=5, sticky='n,w')
    
    overlay = larger_ref.copy()
    output = larger_image.copy()
    cv2.addWeighted(overlay, 1, output, 0.5, 0, output)
    
    pil_image = Image.fromarray(output)
    # Convert the PIL Image to an ImageTk PhotoImage
    photo = ImageTk.PhotoImage(image=pil_image)
    
    # Update the image label
    image_label.config(image=photo)
    image_label.image = photo  # Keep a reference to the image to prevent it from being garbage collected
    
    if master == None:
        window.mainloop()
    else:
        master.wait_window(window)

    
    # output when GUI is closed:
    return shift_x_accum, shift_y_accum


# Create the window and run
if __name__ == "__main__":
    print("Final image shift (x,y):", Shift_it(master = None, ref_RGB=None, image_RGB=None))
    
    
