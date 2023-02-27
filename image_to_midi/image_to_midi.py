from musicpy import *
from PIL import Image, ImageFont, ImageDraw, ImageTk

config_dict = {
    'ascii_character_set': 'M@N%W$E#RK&FXYI*l]}1/+i>"!~\';,`:.',
    'resize_ratio': 1,
    'bit_number': 8,
    'image_width_ratio': 1,
    'image_height_ratio': 1,
    'colored_images': False
}


def get_char(r, g, b, unit, ascii_character_set):
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    return ascii_character_set[int(gray / unit)]


def img_to_ascii(path,
                 output=False,
                 name='Untitled.txt',
                 rotate=0,
                 max_height=None,
                 max_width=None):
    ascii_character_set = config_dict['ascii_character_set']
    bit_number = config_dict['bit_number']
    resize_ratio = config_dict['resize_ratio']
    image_width_ratio = config_dict['image_width_ratio']
    image_height_ratio = config_dict['image_height_ratio']
    colored_images = config_dict['colored_images']
    length = len(ascii_character_set)
    K = 2**bit_number
    unit = (K + 1) / length
    im = Image.open(path)
    if rotate != 0:
        im = im.rotate(-rotate, expand=True)
    WIDTH = int((im.width * image_width_ratio / 6) / resize_ratio)
    HEIGHT = int((im.height * image_height_ratio / 12) / resize_ratio)
    im_resize = im.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    txt = ""
    if max_height:
        HEIGHT = min(HEIGHT, max_height)
    if max_width:
        WIDTH = min(WIDTH, max_width)
    if colored_images:
        im_txt = Image.new(
            "RGB",
            (int(im.width / resize_ratio), int(im.height / resize_ratio)),
            (2**bit_number - 1, 2**bit_number - 1, 2**bit_number - 1))
        colors = []
        for i in range(HEIGHT):
            for j in range(WIDTH):
                pixel = im_resize.getpixel((j, i))[:3]
                colors.append(pixel)
                txt += get_char(*pixel, unit, ascii_character_set)
            txt += '\n'
            colors.append((255, 255, 255))
        if output:
            with open(name, 'w') as f:
                f.write(txt)
        return txt, colors, im_txt
    else:
        for i in range(HEIGHT):
            for j in range(WIDTH):
                pixel = im_resize.getpixel((j, i))[:3]
                txt += get_char(*pixel, unit, ascii_character_set)
            txt += '\n'
        if output:
            with open(name, 'w') as f:
                f.write(txt)
        return txt


def image_to_midi(path,
                  direction=0,
                  max_keys=100,
                  line_interval=1 / 16,
                  remapping_colors=None,
                  filter_value=None,
                  extra_interval=0,
                  adjust_scale=None,
                  rotate=None,
                  whole_reverse=False,
                  each_line_reverse=False,
                  start='C0'):
    # there are 3 direction modes: 0, 1, other values

    # 0: from left to right, used in daw representation

    # 1: from buttom to top, used in piano roll representation

    # other values: you can custom the rotation angle of the images and
    # whether reverse the image ascii list and each line or not
    if type(start) == str:
        start = N(start).degree
    ascii_character_set = config_dict['ascii_character_set']
    ascii_length = len(ascii_character_set)
    if remapping_colors:
        for i in range(16):
            if i not in remapping_colors:
                remapping_colors[i] = i
    result = chord([])
    if adjust_scale is not None:
        adjust_scale_names = adjust_scale.names()
    if direction == 0:
        current_text = img_to_ascii(path, rotate=90, max_width=max_keys)
        current_text_list = current_text.split('\n')
    elif direction == 1:
        current_text = img_to_ascii(path, max_width=max_keys)
        current_text_list = current_text.split('\n')
        current_text_list.reverse()
    else:
        current_text = img_to_ascii(path, rotate=rotate, max_width=max_keys)
        current_text_list = current_text.split('\n')
        if whole_reverse:
            current_text_list.reverse()
        if each_line_reverse:
            current_text_list = [i[::-1] for i in current_text_list]

    for k in range(len(current_text_list)):
        each = current_text_list[k]
        if each:
            current_line = [(ascii_character_set.index(each[i]), i + start)
                            for i in range(len(each))]
            if filter_value is not None:
                lower_bound, upper_bound = filter_value
                current_line = [
                    i for i in current_line
                    if lower_bound <= i[0] < upper_bound
                ]
                if not current_line:
                    if result.interval:
                        result.interval[-1] += line_interval + extra_interval
                    else:
                        result.start_time += line_interval + extra_interval
                    continue
            if remapping_colors:
                current_chord = chord([
                    degree_to_note(j[1],
                                   channel=remapping_colors[round(
                                       15 * (j[0] / ascii_length))])
                    for j in current_line
                ],
                                      interval=0,
                                      duration=line_interval)
            else:
                current_chord = chord([
                    degree_to_note(j[1],
                                   channel=round(15 * (j[0] / ascii_length)))
                    for j in current_line
                ],
                                      interval=0,
                                      duration=line_interval)
            if adjust_scale is not None:
                available_inds = [
                    i for i in range(len(current_chord.notes))
                    if current_chord.notes[i].name in adjust_scale_names
                ]
                current_chord.notes = [
                    current_chord.notes[i] for i in available_inds
                ]
                current_chord.interval = [
                    current_chord.interval[i] for i in available_inds
                ]
            current_chord.interval[-1] = line_interval + extra_interval
            result.notes += current_chord.notes
            result.interval += current_chord.interval
    return result
