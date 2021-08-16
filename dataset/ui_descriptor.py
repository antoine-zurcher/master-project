import copy
import os

import num2word

import vocabulary
from data_labeller import Label
from nltk.corpus import wordnet as wn
import nlpaug.augmenter.word as naw
from googletrans import Translator
from google.cloud import translate

from random import seed
from random import random

seed(1)
# context_aug = naw.ContextualWordEmbsAug(model_path='bert-base-uncased', action="insert")
# delete_aug = naw.RandomWordAug()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'masterproject-307316-27f773a9a493.json'
translate_client = translate.TranslationServiceClient()
location = "global"
project_id = 'masterproject-307316'
parent = f"projects/{project_id}/locations/{location}"


def describe_ui(ui):
    label = ui.label
    if label == Label.POPUP or label == Label.POPUP_LOGIN or label == Label.POPUP_LIST:
        ui = crop_popup(ui)
    width = ui.width
    height = ui.height
    components = ui.components
    # sort the components from top to bottom and if aligned from left to right
    components_sorted = components.sort_values(['center_y', 'center_x'], ascending=(True, True))
    # remove components that have too long text
    components_sorted = components_sorted[components_sorted.text.str.count(' ') < 6]
    components_sorted = components_sorted.reset_index(drop=True)
    components_sorted_text = components_sorted[components_sorted.text != '']
    text_components = ['Text', 'EditText', 'TextButton', 'CheckedTextView', 'Image']
    nb_text_components = components_sorted_text.index.size
    nb_components = nb_text_components + components_sorted[components_sorted['type'] == 'Image'].index.size
    count_comp = 0
    sentence_counter = 0
    were_aligned = False
    cnt_aligned = 0
    description = vocabulary.start()

    if label == Label.LIST or label == Label.POPUP or label == Label.POPUP_LOGIN or label == Label.POPUP_LIST \
            or label == Label.LOGIN or label == Label.INFORMATION:
        if label == Label.LIST:
            description += 'a ' + vocabulary.interface() + 'with a list of items ' + vocabulary.containing()
        elif label == Label.POPUP:
            description += 'a pop-up window ' + vocabulary.containing()
        elif label == Label.POPUP_LOGIN:
            description += 'a pop-up window to login ' + vocabulary.containing()
        elif label == Label.POPUP_LIST:
            description += 'a pop-up window with a list of items ' + vocabulary.containing()
        elif label == Label.LOGIN:
            description += 'a login ' + vocabulary.interface() + vocabulary.containing()
        elif label == Label.INFORMATION:
            description += 'an information ' + vocabulary.interface() + vocabulary.containing()

        for i, component in components_sorted.iterrows():
            if component.type == 'Image':
                count_comp += 1
                if were_aligned:
                    if cnt_aligned > 0:
                        cnt_aligned -= 1
                        continue
                    elif cnt_aligned == 0:
                        were_aligned = False
                        continue
                sentence_counter += 1
                area_ui = width * height
                if is_next_image_aligned(i, components_sorted):
                    nb_aligned = nb_image_aligned(i, components_sorted)
                    cnt_aligned = nb_aligned - 2
                    description += num2word.word(cnt_aligned).lower() + ' images on the same level '
                    were_aligned = True
                else:
                    description += 'a ' + size_image(component, area_ui) + 'image '

                # if it is the first component
                if count_comp == 1:
                    width_component = component.xmax - component.xmin
                    description += 'located in the ' + get_position(component.center_x, component.center_y, width,
                                                                    height,
                                                                    left_right=width_component < 0.7 * width)
                    description += vocabulary.position() + 'of the ' + vocabulary.interface()
                # if it is not the last component
                if count_comp != nb_components:
                    # if 3 components were described, start new sentence
                    if sentence_counter > 2:
                        description = description[:-1] + vocabulary.new_sentence()
                        sentence_counter = 0
                    else:
                        description += vocabulary.connector()
                # if it is the second last component
                elif count_comp == nb_components - 1:
                    description += vocabulary.final_connector()
                # if it is the last component
                else:
                    description = description[:-1] + '.'

            if component.type in text_components and component.text != '':
                count_comp += 1
                sentence_counter += 1
                # if the previous iteration described two components at once, skip the description of the next component
                if were_aligned:
                    were_aligned = False
                    continue
                if is_next_text_aligned(i, components_sorted, text_components):
                    next_component = components_sorted.iloc[i + 1]
                    if component.type == 'Text':
                        if next_component.type == 'Text':
                            if '?' in component.text and '?' in next_component.text:
                                description += 'two text boxes on the same level asking ' + component.text
                                description += ' and ' + next_component.text + ' '
                            else:
                                description += 'two text boxes on the same level saying ' + component.text
                                description += ' and ' + next_component.text + ' '
                        elif next_component.type == 'EditText':
                            description += 'a text box and an input field on the same level saying ' + component.text
                            description += ' and ' + next_component.text + ' '
                        elif next_component.type == 'TextButton':
                            description += 'a text box and a button on the same level saying ' + component.text
                            description += ' and ' + next_component.text + ' '
                        elif next_component.type == 'CheckedTextView':
                            description += 'a text box and a checkbox on the same level saying ' + component.text
                            description += ' and ' + next_component.text + ' '

                    elif component.type == 'EditText':
                        if next_component.type == 'Text':
                            description += 'an input field and a text box on the same level saying ' + component.text
                            description += ' and ' + next_component.text + ' '
                        elif next_component.type == 'EditText':
                            description += 'two input fields on the same level saying ' + component.text
                            description += ' and ' + next_component.text + ' '
                        elif next_component.type == 'TextButton':
                            description += 'an input field and a button on the same level saying ' + component.text
                            description += ' and ' + next_component.text + ' '
                        elif next_component.type == 'CheckedTextView':
                            description += 'an input field and a checkbox on the same level saying ' + component.text
                            description += ' and ' + next_component.text + ' '

                    elif component.type == 'TextButton':
                        if next_component.type == 'Text':
                            description += 'a button and a text box on the same level saying ' + component.text
                            description += ' and ' + next_component.text + ' '
                        elif next_component.type == 'EditText':
                            description += 'a button and an input field on the same level saying ' + component.text
                            description += ' and ' + next_component.text + ' '
                        elif next_component.type == 'TextButton':
                            if possible_verb(component.text):
                                description += 'two buttons on the same level to ' + component.text
                                description += ' and ' + next_component.text + ' '
                            else:
                                description += 'two buttons on the same level for ' + component.text
                                description += ' and ' + next_component.text + ' '
                        elif next_component.type == 'CheckedTextView':
                            description += 'a button and a checkbox on the same level saying ' + component.text
                            description += ' and ' + next_component.text + ' '

                    elif component.type == 'CheckedTextView':
                        if next_component.type == 'Text':
                            description += 'a text box and checkbox on the same level saying ' + component.text
                            description += ' and ' + next_component.text + ' '
                        elif next_component.type == 'EditText':
                            description += 'a check and an input field on the same level saying ' + component.text
                            description += ' and ' + next_component.text + ' '
                        elif next_component.type == 'TextButton':
                            description += 'a checkbox and a button on the same level saying ' + component.text
                            description += ' and ' + next_component.text + ' '
                        elif next_component.type == 'CheckedTextView':
                            description += 'two checkboxes on the same level saying ' + component.text
                            description += ' and ' + next_component.text + ' '

                    were_aligned = True
                    # if it is the first two components
                    if count_comp == 1:
                        description += 'located in the ' + get_position(component.center_x, component.center_y,
                                                                        width, height, left_right=False)
                        description += vocabulary.position() + 'of the ' + vocabulary.interface()
                    if count_comp != nb_components - 1:
                        # if 3 components were described, start new sentence
                        if sentence_counter > 2:
                            description = description[:-1] + vocabulary.new_sentence()
                            sentence_counter = 0
                        else:
                            description += vocabulary.connector()
                    # if it is the last two components
                    else:
                        description = description[:-1] + '.'

                else:
                    if component.type == 'Text':
                        if '?' in component.text:
                            description += 'a text box asking ' + component.text + ' '
                        else:
                            description += 'a text box saying ' + component.text + ' '
                    elif component.type == 'EditText':
                        if possible_verb(component.text):
                            description += 'a input field to ' + component.text + ' '
                        else:
                            description += 'a input field for the ' + component.text + ' '
                    elif component.type == 'TextButton':
                        if possible_verb(component.text):
                            description += 'a button to ' + component.text + ' '
                        else:
                            description += 'a button for ' + component.text + ' '
                    elif component.type == 'CheckedTextView':
                        description += 'a checkbox saying ' + component.text + ' '

                    # if it is the first component
                    if count_comp == 1:
                        width_component = component.xmax - component.xmin
                        description += 'located in the ' + get_position(component.center_x, component.center_y, width,
                                                                        height,
                                                                        left_right=width_component < 0.7 * width)
                        description += vocabulary.position() + 'of the ' + vocabulary.interface()
                    # if it is not the last component
                    if count_comp != nb_components:
                        # if 3 components were described, start new sentence
                        if sentence_counter > 2:
                            description = description[:-1] + vocabulary.new_sentence()
                            sentence_counter = 0
                        else:
                            description += vocabulary.connector()
                    # if it is the second last component
                    elif count_comp == nb_components - 1:
                        description += vocabulary.final_connector()
                    # if it is the last component
                    else:
                        description = description[:-1] + '.'
    elif label == Label.SETTINGS:
        description += 'a settings ' + vocabulary.interface() + vocabulary.containing()
        nb_textbox = components_sorted_text.index.size
        if components_sorted_text.text.iloc[0] == 'settings':
            nb_textbox -= 1
        nb_checkbox = components_sorted[components_sorted['type'] == 'CheckedTextView'].index.size
        description += num2word.word(nb_textbox).lower() + ' textboxes with ' \
                       + num2word.word(nb_checkbox).lower() + ' checkboxes.'
    elif label == Label.MENU:
        description += 'a menu ' + vocabulary.interface() + vocabulary.containing()
        counter = 0
        nb_img = 0
        xmin_drawer = components[ui.components['type'] == 'Drawer'].xmin.item()
        ymin_drawer = components[ui.components['type'] == 'Drawer'].ymin.item()
        xmax_drawer = components[ui.components['type'] == 'Drawer'].xmax.item()
        ymax_drawer = components[ui.components['type'] == 'Drawer'].ymax.item()
        area_ui = width * height
        for i, component in components.iterrows():
            if component.type == 'Text' and xmin_drawer < component.center_x < xmax_drawer and ymin_drawer < component.center_y < ymax_drawer:
                counter += 1
            if component.type == 'Image':
                nb_img += 1
        description += 'a list of ' + num2word.word(counter).lower() + ' textboxes.'
        if nb_img > 0:
            count_img = 0
            description = description[:-1] + ' with '
            for i, component in components_sorted.iterrows():
                if component.type == 'Image':
                    count_img += 1
                    description += 'a ' + size_image(component, area_ui) + 'image '

                    if count_img == 1:
                        description += 'located in the ' + get_position(component.center_x, component.center_y,
                                                                        width, height, left_right=False)
                        description += vocabulary.position() + 'of the ' + vocabulary.interface()
                    if count_img != nb_img - 1 and nb_img != 1:
                        # if 3 components were described, start new sentence
                        if sentence_counter > 2:
                            description = description[:-1] + vocabulary.new_sentence()
                            sentence_counter = 0
                        else:
                            description += vocabulary.connector()
                    # if it is the last two components
                    else:
                        description = description[:-1] + '.'

    elif label == Label.GALLERY:
        description += 'a gallery-type ' + vocabulary.interface() + vocabulary.containing()
        counter = 0
        for i, component in components_sorted.iterrows():
            if component.type == 'Image':
                area_ui = width * height
                area_image = (component.xmax - component.xmin) * (component.ymax - component.ymin)
                ratio = area_image / area_ui
                if ratio > 0.04:
                    counter += 1
        description += 'a grid of ' + num2word.word(counter).lower() + ' images '
        nb_textbox = components_sorted_text.index.size
        if nb_textbox >= counter:
            description += 'with text descriptions.'
        else:
            description = description[:-1] + '.'
        nb_textbutton = (components_sorted.type == 'TextButton').sum()
        if nb_textbutton > 0:
            if nb_textbutton == 1:
                description += ' Add as well a text button saying ' \
                               + components_sorted[components_sorted.type == 'TextButton'].text.item() + '.'
            else:
                description += ' Add as well ' + num2word.word(int(nb_textbutton)).lower() + ' text buttons saying '
                df_textbutton = components_sorted[components_sorted.type == 'TextButton']
                for i, tb in df_textbutton.iterrows():
                    if i != nb_textbutton - 2:
                        description += tb.text + ', '
                    elif i == nb_textbutton - 2:
                        description += tb.text + ' and '
                    elif i == nb_textbutton - 1:
                        description += tb.text + '.'
    elif label == Label.SHOP:
        description += 'a shopping ' + vocabulary.interface() + vocabulary.containing()
        counter = 0
        for i, component in components.iterrows():
            if component.type == 'Image':
                area_ui = width * height
                area_image = (component.xmax - component.xmin) * (component.ymax - component.ymin)
                ratio = area_image / area_ui
                if ratio > 0.01:
                    counter += 1
        description += 'a grid of ' + num2word.word(counter).lower() + ' items. '
        description += 'The ' + vocabulary.interface() + 'should also ' + vocabulary.contain()
        filter_components = ['EditText', 'TextButton', 'CheckedTextView']
        nb_components_filter = components_sorted[components_sorted['type'].isin(filter_components)].index.size
        for i, component in components_sorted.iterrows():
            if component.type in filter_components and component.text != '':
                count_comp += 1
                sentence_counter += 1
                # if the previous iteration described two components at once, skip the description of the next component
                if were_aligned:
                    were_aligned = False
                    continue
                if is_next_text_aligned(i, components_sorted, text_components):
                    next_component = components_sorted.iloc[i + 1]

                    if component.type == 'EditText':
                        if next_component.type == 'EditText':
                            description += 'two input fields on the same level saying ' + component.text
                            description += ' and ' + next_component.text + ' '
                        elif next_component.type == 'TextButton':
                            description += 'an input field and a button on the same level saying ' + component.text
                            description += ' and ' + next_component.text + ' '
                        elif next_component.type == 'CheckedTextView':
                            description += 'an input field and a checkbox on the same level saying ' + component.text
                            description += ' and ' + next_component.text + ' '

                    elif component.type == 'TextButton':
                        if next_component.type == 'EditText':
                            description += 'a button and an input field on the same level saying ' + component.text
                            description += ' and ' + next_component.text + ' '
                        elif next_component.type == 'TextButton':
                            if possible_verb(component.text):
                                description += 'two buttons on the same level to ' + component.text
                                description += ' and ' + next_component.text + ' '
                            else:
                                description += 'two buttons on the same level for ' + component.text
                                description += ' and ' + next_component.text + ' '
                        elif next_component.type == 'CheckedTextView':
                            description += 'a button and a checkbox on the same level saying ' + component.text
                            description += ' and ' + next_component.text + ' '

                    elif component.type == 'CheckedTextView':
                        if next_component.type == 'EditText':
                            description += 'a check and an input field on the same level saying ' + component.text
                            description += ' and ' + next_component.text + ' '
                        elif next_component.type == 'TextButton':
                            description += 'a checkbox and a button on the same level saying ' + component.text
                            description += ' and ' + next_component.text + ' '
                        elif next_component.type == 'CheckedTextView':
                            description += 'two checkboxes on the same level saying ' + component.text
                            description += ' and ' + next_component.text + ' '

                    were_aligned = True
                    # if it is the first two components
                    if count_comp == 1:
                        description += 'located in the ' + get_position(component.center_x, component.center_y,
                                                                        width, height, left_right=False)
                        description += vocabulary.position() + 'of the ' + vocabulary.interface()
                    if count_comp != nb_components_filter - 1:
                        # if 3 components were described, start new sentence
                        if sentence_counter > 2:
                            description = description[:-1] + vocabulary.new_sentence()
                            sentence_counter = 0
                        else:
                            if count_comp != 1:
                                description += 'located in the ' + get_position(component.center_x, component.center_y,
                                                                                width, height, left_right=False) \
                                               + vocabulary.position()
                            description += vocabulary.connector()
                    # if it is the last two components
                    else:
                        description += 'located in the ' + get_position(component.center_x, component.center_y,
                                                                        width, height, left_right=False) \
                                       + vocabulary.position()
                        description = description[:-1] + '.'

                else:
                    if component.type == 'EditText':
                        if possible_verb(component.text):
                            description += 'an input field to ' + component.text + ' '
                        else:
                            description += 'an input field for the ' + component.text + ' '
                    elif component.type == 'TextButton':
                        if possible_verb(component.text):
                            description += 'a button to ' + component.text + ' '
                        else:
                            description += 'a button for ' + component.text + ' '
                    elif component.type == 'CheckedTextView':
                        description += 'a checkbox saying ' + component.text + ' '

                    # if it is the first component
                    if count_comp == 1:
                        width_component = component.xmax - component.xmin
                        description += 'located in the ' + get_position(component.center_x, component.center_y, width,
                                                                        height,
                                                                        left_right=width_component < 0.7 * width)
                        description += vocabulary.position() + 'of the ' + vocabulary.interface()
                    # if it is not the last component
                    if count_comp != nb_components_filter:
                        # if 3 components were described, start new sentence
                        if sentence_counter > 2:
                            description = description[:-1] + vocabulary.new_sentence()
                            sentence_counter = 0
                        else:
                            if count_comp != 1:
                                description += 'located in the ' + get_position(component.center_x, component.center_y,
                                                                                width, height, left_right=False) \
                                               + vocabulary.position()
                            description += vocabulary.connector()
                    # if it is the second last component
                    elif count_comp == nb_components_filter - 1:
                        description += vocabulary.final_connector()
                    # if it is the last component
                    else:
                        description += 'located in the ' + get_position(component.center_x, component.center_y,
                                                                        width, height, left_right=False) \
                                       + vocabulary.position()
                        description = description[:-1] + '.'

    return augment_description(description)


def augment_description(description):
    # Insert word by contextual word embeddings
    # desc_insert = context_aug.augment(description)
    desc_insert = description
    # Back translate from EN to DE, then from DE to EN
    desc_de = translate_text(desc_insert, src='en-US', dest='de')
    desc_en = translate_text(desc_de, src='de', dest='en-US')
    # Randomly delete a word
    desc_del = desc_en
    # Cut long description away
    desc_cut = random_cut(desc_del, n_words=15, prob=0.5)
    return desc_cut


def translate_text(text, src, dest):
    response = translate_client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # mime types: text/plain, text/html
            "source_language_code": src,
            "target_language_code": dest,
        }
    )
    return response.translations[0].translated_text


def random_cut(description, n_words, prob):
    value = random()
    if value <= prob:
        cut_description = ' '.join(description.split()[:n_words])
        return cut_description
    return description


def get_position(x, y, width, height, left_right=False):
    # define the position intervals by dividing the width and height by 3
    top = range(0, round(height / 3))
    center = range(round(height / 3) + 1, round(2 * height / 3))
    bottom = range(round(2 * height / 3) + 1, height)

    position = ''
    if y in top:
        position = 'top '
    elif y in center:
        position = 'center '
    elif y in bottom:
        position = 'bottom '

    if left_right:
        left = range(0, round(width / 3))
        middle = range(round(width / 3) + 1, round(2 * width / 3))
        right = range(round(2 * width / 3) + 1, width)

        if x in left:
            position += 'left '
        elif x in middle:
            if y not in center:
                position += 'middle '
        elif x in right:
            position += 'right '

    return position


def is_next_text_aligned(i, components_sorted, text_components):
    ymin = components_sorted.iloc[i].ymin
    ymax = components_sorted.iloc[i].ymax
    length = components_sorted.index.size

    if i + 1 < length and components_sorted.iloc[i + 1].type in text_components and components_sorted.iloc[
        i + 1].text != '':
        return ymin < components_sorted.iloc[i + 1].center_y < ymax
    else:
        return False


def is_next_image_aligned(i, components_sorted):
    ymin = components_sorted.iloc[i].ymin
    ymax = components_sorted.iloc[i].ymax
    length = components_sorted.index.size

    if i + 1 < length and components_sorted.iloc[i + 1]['type'] == 'Image':
        return ymin < components_sorted.iloc[i + 1].center_y < ymax
    else:
        return False


def nb_image_aligned(i, components_sorted):
    ymin = components_sorted.iloc[i].ymin
    ymax = components_sorted.iloc[i].ymax
    length = components_sorted.index.size
    counter = 1

    while i + counter < length and components_sorted.iloc[i + counter]['type'] == 'Image' and ymin < \
            components_sorted.iloc[i + counter].center_y < ymax:
        counter += 1

    return counter


def possible_verb(words):
    first_word = words.split()[0]
    # Does not recognize login as a verb, only log in
    if first_word.lower() == 'login':
        return True
    else:
        return 'v' in set(s.pos() for s in wn.synsets(first_word))


def crop_popup(ui):
    ui_popup = copy.deepcopy(ui)
    nb_components = ui_popup.components.index.size
    drop = []
    if ui_popup.components.type.str.count('Modal').sum() == 1:
        xmin_popup = ui_popup.components[ui.components['type'] == 'Modal'].xmin.item()
        ymin_popup = ui_popup.components[ui.components['type'] == 'Modal'].ymin.item()
        xmax_popup = ui_popup.components[ui.components['type'] == 'Modal'].xmax.item()
        ymax_popup = ui_popup.components[ui.components['type'] == 'Modal'].ymax.item()
    elif ui_popup.components.type.str.count('Drawer').sum() == 1:
        xmin_popup = ui_popup.components[ui.components['type'] == 'Drawer'].xmin.item()
        ymin_popup = ui_popup.components[ui.components['type'] == 'Drawer'].ymin.item()
        xmax_popup = ui_popup.components[ui.components['type'] == 'Drawer'].xmax.item()
        ymax_popup = ui_popup.components[ui.components['type'] == 'Drawer'].ymax.item()
    else:
        return ui

    for i in range(nb_components):
        if not (xmin_popup < ui_popup.components.iloc[i].center_x < xmax_popup and
                ymin_popup < ui_popup.components.iloc[i].center_y < ymax_popup):
            drop.append(i)

    ui_popup.components.drop(drop, inplace=True)
    ui_popup.components.reset_index(drop=True, inplace=True)
    ui_popup.width = xmax_popup - xmin_popup
    ui_popup.height = ymax_popup - ymin_popup
    ui_popup.components.xmin = ui_popup.components.xmin - xmin_popup
    ui_popup.components.ymin = ui_popup.components.ymin - ymin_popup
    ui_popup.components.xmax = ui_popup.components.xmax - xmin_popup
    ui_popup.components.ymax = ui_popup.components.ymax - ymin_popup
    ui_popup.components.center_x = ui_popup.components.center_x - xmin_popup
    ui_popup.components.center_y = ui_popup.components.center_y - ymin_popup

    return ui_popup


def size_image(component, area_ui):
    area_image = (component.xmax - component.xmin) * (component.ymax - component.ymin)
    ratio = area_image / area_ui
    if ratio < 0.1:
        return 'small '
    elif ratio < 0.2:
        return 'medium-sized '
    else:
        return 'large '
