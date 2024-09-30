#GUI to manually extract the scaling factor between two microscopy images (e.g. one from DHM, one from fluorescence)
import tkinter as tk
from math import sqrt
from tkinter import filedialog, messagebox

from image_import import path_to_TkPhotoImage

def get_even_or_lower_even(n):
    if n % 2 == 0:
        return n
    else:
        return n - 1

class Get_scaling_factor:
    
    def __init__(self, master=None, passed_data=None, callback=None):
        
        self.callback = callback  # Reference to the function to call in MainGUI
        
        # If the master is None, this means it's being run standalone
        if master is None:
            self.window = tk.Tk()  # Create a new main window (Tk)
        else:
            self.window = tk.Toplevel(master)  # Create a new independent window (Toplevel)
        
        self.window.title("Get Scaling factor")
        
        if passed_data == None:
            
            self.ref_tk, self.ref_height, self.ref_width = path_to_TkPhotoImage(filedialog.askopenfilename(title="Select a reference file"))
            
            self.img_tk, self.image_height, self.image_width = path_to_TkPhotoImage(filedialog.askopenfilename(title="Select an image file"))
            
        else: self.ref_tk, self.img_tk, self.ref_height, self.ref_width, self.image_height, self.image_width = passed_data
        
        self.ref_canvas = tk.Canvas(self.window, width=self.ref_width, height=self.ref_height)
        self.img_canvas = tk.Canvas(self.window, width=self.image_width, height=self.image_height)
        self.ref_canvas.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        self.img_canvas.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
        
        self.ref_canvas.create_image(0, 0, anchor=tk.NW, image=self.ref_tk)
        self.img_canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)
        
        self.img_label = tk.Label(self.window, text="Mouse Position on image: ")
        self.img_label.grid(row=1, column=1, padx=5, pady=5, sticky="nw")
        
        self.ref_label = tk.Label(self.window, text="Mouse Position on reference: ")
        self.ref_label.grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        
        self.img_positions = []
        self.img_pos_count = 0
        self.ref_positions = []
        self.ref_pos_count = 0
        
        self.img_canvas.bind("<Motion>", self.img_mouse_move)
        self.img_canvas.bind("<Double-1>", self.save_img_position)
        
        self.ref_canvas.bind("<Motion>", self.ref_mouse_move)
        self.ref_canvas.bind("<Double-1>", self.save_ref_position)
        
        self.aframe = tk.LabelFrame(self.window, text="Truc")
        self.display = tk.Text(self.aframe, height = 25, width = 16)
        self.display.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        self.calc_button = tk.Button(self.aframe, text="Calculate scaling factor", command=self.calc_fact)
        self.calc_button.grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        self.close_button = tk.Button(self.aframe, text="Close Scaling GUI", command=self.close_GUI)
        self.close_button.grid(row=2, column=0, padx=5, pady=5, sticky="nw")
        
        self.aframe.grid(row=0, column=2, padx=5, pady=5, sticky="nw")
        
    def img_mouse_move(self, event):
        self.img_label.config(text=f"Mouse Position: {event.x}, {event.y}")
        
    def ref_mouse_move(self, event):
        self.ref_label.config(text=f"Mouse Position: {event.x}, {event.y}")    
    
    def save_img_position(self, event):
        x, y = event.x, event.y
        self.img_positions.append((x, y))
        self.img_pos_count = self.img_pos_count + 1
        print(f"Imag pos N°{self.img_pos_count}:\nx = {x}, y = {y}\n")
        
        self.display.insert(tk.END,f"Imag pos N°{self.img_pos_count}:\nx = {x}, y = {y}\n")
                
    def save_ref_position(self, event):
        x, y = event.x, event.y
        self.ref_positions.append((x, y))
        self.ref_pos_count = self.ref_pos_count + 1
        print(f"Ref pos N°{self.img_pos_count}:\nx = {x}, y = {y}\n")
        
        self.display.insert(tk.END,f"Ref pos N°{self.img_pos_count}:\nx = {x}, y = {y}\n")
                
    def calc_fact(self):
        if len(self.img_positions) < 2 or len(self.ref_positions) < 2:
            messagebox.showwarning("Warning", "Not enough positions saved to calculate distances.")
            return
        
        abc = min(len(self.img_positions),len(self.ref_positions))
        
        bcd = get_even_or_lower_even(abc)
        
        mean_ratio = 0
        k=0
        # Euclidean distances between pairs of saved positions
        for i in range(bcd):
            
            if i % 2 == 0:
                
                x1, y1 = self.img_positions[i]
                x2, y2 = self.img_positions[i+1]
                
                img_dist = sqrt((x2 - x1)**2 + (y2 - y1)**2)
                
                x1, y1 = self.ref_positions[i]
                x2, y2 = self.ref_positions[i+1]
                
                ref_dist = sqrt((x2 - x1)**2 + (y2 - y1)**2)
                
                ratio = ref_dist/img_dist
                
                k=k+1
                mean_ratio = mean_ratio + ratio
                
        mean_ratio = mean_ratio/k
        print(f"\nNumber of marker pairs: {bcd}\nNumber of distances: {bcd/2}\nApproximative scaling factor: {mean_ratio}")
        
        if self.callback:
            self.callback(mean_ratio)  # Call the function in MainGUI and pass the data
              
        self.display.insert(tk.END,f"\nNumber of marker pairs: {bcd}\nApproximative scaling factor: {mean_ratio}")
        
        # #send data back to main GUI
        # if self.callback:
        #     self.callback(mean_ratio)  # Call the function in MainGUI and pass the data
        
        # Save to file
        k=1
        with open("Positions and scaling factor.txt", "w") as fileID:
            for i in range(bcd):
                fileID.write(f"Reference position N°{i+1} (x,y): {self.ref_positions[i]}\n")
            for i in range(bcd):
                fileID.write(f"Image position N°{i+1} (x,y): {self.img_positions[i]}\n")
            
            fileID.write(f"\nNumber of marker pairs: {bcd}\nNumber of distances: {bcd/2}\nApproximative scaling factor: {mean_ratio}")

        fileID.close()
        
    def close_GUI(self):
        print("Scaling-GUI closed")
        self.window.destroy()

    
# If this file is run as the main script, create a standalone GUI
if __name__ == "__main__":
    app = Get_scaling_factor()
    app.window.mainloop()
