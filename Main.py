import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk

from Get_scaling_factor import Get_scaling_factor
from Shift_it import Shift_it

from image_import import path_to_display, path_to_TkPhotoImage, path_to_RGB


class MainGUI:
    def __init__(self, root):
        self.root = root
        root.title("DHM-FLUO registration")
        root.geometry("930x640")
        
        self.left_frame = tk.LabelFrame(root)
        
        self.Load_ref_frame = tk.LabelFrame(self.left_frame, text="Load reference image")
        
        self.button1 = tk.Button(self.Load_ref_frame, text="Browse", command=self.load_ref)
        self.button1.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        
        self.label_image1 = tk.Label(self.Load_ref_frame, text="Drag and Drop Reference Here", bg="lightgray", width=35, height=10)
        self.label_image1.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
        self.label_image1.drop_target_register(DND_FILES)
        self.label_image1.dnd_bind('<<Drop>>', self.on_ref_drop)
        
        
        self.Load_image_frame = tk.LabelFrame(self.left_frame, text="Load source image")
        
        self.button2 = tk.Button(self.Load_image_frame, text="Browse", command=self.load_image)
        self.button2.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        
        self.label_image2 = tk.Label(self.Load_image_frame, text="Drag and Drop Image Here", bg="lightgray", width=35, height=10)
        self.label_image2.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
        self.label_image2.drop_target_register(DND_FILES)
        self.label_image2.dnd_bind('<<Drop>>', self.on_image_drop)
        
        
        self.Load_ref_frame.grid(row=0, column=0, padx=5, pady=5, sticky='n,w')
        self.Load_image_frame.grid(row=1, column=0, padx=5, pady=5, sticky='n,w')
        
        self.left_frame.grid(row=0, column=0, padx=5, pady=5, sticky='n,w')
        
        
        default_image = Image.new("RGB", (300, 300), "grey")
        default_photo = ImageTk.PhotoImage(default_image)
        self.ref_label = tk.Label(self.left_frame, image=default_photo)
        self.ref_label.grid(row=0, column=1, padx=5, pady=5, sticky="n,w")
        
        self.image_label = tk.Label(self.left_frame, image=default_photo)
        self.image_label.grid(row=1, column=1, padx=5, pady=5, sticky="n,w")
        
        # sub GUIs
        self.aframe = tk.LabelFrame(root)
        
        self.scal_label = tk.Label(self.aframe, text= "I. Rescaling of the source image:\nEnter a manual factor or use the sub GUI")
        self.scal_label2 = tk.Label(self.aframe, text= "Scaling factor:")
        self.scal_entry = tk.Entry(self.aframe, width=6)
        self.scal_entry.insert(0,"1")
        self.scal_button = tk.Button(self.aframe, text="Open Scaling GUI", command=self.start_scaling_GUI)
        
        self.space_label = tk.Label(self.aframe, text= "   ")
        self.space_label2 = tk.Label(self.aframe, text= "   ")
        self.space_label3 = tk.Label(self.aframe, text= "   ")
        
        self.shift_button = tk.Button(self.aframe, text="Open Shifting GUI", command=self.start_shifting_GUI)
        
        self.shift_label = tk.Label(self.aframe, text= "II. To shift the source image, open the sub GUI")
        self.shift_label2 = tk.Label(self.aframe, text= "Image shift (x,y):")
        self.shift_entry = tk.Entry(self.aframe, width=9)
        self.shift_entry.insert(0,"")
        
        self.info_button = tk.Button(self.aframe, text="INFO", command=self.show_info)
        
        self.close_button = tk.Button(self.aframe, text="EXIT", command=self.close_GUI)
        
        self.scal_label.grid(row=0, column=0, padx=5, pady=5, sticky="n,w")
        self.scal_label2.grid(row=1, column=0, padx=5, pady=5, sticky="n,w")
        self.scal_entry.grid(row=2, column=0, padx=5, pady=5, sticky="n,w")
        self.scal_button.grid(row=3, column=0, padx=5, pady=5, sticky="n,w")
        self.space_label.grid(row=4, column=0, padx=5, pady=5, sticky="n,w")
        
        self.shift_label.grid(row=5, column=0, padx=5, pady=5, sticky="n,w")
        self.shift_button.grid(row=6, column=0, padx=5, pady=5, sticky="n,w")
        self.shift_label2.grid(row=7, column=0, padx=5, pady=5, sticky="n,w")
        self.shift_entry.grid(row=8, column=0, padx=0, pady=5, sticky="n,w")
        self.space_label2.grid(row=9, column=0, padx=5, pady=5, sticky="n,w")
        
        self.info_button.grid(row=10, column=0, padx=5, pady=5, sticky="n,w")
        
        self.space_label3.grid(row=11, column=0, padx=5, pady=5, sticky="n,w")
        
        self.close_button.grid(row=12, column=0, padx=5, pady=5, sticky="nw")
        
        self.aframe.grid(row=0, column=2, padx=5, pady=5, sticky="n,w")
        
        # initialize some variables
        self.ref_tk = None
        self.img_tk = None
        self.ref_height = None
        self.ref_width = None
        self.image_height = None
        self.image_width = None
        self.ref_path = None
        self.image_path = None

    # Function to load image via button click
    def load_ref(self):
        self.ref_path = filedialog.askopenfilename(filetypes=[("Select a reference image", "*.png;*.jpg;*.jpeg;*.bmp;*.tif;*.tiff;*.bin;*.bnr")])
        if self.ref_path:
            path_to_display(self.ref_path, self.ref_label)
            
            self.ref_tk, self.ref_height, self.ref_width = path_to_TkPhotoImage(self.ref_path)
    
    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Select a source reference image", "*.png;*.jpg;*.jpeg;*.bmp;*.tif;*.tiff;*.bin;*.bnr")])
        if self.image_path:
            path_to_display(self.image_path, self.image_label)
            
            self.img_tk, self.image_height, self.image_width = path_to_TkPhotoImage(self.image_path)
    
    # Function to handle the file drop event
    def on_ref_drop(self, event):
        self.ref_path = event.data.strip("{}")
        path_to_display(self.ref_path, self.ref_label)
        
        self.ref_tk, ref_height, ref_width = path_to_TkPhotoImage(self.ref_path)
    
    def on_image_drop(self, event):
        self.image_path = event.data.strip("{}")
        path_to_display(self.image_path, self.image_label) 
        
        self.img_tk, self.image_height, self.image_width = path_to_TkPhotoImage(self.image_path)
    
    def start_scaling_GUI(self):
        print("Scaling-GUI activated")
        
        if self.ref_tk == None:
            self.ref_path = filedialog.askopenfilename(filetypes=[("Select a reference image", "*.png;*.jpg;*.jpeg;*.bmp;*.tif;*.tiff;*.bin;*.bnr")])
            if self.ref_path:
                path_to_display(self.ref_path, self.ref_label)
                
                self.ref_tk, self.ref_height, self.ref_width = path_to_TkPhotoImage(self.ref_path)
        
        if self.img_tk == None:
            self.image_path = filedialog.askopenfilename(filetypes=[("Select a source reference image", "*.png;*.jpg;*.jpeg;*.bmp;*.tif;*.tiff;*.bin;*.bnr")])
            if self.image_path:
                path_to_display(self.image_path, self.image_label)
                
                self.img_tk, self.image_height, self.image_width = path_to_TkPhotoImage(self.image_path)
        
        #Pass data to sub GUI
        passed_data = self.ref_tk, self.img_tk, self.ref_height, self.ref_width, self.image_height, self.image_width
        
        # call sub GUI
        Get_scaling_factor(self.root, passed_data=passed_data, callback=self.receive_data_from_second_gui)

    # Method to receive data back from the second GUI
    def receive_data_from_second_gui(self, data):
        print("Scaling factor from \"Scaling-GUI\":", data)
        self.scal_entry.insert(0, str(data))
        
    def start_shifting_GUI(self):
        
        if self.ref_path == None:
            self.ref_path = filedialog.askopenfilename(filetypes=[("Select a reference image", "*.png;*.jpg;*.jpeg;*.bmp;*.tif;*.tiff;*.bin;*.bnr")])
            path_to_display(self.ref_path, self.ref_label)
            
        self.ref_RGB = path_to_RGB(self.ref_path)
            
        if self.image_path == None:
            self.image_path = filedialog.askopenfilename(filetypes=[("Select a source reference image", "*.png;*.jpg;*.jpeg;*.bmp;*.tif;*.tiff;*.bin;*.bnr")])
            path_to_display(self.image_path, self.image_label)
            
        self.image_RGB = path_to_RGB(self.image_path)
        
        print(self.scal_entry.get())
        
        print("Shift-it-GUI activated")
        shift_x, shift_y = Shift_it(master = self.root, ref_RGB = self.ref_RGB, image_RGB = self.image_RGB, scaling_factor = self.SF_entry.get())
        print("Final image shift (x,y):", shift_x, shift_y)
        print("Shift-it-GUI closed")
        
        shift_string = str(shift_x) + "   ,   " + str(shift_y)
        self.shift_entry.delete(0, tk.END)
        self.shift_entry.insert(0,shift_string)
        
    def show_info(self):
        with open('_read me.txt') as f:
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
