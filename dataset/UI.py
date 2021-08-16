import io

from spellchecker import SpellChecker

from XMLReader import XMLReader
from PIL import Image
import cv2
import numpy as np
from google.cloud import vision

from data_labeller import Label


def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


def opening(image):
    kernel = np.ones((2, 2), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


def preprocess_image(image):
    resized = cv2.resize(image, None, fx=1, fy=1, interpolation=cv2.INTER_CUBIC)
    gray = get_grayscale(resized)
    thresh = thresholding(gray)
    # if the background is black, invert the image
    if np.mean(thresh) < 127:
        thresh = cv2.bitwise_not(thresh)
    opened = opening(thresh)
    return opened


class UI:
    def __init__(self, xml_path):
        # read XML file of the UI
        xml = XMLReader(xml_path)
        self.name = xml.get_name().replace('.jpg', '')
        self.dataset = xml.get_dataset()
        self.xml_path = xml_path
        self.JPEG_path = xml_path.replace('Annotations', 'JPEGImages').replace('.xml', '.jpg')
        self.width = xml.get_width()
        self.height = xml.get_height()
        self.components = xml.get_components()
        self.label = Label.ABSTAIN
        self.put_text_right_component()

    def get_text_ocr(self, vision_client):
        # Read the text from the text type components
        ui_full = Image.open(self.JPEG_path)
        spell = SpellChecker(language='en', case_sensitive=True)
        nb_components = self.components.index.size
        text_list = []

        for i in range(nb_components):
            if self.components.loc[i].type == 'Text' or self.components.loc[i].type == 'TextButton':
                # crop the image to the bounding box
                ui_cropped = ui_full.crop((self.components.loc[i].xmin,
                                           self.components.loc[i].ymin,
                                           self.components.loc[i].xmax,
                                           self.components.loc[i].ymax))
                img_byte_arr = io.BytesIO()
                ui_cropped.save(img_byte_arr, format='JPEG')
                img_byte_arr = img_byte_arr.getvalue()
                image = vision.Image(content=img_byte_arr)

                response = vision_client.text_detection(image=image)
                if response.text_annotations:
                    text = response.text_annotations[0].description.replace('\n', ' ')
                    # remove ' ' at the end
                    if len(text) > 0:
                        text = text[:-1]
                    # remove weird O recognition that dont exist in english
                    replace_characters_low = ['ô', 'ò', 'õ', 'ó', 'ö']
                    replace_characters_cap = ['Ô', 'Ò', 'Õ', 'Ó', 'Ö']
                    for char in replace_characters_low:
                        text = text.replace(char, 'o')
                    for char in replace_characters_cap:
                        text = text.replace(char, 'O')

                    if self.components.loc[i].type == 'TextButton':
                        if len(text) > 2:
                            if 'facebook' in text.lower():
                                if text[0].lower() == 'f' and text.count(' ') > 0:
                                    if text[1] == ' ':
                                        text = text[2:]
                                    else:
                                        text = text[1:]
                            # if there is a random character at the beginning of the text (corresponds to the icon)
                            elif text[1] == ' ' and (text[0].lower() != 'a' or text[0].lower() != 'i'):
                                text = text[2:]
                            else:
                                corrected_words = [spell.correction(word) for word in spell.split_words(text)]
                                if corrected_words[0] == 'i':
                                    corrected_words.pop(0)
                                text = ' '.join(corrected_words)
                    text_list.append(text.lower())
                else:
                    text_list.append('')

                # # convert image from PIl to cv2
                # ui_cropped_cv = cv2.cvtColor(np.array(ui_cropped), cv2.COLOR_RGB2BGR)
                # # preprocess image to increase OCR accuracy
                # ui_cropped_pre = preprocess_image(ui_cropped_cv)
                # # Image.fromarray(cv2.cvtColor(ui_cropped_pre, cv2.COLOR_BGR2RGB)).show()
                # # apply OCR to image
                # text = pytesseract.image_to_string(ui_cropped_pre, lang='eng', config='--psm 7 --oem 2').strip().replace('\n\n', ' ')

            else:
                text_list.append('')

        self.components.text = text_list

    def put_text_right_component(self):
        # rearranges the text value of the EditText and CheckedTextView components
        nb_components = self.components.index.size

        for i in range(nb_components):
            component_i = self.components.loc[i]
            if component_i.type == 'EditText' or component_i.type == 'CheckedTextView':
                for j in range(nb_components):
                    component_j = self.components.loc[j]
                    if component_j.type == 'Text':
                        if component_i.xmin < component_j.center_x < component_i.xmax \
                                and component_i.ymin < component_j.center_y < component_i.ymax:
                            self.components.loc[i, 'text'] = component_j.text
                            self.components.loc[j, 'text'] = ''

