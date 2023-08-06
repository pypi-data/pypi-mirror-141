"""
Module to create cool ascii effects from images

"""

import os

from PIL import Image,ImageDraw,ImageFont
from typing import Union

from . import util



char_pixels        = " .:-=+*#%@"
char_pixels_invert = "@%#*+=-:. "



def save_as_text(in_file:str, out_file: str = "ascii.txt", out_size: Union[list,tuple] = None, pixel_string: str = char_pixels_invert):
    '''
    Saves the ascii version of the input image into a text file.

    Parameters:
        in_file      : Path to input image file
        out_file     : Path to save file ascii text file. (saves into ./ascii.txt by default)
        out_size     : Tuple or list containing width,height info for number of text columns and rows in the output ascii art. 
                      (Default value is None i.e maintains the original width and height)

        pixel_string : String containing characters that represent ascii pixels sorted according to intensity (Darkest first, Brightest last).
                      (Default value is "@%#*+=-:. " with '@' representing darker shades in image, ' ' representing brighter shades or vice versa)

    Example:
        ascii_as_text("image.jpeg",out_file="ascii_file.txt",out_size=[700,500],pixels = "@%#*+=-:. "):
        
        - The above function call attempts to open an image file "image.jpeg", processes it and saves into a text file located at "ascii_file.txt"
          with a size of 700 columns and 500 rows, where "@" represents the darkest character and " " represents the brightest character

    '''

    try:
        with Image.open(in_file) as im:

            #Resize image if required to match output column-row count
            if(out_size is not None):

                if(type(out_size) in [list,tuple]):
                    
                    if(len(out_size) != 2):
                        raise Exception("Expected list or tuple of size 2.")
                    else:
                        if not all(isinstance(x, (int,float)) for x in out_size):
                            raise Exception("Unexpected non-numeric value in input data.")
                        else:
                            im = im.resize(out_size)
                else:
                    raise Exception("Expected list or tuple of size 2. Received {} instead.".format(type(out_size)))                    


            width  = im.width
            height = im.height 

            #Convert image to greyscale and load pixel data
            grey_image  = im.convert("L")
            grey_pixels = list(grey_image.getdata())

            
            #Map pixel data from greyscale (0-255) to ascii pixel intensity
            pixel_indexes = []
            for i in range(len(grey_pixels)):
                val = grey_pixels[i]
                pixel_indexes.append(util.map(val,(0,255),(0,len(pixel_string)-1)))

            
            #Create ascii string representation of image
            cursor = 0
            ascii_text = ""
    
            pixel_list = list(pixel_string)

            for h in range(height):
                for w in range(width):
                    ascii_text += pixel_list[int(pixel_indexes[cursor])]
                    cursor +=1
                ascii_text += "\n"
            
            #save ascii string to file
            with open(out_file,"w") as file:
                file.write(ascii_text)

    except Exception as err:
                print(type(err).__name__,__file__,err.__traceback__.tb_lineno)
                print(err)



def print_ascii(in_file:str, out_size: Union[list,tuple] = None, pixel_string: str = char_pixels):
    '''
    Prints ascii version of the input image onto the console.

    Parameters:
        in_file       : Path to input image file
        out_size      : Sets the number of columns and rows to print ascii image
                        (Default value is None i.e maintains the original width and height)

        pixel_string  : String containing characters sorted according to intensity that represent pixels in the ascii version.
                        (Default value is " .:-=+*#%@" with ' ' representing darker shades in image, '@' representing brighter shades or vice versa)

    '''

    try:
        with Image.open(in_file) as im:

            #Resize image if required to match output column-row count
            if(out_size is not None):

                if(type(out_size) in [list,tuple]):
                    
                    if(len(out_size) != 2):
                        raise Exception("Expected list or tuple of size 2.")
                    else:
                        if not all(isinstance(x, (int,float)) for x in out_size):
                            raise Exception("Unexpected non-numeric value in input data.")
                        else:
                            im = im.resize(out_size)
                else:
                    raise Exception("Expected list or tuple of size 2. Received {} instead.".format(type(out_size)))                    


            width  = im.width
            height = im.height 

            #Convert image to greyscale and load pixel data
            grey_image  = im.convert("L")
            grey_pixels = list(grey_image.getdata())

            
            #Map pixel data from greyscale (0-255) to ascii pixel intensity
            pixel_indexes = []
            for i in range(len(grey_pixels)):
                val = grey_pixels[i]
                pixel_indexes.append(util.map(val,(0,255),(0,len(pixel_string)-1)))

            
            #Create ascii string representation of image
            cursor = 0
            ascii_text = ""
    
            pixel_list = list(pixel_string)

            for h in range(height):
                for w in range(width):
                    ascii_text += pixel_list[int(pixel_indexes[cursor])]
                    cursor +=1
                ascii_text += "\n"
            
            #print ascii string to console
            print(ascii_text)
                
    except Exception as err:
                print(type(err).__name__,__file__,err.__traceback__.tb_lineno)
                print(err)



def save_as_image( in_file:str,  mode:str = "RGB", out_file:str="ascii.png", out_size: Union[list,tuple] = None, font_size:int=10, custom_font:str = None, pixel_string:str = char_pixels, message:str = None):
    '''
    Saves ascii version of input image file as another image file

    Parameters:
        in_file      : Path to input image file
        mode         : Sets the output image color mode. 'L' for greyscale mode and "RGB" to save as coloured image
                       (Default value is "RGB")

        out_file     : Path to save file ascii image file. (saves into ./ascii.png by default)
        out_size     : Tuple or list containing width and height for number of text columns and rows in the output file. 
                       (Default value is None i.e maintains the original width and height)

        font_size    : Font size of ascii text on image
                       (Default size 10)

        custom_font  : Path to custom Truetype or OpenType font
                       (Default font is Courier)
                      

        pixel_string : String containing characters sorted according to intensity that represent pixels in the ascii version.
                      (Default value is " .:-=+*#%@" with ' ' representing darker shades in image, '@' representing brighter shades or vice versa)
        
        message      : Prints the input message over the image. This value is ignored if mode is set as "L"

    Example:
        save_as_image( "image.jpeg", "RGB", "ascii.png", (500,500), message = "Hello"):
        
        - The above function call attempts to open an image file "image.jpeg" in RGB mode, prints the message "Hello" over it continuously. The result is resized into 500x500 and saved into "ascii.png" 


    '''

    try:
         with Image.open(in_file) as im:

            width  = im.width
            height = im.height 

            pixel_list = list(pixel_string)

            
            # Load font
            fnt = None
            if custom_font is not None:
                fnt = ImageFont.truetype(custom_font, font_size)
            else:
                path = os.path.dirname(__file__) + "/assets/courier.ttf"
                fnt = ImageFont.truetype(path, font_size)

            fntsize = fnt.getsize("@")
            fnt_width  = fntsize[0]
            fnt_height = fntsize[1]
            

            # Resize image according to font size so that output image maintains same width and height
            new_width  = int(width  / fnt_width)
            new_height = int(height /  fnt_height)
            im = im.resize((new_width, new_height))


            # Load color as well as greyscale image data
            rgb_pixels = list(im.getdata())

            grey = im.convert("L")
            grey_pixels = list(grey.getdata())


            # Map pixel data from greyscale (0-255) to ascii pixel intensity
            for i in range(len(grey_pixels)):
                val = grey_pixels[i]
                grey_pixels[i] = util.map(val,(0,255),(0,len(pixel_string)-1))


            # Create output image with approx original width and height of input image and get drawing context
            out = Image.new("RGB", (new_width * fnt_width, new_height * fnt_height), (0, 0, 0))
            context = ImageDraw.Draw(out)

            if(mode=="L"):
                #
                # (Greyscale Mode) Create ascii string representation of image and draw into context
                #
                cursor = 0
                ascii_text = ""
                for h in range(new_height):
                    for w in range(new_width):
                        ascii_text += pixel_list[int(grey_pixels[cursor])]
                        cursor +=1
                    ascii_text += "\n"
                context.multiline_text((0,0),ascii_text,font=fnt,fill=(255,255,255))

            elif(mode=="RGB"):
                #
                # Color Mode
                # 
                if message is not None:
                    
                    # Prints custom message if present
                    cursor = 0
                    msg_cursor = 0
                    msg_len = len(message) - 1
                    for h in range(0,new_height * fnt_height,fnt_height):
                        for w in range(0,new_width * fnt_width,fnt_width):
                            context.text((w, h), message[msg_cursor] , font=fnt, fill=rgb_pixels[cursor]) 
                            cursor+=1
                            if msg_cursor < msg_len:
                                msg_cursor += 1
                            else:
                                msg_cursor = 0
                else:
                    # Prints default pixel intensity mappings
                    cursor = 0
                    for h in range(0,new_height * fnt_height,fnt_height):
                        for w in range(0,new_width * fnt_width,fnt_width):
                            context.text((w, h),pixel_list[int(grey_pixels[cursor])] , font=fnt, fill=rgb_pixels[cursor]) 
                            cursor+=1

            
            # Resize image according to specified output size
            if(out_size is not None):
                out = out.resize(out_size)

            # Save image file
            out.save(out_file)

    except Exception as err:
                print(type(err).__name__,__file__,err.__traceback__.tb_lineno)
                print(err)

