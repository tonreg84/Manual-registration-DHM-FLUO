import os
from tkinter import messagebox
import numpy as np
import cv2
from tifffile import imread, imsave
import binkoala

def Stack_registration(stack_path, ref_width, ref_height, scaling_factor, x_shift, y_shift):
    larger_image_width = ref_width # max(ref_width,sdasdsa)
    larger_image_height = ref_height # max(ref_height,asdasdasd)
        
    # create homography matrix for scaling
    Hscale = np.zeros((3, 3))
    Hscale[0,0] = scaling_factor
    Hscale[1,1] = scaling_factor
    Hscale[2,2] = 1
    Hscale[0,2] = 0
    Hscale[1,2] = 0   
    
    # create homography matrix for shifting
    Hshift = np.zeros((3, 3))
    Hshift[0,0] = 1
    Hshift[1,1] = 1
    Hshift[2,2] = 1
    Hshift[0,2] = x_shift
    Hshift[1,2] = y_shift    
    
    file_name, file_extension = os.path.splitext(stack_path)
    
    # registration for "LynceeTec bin files" (every file is a single frame of a DHM recording)
    if file_extension == ".bin":
        
        binfolder=os.path.dirname(stack_path)
        
        new_folder = binfolder + "/registered"
        
        if not os.path.isdir(new_folder):
            os.mkdir(new_folder)
        
        if len(os.listdir(new_folder)) != 0:
            answ = messagebox.askquestion('Output folder is not empty!', 'Output folder is not empty.\nDo you want to proceed?')
        else: 
            answ = "yes"
        
        if answ == "yes":
            
            file = binfolder + '/00000'+'_phase.bin'
            
            if not os.path.isfile(file):
                messagebox.showinfo('Error', 'File 00000_phase.bin missing.')
            else:
                
                bincheck = True
                k=0
                while bincheck == True:
                    
                    infile = binfolder+'/'+str(k).rjust(5, '0')+'_phase.bin'
                    
                    if os.path.isfile(infile):
                        
                        print("Processing:",infile)
                        #load bin-file #k
                        (phase_map,in_file_header)=binkoala.read_mat_bin(infile)
                        w=in_file_header['width'][0]
                        h=in_file_header['height'][0]
                        pz=in_file_header['px_size'][0]
                        hconv=in_file_header['hconv'][0]
                        
                        # rescale image
                        new_height = round(h* scaling_factor)
                        new_width = round(w* scaling_factor)
                        new_pixel_size = pz/scaling_factor
                        new_phase_map = cv2.warpPerspective(phase_map, Hscale, (new_width, new_height))
                        
                        # Create the larger image with the specified background value
                        larger_image = np.full((larger_image_height,larger_image_width), 0.500, dtype=np.float32)
                        
                        # shift image
                        # Determine the placement region in the larger image
                        start_row = y_shift
                        start_col = x_shift
                        end_row = y_shift + new_height
                        end_col = x_shift + new_width
                        
                        # Place the smaller image in the larger one
                        larger_image[start_row:end_row, start_col:end_col] = new_phase_map
                        
                        #save new bin-file #k
                        outfile=new_folder+'/'+str(k).rjust(5, '0')+'_phase.bin'
                        binkoala.write_mat_bin(outfile, larger_image, larger_image_width, larger_image_height, new_pixel_size, hconv, unit_code=1)
                        
                    else: 
                        bincheck = False
                    
                    k = k+1
    
    tif_files = []
    # registration for "tiff files" (every file is a single frame of a DHM recording)
    if file_extension == ".tif":
        tif_files = sorted([f for f in os.listdir(os.path.dirname(stack_path)) if f.endswith(('.tif'))])
    elif file_extension == ".tiff":
        tif_files = sorted([f for f in os.listdir(os.path.dirname(stack_path)) if f.endswith(('.tiff'))])
    
    if len(tif_files) != 0:
        registered_folder=os.path.join(os.path.dirname(stack_path),"registered")
        if not os.path.isdir(registered_folder):
            os.mkdir(registered_folder)
            
        if len(os.listdir(registered_folder)) != 0:
            answ = messagebox.askquestion('Output folder is not empty!', 'Output folder is not empty.\nDo you want to proceed?')
        else: 
            answ = "yes"
        
        if answ == "yes":
            
            dummy_path = os.path.dirname(stack_path) + "/dummy.bin"

            for file in tif_files:
                
                file_path = os.path.join(os.path.dirname(stack_path),file) 
                print("Processing:",file_path)
                phase_map = imread(file_path, key=0)
                
                height, width = phase_map.shape
    
                # rescale image
                new_height = round(height* scaling_factor)
                new_width = round(width* scaling_factor)
                new_phase_map = cv2.warpPerspective(phase_map, Hscale, (new_width, new_height))

                # Create the larger image with the specified background value
                larger_image = np.full((larger_image_height,larger_image_width), 0.500, dtype=np.float32)
                
                # shift image
                # Determine the placement region in the larger image
                start_row = y_shift
                start_col = x_shift
                end_row = y_shift + new_height
                end_col = x_shift + new_width
                                
                # Place the smaller image in the larger one
                larger_image[start_row:end_row, start_col:end_col] = new_phase_map
                
                # save new file
                binkoala.write_mat_bin(dummy_path, larger_image, larger_image_width, larger_image_height, 1, 1.05997195e-07, unit_code=1)
                
                (new_phase_map,in_file_header)=binkoala.read_mat_bin(dummy_path)
                
                new_file = os.path.join(registered_folder,file)
                
                imsave(new_file, new_phase_map, photometric='minisblack', compression=5, append=False, bitspersample=32, planarconfig=1, subfiletype=3)
            os.remove(dummy_path)

    # registration for a "LynceeTec bnr file" (a stack of frames of a DHM recording)             
    if file_extension == ".bnr":
        
        new_file = file_name + "_registered.bnr"
        print(new_file)
        
        if os.path.isfile(new_file):
            answ = messagebox.askquestion('Output file exist already!', 'Output file exist already.\nDo you want to overwrite?')
        else: 
            answ = "yes"
        
        if answ == "yes":
            
            #get metadata from input file
            infileID = open(stack_path, 'rb')
            nImages = np.fromfile(infileID, dtype="i4", count=1)
            nImages = nImages[0]
            w = np.fromfile(infileID, dtype="i4", count=1)
            w=w[0]
            h = np.fromfile(infileID, dtype="i4", count=1)
            h=h[0]
            pz = np.fromfile(infileID, dtype="f4", count=1)
            pz=pz[0]
            wavelength = np.fromfile(infileID, dtype="f4", count=1)
            wavelength=wavelength[0]
            n_1 = np.fromfile(infileID, dtype="f4", count=1)
            n_1 = n_1[0]
            n_2 = np.fromfile(infileID, dtype="f4", count=1)
            n_2 = n_2[0]
            
            #timestamps = numpy.fromfile(fileID, dtype="i4", count=nImages)
            timestamps = [0] * nImages
            for k in range(0,nImages):
                timestamps[k] = np.fromfile(infileID, dtype="f4", count=1)
                
            new_height = round(h* scaling_factor)
            new_width = round(w* scaling_factor)
            new_pixel_size = pz/scaling_factor
            
            #write meta data to new bnr file
            outfileID=open(new_file,'w')
            np.array(nImages, dtype=np.int32).tofile(outfileID)
            np.array(larger_image_width, dtype=np.int32).tofile(outfileID)
            np.array(larger_image_height, dtype=np.int32).tofile(outfileID)
            np.array(new_pixel_size, dtype=np.float32).tofile(outfileID)
            np.array(wavelength, dtype=np.float32).tofile(outfileID)
            np.array(n_1, dtype=np.float32).tofile(outfileID)
            np.array(n_2, dtype=np.float32).tofile(outfileID)
            for k in range(0,nImages):
                np.array(timestamps[k], dtype=np.float32).tofile(outfileID)
            
            # initialize phase_map container
            phase_map = np.zeros((h,w))
            
            #read the frames of the stack 
            for i in range(nImages):
                
                # read frame #i:
                for k in range(h):
                    
                    phase_map[k,:] = np.fromfile(infileID, dtype="f4", count=w)
                
                # transform image
                new_phase_map = cv2.warpPerspective(phase_map, Hscale, (new_width, new_height))
                
                # Create the larger image with the specified background value
                larger_image = np.full((larger_image_height,larger_image_width), 0.500, dtype=np.float32)
                
                # shift image
                # Determine the placement region in the larger image
                start_row = y_shift
                start_col = x_shift
                end_row = y_shift + new_height
                end_col = x_shift + new_width           
                # Place the smaller image in the larger one
                larger_image[start_row:end_row, start_col:end_col] = new_phase_map
                
                #write frame to new bnr file
                larger_image.astype(np.float32).tofile(outfileID)
                
            infileID.close
            outfileID.close