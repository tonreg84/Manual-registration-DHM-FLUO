#GUI to manually align an image to a reference, gives the resulting x and y shift in pixels
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance
from Image_import import path_to_RGB
import numpy as np
import cv2

current_rectangle = None

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
            return False


def Rough(master=None, ref_path=None, image_path=None, scaling_factor=75):
    
    # Load reference and source images
    if master == None:
        ref_path = filedialog.askopenfilename(title="Select a reference file")
        # reference, ref_height, ref_width = path_to_RGB(reference_path)
        image_path = filedialog.askopenfilename(title="Select an image file")
        # image, image_height, image_width = path_to_RGB(image_path)    
    reference, ref_height, ref_width = path_to_RGB(ref_path)
    image, image_height, image_width = path_to_RGB(image_path)
    # Convert the RGB images to uint8
    RGB_ref_uint8 = reference.astype(np.uint8)
    RGB_image_uint8 = image.astype(np.uint8)
    # Convert to PIL Image
    reference = Image.fromarray(RGB_ref_uint8)
    image = Image.fromarray(RGB_image_uint8)


    # image treatment:
        
    # Resize images to fit screen
    reference = reference.resize((int(ref_width*scaling_factor/100), int(ref_height*scaling_factor/100)),Image.LANCZOS)
    image_width = int(image_width*scaling_factor/100)
    image_height = int(image_height*scaling_factor/100)
    image = image.resize((image_width, image_height),Image.LANCZOS)

    # Enhance contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)  # Increase contrast by a factor (e.g., 2.0)
    
    # make the image semi-transparent
    alpha = int(0.5 * 255)
    a = Image.new("L", image.size, alpha)  # Create a new alpha channel
    r, g, b = image.split()
    # a = a.point(lambda p: alpha)
    image = Image.merge("RGBA", (r, g, b, a))
    
    # Variables to store source image, offset, and scaling
    canv_image_id = None
    x_offset = 0
    y_offset = 0
    source_scaling = 1
    
    # Variables to store starting point and rectangle ID
    start_x = None
    start_y = None

    drawing_mode = False  # Controls whether drawing is active
    x1 = 0
    y1 = 0
    x2 = ref_width
    y2 = ref_height
    

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
        canvas.move(canv_image_id, dx, dy)
        drag_data["x"] = event.x
        drag_data["y"] = event.y
        
    def start_draw(event):
        """Start drawing the rectangle (only if drawing mode is active)."""
        nonlocal drawing_mode, start_x, start_y
        global current_rectangle
        
        if current_rectangle:
            canvas.delete(current_rectangle)
            current_rectangle = None  # Clear reference
        
        if drawing_mode:
            start_x = event.x
            start_y = event.y
            current_rectangle = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline="blue", width=2)
            
    def draw_rectangle(event):
        """Update the rectangle as the mouse is dragged (only if drawing mode is active)."""
        nonlocal drawing_mode, start_x, start_y
        global current_rectangle
        if drawing_mode and current_rectangle:
            # Update the rectangle dimensions
           canvas.coords(current_rectangle, start_x, start_y, event.x, event.y)
           
    def end_draw(event):
        """Finalize the rectangle, display its details, and disable drawing mode."""
        nonlocal drawing_mode, start_x, start_y, x1,y1,x2,y2
        global current_rectangle
        if drawing_mode:
            end_x, end_y = event.x, event.y

            # Calculate position, width, and height
            x1, y1 = start_x, start_y
            x2, y2 = end_x, end_y
            x1, x2 = sorted((x1, x2))
            y1, y2 = sorted((y1, y2))

            x1 = int(x1 /scaling_factor*100)
            y1 = int(y1 /scaling_factor*100)
            x2 = int(x2 /scaling_factor*100)
            y2 = int(y2 /scaling_factor*100)
            print(x1,y1,x2,y2)

            # Reset for the next rectangle and disable drawing mode
            start_x = None
            start_y = None
            
            # drawing_mode = False
            
            # # Bind mouse events again for image dragging
            # canvas.tag_bind(canv_image_id,"<Button-1>", start_drag)
            # canvas.tag_bind(canv_image_id,"<B1-Motion>", drag_image)
    
    def activate_drawing():
        """First disable dragging of source image, the enable ROI drawing mode."""
        nonlocal drawing_mode
        global current_rectangle
        
        if drawing_mode:
            drawing_mode = False
            
            activate_button.config(text="Activate Drawing Mode\nto crop the reference image")
            
            canvas.unbind("<Button-1>")
            canvas.unbind("<B1-Motion>")
            canvas.unbind("<ButtonRelease-1>")
            
            # Bind mouse events again for image dragging
            canvas.tag_bind(canv_image_id,"<Button-1>", start_drag)
            canvas.tag_bind(canv_image_id,"<B1-Motion>", drag_image)
            
        else:
            drawing_mode = True
            
            if current_rectangle:
                canvas.delete(current_rectangle)
                current_rectangle = None  # Clear reference
            
            activate_button.config(text="Deactivate Drawing Mode")
            
            canvas.tag_unbind(canv_image_id, "<Button-1>")
            canvas.tag_unbind(canv_image_id, "<B1-Motion>")
    
            canvas.bind("<Button-1>", start_draw)
            canvas.bind("<B1-Motion>", draw_rectangle)
            canvas.bind("<ButtonRelease-1>", end_draw)
            
            
    def return_shift():
        # Pass the accumulated shift back to the main GUI
        print("Rough image shift (x,y):", x_offset/scaling_factor*100, y_offset/scaling_factor*100) # apply inverse scaling factor for shift in real scale
        print("Crop (x1,y1,x2,y2):", x1,y1,x2,y2)
        window.destroy()
    
    
    def scale_up(event):
        nonlocal source_scaling, image, image_width, image_height, new_image_tk, canv_image_id
        nonlocal x_offset, y_offset
        
        if is_float(scale_entry.get()) == False:
            tk.messagebox.showinfo('Error', "Enter a percentage number (below 100%).")
            scale_entry.delete(0, tk.END)
            scale_entry.insert(0, 1)
        else:
            if float(scale_entry.get()) <= 0 or float(scale_entry.get()) >100:
                tk.messagebox.showinfo('Error', "Enter a percentage number (below 100%).")
                scale_entry.delete(0, tk.END)
                scale_entry.insert(0, 1)
            else:
                source_scaling = source_scaling + float(scale_entry.get())/100
                total_scale_label.config(text=f"Total scale factor = {source_scaling}")
                
                # Up-scale the image
                new_image = image.resize((int(image_width*source_scaling), int(image_height*source_scaling)),Image.LANCZOS)
                
                new_image_tk = ImageTk.PhotoImage(new_image)
                canvas.itemconfig(canv_image_id, image=new_image_tk)
        
        
    def scale_down(event):
        nonlocal source_scaling, image, image_width, image_height, new_image_tk, canv_image_id
        nonlocal x_offset, y_offset
        
        if is_float(scale_entry.get()) == False:
            tk.messagebox.showinfo('Error', "Enter a percentage number (below 100%).")
            scale_entry.delete(0, tk.END)
            scale_entry.insert(0, 1)
        else:
            if float(scale_entry.get()) <= 0 or float(scale_entry.get()) >100:
                tk.messagebox.showinfo('Error', "Enter a percentage number (below 100%).")
                scale_entry.delete(0, tk.END)
                scale_entry.insert(0, 1)
            else:
                source_scaling = source_scaling - float(scale_entry.get())/100
                total_scale_label.config(text=f"Total scale factor = {source_scaling}")
                
                # Down-scale the image
                new_image = image.resize((int(image_width*source_scaling), int(image_height*source_scaling)),Image.LANCZOS)
                
                new_image_tk = ImageTk.PhotoImage(new_image)
                canvas.itemconfig(canv_image_id, image=new_image_tk)
        
    
    #create GUI
    if master == None:
        window = tk.Tk()
    else:
        window = tk.Toplevel(master)
    window.title("Rough stuff")
    window.geometry("1400x950")

    # Data for dragging
    drag_data = {"x": 0, "y": 0}

    # Create a canvas to display images
    canvas = tk.Canvas(window, width=int(ref_width*scaling_factor/100), height=int(ref_height*scaling_factor/100), bg="white")
    canvas.grid(row=0, column=0, padx=5, pady=5, sticky="n,w",rowspan = 10)
    
    # Create ImageTk objects
    ref_tk = ImageTk.PhotoImage(reference)
    image_tk = ImageTk.PhotoImage(image)
    new_image_tk = image_tk # initialize this ImageTk.PhotoImage variable
    
    # Display the images on the canvas, sticking to the upper right corner
    canvas.create_image(0, 0, anchor=tk.NW, image=ref_tk)
    canv_image_id = canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)

    # Bind mouse events for image dragging
    canvas.tag_bind(canv_image_id,"<Button-1>", start_drag)
    canvas.tag_bind(canv_image_id,"<B1-Motion>", drag_image)
    
    scale_label = tk.Label(window, text= "To scale up/down press up/down arrow key\n")
    scale_label.grid(row=0, column=1, padx=5, pady=5, sticky="n,w")
    
    scale_label2 = tk.Label(window, text= "Scaling by percent:")
    scale_label2.grid(row=1, column=1, padx=5, pady=5, sticky="n,w")
    
    scale_entry = tk.Entry(window, width=12)
    scale_entry.grid(row=2, column=1, padx=5, pady=5, sticky="n,w")
    scale_entry.insert(0,"1")
    
    total_scale_label = tk.Label(window, text= "Total scale factor = 1")
    total_scale_label.grid(row=3, column=1, padx=5, pady=5, sticky="n,w")
    
    activate_button = tk.Button(window, text="Activate Drawing Mode\nto crop the reference image", width = 25, height = 2, command=activate_drawing)
    activate_button.grid(row=5, column=1, padx=5, pady=5, sticky="n,w")
    
    tk.Label(window, text= "Attention: The cropping rectangle\nmust contain the whole\nsource image.").grid(row=6, column=1, padx=5, pady=5, sticky="n,w")
    
    # Bind keys to functions
    window.bind("<Up>", scale_up)   # Press "Up Arrow" to scale up
    window.bind("<Down>", scale_down) # Press "Down Arrow" to scale down

    # Button to stop and return rough shift
    load_button = tk.Button(window, text="Rough shift, rough scaling,\nand refrence crop done",width = 25, height = 2, command=return_shift)
    load_button.grid(row=7, column=1, padx=5, pady=5, sticky="n,w")
    
    if master == None:
        window.mainloop()
    else:
        master.wait_window(window)

    # output when GUI is closed:
    return int(x_offset/scaling_factor*100), int(y_offset/scaling_factor*100), x1,y1,x2,y2, source_scaling

# Create the window and run
if __name__ == "__main__":
    Rough(master = None, ref_path=None, image_path=None, scaling_factor=50)
    