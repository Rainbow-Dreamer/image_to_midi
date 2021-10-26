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
 
 Note: Each pixel of the image will convert to a note with a MIDI channel based on its color depth, the lighter the pixel is, the smaller the MIDI channel number of the note it corresponds to is, you should customize the colors corresponding to MIDI channels 0 - 15 from lightest to deepest in order to get the best viewing result when you put the resulted MIDI files in DAW or piano roll software.
 ## Installation
 You can use pip to install this package, run this line in cmd/terminal to install.
 ```
 pip install image_to_midi
 ```
 
 ## Usage
 Firstly we will talk about the conversion parameters of this pacakge.
 * ascii_character_set: The ASCII character set that ranges from deepest to lightest color depth. The default value is ``M@N%W$E#RK&FXYI*l]}1/+i>"!~\';,`:.``
 * resize_ratio: The resize ratio of the image to convert, could be an integer or a float, the smaller it is, the larger the image will be resized to, for example, 1 is for no resizing, 0.5 is for resize as 2 times large, 2 is for resize as 2 times small. The default value is 1
 * bit_number: The bit number the image will be converted as gray scales. The default value is 8
 * image_width_ratio: the width resize ratio of the image. The default value is 1
 * image_height_ratio: the height resize ratio of the image. The default value is 1
 
 You can change these parameters by `set_value` function using keyword arguments.
 ```python
 set_value(resize_ratio=2)
 ```
 
