Manual registration DHM-FLUO
Autor: tonreg, team UMI, CNP-CHUV Lausanne
 
Version 01 - 30.09.2024

Program suite to rescale and align microscopy images. A source image is transformed in reference to another image. For example a DHM image and a epifluorescence image.

How to use the program suite:

Main.py - main GUI:
Use it to load the source and the reference images, to display them, and to call the sub GUIs "Get_scaling_factor.py" and "Shift_it.py". You can run the sub GUIs directly from an IDE, too. Anyway, you need to load a reference image and a (rescaled) source image.
Possible image formats: .png, .jpg, .jpeg, .bmp, .tif, .tiff, as well as the LynceeTec formats .bin and .bnr

We are assume the same scaling factor for image width and height.

Get_scaling_factor.py
- Program to find the scaling factor (alternative ways to find the scaling factor: take the ratio of the pixel sizes, find the scaling factor manually using imageJ fro example)
- Shows the images in real size, i.e., if the image is 800x800 pixels, it will take 800x800 pixels of the screen to show it. Therfore, you need to crop bigger images before loading them (mind to keep the most interesting ROI).
- Find landmarks, which are clearly indentifiable in reference and source image. Double click every landmark in both, reference and source image. The order of clicking is important!
- Try to find landmarks as far from each other as possible and as many as possible.
- At least 2 landmarks per image are needed. 

Shift-it.py
- Program to find the x and y pixel shift (rigid translation)
- Gives out "image_shifted_final.png" and "image_shifted_overlay.png"
