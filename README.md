# image_to_midi
 This is a python package that turns any images into MIDI files that views the same as them.
 
 This package firstly convert the image to ASCII characters by pixels in terms of gray scale, and then convert each pixel of the image to a note with a MIDI channel (0 - 15) based on the color depth of the pixel, which is the places of the converted ASCII character of that pixel at the ASCII character set defined by the user. The deeper the color depth of a pixel is, the larger the MIDI channel number of the note it corresponds to is. For example, the pixel with the lightest color of the image will map to MIDI channel 0, while the deepest color will map to MIDI channel 15.
 
 The default ASCII character set is
 ```
 M@N%W$E#RK&FXYI*l]}1/+i>"!~\';,`:.
 ```
 
 You can customize the note interval between each pixel horizontally the unit is bar of 4/4 time signature.
 
 For the direction of the note transformation through the images, there are basically 2 directions, one is for viewing in a DAW, and the another one is for viewing in a piano roll software with a waterfall effect (dropping from the top). You can also customize the rotation angle of the image to transform, together with whether to flip the image or not.
 
 You can also choose to filter out the light colors you don't want to have in the resulted MIDI files according to a color depth tolerance.
 
 **Note: Each pixel of the image will convert to a note with a MIDI channel based on its color depth, the lighter the pixel is, the smaller the MIDI channel number of the note it corresponds to is, you should customize the colors corresponding to MIDI channels 0 - 15 from lightest to deepest in order to get the best viewing result when you put the resulted MIDI files in DAW or piano roll software.**
 
 ## Installation
 You can use pip to install this package, run this line in cmd/terminal to install.
 ```
 pip install image_to_midi
 ```
 
 ## Importing
 ```python
 import image_to_midi as im
 ```
 
 ## Usage
 Firstly we will talk about the conversion parameters of this pacakge.
 
 This package uses a dictionary called `config_dict` to store the image conversion parameters, which are
 
 * ascii_character_set: The ASCII character set that ranges from deepest to lightest color depth. The default value is ``M@N%W$E#RK&FXYI*l]}1/+i>"!~\';,`:.``
 * resize_ratio: The resize ratio of the image to convert, could be an integer or a float, the smaller it is, the larger the image will be resized to, for example, 1 is for no resizing, 0.5 is for resize as 2 times large, 2 is for resize as 2 times small. The default value is 1
 * bit_number: The bit number the image will be converted as gray scales. The default value is 8
 * image_width_ratio: the width resize ratio of the image. The default value is 1
 * image_height_ratio: the height resize ratio of the image. The default value is 1
 
 You can change these parameters by updating the values of the corresponding key of `config_dict`. For example,
 ```python
 im.config_dict['resize_ratio'] = 2
 ```
 
 Then we will talk about how to convert images to MIDI files using this package. You can use `image_to_midi` function to convert an image to a MIDI file.
 
 **Note: the return value of this function is a musicpy's chord instance, you can use musicpy's `write` function to write the return value to a MIDI file.**
 
 ```python
 image_to_midi(path,
               direction=0,
               max_keys=130,
               line_interval=1 / 16,
               remapping_colors=None,
               filter_value=None,
               extra_interval=0,
               adjust_scale=None,
               rotate=None,
               whole_reverse=False,
               each_line_reverse=False)
```

* path: the file path of the image

* direction: there are 3 direction modes: 0, 1, other values  
0: from left to right, used in daw representation  
1: from buttom to top, used in piano roll representation  
other values: you can custom the rotation angle of the images and whether reverse the image ascii list and each line or not

* max_keys: the maximum key number the MIDI file has, when converting the image, if the line has more pixels than this parameter, then the exceeded part will be cut off

* line_interval: the duration of notes of each line of pixels of the image, the unit is bar of 4/4 time signature

* remapping_colors: you can pass in a dictionary to remap the MIDI channel numbers to a new order of MIDI channel numbers

* filter_value: you can set an index of the ASCII character set to filter out the ASCII characters to convert which index is after this value

* extra_interval: you can set this value if you want to have extra spaces between each 2 adjacent lines of notes

* adjust_scale: adjust the notes of each line of pixels to a scale like C major, D mixolydian, it will filter out the notes that does not belong to the scale of each line of notes, this value must be a musicpy's scale instance

* rotate: when the parameter `direction` is set to a value that is not 0 or 1, you can set this value to specify the rotation angle of the image to convert, the rotation angle is clockwise for positive number, counterclockwise for negative number

* whole_reverse: when the parameter `direction` is set to a value that is not 0 or 1, you can set this value to specify whether to reverse the lines of pixels of the image

* each_line_reverse: when the parameter `direction` is set to a value that is not 0 or 1, you can set this value to specify whetehr to reverse each line of pixels of the image

You can use musicpy's `write` function to write the return value of this function to a MIDI file.
```python
result = im.image_to_midi('1.jpg')
im.write(result, name='1.mid')
```

## Some extra notes
The starting note pitch of the conversion is C0, which corresponds to MIDI note number 12. (If it starts from 0 then we will have some notes has pitch like `B-1`, which cannot be shown in most DAW and piano roll softwares)

If you would like to fit the resulted MIDI files into a standard 88-keys piano which has pitch range A0 to C8, it is easy to firstly set the `max_key` parameter to 88 and then use `up` function of chord type of musicpy to shift the resulted chord type to be starting from A0, like `result = result.up(9)`, since the MIDI note number of A0 is 21.
