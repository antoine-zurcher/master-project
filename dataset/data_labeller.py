import copy

from textblob import TextBlob
import numpy as np


# Define the UI label mappings
class Label:
    ABSTAIN = -1
    LIST = 0
    POPUP = 1
    POPUP_LOGIN = 2
    POPUP_LIST = 3
    LOGIN = 4
    INFORMATION = 5
    SETTINGS = 6
    MENU = 7
    GALLERY = 8
    SHOP = 9


def check_words_in_ui(ui, words):
    tb = TextBlob('')
    for text in ui.components.text:
        tb = tb + TextBlob(text + ' ')
    # replace the money symbols by text since TextBlob removes symbols in tb.words
    tb = tb.replace('$', ' dollar ').replace('£', ' pound ').replace('€', ' euro ')
    for i in range(len(tb.words) - 1):
        word1 = tb.words[i]
        word2 = tb.words[i+1]
        if word1.lower() == 'sign' and word2.lower() == 'in':
            tb.words.append('sign in')
        if word1.lower() == 'log' and word2.lower() == 'in':
            tb.words.append('log in')
    condition = False
    for word in words:
        condition += word.lower() in tb.words.lower()
    return condition.__bool__()


def find_label(ui):
    # classify the UIs using a decision tree
    if lf_component_modal(ui):
        # only analyze the content of the popup
        ui_popup = crop_popup(ui)
        if lf_keyword_login(ui_popup):
            return Label.POPUP_LOGIN
        if lf_layout_list(ui_popup):
            return Label.POPUP_LIST
        return Label.POPUP
    if lf_component_menu(ui):
        return Label.MENU
    if lf_keyword_login(ui) and lf_component_text_button(ui):
        return Label.LOGIN
    if lf_layout_image(ui):
        return Label.INFORMATION
    if lf_keyword_shop(ui):
        return Label.SHOP
    if lf_keyword_settings(ui):
        return Label.SETTINGS
    if lf_layout_gallery(ui):
        return Label.GALLERY
    if lf_layout_list(ui):
        return Label.LIST
    return Label.ABSTAIN


def classify_ui(ui_list):
    for ui in ui_list:
        ui.label = find_label(ui)


def crop_popup(ui):
    ui_popup = copy.deepcopy(ui)
    nb_components = ui_popup.components.index.size
    drop = []
    xmin = ui_popup.components[ui.components['type'] == 'Modal'].xmin.item()
    ymin = ui_popup.components[ui.components['type'] == 'Modal'].ymin.item()
    xmax = ui_popup.components[ui.components['type'] == 'Modal'].xmax.item()
    ymax = ui_popup.components[ui.components['type'] == 'Modal'].ymax.item()
    for i in range(nb_components):
        if not (xmin < ui_popup.components.iloc[i].center_x < xmax and ymin < ui_popup.components.iloc[i].center_y < ymax):
            drop.append(i)

    ui_popup.components.drop(drop, inplace=True)
    return ui_popup


# 0
def lf_layout_list(ui):
    # ui contains 3/4 of the text components that are vertically aligned
    condition = False
    nb_text = ui.components[ui.components['type'] == 'Text'].index.size
    if nb_text > 0:
        center_x_text = ui.components[ui.components['type'] == 'Text'].center_x
        xmin_text = ui.components[ui.components['type'] == 'Text'].xmin
        xmax_text = ui.components[ui.components['type'] == 'Text'].xmax
        nb_aligned = np.zeros(center_x_text.__len__())
        for i in range(len(nb_aligned)):
            interval = [xmin_text.iloc[i], xmax_text.iloc[i]]
            for j in range(len(nb_aligned)):
                if interval[0] < center_x_text.iloc[j] < interval[1]:
                    nb_aligned[i] += 1
        max_aligned = nb_aligned.max()
        condition = max_aligned > 5 and max_aligned > 0.75 * nb_text
    return condition


# 1
def lf_layout_gallery(ui):
    # ui contains 3/4 of the images that are vertically or horizontally aligned
    condition = False
    nb_image = ui.components.type.str.count('Image').sum()
    area_ui = ui.width * ui.height
    image_components = ui.components[ui.components['type'].str.contains('Image|Icon')]
    area_images = (image_components.xmax - image_components.xmin) * (image_components.ymax - image_components.ymin)
    if nb_image > 0 and any(area_images / area_ui > 0.01):
        center_x_image = ui.components[ui.components['type'].str.contains('Image')].center_x
        center_y_image = ui.components[ui.components['type'].str.contains('Image')].center_y
        xmin_image = ui.components[ui.components['type'].str.contains('Image')].xmin
        xmax_image = ui.components[ui.components['type'].str.contains('Image')].xmax
        ymin_image = ui.components[ui.components['type'].str.contains('Image')].ymin
        ymax_image = ui.components[ui.components['type'].str.contains('Image')].ymax
        nb_aligned_ver = np.zeros(center_x_image.__len__())
        nb_aligned_hor = np.zeros(center_x_image.__len__())

        for i in range(len(nb_aligned_ver)):
            interval = [xmin_image.iloc[i], xmax_image.iloc[i]]
            for j in range(len(nb_aligned_ver)):
                if interval[0] < center_x_image.iloc[j] < interval[1]:
                    nb_aligned_ver[i] += 1
        max_aligned_ver = nb_aligned_ver.max()

        for i in range(len(nb_aligned_hor)):
            interval = [ymin_image.iloc[i], ymax_image.iloc[i]]
            for j in range(len(nb_aligned_hor)):
                if interval[0] < center_y_image.iloc[j] < interval[1]:
                    nb_aligned_hor[i] += 1
        max_aligned_hor = nb_aligned_hor.max()

        condition = (max_aligned_ver > 1 or max_aligned_hor > 1) and nb_aligned_ver.mean() * nb_aligned_hor.mean() > \
                    0.75 * nb_image
    return condition


# 4
def lf_component_modal(ui):
    # ui contains Modal component
    condition = ui.components.type.str.contains('Modal').sum().__bool__()
    return condition


# 6
def lf_keyword_login(ui):
    # ui contains words like sign in, login,...
    condition = check_words_in_ui(ui,
                                  ['sign in', 'log in', 'login', 'sign up', 'username', 'email', 'e-mail', 'password',
                                   'facebook', 'account'])
    return condition


# 9
def lf_layout_image(ui):
    # ui contains one large image
    area_ui = ui.width * ui.height
    image_components = ui.components[ui.components['type'] == 'Image']
    area_images = (image_components.xmax - image_components.xmin) * (image_components.ymax - image_components.ymin)
    nb_large_image = sum(i > 0.05 for i in area_images / area_ui)
    condition = nb_large_image == 1
    return condition


# 10
def lf_keyword_support(ui):
    # ui contains words like customer, support,...
    condition = check_words_in_ui(ui,
                                  ['support', 'faq', 'customer', 'service', 'feedback', 'license', 'agreement',
                                   'search', 'help', 'question', 'questions', '?'])
    return condition


# 11
def lf_keyword_settings(ui):
    # ui contains words like settings, preferences,...
    condition = check_words_in_ui(ui,
                                  ['settings', 'preferences', 'advanced', 'security', 'set', 'adjust', 'activate'])
    return condition


# 14
def lf_component_menu(ui):
    # ui contains a menu (drawer)
    nb_menu = ui.components.type.str.count('Drawer').sum()
    condition = nb_menu > 0
    return condition


# 16
def lf_component_map(ui):
    # ui contains a map
    nb_map = ui.components.type.str.count('Map').sum()
    condition = nb_map > 0
    return condition


# 17
def lf_keyword_next(ui):
    # ui contains words like skip
    condition = check_words_in_ui(ui, ['skip'])
    return condition


# 18
def lf_keyword_shop(ui):
    # ui contains words like cart, ship,...
    condition = check_words_in_ui(ui, ['ship', 'shipping', 'dollar', 'pound', 'euro', 'payment', 'credit'])
    return condition


# 19
def lf_component_text_button(ui):
    # ui contains a TextButton
    nb_text_button = ui.components.type.str.count('TextButton').sum()
    condition = nb_text_button > 0
    return condition
