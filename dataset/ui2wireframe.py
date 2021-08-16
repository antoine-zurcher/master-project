from PIL import Image, ImageDraw, ImageFont
import pickle
import cv2
import numpy as np
import json
import base64
from io import BytesIO
import pandas as pd
import textwrap
from lorem_text import lorem

font_style = 'arial.ttf'
font_size = 30

white = (255, 255, 255)
black = (0, 0, 0)
dark_gray = (50, 50, 50)
size = (1080, 1800)


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def draw_wireframe(ui_):
    wireframe = Image.new('RGBA', size, white)
    wf_draw = ImageDraw.Draw(wireframe)

    components = crop_components(ui_)
    components = resize_ui(components, ui_.width, ui_.height)

    ui_image = Image.open(ui_.JPEG_path)
    ui_resized = ui_image.resize(size, Image.ANTIALIAS)
    components['area'] = ((components.xmax - components.xmin) * (components.ymax - components.ymin)).values
    components_sorted_area = components.sort_values('area', ascending=False)
    components_sorted_area = components_sorted_area.reset_index(drop=True)
    df_json = components_sorted_area.rename(columns={'type': 'type',
                                                     'xmin': 'xmin',
                                                     'ymin': 'ymin',
                                                     'xmax': 'xmax',
                                                     'ymax': 'ymax',
                                                     'center_x': 'center_x',
                                                     'center_y': 'center_y',
                                                     'text': 'value',
                                                     'area': 'area',
                                                     }).copy(deep=True)
    df_json['font_size'] = 0

    for i, component in components_sorted_area.iterrows():
        if component['type'] == 'Text' and component.text != '':
            pos = (component.xmin, component.ymin)
            # if the text is not too long
            # if component.text.count(' ') < 2:
            text = component.text.capitalize()
            target_width = component.xmax - component.xmin
            target_height = component.ymax - component.ymin
            if len(component.text) < 30:
                wf_draw.text(pos, text, font=ImageFont.truetype(font_style, size=fit_font_size(text, target_width, target_height)),
                             fill=black, anchor='lt')
                df_json.loc[i, 'font_size'] = fit_font_size(text, target_width, target_height)
            else:
                font = ImageFont.truetype(font_style, size=font_size)
                multiline_text = text_wrap(text, font, wf_draw, target_width, target_height)
                wf_draw.text(pos, multiline_text, font=font, fill=black)
                df_json.loc[i, 'font_size'] = font_size
            # else generate random lorem ipsum sentences of same length
            # else:
            #     nb_words = component.text.count(' ') + 1
            #     text = lorem.words(nb_words).capitalize()
            #     wf_draw.text(pos, text, font=ImageFont.truetype(font_style, size=25), fill=black, anchor='lt')
        elif component['type'] == 'TextButton':
            xy = [(component.xmin, component.ymin), (component.xmax, component.ymax)]
            wf_draw.rounded_rectangle(xy, 25, fill=dark_gray, outline=white)
            text = component.text.capitalize()
            pos = (component.center_x, component.center_y)
            wf_draw.text(pos, text, font=ImageFont.truetype(font_style, size=40),
                         fill=white, anchor='mm')
            df_json.loc[i, 'font_size'] = 40
        elif component['type'] == 'EditText' and component.text != '':
            xy_rect = [(component.xmin, component.ymin), (component.xmax, component.ymax)]
            width_comp = component.xmax - component.xmin
            height_comp = component.ymax - component.ymin
            wf_draw.rectangle(xy_rect, outline=black, width=5)
            xy_line = [(component.xmin + 20, component.ymin + 0.8 * height_comp),
                       (component.xmax - 20, component.ymin + 0.8 * height_comp)]
            xmin, ymin, xmax, ymax = find_text_box(component, components_sorted_area)
            pos = (component.xmin + 20, component.ymin + height_comp / 2)
            for j, component_icon in components_sorted_area.iterrows():
                if component_icon['type'] == 'Icon':
                    if component.xmin < component_icon.center_x < component.xmax - width_comp/2 and \
                            component.ymin < component_icon.center_y < component.ymax:
                        pos = (component_icon.xmax + 20, component.ymin + height_comp / 2)
                        xy_line = [(component_icon.xmax + 20, component.ymin + 0.8 * height_comp),
                                   (component.xmax - 20, component.ymin + 0.8 * height_comp)]
                        break
            wf_draw.line(xy_line, fill=black, width=3)
            text = component.text.capitalize()
            target_width = xmax - xmin
            target_height = ymax - ymin
            wf_draw.text(pos, text, font=ImageFont.truetype(font_style, size=fit_font_size(text, target_width, target_height)),
                         fill=black, anchor='lm')
            df_json.loc[i, 'font_size'] = fit_font_size(text, target_width, target_height)
        elif component['type'] == 'Image' or component['type'] == 'Map':
            xy_rect = [(component.xmin, component.ymin), (component.xmax, component.ymax)]
            width_comp = component.xmax - component.xmin
            height_comp = component.ymax - component.ymin
            area = width_comp * height_comp
            if area < 8000:
                im_image = ui_resized.crop((component.xmin,
                                            component.ymin,
                                            component.xmax,
                                            component.ymax))
                im_cv = cv2.cvtColor(np.array(im_image), cv2.COLOR_RGB2BGR)
                im_gray = cv2.cvtColor(im_cv, cv2.COLOR_BGR2GRAY)
                im_thresh = cv2.threshold(im_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                border_pixel = get_border(im_thresh)
                if border_pixel.sum() < len(border_pixel) * (255 / 2):
                    im_thresh = cv2.bitwise_not(im_thresh)
                im_image = Image.fromarray(cv2.cvtColor(im_thresh, cv2.COLOR_BGR2RGB))
                im_image = white_to_transparency(im_image)
                wireframe.paste(im_image, box=(component.xmin, component.ymin), mask=im_image)
                buffered = BytesIO()
                im_image.save(buffered, format='PNG')
                img_str = base64.b64encode(buffered.getvalue())
                img_base64 = bytes("data:image/png;base64,", encoding='utf-8') + img_str
                df_json.loc[i, 'value'] = img_base64
            else:
                wf_draw.rectangle(xy_rect, fill=white, outline=black, width=5)
                wf_draw.line([(component.xmin, component.ymin),
                              (component.xmin + width_comp, component.ymin + height_comp)], fill=black, width=5)
                wf_draw.line([(component.xmin, component.ymin + height_comp),
                              (component.xmin + width_comp, component.ymin)], fill=black, width=5)
        elif component['type'] == 'Icon':
            icon_image = ui_resized.crop((component.xmin,
                                          component.ymin,
                                          component.xmax,
                                          component.ymax))
            icon_cv = cv2.cvtColor(np.array(icon_image), cv2.COLOR_RGB2BGR)
            icon_gray = cv2.cvtColor(icon_cv, cv2.COLOR_BGR2GRAY)
            icon_thresh = cv2.threshold(icon_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            border_pixel = get_border(icon_thresh)
            if border_pixel.sum() < len(border_pixel) * (255 / 2):
                icon_thresh = cv2.bitwise_not(icon_thresh)
            icon_image = Image.fromarray(cv2.cvtColor(icon_thresh, cv2.COLOR_BGR2RGB))
            icon_image = white_to_transparency(icon_image)
            wireframe.paste(icon_image, box=(component.xmin, component.ymin), mask=icon_image)
            buffered = BytesIO()
            icon_image.save(buffered, format='PNG')
            img_str = base64.b64encode(buffered.getvalue())
            img_base64 = bytes("data:image/png;base64,", encoding='utf-8') + img_str
            df_json.loc[i, 'value'] = img_base64
        elif component['type'] == 'CheckedTextView':
            if component.text != '':
                height_comp = component.ymax - component.ymin
                xy_rect = [(component.xmin, component.ymin), (component.xmin + height_comp, component.ymax)]
                wf_draw.rectangle(xy_rect, outline=black, width=5)
                xmin, ymin, xmax, ymax = find_text_box(component, components_sorted_area)
                pos = (xmin, ymin)
                if component.xmin <= xmin <= component.xmin + height_comp:
                    pos = (xmin + height_comp + 20, ymin)
                text = component.text.capitalize()
                target_width = xmax - xmin
                target_height = ymax - ymin
                wf_draw.text(pos, text, font=ImageFont.truetype(font_style, size=fit_font_size(text, target_width, target_height)),
                             fill=black, anchor='lt')
                df_json.loc[i, 'font_size'] = fit_font_size(text, target_width, target_height)
            else:
                cb_image = ui_resized.crop((component.xmin,
                                            component.ymin,
                                            component.xmax,
                                            component.ymax))
                cb_cv = cv2.cvtColor(np.array(cb_image), cv2.COLOR_RGB2BGR)
                cb_gray = cv2.cvtColor(cb_cv, cv2.COLOR_BGR2GRAY)
                cb_thresh = cv2.threshold(cb_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                border_pixel = get_border(cb_thresh)
                if border_pixel.sum() < len(border_pixel) * (255 / 2):
                    cb_thresh = cv2.bitwise_not(cb_thresh)
                cb_image = Image.fromarray(cv2.cvtColor(cb_thresh, cv2.COLOR_BGR2RGB))
                wireframe.paste(cb_image, box=(component.xmin, component.ymin))
        elif component['type'] == 'PageIndicator':
            xy_circle1, xy_circle2, xy_circle3 = get_xy_circles(component)
            wf_draw.ellipse(xy_circle1, outline=black, width=3)
            wf_draw.ellipse(xy_circle2, outline=black, width=3)
            wf_draw.ellipse(xy_circle3, outline=black, width=3)
        elif component['type'] == 'Drawer' or component['type'] == 'Bottom_Navigation' \
                or component['type'] == 'Modal' or component['type'] == 'Card' or component['type'] == 'Toolbar':
            xy_rect = [(component.xmin, component.ymin), (component.xmax, component.ymax)]
            wf_draw.rectangle(xy_rect, outline=black, width=5)
        elif component['type'] == 'Switch':
            height_comp = component.ymax - component.ymin
            xy_rect = [(component.xmin, component.ymin + 0.25 * height_comp),
                       (component.xmax, component.ymax - 0.25 * height_comp)]
            wf_draw.rounded_rectangle(xy_rect, height_comp * 0.25, outline=black, width=5)
            radius = height_comp / 2
            xy_circle = [(component.xmin, component.ymin),
                         (component.xmin + 2 * radius, component.ymin + 2 * radius)]
            wf_draw.ellipse(xy_circle, fill=white, outline=black, width=5)
        elif component['type'] == 'CheckBox' or component['type'] == 'Checkbox':
            height_comp = component.ymax - component.ymin
            xy_rect = [(component.xmin, component.ymin), (component.xmin + height_comp, component.ymax)]
            wf_draw.rectangle(xy_rect, outline=black, width=5)
        elif component['type'] == 'Multi_Tab':
            xy_rect = [(component.xmin, component.ymin), (component.xmax, component.ymax)]
            wf_draw.rectangle(xy_rect, outline=black, width=5)
            width_comp = component.xmax - component.xmin
            nb_textbox = count_nb_textbox(component, components_sorted_area)
            xy_line = [(component.xmin, component.ymax - 5),
                       (component.xmin + int(width_comp / nb_textbox), component.ymax - 5)]
            wf_draw.line(xy_line, fill=black, width=10)
            df_json.loc[i, 'value'] = nb_textbox


    # wireframe.show()
    wireframe = wireframe.convert('RGB')
    df_json_sorted = df_json.sort_values(['center_y', 'center_x'], ascending=(True, True))
    df_json_sorted = df_json_sorted.reset_index(drop=True)
    return wireframe, df_json_sorted


def crop_components(ui_):
    components = ui_.components.copy(deep=True)
    if 'Modal' in components.type.values:
        nb_components = components.index.size
        drop = []
        xmin_popup = components[components['type'] == 'Modal'].xmin.item()
        ymin_popup = components[components['type'] == 'Modal'].ymin.item()
        xmax_popup = components[components['type'] == 'Modal'].xmax.item()
        ymax_popup = components[components['type'] == 'Modal'].ymax.item()
        for i in range(nb_components):
            if not (xmin_popup < components.iloc[i].center_x < xmax_popup and
                    ymin_popup < components.iloc[i].center_y < ymax_popup):
                drop.append(i)
        components.drop(drop, inplace=True)
        components.reset_index(drop=True, inplace=True)

    if 'Drawer' in ui_.components.type.values:
        nb_components = components.index.size
        drop = []
        xmin_menu = components[components['type'] == 'Drawer'].xmin.item()
        ymin_menu = components[components['type'] == 'Drawer'].ymin.item()
        xmax_menu = components[components['type'] == 'Drawer'].xmax.item()
        ymax_menu = components[components['type'] == 'Drawer'].ymax.item()
        for i in range(nb_components):
            if not (xmin_menu < components.iloc[i].center_x < xmax_menu and
                    ymin_menu < components.iloc[i].center_y < ymax_menu):
                drop.append(i)
        components.drop(drop, inplace=True)
        components.reset_index(drop=True, inplace=True)

    return components


def resize_ui(components, ui_width, ui_height):
    if not (1070 < ui_width < 1090) or not (1790 < ui_width < 1810):
        width_ratio = size[0] / ui_width
        height_ratio = size[1] / ui_height

        components.xmin = (components.xmin * width_ratio).round().astype(int)
        components.xmax = (components.xmax * width_ratio).round().astype(int)
        components.center_x = (components.center_x * width_ratio).round().astype(int)

        components.ymin = (components.ymin * height_ratio).round().astype(int)
        components.ymax = (components.ymax * height_ratio).round().astype(int)
        components.center_y = (components.center_y * height_ratio).round().astype(int)
    return components


def text_wrap(text, font, draw, max_width, max_height):
    lines = [[]]
    words = text.split()
    for word in words:
        # try putting this word in last line then measure
        lines[-1].append(word)
        (w, h) = draw.multiline_textsize('\n'.join([' '.join(line) for line in lines]), font=font)
        if w > max_width:  # too wide
            # take it back out, put it on the next line, then measure again
            lines.append([lines[-1].pop()])
            (w, h) = draw.multiline_textsize('\n'.join([' '.join(line) for line in lines]), font=font)
            if h > max_height:  # too high now, cannot fit this word in, so take out - add ellipses
                lines.pop()
                # try adding ellipses to last word fitting (i.e. without a space)
                lines[-1][-1] += '...'
                # keep checking that this doesn't make the textbox too wide,
                # if so, cycle through previous words until the ellipses can fit
                while draw.multiline_textsize('\n'.join([' '.join(line) for line in lines]), font=font)[
                    0] > max_width:
                    lines[-1].pop()
                    lines[-1][-1] += '...'
                break
    return '\n'.join([' '.join(line) for line in lines])


def fit_font_size(text, target_width, target_height):
    font = ImageFont.truetype(font_style, size=font_size)
    text_w, text_h = font.getsize(text)
    ratio_w = target_width / text_w
    ratio_h = target_height / text_h
    ratio = min(ratio_w, ratio_h)
    target_font_size = int(round(font_size * ratio, 0))
    return max(target_font_size, font_size)


def find_text_box(component, components):
    xmin = component.xmin
    ymin = component.ymin
    xmax = component.xmax
    ymax = component.ymax
    for i, text_box in components.iterrows():
        if text_box['type'] == 'Text':
            if xmin < text_box.center_x < xmax and ymin < text_box.center_y < ymax:
                return text_box.xmin, text_box.ymin, text_box.xmax, text_box.ymax


def count_nb_textbox(component, components):
    counter = 0
    xmin = component.xmin
    ymin = component.ymin
    xmax = component.xmax
    ymax = component.ymax
    for i, text_box in components.iterrows():
        if text_box['type'] == 'Text' or text_box['type'] == 'Icon' or text_box['type'] == 'Image':
            if xmin < text_box.center_x < xmax and ymin < text_box.center_y < ymax:
                counter += 1
    return counter


def find_text(component, components):
    xmin = component.xmin
    ymin = component.ymin
    xmax = component.xmax
    ymax = component.ymax
    for i, text_box in components.iterrows():
        if text_box['type'] == 'Text':
            if xmin < text_box.center_x < xmax and ymin < text_box.center_y < ymax:
                return text_box.text


def get_xy_circles(component):
    width_comp = component.xmax - component.xmin
    height_comp = component.ymax - component.ymin
    radius = min(width_comp, height_comp) / 2
    if width_comp < height_comp:
        xy_circle1 = [(component.center_x - radius, component.center_y - 4 * radius),
                      (component.center_x + radius, component.center_y - 2 * radius)]
        xy_circle2 = [(component.center_x - radius, component.center_y - radius),
                      (component.center_x + radius, component.center_y + radius)]
        xy_circle3 = [(component.center_x - radius, component.center_y + 2 * radius),
                      (component.center_x + radius, component.center_y + 4 * radius)]
    else:
        xy_circle1 = [(component.center_x - 4 * radius, component.center_y - radius),
                      (component.center_x - 2 * radius, component.center_y + radius)]
        xy_circle2 = [(component.center_x - radius, component.center_y - radius),
                      (component.center_x + radius, component.center_y + radius)]
        xy_circle3 = [(component.center_x + 2 * radius, component.center_y - radius),
                      (component.center_x + 4 * radius, component.center_y + radius)]
    return xy_circle1, xy_circle2, xy_circle3


def get_border(array, corner=0, direction='cw'):
    if corner > 0:
        # Rotate the array so we start on a different corner
        array = np.rot90(array, k=corner)
    if direction is 'ccw':
        # Transpose the array so we march around counter-clockwise
        array = array.T

    border = []
    border += list(array[0, :-1])  # Top row (left to right), not the last element.
    border += list(array[:-1, -1])  # Right column (top to bottom), not the last element.
    border += list(array[-1, :0:-1])  # Bottom row (right to left), not the last element.
    border += list(array[::-1, 0])  # Left column (bottom to top), all elements element.
    border.pop()

    return np.array(border)


def white_to_transparency(img):
    x = np.asarray(img.convert('RGBA')).copy()

    x[:, :, 3] = (255 * (x[:, :, :3] != 255).any(axis=2)).astype(np.uint8)

    return Image.fromarray(x)


if __name__ == '__main__':
    ui_path = 'C:\\Users\\Antoine\\CloudStation\\EPFL\\Master 4\\Master project\\Dataset\\VINS Dataset\\ui_list.dat'

    with open(ui_path, 'rb') as f:
        ui_list_saved = pickle.load(f)

    type_comp = ['Text', 'TextButton', 'EditText', 'Image', 'Icon', 'CheckedTextView', 'BackgroundImage',
                 'UpperTaskBar',
                 'PageIndicator', 'Drawer', 'Modal', 'Switch', 'Spinner', 'Card', 'Toolbar', 'CheckBox', 'Checkbox',
                 'Multi_Tab', 'Remember', 'Bottom_Navigation', 'Map']

    wf_directory = 'C:\\Users\\Antoine\\CloudStation\\EPFL\\Master 4\\Master project\\prototype\\assets\\wireframes\\'
    json_directory = 'C:\\Users\\Antoine\\CloudStation\\EPFL\\Master 4\\Master project\\Dataset\\VINS Dataset\\JSON\\'

    im, ui_json = draw_wireframe(ui_list_saved[2])
    count = 0
    for ui in ui_list_saved:
        count += 1
        print(ui.name + ' ' + count)
        im, ui_json = draw_wireframe(ui)
        im.save(wf_directory + ui.name + '.jpg')
        ui_json.to_json(json_directory + ui.name + '.json', orient='index')
