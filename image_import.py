from os import path
from PIL import Image, ImageTk
import numpy
import cv2
import matplotlib.pyplot as plt

# Function to read an image file (.png;.jpg;.jpeg;.bmp;.tif;.tiff; LynceeTec: .bin;.bnr)
# and transform it to Tkinter photo format, gives also dimensions in pixel
def path_to_TkPhotoImage(image_path):
    
    # default output:
    default_image = Image.new("RGB", (300, 300), "grey")
    height = 300
    width = 300
    photo = ImageTk.PhotoImage(default_image)
     
    file_name, file_extension = path.splitext(image_path)
    if file_extension == ".bin": 
        import binkoala
        try:
            (phase_map,in_file_header)=binkoala.read_mat_bin(image_path)
            
            width = str(in_file_header['width'][0])
            height = str(in_file_header['height'][0])
            
            # Normalize the float array to range [0, 1]
            normalized_array = (phase_map - phase_map.min()) / (phase_map.max() - phase_map.min())
            # Create a viridis colormap
            cmap = plt.get_cmap('viridis')
            # Apply the colormap to the normalized array
            cmap_array = cmap(normalized_array)
            # Convert the matplotlib array to a PIL image
            image = Image.fromarray((cmap_array[:, :, :3] * 255).astype(numpy.uint8))
            # Convert PIL image to Tkinter-compatible format
            photo = ImageTk.PhotoImage(image)
            
        except Exception as e:
            print(f"Error loading bin file: {e}") 
            
    elif file_extension == ".bnr": 
        try:
            #get header info:
            fileID = open(image_path, 'rb')
            nImages = numpy.fromfile(fileID, dtype="i4", count=1)
            nImages = nImages[0]
            w = numpy.fromfile(fileID, dtype="i4", count=1)
            width=w[0]
            w=w[0]
            h = numpy.fromfile(fileID, dtype="i4", count=1)
            height=h[0]
            h=h[0]
            pz = numpy.fromfile(fileID, dtype="f4", count=1)
            wave = numpy.fromfile(fileID, dtype="f4", count=1)
            n_1 = numpy.fromfile(fileID, dtype="f4", count=1)
            n_2 = numpy.fromfile(fileID, dtype="f4", count=1)
            #timestamps = numpy.fromfile(fileID, dtype="i4", count=nImages)
            timestamps = [0] * nImages
            for k in range(0,nImages):
                x=numpy.fromfile(fileID, dtype="i4", count=1)
                timestamps[k] = x[0]
            #get first image from sequence
            phase_map = numpy.zeros((h,w))
            for k in range(h):
                phase_map[k,:] = numpy.fromfile(fileID, dtype="f4", count=w)
            phase_map=numpy.single(phase_map)
            fileID.close
            
            #display image
            # Normalize the float array to range [0, 1]
            normalized_array = (phase_map - phase_map.min()) / (phase_map.max() - phase_map.min())
            # Create a viridis colormap
            cmap = plt.get_cmap('viridis')
            # Apply the colormap to the normalized array
            cmap_array = cmap(normalized_array)
            # Convert the matplotlib array to a PIL image
            image = Image.fromarray((cmap_array[:, :, :3] * 255).astype(numpy.uint8))
            # Convert PIL image to Tkinter-compatible format
            photo = ImageTk.PhotoImage(image)    
            
        except Exception as e:
            print(f"Error loading bnr file: {e}") 

    elif file_extension == ".tif" or file_extension == ".tiff":
        from tifffile import imread
        try:
            phase_map = imread(image_path, key=0)
            width = str(len(phase_map[0,:]))
            height = str(len(phase_map[:,0]))
            
            # Normalize the float array to range [0, 1]
            normalized_array = (phase_map - phase_map.min()) / (phase_map.max() - phase_map.min())
            # Create a viridis colormap
            cmap = plt.get_cmap('viridis')
            # Apply the colormap to the normalized array
            cmap_array = cmap(normalized_array)
            # Convert the matplotlib array to a PIL image
            image = Image.fromarray((cmap_array[:, :, :3] * 255).astype(numpy.uint8))
            # Convert PIL image to Tkinter-compatible format
            photo = ImageTk.PhotoImage(image)

        except Exception as e:
            print(f"Error loading tif / tiff file: {e}") 

    else:
        try:
            image = cv2.imread(image_path)
            height, width = image.shape[:2]
            
            pil_image = Image.fromarray(image)
            # Convert the PIL Image to an ImageTk PhotoImage
            photo = ImageTk.PhotoImage(image=pil_image)

        except Exception as e:
            print(f"Error loading image: {e}")

    return photo, height, width

# Function to read an image file (.png;.jpg;.jpeg;.bmp;.tif;.tiff; LynceeTec: .bin;.bnr)
# and transform it to Tkinter photo format, rezises it to 300*300 pixels and display the image in the specified "label"
def path_to_display(image_path, label):
    
    file_name, file_extension = path.splitext(image_path)
    if file_extension == ".bin": 
        import binkoala
        try:
            (phase_map,in_file_header)=binkoala.read_mat_bin(image_path)
            
            # Normalize the float array to range [0, 1]
            normalized_array = (phase_map - phase_map.min()) / (phase_map.max() - phase_map.min())
            # Create a viridis colormap
            cmap = plt.get_cmap('viridis')
            # Apply the colormap to the normalized array
            cmap_array = cmap(normalized_array)
            # Convert the matplotlib array to a PIL image
            image = Image.fromarray((cmap_array[:, :, :3] * 255).astype(numpy.uint8))
            image = image.resize((300, 300))
            # Convert PIL image to Tkinter-compatible format
            photo = ImageTk.PhotoImage(image)
            # Update the image label
            label.config(image=photo)
            label.image = photo  # Keep a reference to the image to prevent it from being garbage collected
            
        except Exception as e:
            print(f"Error loading bin file: {e}") 
            
    elif file_extension == ".bnr": 
        try:
            #get header info:
            fileID = open(image_path, 'rb')
            nImages = numpy.fromfile(fileID, dtype="i4", count=1)
            nImages = nImages[0]
            w = numpy.fromfile(fileID, dtype="i4", count=1)
            w=w[0]
            h = numpy.fromfile(fileID, dtype="i4", count=1)
            h=h[0]
            pz = numpy.fromfile(fileID, dtype="f4", count=1)
            wave = numpy.fromfile(fileID, dtype="f4", count=1)
            n_1 = numpy.fromfile(fileID, dtype="f4", count=1)
            n_2 = numpy.fromfile(fileID, dtype="f4", count=1)
            #timestamps = numpy.fromfile(fileID, dtype="i4", count=nImages)
            timestamps = [0] * nImages
            for k in range(0,nImages):
                x=numpy.fromfile(fileID, dtype="i4", count=1)
                timestamps[k] = x[0]
            #get first image from sequence
            phase_map = numpy.zeros((h,w))
            for k in range(h):
                phase_map[k,:] = numpy.fromfile(fileID, dtype="f4", count=w)
            phase_map=numpy.single(phase_map)
            fileID.close
            
            #display image
            # Normalize the float array to range [0, 1]
            normalized_array = (phase_map - phase_map.min()) / (phase_map.max() - phase_map.min())
            # Create a viridis colormap
            cmap = plt.get_cmap('viridis')
            # Apply the colormap to the normalized array
            cmap_array = cmap(normalized_array)
            # Convert the matplotlib array to a PIL image
            image = Image.fromarray((cmap_array[:, :, :3] * 255).astype(numpy.uint8))
            image = image.resize((300, 300))
            # Convert PIL image to Tkinter-compatible format
            photo = ImageTk.PhotoImage(image)
            # Update the image label
            label.config(image=photo)
            label.image = photo  # Keep a reference to the image to prevent it from being garbage collected            
            
        except Exception as e:
            print(f"Error loading bnr file: {e}") 

    elif file_extension == ".tif" or file_extension == ".tiff":
        from tifffile import imread
        try:
            phase_map = imread(image_path, key=0)
            
            # Normalize the float array to range [0, 1]
            normalized_array = (phase_map - phase_map.min()) / (phase_map.max() - phase_map.min())
            # Create a viridis colormap
            cmap = plt.get_cmap('viridis')
            # Apply the colormap to the normalized array
            cmap_array = cmap(normalized_array)
            # Convert the matplotlib array to a PIL image
            image = Image.fromarray((cmap_array[:, :, :3] * 255).astype(numpy.uint8))
            image = image.resize((300, 300))
            # Convert PIL image to Tkinter-compatible format
            photo = ImageTk.PhotoImage(image)
            # Update the image label
            label.config(image=photo)
            label.image = photo  # Keep a reference to the image to prevent it from being garbage collected   

        except Exception as e:
            print(f"Error loading tif / tiff file: {e}") 

    else:
        try:
            image = cv2.imread(image_path)
            
            pil_image = Image.fromarray(image)
            pil_image = pil_image.resize((300, 300))
            # Convert the PIL Image to an ImageTk PhotoImage
            photo = ImageTk.PhotoImage(image=pil_image)
            # Set the image in the label
            label.config(image=photo)
            label.image = photo  # Keep a reference to the image to prevent garbage collection
        except Exception as e:
            print(f"Error loading image: {e}")
            
# Function to read an image file (.png;.jpg;.jpeg;.bmp;.tif;.tiff; LynceeTec: .bin;.bnr)
# and transform it to RGB format (array of dimensions H*W*3)
def path_to_RGB(image_path):
    
    file_name, file_extension = path.splitext(image_path)
    if file_extension == ".bin": 
        import binkoala
        try:
            (phase_map,in_file_header)=binkoala.read_mat_bin(image_path)
            
            # Normalize the float array to range [0, 1]
            normalized_array = (phase_map - phase_map.min()) / (phase_map.max() - phase_map.min())
            # Create a viridis colormap
            cmap = plt.get_cmap('viridis')
            # Apply the colormap to the normalized array
            cmap_array = cmap(normalized_array)
            # extract first 3 planes and rescale:            
            RGB_image = cmap_array[:, :, :3]* 255
            
        except Exception as e:
            print(f"Error loading bin file: {e}") 
            
    elif file_extension == ".bnr": 
        try:
            #get header info:
            fileID = open(image_path, 'rb')
            nImages = numpy.fromfile(fileID, dtype="i4", count=1)
            nImages = nImages[0]
            w = numpy.fromfile(fileID, dtype="i4", count=1)
            w=w[0]
            h = numpy.fromfile(fileID, dtype="i4", count=1)
            h=h[0]
            pz = numpy.fromfile(fileID, dtype="f4", count=1)
            wave = numpy.fromfile(fileID, dtype="f4", count=1)
            n_1 = numpy.fromfile(fileID, dtype="f4", count=1)
            n_2 = numpy.fromfile(fileID, dtype="f4", count=1)
            #timestamps = numpy.fromfile(fileID, dtype="i4", count=nImages)
            timestamps = [0] * nImages
            for k in range(0,nImages):
                x=numpy.fromfile(fileID, dtype="i4", count=1)
                timestamps[k] = x[0]
            #get first image from sequence
            phase_map = numpy.zeros((h,w))
            for k in range(h):
                phase_map[k,:] = numpy.fromfile(fileID, dtype="f4", count=w)
            phase_map=numpy.single(phase_map)
            fileID.close
            
            #display image
            # Normalize the float array to range [0, 1]
            normalized_array = (phase_map - phase_map.min()) / (phase_map.max() - phase_map.min())
            # Create a viridis colormap
            cmap = plt.get_cmap('viridis')
            # Apply the colormap to the normalized array
            cmap_array = cmap(normalized_array) # matrix with dimensions (H,W,4), 4th plane are only "1"s
            # extract first 3 planes and rescale:            
            RGB_image = cmap_array[:, :, :3]* 255
            
        except Exception as e:
            print(f"Error loading bnr file: {e}") 

    elif file_extension == ".tif" or file_extension == ".tiff":
        from tifffile import imread
        try:
            phase_map = imread(image_path, key=0)
            
            # Normalize the float array to range [0, 1]
            normalized_array = (phase_map - phase_map.min()) / (phase_map.max() - phase_map.min())
            # Create a viridis colormap
            cmap = plt.get_cmap('viridis')
            # Apply the colormap to the normalized array        
            cmap_array = cmap(normalized_array)
            # extract first 3 planes and rescale:            
            RGB_image = cmap_array[:, :, :3]* 255

        except Exception as e:
            print(f"Error loading tif / tiff file: {e}") 

    else:
        try:
            RGB_image = cv2.imread(image_path)
            
        except Exception as e:
            print(f"Error loading image: {e}")
    
    return RGB_image