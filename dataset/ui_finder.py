import json
import math
import pickle
import random
import matplotlib.pyplot as plt
from pylab import imread
import numpy as np
import re
import num2words

import requests

from UIDatasheet import UIDatasheet

from transformers import AutoTokenizer, AutoModelForQuestionAnswering, AutoModelForSequenceClassification
from transformers import QuestionAnsweringPipeline, ZeroShotClassificationPipeline
tokenizer_qa = AutoTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
model_qa = AutoModelForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
question_answerer = QuestionAnsweringPipeline(model_qa, tokenizer_qa)

tokenizer_zsc = AutoTokenizer.from_pretrained("typeform/distilbert-base-uncased-mnli")
model_zsc = AutoModelForSequenceClassification.from_pretrained("typeform/distilbert-base-uncased-mnli")
zero_shot_classifier = ZeroShotClassificationPipeline(model=model_zsc, tokenizer=tokenizer_zsc)

labels = ['bare', 'empty', 'buy', 'sell', 'shop', 'form', 'grid', 'gallery', 'list', 'log in', 'sign up', 'sign in',
          'register', 'map', 'menu', 'popup', 'news', 'newsfeed', 'profile', 'search', 'find', 'settings',
          'preferences', 'terms', 'conditions', 'tutorial', 'welcome', 'start']

ui_path = 'C:\\Users\\Antoine\\CloudStation\\EPFL\\Master 4\\Master project\\Dataset\\VINS Dataset\\ui_list.dat'
wf_path = 'C:\\Users\\Antoine\\CloudStation\\EPFL\\Master 4\\Master project\\prototype\\assets\\wireframes\\'

with open(ui_path, 'rb') as f:
    ui_list_saved = pickle.load(f)

with open('C:\\Users\\Antoine\\CloudStation\\EPFL\\Master 4\\Master project\\Dataset\\VINS Dataset\\ui_datasheet_list.dat', 'rb') as f:
    ui_datasheet_list = pickle.load(f)


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class ResponseError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- response expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


def get_label(ui_datasheet):
    description = ui_datasheet.description
    ui_word = 'interface'
    description = description.replace('page', 'interface')
    description = description.replace('screen', 'interface')

    label_resp1 = question_answerer(question='What is the type of the {}?'.format(ui_word), context=description)
    answer = label_resp1['answer']
    score_qa = label_resp1['score']

    label = zero_shot_classifier(sequences=answer, candidate_labels=labels)['labels'][0]
    score_zsc = zero_shot_classifier(sequences=answer, candidate_labels=labels)['scores'][0]

    if answer == description or score_zsc < 0.4:
        label_resp2 = question_answerer(question='What is the {} for?'.format(ui_word), context=description)
        answer = label_resp2['answer']
        # raise ResponseError('Label request QA', 'The request could not find an answer')

        label = zero_shot_classifier(sequences=answer, candidate_labels=labels)['labels'][0]
        score_zsc2 = zero_shot_classifier(sequences=answer, candidate_labels=labels)['scores'][0]
        if score_zsc2 < 0.5:
            print('Could not determine the label of the {}'.format(ui_word))
            label = None
    ui_datasheet.label = label


def get_components(ui_datasheet):
    description = ui_datasheet.description
    ui_word = 'interface'
    description = description.replace('page', 'interface')
    description = description.replace('screen', 'interface')

    label_resp1 = question_answerer(question='What are on the {}?'.format(ui_word), context=description)
    answer = label_resp1['answer']
    score_qa = label_resp1['score']

    if answer == description:
        print('Could not determine what is on the {}'.format(ui_word))
    else:
        desc_mod = description
        desc_mod = desc_mod.replace('a ', 'one ')
        desc_mod = desc_mod.replace('an ', 'one ')
        if 'button' in answer:
            label_resp2 = question_answerer(question='How many buttons are on the {}?'.format(ui_word), context=description)
            answer2 = label_resp2['answer']
            if answer2 == 'one':
                ui_datasheet.nb_buttons = 1
            elif answer2 == 'two':
                ui_datasheet.nb_buttons = 2
            elif answer2 == 'three':
                ui_datasheet.nb_buttons = 3
            elif answer2 == 'four':
                ui_datasheet.nb_buttons = 4
            elif answer2 == 'five':
                ui_datasheet.nb_buttons = 5
            else:
                print('Could not determine the number of buttons')
            if ui_datasheet.nb_buttons:
                label_resp3 = question_answerer(question='Where are the buttons located?', context=description)
                answer3 = label_resp3['answer']

                # if 'top' in answer3:

        if 'image' in answer or 'photo' in answer:
            label_resp2 = question_answerer(question='How many images are on the {}?'.format(ui_word), context=description)
            answer2 = label_resp2['answer']
            if answer2 == 'one':
                ui_datasheet.nb_images = 1
            elif answer2 == 'two':
                ui_datasheet.nb_images = 2
            elif answer2 == 'three':
                ui_datasheet.nb_images = 3
            elif answer2 == 'four':
                ui_datasheet.nb_images = 4
            elif answer2 == 'five':
                ui_datasheet.nb_images = 5
            elif answer2 == 'six':
                ui_datasheet.nb_images = 6
            elif answer2 == 'seven':
                ui_datasheet.nb_images = 7
            elif answer2 == 'eight':
                ui_datasheet.nb_images = 8
            elif answer2 == 'nine':
                ui_datasheet.nb_images = 9
            elif answer2 == 'ten':
                ui_datasheet.nb_images = 10
            else:
                print('Could not determine the number of images')
        if 'checkbox' in answer:
            label_resp2 = question_answerer(question='How many checkboxes are on the {}?'.format(ui_word), context=description)
            answer2 = label_resp2['answer']
            if answer2 == 'one':
                ui_datasheet.nb_checkbox = 1
            elif answer2 == 'two':
                ui_datasheet.nb_checkbox = 2
            elif answer2 == 'three':
                ui_datasheet.nb_checkbox = 3
            elif answer2 == 'four':
                ui_datasheet.nb_checkbox = 4
            elif answer2 == 'five':
                ui_datasheet.nb_checkbox = 5
            else:
                print('Could not determine the number of checkboxes')
        if 'input field' in answer:
            label_resp2 = question_answerer(question='How many input fields are on the {}?'.format(ui_word), context=description)
            answer2 = label_resp2['answer']
            if answer2 == 'one':
                ui_datasheet.nb_input_fields = 1
            elif answer2 == 'two':
                ui_datasheet.nb_input_fields = 2
            elif answer2 == 'three':
                ui_datasheet.nb_input_fields = 3
            elif answer2 == 'four':
                ui_datasheet.nb_input_fields = 4
            elif answer2 == 'five':
                ui_datasheet.nb_input_fields = 5
            else:
                print('Could not determine the number of input fields')
        if 'map' in answer:
            label_resp2 = question_answerer(question='How many maps are on the {}?'.format(ui_word), context=description)
            answer2 = label_resp2['answer']
            if answer2 == 'one':
                ui_datasheet.nb_map = 1
            else:
                print('Could not determine the number of maps')


def search_wf(ui_datasheet, k):
    label = ui_datasheet.label
    topk_list = []
    global ui_datasheet_list
    if label is None:
        topk_list = apply_knn(ui_datasheet, ui_datasheet_list, k)

    if label == 'bare' or label == 'empty':
        ui_datasheet_sel = []
        for i in range(len(ui_datasheet_list)):
            if ui_datasheet_list[i].label == 'bare':
                ui_datasheet_sel.append(ui_datasheet_list[i])
        topk_list = apply_knn(ui_datasheet, ui_datasheet_sel, k)

    if label == 'buy' or label == 'sell' or label == 'shop':
        ui_datasheet_sel = []
        for i in range(len(ui_datasheet_list)):
            if ui_datasheet_list[i].label == 'shop':
                ui_datasheet_sel.append(ui_datasheet_list[i])
        topk_list = apply_knn(ui_datasheet, ui_datasheet_sel, k)

    if label == 'form':
        ui_datasheet_sel = []
        for i in range(len(ui_datasheet_list)):
            if ui_datasheet_list[i].label == 'form':
                ui_datasheet_sel.append(ui_datasheet_list[i])
        topk_list = apply_knn(ui_datasheet, ui_datasheet_sel, k)

    if label == 'gallery' or label == 'grid':
        ui_datasheet_sel = []
        for i in range(len(ui_datasheet_list)):
            if ui_datasheet_list[i].label == 'gallery':
                ui_datasheet_sel.append(ui_datasheet_list[i])
        topk_list = apply_knn(ui_datasheet, ui_datasheet_sel, k)

    if label == 'list':
        ui_datasheet_sel = []
        for i in range(len(ui_datasheet_list)):
            if ui_datasheet_list[i].label == 'list':
                ui_datasheet_sel.append(ui_datasheet_list[i])
        topk_list = apply_knn(ui_datasheet, ui_datasheet_sel, k)

    if label == 'log in' or label == 'sign up' or label == 'sign in' or label == 'register':
        ui_datasheet_sel = []
        for i in range(len(ui_datasheet_list)):
            if ui_datasheet_list[i].label == 'login' and label in ui_datasheet_list[i].button_text:
                ui_datasheet_sel.append(ui_datasheet_list[i])
        topk_list = apply_knn(ui_datasheet, ui_datasheet_sel, k)

    if label == 'map':
        ui_datasheet_sel = []
        for i in range(len(ui_datasheet_list)):
            if ui_datasheet_list[i].label == 'maps':
                ui_datasheet_sel.append(ui_datasheet_list[i])
        topk_list = apply_knn(ui_datasheet, ui_datasheet_sel, k)

    if label == 'menu':
        ui_datasheet_sel = []
        for i in range(len(ui_datasheet_list)):
            if ui_datasheet_list[i].label == 'menu':
                ui_datasheet_sel.append(ui_datasheet_list[i])
        topk_list = apply_knn(ui_datasheet, ui_datasheet_sel, k)

    if label == 'popup':
        ui_datasheet_sel = []
        for i in range(len(ui_datasheet_list)):
            if ui_datasheet_list[i].label == 'modal':
                ui_datasheet_sel.append(ui_datasheet_list[i])
        topk_list = apply_knn(ui_datasheet, ui_datasheet_sel, k)

    if label == 'news' or label == 'newsfeed':
        ui_datasheet_sel = []
        for i in range(len(ui_datasheet_list)):
            if ui_datasheet_list[i].label == 'news':
                ui_datasheet_sel.append(ui_datasheet_list[i])
        topk_list = apply_knn(ui_datasheet, ui_datasheet_sel, k)

    if label == 'profile':
        ui_datasheet_sel = []
        for i in range(len(ui_datasheet_list)):
            if ui_datasheet_list[i].label == 'profile':
                ui_datasheet_sel.append(ui_datasheet_list[i])
        topk_list = apply_knn(ui_datasheet, ui_datasheet_sel, k)

    if label == 'search' or label == 'find':
        ui_datasheet_sel = []
        for i in range(len(ui_datasheet_list)):
            if ui_datasheet_list[i].label == 'search':
                ui_datasheet_sel.append(ui_datasheet_list[i])
        topk_list = apply_knn(ui_datasheet, ui_datasheet_sel, k)

    if label == 'settings' or label == 'preferences':
        ui_datasheet_sel = []
        for i in range(len(ui_datasheet_list)):
            if ui_datasheet_list[i].label == 'settings':
                ui_datasheet_sel.append(ui_datasheet_list[i])
        topk_list = apply_knn(ui_datasheet, ui_datasheet_sel, k)

    if label == 'terms' or label == 'conditions':
        ui_datasheet_sel = []
        for i in range(len(ui_datasheet_list)):
            if ui_datasheet_list[i].label == 'terms':
                ui_datasheet_sel.append(ui_datasheet_list[i])
        topk_list = apply_knn(ui_datasheet, ui_datasheet_sel, k)

    if label == 'tutorial' or label == 'welcome' or label == 'start':
        ui_datasheet_sel = []
        for i in range(len(ui_datasheet_list)):
            if ui_datasheet_list[i].label == 'tutorial':
                ui_datasheet_sel.append(ui_datasheet_list[i])
        topk_list = apply_knn(ui_datasheet, ui_datasheet_sel, k)
    return topk_list


def apply_knn(ui_datasheet, ui_datasheet_list, k):
    distances = np.zeros((len(ui_datasheet_list), 2), int)

    distances[:, 0] = np.arange(len(ui_datasheet_list))
    name_list = []
    for i in range(len(ui_datasheet_list)):
        name_list.append(ui_datasheet_list[i].name)

    if ui_datasheet.nb_buttons is not None:
        for i in range(len(ui_datasheet_list)):
            distances[i, 1] += (ui_datasheet.nb_buttons - ui_datasheet_list[i].nb_buttons) ** 2

    if ui_datasheet.nb_images is not None:
        for i in range(len(ui_datasheet_list)):
            distances[i, 1] += (ui_datasheet.nb_images - ui_datasheet_list[i].nb_images) ** 2

    if ui_datasheet.nb_checkbox is not None:
        for i in range(len(ui_datasheet_list)):
            distances[i, 1] += (ui_datasheet.nb_checkbox - ui_datasheet_list[i].nb_checkbox) ** 2

    if ui_datasheet.nb_input_fields is not None:
        for i in range(len(ui_datasheet_list)):
            distances[i, 1] += (ui_datasheet.nb_input_fields - ui_datasheet_list[i].nb_input_fields) ** 2

    if ui_datasheet.nb_map is not None:
        for i in range(len(ui_datasheet_list)):
            distances[i, 1] += (ui_datasheet.nb_map - ui_datasheet_list[i].nb_map) ** 2

    match = []
    for i in range(len(ui_datasheet_list)):
        if distances[i, 1] == 0:
            match.append(distances[i, 0])

    topk_list = []
    if len(match) >= k:
        topk_list = random.sample(match, k)
    else:
        sorted_dist = sorted(distances, key=lambda x: x[1])
        for j in range(k):
            topk_list.append(sorted_dist[j][0])

    for i in range(len(topk_list)):
        topk_list[i] = name_list[topk_list[i]]

    return topk_list


def print_info(ui_datasheet):
    info = ''
    info += 'Information retrieved: '
    if ui_datasheet.label:
        info += 'Label: ' + ui_datasheet.label
    if ui_datasheet.nb_buttons:
        info += ', Nb buttons: {}'.format(ui_datasheet.nb_buttons)
    if ui_datasheet.nb_images:
        info += ', Nb images: {}'.format(ui_datasheet.nb_images)
    if ui_datasheet.nb_checkbox:
        info += ', Nb checkboxes: {}'.format(ui_datasheet.nb_checkbox)
    if ui_datasheet.nb_input_fields:
        info += ', Nb input fields: {}'.format(ui_datasheet.nb_input_fields)
    if ui_datasheet.nb_map:
        info += ', Nb maps: {}'.format(ui_datasheet.nb_map)
    return info


# description = 'Give me a page to sign up with an account'
# description = 'A screen for buying some items'
# description = 'I want a form page with four input fields and one button'
# description = 'I would like to have a interface to log in with two input fields and one button'
# description = 'I want an interface with a grid of five images'
# description = 'An interface for the settings'
# description = 'An interface to set my preferences'
#
# description = 'I want a newsfeed interface with an image at the top and an image at the bottom'
# description = 'I want a login page with three buttons'
#
# description = re.sub(r"(\d+)", lambda x: num2words.num2words(int(x.group(0))), description)
# ui_datasheet = UIDatasheet()
# ui_datasheet.description = description
# get_label(ui_datasheet)
# get_components(ui_datasheet)
# print_info(ui_datasheet)
#
# wf_list = search_wf(ui_datasheet, 4)
# if wf_list:
#     fig = plt.figure(figsize=(11, 11))
#     columns = 2
#     rows = 2
#     for i in range(1, columns * rows + 1):
#         img = imread(wf_path + wf_list[i - 1] + '.jpg')
#         fig.add_subplot(rows, columns, i)
#         plt.xticks([])
#         plt.yticks([])
#         plt.imshow(img)
#     plt.show()