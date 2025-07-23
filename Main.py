import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk

from Get_scaling_factor import Get_scaling_factor
from Shift_it import Shift_it
from Rough import Rough

from Image_import import path_to_display, path_to_TkPhotoImage, path_to_RGB

from Stack_registration import Stack_registration


class MainGUI:
    def __init__(self, root):
        self.root = root
        root.title("DHM-FLUO registration")
        root.geometry("1085x645")
        
        self.left_frame = tk.LabelFrame(root)
        self.left_frame.grid(row=0, column=0, padx=5, pady=5, sticky='n,w')
        
        self.Load_ref_frame = tk.LabelFrame(self.left_frame, text="Load reference image")
        self.Load_ref_frame.grid(row=0, column=0, padx=5, pady=5, sticky='n,w')
        
        self.button1 = tk.Button(self.Load_ref_frame, text="Browse", command=self.load_ref)
        self.button1.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        
        self.label_image1 = tk.Label(self.Load_ref_frame, text="Drag and Drop Reference Here", bg="lightgray", width=25, height=10)
        self.label_image1.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
        self.label_image1.drop_target_register(DND_FILES)
        self.label_image1.dnd_bind('<<Drop>>', self.on_ref_drop)
        
        self.ref_size_label = tk.Label(self.left_frame, text="Reference image size (w*h): ... * ...")
        self.ref_size_label.grid(row=1, column=0, padx=5, pady=5, sticky="n,w")
        
        self.Load_image_frame = tk.LabelFrame(self.left_frame, text="Load source image")
        self.Load_image_frame.grid(row=2, column=0, padx=5, pady=5, sticky='n,w')
        
        self.button2 = tk.Button(self.Load_image_frame, text="Browse", command=self.load_image)
        self.button2.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        
        self.label_image2 = tk.Label(self.Load_image_frame, text="Drag and Drop Image Here", bg="lightgray", width=25, height=10)
        self.label_image2.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
        self.label_image2.drop_target_register(DND_FILES)
        self.label_image2.dnd_bind('<<Drop>>', self.on_image_drop)
        
        self.img_size_label = tk.Label(self.left_frame, text="Source image size (w*h): ... * ...")
        self.img_size_label.grid(row=3, column=0, padx=5, pady=5, sticky="n,w")


        default_image = Image.new("RGB", (300, 300), "grey")
        default_photo = ImageTk.PhotoImage(default_image)
        self.ref_label = tk.Label(self.left_frame, image=default_photo)
        self.ref_label.grid(row=0, column=1, padx=5, pady=5, sticky="n,w", rowspan = 2)
        
        self.image_label = tk.Label(self.left_frame, image=default_photo)
        self.image_label.grid(row=2, column=1, padx=5, pady=5, sticky="n,w",rowspan = 2)
        
        # sub GUIs
        self.right_frame = tk.LabelFrame(root, text="Buttons and stuff")
        
        self.space_label0 = tk.Label(self.right_frame, text= "   ")
        
        self.scal_label = tk.Label(self.right_frame, text= 'I. Get the scaling factor:\n\ni) Enter scaling factor manually:')
        self.scal_label.grid(row=0, column=0, padx=5, pady=0, sticky="n")
        
        self.scal_entry = tk.Entry(self.right_frame, width=12)
        self.scal_entry.grid(row=1, column=0, padx=5, pady=0, sticky="n")
        self.scal_entry.insert(0,"1")
        
        self.scal_label = tk.Label(self.right_frame, text= 'or\nii) Use "Rough GUI" --->\nor')
        self.scal_label.grid(row=2, column=0, padx=5, pady=0, sticky="n")
        
        self.scal_button = tk.Button(self.right_frame, text="iii) Open Scaling GUI", command=self.start_scaling_GUI)
        self.scal_button.grid(row=3, column=0, padx=10, pady=0, sticky="n")

        
        self.space_label = tk.Label(self.right_frame, text= "   ")
        self.space_label.grid(row=4, column=0, padx=5, pady=5, sticky="n")
        
        self.space_label2 = tk.Label(self.right_frame, text= "   ")
        self.space_label3 = tk.Label(self.right_frame, text= "   ")
        
        self.shift_button = tk.Button(self.right_frame, text="Open Shifting GUI", command=self.start_shifting_GUI)
        
        self.shift_label = tk.Label(self.right_frame, text= "II. Get the xy shift:\nEnter manually or use the sub GUI")
        self.shift_label2 = tk.Label(self.right_frame, text= "Image shift (x,y):")
        
        self.sssframe = tk.Frame(self.right_frame)
        self.shift_x_entry = tk.Entry(self.sssframe, width=6)
        self.shift_x_entry.insert(0,"0")
        self.shift_y_entry = tk.Entry(self.sssframe, width=6)
        self.shift_y_entry.insert(0,"0")
        self.shift_x_entry.grid(row=0, column=0, padx=0, pady=5, sticky="n")
        self.shift_y_entry.grid(row=0, column=1, padx=0, pady=5, sticky="n")
        
        
        self.stack_label = tk.Label(self.right_frame, text= "III. Rescale and align a whole stack")
        self.stack_button = tk.Button(self.right_frame, text="Load stack and process", command=self.stack_reg)
        
        self.info_button = tk.Button(self.right_frame, text="INFO", command=self.show_info)
        
        self.close_button = tk.Button(self.right_frame, text="EXIT", command=self.close_GUI)
        
        self.shift_label.grid(row=5, column=0, padx=5, pady=5, sticky="n")
        self.shift_button.grid(row=6, column=0, padx=5, pady=5, sticky="n")
        self.shift_label2.grid(row=7, column=0, padx=5, pady=5, sticky="n")
        self.sssframe.grid(row=8, column=0, padx=5, pady=5, sticky="n")
        self.space_label2.grid(row=9, column=0, padx=5, pady=5, sticky="n")
        self.stack_label.grid(row=10, column=0, padx=5, pady=5, sticky="n")
        self.stack_button.grid(row=11, column=0, padx=5, pady=5, sticky="n")
        self.space_label3.grid(row=12, column=0, padx=5, pady=5, sticky="n")
        self.info_button.grid(row=13, column=0, padx=5, pady=5, sticky="n")
        self.close_button.grid(row=14, column=0, padx=5, pady=5, sticky="n")
        
        self.right_frame.grid(row=0, column=2, padx=5, pady=5, sticky="n")
        
        # rough frame
        self.rough_frame = tk.LabelFrame(root, text="Rough stuff")
        
        self.rrrframe = tk.Frame(self.rough_frame)
        self.rescale_label = tk.Label(self.rrrframe, text= "Rescale images to")
        self.rescale_label.grid(row=0, column=0, padx=0, pady=5, sticky="n")
        self.rough_scale_entry = tk.Entry(self.rrrframe, width=6)
        self.rough_scale_entry.grid(row=0, column=1, padx=0, pady=5, sticky="n")
        self.rough_scale_entry.insert(0,"75")
        self.rescale_label2 = tk.Label(self.rrrframe, text= "%")
        self.rescale_label2.grid(row=0, column=2, padx=0, pady=5, sticky="n")
        self.rrrframe.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        
        self.rough_button = tk.Button(self.rough_frame, text="Do a rough alignment", command=self.rough)
        self.rough_button.grid(row=1, column=0, padx=5, pady=5, sticky="n")
        
        self.rough_shift_label = tk.Label(self.rough_frame, text= "Rough shift (x,y):")
        self.rough_shift_label.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        
        self.RRRframe = tk.Frame(self.rough_frame)
        self.rough_shift_x_entry = tk.Entry(self.RRRframe, width=6)
        self.rough_shift_x_entry.grid(row=0, column=0, padx=0, pady=5, sticky="n")
        self.rough_shift_x_entry.insert(0,"0")
        self.rough_shift_x_entry.config(state="disabled")
        self.rough_shift_y_entry = tk.Entry(self.RRRframe, width=6)
        self.rough_shift_y_entry.grid(row=0, column=1, padx=0, pady=5, sticky="n")
        self.rough_shift_y_entry.insert(0,"0")
        self.rough_shift_y_entry.config(state="disabled")
        self.RRRframe.grid(row=3, column=0, padx=5, pady=5, sticky="n")

        self.rough_frame.grid(row=0, column=3, padx=5, pady=5, sticky="n")
        
        # initialize some variables
        self.ref_tk = None
        self.img_tk = None
        self.ref_height = None
        self.ref_width = None
        self.image_height = None
        self.image_width = None
        self.ref_path = ""
        self.image_path = ""
        
        self.fine_shift_x = 0
        self.fine_shift_y = 0
        
        self.rough_shift_x = 0
        self.rough_shift_y = 0
        self.rough_crop = None

    # Function to load image via button click
    def load_ref(self):
        self.ref_path = filedialog.askopenfilename(title = "Select a reference image", filetypes=[("Open", "*.png;*.jpg;*.jpeg;*.bmp;*.tif;*.tiff;*.bin;*.bnr")])
        if self.ref_path != "":
            path_to_display(self.ref_path, self.ref_label)
            
            self.ref_tk, self.ref_height, self.ref_width = path_to_TkPhotoImage(self.ref_path)
            
            self.ref_size_label.config(text=f"Reference image size (w*h):   {self.ref_width} * {self.ref_height}")
            
            # initialize
            self.rough_shift_x = 0
            self.rough_shift_y = 0
            self.rough_crop = None
            
    def load_image(self):
        self.image_path = filedialog.askopenfilename(title = "Select a source reference image",filetypes=[("Open", "*.png;*.jpg;*.jpeg;*.bmp;*.tif;*.tiff;*.bin;*.bnr")])
        if self.image_path != "":
            path_to_display(self.image_path, self.image_label)
            
            self.img_tk, self.image_height, self.image_width = path_to_TkPhotoImage(self.image_path)
            
            self.img_size_label.config(text=f"Source image size (w*h):   {self.image_width} * {self.image_height}")
            
            # initialize
            self.rough_shift_x = 0
            self.rough_shift_y = 0
            self.rough_crop = None
    
    # Function to handle the file drop event
    def on_ref_drop(self, event):
        self.ref_path = event.data.strip("{}")
        path_to_display(self.ref_path, self.ref_label)
        
        self.ref_tk, self.ref_height, self.ref_width = path_to_TkPhotoImage(self.ref_path)
        
        self.ref_size_label.config(text=f"Reference image size (w*h):   {self.ref_width} * {self.ref_height}")
        
        # initialize
        self.rough_shift_x = 0
        self.rough_shift_y = 0
        self.rough_crop = None
    
    def on_image_drop(self, event):
        self.image_path = event.data.strip("{}")
        path_to_display(self.image_path, self.image_label)
        
        self.img_tk, self.image_height, self.image_width = path_to_TkPhotoImage(self.image_path)
        
        self.img_size_label.config(text=f"Source image size (w*h):   {self.image_width} * {self.image_height}")
        
        # initialize
        self.rough_shift_x = 0
        self.rough_shift_y = 0
        self.rough_crop = None
    
    
    def rough(self):
        print("Starting Rough-GUI")
        # call a gui to do a rough overlay, first check some input
        scaling_factor = None
        try:
            scaling_factor = float(self.rough_scale_entry.get())
            if scaling_factor < 0 or scaling_factor >100:
                tk.messagebox.showinfo('Error', "Enter a percentage number (below 100%).")
                scaling_factor = None
        except:
            tk.messagebox.showinfo('Error', "Enter a percentage number.")
            scaling_factor = None
            
        if scaling_factor:
            
            # check if ref and source image have been imported
            if self.ref_path == "":
                self.load_ref()
                
                if self.ref_path == "":
                    print("Starting Rough-GUI cancelled. No reference image selected")
                else:

                    if self.image_path == "":
                        self.load_image()
                        if self.image_path == "":
                            print("Starting Rough-GUI cancelled. No source image selected")
            else:
                if self.image_path == "":
                    self.load_image()
                    if self.image_path == "":
                        print("Starting Rough-GUI cancelled. No source image selected")
                            
            if self.ref_path != "" and self.image_path != "":
                
                self.rough_shift_x, self.rough_shift_y, x1,y1,x2,y2, self.rough_scaling = Rough(master = self.root, ref_path = self.ref_path, image_path = self.image_path, scaling_factor = scaling_factor)
                self.rough_crop = [x1,y1,x2,y2]
                print("Rough image shift (x,y):", self.rough_shift_x, self.rough_shift_y)
                print("Reference image crop (x, y, w, h):", x1,y1,x2,y2)
                print("Rough scaling:", self.rough_scaling)
                print("Rough-GUI closed.")
                
                self.rough_shift_x_entry.config(state="normal")
                self.rough_shift_y_entry.config(state="normal")
            
                self.rough_shift_x_entry.delete(0, tk.END)
                self.rough_shift_x_entry.insert(0,str(self.rough_shift_x))
                self.rough_shift_y_entry.delete(0, tk.END)
                self.rough_shift_y_entry.insert(0,str(self.rough_shift_y))
                
                self.scal_entry.delete(0, tk.END)
                self.scal_entry.insert(0, str(self.rough_scaling))
                
                self.rough_shift_x_entry.config(state="disabled")
                self.rough_shift_y_entry.config(state="disabled")
    
    
    # Method to receive data back from the second GUI
    def receive_data_from_second_gui(self, data):
        self.scal_entry.delete(0, tk.END)
        self.scal_entry.insert(0, str(data))
    
    
    def start_scaling_GUI(self):
        print("Starting Scaling-GUI...")

        # check if ref and source image have been imported
        if self.ref_path == "":
            self.load_ref()
            
            if self.ref_path == "":
                print("Starting Scaling-GUI cancelled. No reference image selected")
            else:
                if self.image_path == "":
                    self.load_image()
                    if self.image_path == "":
                        print("Starting Scaling-GUI cancelled. No source image selected")
        else:
            if self.image_path == "":
                self.load_image()
                if self.image_path == "":
                    print("Starting Scaling-GUI cancelled. No source image selected")

        if self.ref_path != "" and self.image_path != "":
            # apply crop on reference if needed
            if self.rough_crop:
                # Crop the image using NumPy slicing
                # RGB_image = RGB_image[self.rough_crop[1]:self.rough_crop[3], self.rough_crop[0]:self.rough_crop[2]]
                ref_width = self.rough_crop[2]-self.rough_crop[0]
                ref_height = self.rough_crop[3]-self.rough_crop[1]
            else:
                ref_width = self.ref_width
                ref_height = self.ref_height
            
            #Pass data to sub GUI
            passed_data = self.ref_tk, self.img_tk, ref_height, ref_width, self.image_height, self.image_width
 
            # call sub GUI
            Get_scaling_factor(master=self.root, passed_data=passed_data, callback=self.receive_data_from_second_gui)
            print("Scaling-GUI closed")
        
        
    def start_shifting_GUI(self):
        print("Starting Shifting-GUI...")
        # check if ref and source image have been imported
        if self.ref_path == "":
            self.load_ref()
            
            if self.ref_path == "":
                print("Starting Shifting-GUI cancelled. No reference image selected")
            else:
                if self.image_path == "":
                    self.load_image()
                    if self.image_path == "":
                        print("Starting Shifting-GUI cancelled. No source image selected")
        else:
            if self.image_path == "":
                self.load_image()
                if self.image_path == "":
                    print("Starting Shifting-GUI cancelled. No source image selected")
                        
        if self.ref_path != "" and self.image_path != "":
            # apply crop on reference if needed
            if self.rough_crop:
                pre_shift_x = self.rough_shift_x - self.rough_crop[0]
                pre_shift_y = self.rough_shift_y - self.rough_crop[1]
            else:
                pre_shift_x = self.rough_shift_x
                pre_shift_y = self.rough_shift_y
            
            self.fine_shift_x, self.fine_shift_y = Shift_it(master = self.root, ref_path = self.ref_path, image_path = self.image_path, scaling_factor = float(self.scal_entry.get()), pre_shift_x = pre_shift_x, pre_shift_y = pre_shift_y)
            print("Final image shift (x,y):", self.fine_shift_x, self.fine_shift_y)
            print("Shifting-GUI closed")

            self.shift_x_entry.delete(0, tk.END)
            self.shift_x_entry.insert(0,str(self.fine_shift_x+self.rough_shift_x))
            self.shift_y_entry.delete(0, tk.END)
            self.shift_y_entry.insert(0,str(self.fine_shift_y+self.rough_shift_y))

            
    def stack_reg(self):
        print("Start stack registration:")
        ref_h = None
        ref_w = None
        if self.ref_path == "":
            ref_path = ""
            ref_path = filedialog.askopenfilename(title = "Select a reference image", filetypes=[("Open", "*.png;*.jpg;*.jpeg;*.bmp;*.tif;*.tiff;*.bin;*.bnr")])
            if ref_path == "":
                print("Stack registration cancelled. No reference image selected.")
            else:
                abc, ref_h, ref_w = path_to_TkPhotoImage(ref_path)
        else: 
            ref_h = self.ref_height
            ref_w = self.ref_width
        
        if ref_h:
            stack_path = ""
            stack_path = filedialog.askopenfilename(title = "Select the first stack file",filetypes=[("Open", "*.tif;*.tiff;*.bin;*.bnr")])
            
            if stack_path == "":
                print("Stack registration cancelled. No source file selected.")
            else:
                print(stack_path)
                
                factor = float(self.scal_entry.get())
                x_shift = int(self.shift_x_entry.get())
                y_shift = int(self.shift_y_entry.get())
                                
                Stack_registration(stack_path, ref_w, ref_h, factor, x_shift, y_shift)
                print("Stack registration completed.")
        
    def show_info(self):
        with open('README.md') as f:
            infotext=f.read()
        f.close()
        tk.messagebox.showinfo("Info", infotext)
            
    def close_GUI(self):
        self.root.destroy()
    
# Create the main window and run the MainGUI
if __name__ == "__main__":
    root = TkinterDnD.Tk() 
    app = MainGUI(root)
    root.mainloop()
