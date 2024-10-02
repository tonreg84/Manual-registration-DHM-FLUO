import os
from tkinter import messagebox
import numpy as np
import cv2

def stack_registration(stack_path, scaling_factor, x_shift, y_shift):
        
    # create homography matrix
    H = np.zeros((3, 3))
    H[0,0] =  scaling_factor
    H[1,1] =  scaling_factor
    H[2,2] = 1
    H[0,2] = x_shift
    H[1,2] = y_shift    
    
    file_name, file_extension = os.path.splitext(stack_path)
    
    # registration for "LynceeTec bin files" (every file is a single frame of a DHM recording)
    if file_extension == ".bin":
        import binkoala
        
        binfolder=os.path.dirname(stack_path)
        
        new_folder = binfolder + "/registered"
        print(new_folder)
        
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
                        
                        #load bin-file #k
                        (phase_map,in_file_header)=binkoala.read_mat_bin(infile)
                        w=in_file_header['width'][0]
                        h=in_file_header['height'][0]
                        pz=in_file_header['px_size'][0]
                        hconv=in_file_header['hconv'][0]
                        
                        # transform image
                        new_height = round(h* scaling_factor)
                        new_width = round(w* scaling_factor)
                        new_pixel_size = pz/scaling_factor
                        new_phase_map = cv2.warpPerspective(phase_map, H, (new_width, new_height))
                        
                        #save new bin-file #k
                        outfile=new_folder+'/'+str(k).rjust(5, '0')+'_phase.bin'
                        binkoala.write_mat_bin(outfile, new_phase_map, new_width, new_height, new_pixel_size, hconv, unit_code=1)
                        
                    else: 
                        bincheck = False
                    
                    k = k+1
        
    # registration for a "LynceeTec bnr file" (a stack of frames of a DHM recording)             
    if file_extension == ".bnr":
        import binkoala
        
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
            np.array(new_width, dtype=np.int32).tofile(outfileID)
            np.array(new_height, dtype=np.int32).tofile(outfileID)
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
                new_phase_map = cv2.warpPerspective(phase_map, H, (new_width, new_height))
                
                #write frame to new bnr file
                new_phase_map.astype(np.float32).tofile(outfileID)
                
            infileID.close
            outfileID.close


        
        