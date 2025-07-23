Manual registration DHM-FLUO
Autor: tonreg, team UMI, CNP-CHUV Lausanne

Program suite to rescale and align microscopy images.
- A source image is transformed in reference to another image to obtain a scaling factor and a x-y shift. For example a DHM image and a epifluorescence image.
- An image sequence can be registered with a scaling factor and a constant x-y shift

How to use the program suite:

Main.py - main GUI:
To load the source and the reference images, display them, and call the sub GUIs "Rough.py", "Get_scaling_factor.py", and "Shift_it.py". You can run the sub GUIs directly, too.
Possible image formats: .png, .jpg, .jpeg, .bmp, .tif, .tiff, as well as the LynceeTec formats .bin and .bnr

We are assume the same scaling factor for image width and height.

Sub-GUIs:

Rough.py: GUI to find a "rough" shift and scaling (can be sufficient for your needs) and to define a crop for the reference image
- You can drag the semi-transparent source (DHM) image over the reference for a rough shift.
- You can rescale the source image by pressing the "up" or "down" key on your keyboard for a rough scaling
- You can define a crop for the reference (Fluo) image: Click on the button "Activate drawing mode", then draw a rectangle on the screen. The rectangle should contain the whole DHM image. This crop will apply when closing the Rough GUI and opening another 
Close this window with the button "Rough shift and crop done". This gives the crop and rough shift parameter back to the main window.
Now you can open the "Shift" window to get a more precise shift. You will see that these windows will use the cropped reference. Or you can directly do a stack alignment.

Get_scaling_factor.py :
- Program to find the scaling factor (alternative ways to find the scaling factor: i) Rough.py, ii) take the ratio of the pixel sizes, iii) find the scaling factor manually with imageJ,...)
- Shows the images in real size, i.e., if the image is 800x800 pixels, it will take 800x800 pixels of the screen to show it. Therfore, you need to crop bigger images before loading them (mind to keep the most interesting ROI).
- Find landmarks, which are clearly indentifiable in reference and source image. Double click every landmark in both, reference and source image. The order of clicking is important!
- Try to find landmarks as far from each other as possible and as many as possible.
- At least 2 landmarks per image are needed.

Shift-it.py :
- Program to find the x and y pixel shift (rigid translation)
- Can save shifted images ("image_shifted_final.png", "image_shifted_overlay.png")

Load and register a whole image sequence (Button "Load stack and process"):
- For file-types "LynceeTec BIN" or tif/tiff (every file is a single frame of a DHM recording), or "LynceeTec BNR" (single-file stack)
- Select the first file of the stack
- bin/if/tiff : saves the modified bin files in a new folder "registered"
- bnr : creates a new file with suffix "_registered.bnr" / "_registered.tif"

Alternative way to register your sequence: open your sequence with imageJ, use Image-Scale... then Image-Transform-Translate...
