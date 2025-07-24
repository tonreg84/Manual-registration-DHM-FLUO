import os
from tkinter import messagebox
import numpy as np
import cv2
from tifffile import imread, imsave
import binkoala

def Stack_registration(root, stack_path, ref_width, ref_height, scaling_factor, x_shift, y_shift):
        
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
    
    if file_extension != ".bin" and file_extension != ".bnr" and file_extension != ".tif" and  file_extension != ".tiff":
        print("Stack registration cancelled. File format not valid.")
    
    if file_extension == ".bin":
        # registration for "LynceeTec bin files" (every file is a single frame of a DHM recording)
        
        binfolder=os.path.dirname(stack_path)
        print("Working on folder",binfolder)
        
        # get the list of bin files to process
        bin_files = []
        bin_files = sorted([f for f in os.listdir(binfolder) if f.endswith(('.bin'))])
        
        new_folder = binfolder + "/registered"
        
        if not os.path.isdir(new_folder):
            os.mkdir(new_folder)
        
        if len(os.listdir(new_folder)) != 0:
            answ = messagebox.askquestion('Output folder is not empty!', 'Output folder is not empty.\nDo you want to proceed?')
            print("Output folder is not empty:\n",binfolder)
        else: 
            answ = "yes"
        if answ == "no":
            print("Stack registration cancelled.")
        if answ == "yes":
            k=0
            for file in bin_files:
                
                infile = binfolder+'/'+file

                print("Processing:",infile)
                #load bin-file #k
                (phase_map,in_file_header)=binkoala.read_mat_bin(infile)
                w=in_file_header['width'][0]
                h=in_file_header['height'][0]
                pz=in_file_header['px_size'][0]
                hconv=in_file_header['hconv'][0]
                
                # rescale image
                height = round(h* scaling_factor)
                width = round(w* scaling_factor)
                new_pixel_size = pz/scaling_factor
                phase_map = cv2.warpPerspective(phase_map, Hscale, (width, height))
                
                # initialize the larger image
                larger_image_height = max(ref_height,height)
                larger_image_width = max(ref_width,width)
                larger_image = np.full((larger_image_height,larger_image_width), 0.500, dtype=np.float32)
                
                # Add rescaled image
                larger_image[0:height, 0:width] = phase_map

                # shift image
                larger_image = cv2.warpPerspective(larger_image, Hshift, (larger_image_width, larger_image_height))
                
                # crop to reference size
                c_height = min(ref_height,height)
                c_width = min(ref_width,width)
                cropped = larger_image[0:c_height, 0:c_width]
                
                #save new bin-file #k
                outfile=new_folder+'/'+file
                binkoala.write_mat_bin(outfile, cropped, c_width, c_height, new_pixel_size, hconv, unit_code=1)
    
            print("Stack registration completed.")
    
    if file_extension == '.tif' or file_extension == '.tiff':
        from tiffs_or_tiffS import tiffs_or_tiffS
        
        (go_on,tiff_type)=tiffs_or_tiffS(root)
        
        print(tiff_type)
        
        if go_on:
            
            if tiff_type == 'singleframe':
                # Registration of single-frame files)

                tif_folder = os.path.dirname(stack_path)
                print("Working on folder",tif_folder)

                tif_files = []
                
                if file_extension == ".tif":
                    tif_files = sorted([f for f in os.listdir(tif_folder) if f.endswith(('.tif'))])
                elif file_extension == ".tiff":
                    tif_files = sorted([f for f in os.listdir(tif_folder) if f.endswith(('.tiff'))])
                    
                print(tif_files)
                
                new_folder=os.path.join(tif_folder,"registered")
                print(new_folder)
                
                if not os.path.isdir(new_folder):
                    os.mkdir(new_folder)
                    
                if len(os.listdir(new_folder)) != 0:
                    answ = messagebox.askquestion('Output folder is not empty!', 'Output folder is not empty.\nDo you want to proceed?')
                    print("Output folder is not empty:\n",new_folder)
                else: 
                    answ = "yes"
                if answ == "no":
                    print("Stack registration cancelled.")
                if answ == "yes":
                    print("hererr")
                    
                    dummy_path = os.path.join(new_folder,"dummy.bin")
        
                    for file in tif_files:
                        
                        file_path = os.path.join(tif_folder,file) 
                        print("Processing:",file_path)
                        phase_map = imread(file_path, key=0)
                        
                        height, width = phase_map.shape
            
                        # rescale image
                        height = round(height* scaling_factor)
                        width = round(width* scaling_factor)
                        phase_map = cv2.warpPerspective(phase_map, Hscale, (width, height))
                        
                        # initialize the larger image
                        larger_image_height = max(ref_height,height)
                        larger_image_width = max(ref_width,width)
                        larger_image = np.full((larger_image_height,larger_image_width), 0.500, dtype=np.float32)
                        
                        # Add rescaled image
                        larger_image[0:height, 0:width] = phase_map

                        # shift image
                        larger_image = cv2.warpPerspective(larger_image, Hshift, (larger_image_width, larger_image_height))
                        
                        # crop to reference size
                        c_height = min(ref_height,height)
                        c_width = min(ref_width,width)
                        cropped = larger_image[0:c_height, 0:c_width]
                        
                        # save new file
                        binkoala.write_mat_bin(dummy_path, cropped, c_width, c_height, 1, 1.05997195e-07, unit_code=1)
                        (new_phase_map,in_file_header)=binkoala.read_mat_bin(dummy_path)
                        new_file = os.path.join(new_folder,file)
                        imsave(new_file, new_phase_map, photometric='minisblack', compression=5, append=False, bitspersample=32, planarconfig=1, subfiletype=3)
                    os.remove(dummy_path)
                    print("Stack registration completed.")
            
            if tiff_type == 'stack':
                print("Registration for tiff-stack under construction...")

      
    if file_extension == ".bnr":
        # registration for a "LynceeTec bnr file" (a stack of frames of a DHM recording)       
        
        print("Registration canceled. This partis under construction.")
        
        # new_file = file_name + "_registered.bnr"
        # print(new_file)
        
        # if os.path.isfile(new_file):
        #     answ = messagebox.askquestion('Output file exist already!', 'Output file exist already.\nDo you want to overwrite?')
        # else: 
        #     answ = "yes"
        
        # if answ == "yes":
            
        #     # get metadata from input file
        #     infileID = open(stack_path, 'rb')
        #     nImages = np.fromfile(infileID, dtype="i4", count=1)
        #     nImages = nImages[0]
        #     w = np.fromfile(infileID, dtype="i4", count=1)
        #     w = w[0]
        #     h = np.fromfile(infileID, dtype="i4", count=1)
        #     h = h[0]
        #     pz = np.fromfile(infileID, dtype="f4", count=1)
        #     pz = pz[0]
        #     wavelength = np.fromfile(infileID, dtype="f4", count=1)
        #     wavelength = wavelength[0]
        #     n_1 = np.fromfile(infileID, dtype="f4", count=1)
        #     n_1 = n_1[0]
        #     n_2 = np.fromfile(infileID, dtype="f4", count=1)
        #     n_2 = n_2[0]
            
        #     #timestamps = numpy.fromfile(fileID, dtype="i4", count=nImages)
        #     timestamps = [0] * nImages
        #     for k in range(0,nImages):
        #         TTT = np.fromfile(infileID, dtype="f4", count=1)
        #         timestamps[k] = TTT[0]
                
        #     height = round(h* scaling_factor)
        #     width = round(w* scaling_factor)
        #     new_pixel_size = pz/scaling_factor
            
        #     larger_image_height = max(ref_height,height)
        #     larger_image_width = max(ref_width,width)
            
        #     # for crop to reference size
        #     c_height = min(ref_height,height)
        #     c_width = min(ref_width,width)
            
        #     # write meta data to new bnr file
        #     outfileID=open(new_file,'wb')
        #     np.array(nImages, dtype=np.int32).tofile(outfileID)
        #     np.array(c_width, dtype=np.int32).tofile(outfileID)
        #     np.array(c_height, dtype=np.int32).tofile(outfileID)
        #     np.array(new_pixel_size, dtype=np.float32).tofile(outfileID)
        #     np.array(wavelength, dtype=np.float32).tofile(outfileID)
        #     np.array(n_1, dtype=np.float32).tofile(outfileID)
        #     np.array(n_2, dtype=np.float32).tofile(outfileID)
        #     for k in range(0,nImages):
        #         np.array(timestamps[k], dtype=np.float32).tofile(outfileID)
            
        #     # initialize phase_map container
        #     phase_map = np.zeros((h,w))
        #     phase_stack = np.zeros((c_height,c_width,nImages))
            
        #     #read the frames of the stack 
        #     for i in range(nImages):
                
        #         print(f"Reading frames {i} of {nImages}")
                
        #         # read frame #i:
        #         for k in range(h):
        #             phase_map[k,:] = np.fromfile(infileID, dtype="f4", count=w)
                
        #         # rescale image
        #         rescaled = cv2.warpPerspective(phase_map, Hscale, (width, height))
                
        #         # initialize the larger image
        #         larger_image = np.full((larger_image_height,larger_image_width), 0.500, dtype=np.float32)
                
        #         # Add rescaled image
        #         larger_image[0:height, 0:width] = rescaled
                
        #         # shift image
        #         larger_image = cv2.warpPerspective(larger_image, Hshift, (larger_image_width, larger_image_height))
                
        #         # crop to reference size
        #         cropped = larger_image[0:c_height, 0:c_width]
                
        #         # add to stack
        #         phase_stack[:,:,i] = cropped
                
        #     infileID.close
            
        #     # write meta data to new bnr file
        #     outfileID=open(new_file,'w')
        #     np.array(nImages, dtype=np.int32).tofile(outfileID)
        #     np.array(c_width, dtype=np.int32).tofile(outfileID)
        #     np.array(c_height, dtype=np.int32).tofile(outfileID)
        #     np.array(new_pixel_size, dtype=np.float32).tofile(outfileID)
        #     np.array(wavelength, dtype=np.float32).tofile(outfileID)
        #     np.array(n_1, dtype=np.float32).tofile(outfileID)
        #     np.array(n_2, dtype=np.float32).tofile(outfileID)
        #     for k in range(0,nImages):
        #         np.array(timestamps[k], dtype=np.float32).tofile(outfileID)
            
        #     # write the frames to the new bnr file
        #     for i in range(nImages):
                
        #         print(f"Writing frames {i} of {nImages}")
                
        #         frame = phase_stack[:,:,i]
        #         print(frame.shape)
                
        #         #write frame to new bnr file
        #         frame.astype(np.float32).tofile(outfileID)

        #     outfileID.close
            
        #     print("Stack registration completed.")
            
    