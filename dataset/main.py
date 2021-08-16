import pickle

from UI import UI
import os
import pytesseract
from google.cloud import vision
import json
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw
import data_labeller
from data_labeller import classify_ui
from ui_descriptor import describe_ui
import seaborn as sns
import matplotlib.pyplot as plt


if __name__ == '__main__':
    # path of the dataset
    path_annotations = 'C:\\Users\\Antoine\\CloudStation\\EPFL\\Master 4\\Master project\\Dataset\\VINS Dataset\\Annotations'
    directory = sorted(os.listdir(path_annotations), key=len)
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'masterproject-307316-27f773a9a493.json'
    # vision_client = vision.ImageAnnotatorClient()
    # ui_list = []

    # for filename in directory:
    #     full_path = os.path.join(path_annotations, filename)
    #     ui = UI(full_path)
    #     ui.get_text_ocr(vision_client)
    #     ui_list.append(ui)

    ui_path = 'C:\\Users\\Antoine\\CloudStation\\EPFL\\Master 4\\Master project\\Dataset\\VINS Dataset\\ui_list.dat'
    # with open(ui_path, 'wb') as f:
    #     pickle.dump(ui_list, f)

    with open(ui_path, 'rb') as f:
        ui_list_saved = pickle.load(f)
    # with open(ui_path, 'wb') as f:
    #     pickle.dump(ui_list, f)

    with open(ui_path, 'rb') as f:
        ui_list_saved = pickle.load(f)

    name_list = []
    for ui in ui_list_saved:
        name_list.append(ui.name+'.jpg')


    name = '1669'
    index = [i for i in range(len(ui_list_saved)) if ui_list_saved[i].name == name][0]
    ui_ = ui_list_saved[index]
    classify_ui(ui_list_saved[index:index + 1])
    description = describe_ui(ui_list_saved[index])

    classify_ui(ui_list_saved)
    nb_descriptions = 5
    for d in range(nb_descriptions):
        description_df = pd.DataFrame('', index=np.arange(len(ui_list_saved)),
                                      columns=['jpeg_file', 'width', 'height', 'label', 'description'])
        drop = []
        list_wf = os.listdir(
            'C:\\Users\\Antoine\\CloudStation\\EPFL\\Master 4\\Master project\\prototype\\assets\\wireframes')
        list_jpg = os.listdir(
            'C:\\Users\\Antoine\\CloudStation\\EPFL\\Master 4\\Master project\\Dataset\\VINS Dataset\\JPEGImages')
        file_diff = list(set(list_wf) ^ set(list_jpg))
        for i in range(len(ui_list_saved)):
            print('{}th round, {}th ui, {}% done'.format(d, i, (i/len(ui_list_saved))*100))
            description_df.loc[i, 'jpeg_file'] = ui_list_saved[i].JPEG_path.split('\\')[-1]
            description_df.loc[i, 'width'] = ui_list_saved[i].width
            description_df.loc[i, 'height'] = ui_list_saved[i].height
            description_df.loc[i, 'label'] = ui_list_saved[i].label
            if ui_list_saved[i].label == -1 or ui_list_saved[i].JPEG_path.split('\\')[-1] in file_diff:
                drop.append(i)
            description_df.loc[i, 'description'] = describe_ui(ui_list_saved[i])

        description_df.drop(drop, inplace=True)
        description_df.reset_index(drop=True, inplace=True)
        json_directory = 'C:\\Users\\Antoine\\CloudStation\\EPFL\\Master 4\\Master project\\Dataset\\VINS Dataset\\'
        description_df.to_json(json_directory + 'descriptions_' + str(d) + '.json', orient='index')

    # ui_df = pd.DataFrame([vars(ui) for ui in ui_list])
    # preds_train = apply_label(ui_df)
    # ui_df.label = preds_train

    label_list = []
    classify_ui(ui_list_saved)
    for ui in ui_list_saved:
        ui.put_text_right_component()

    import matplotlib.pyplot as plt
    import seaborn as sns
    ax = sns.countplot(x=label_list)
    ax.set_xticklabels(
        labels=['Abstain', 'List', 'Popup', 'Popup login', 'Popup list', 'Login', 'Information', 'Settings',
                'Menu', 'Gallery', 'Shop'], rotation=75)
    plt.tight_layout()
    plt.show()

    index = 37
    source_img = Image.open(ui_list_saved[index].JPEG_path).convert("RGBA")
    draw = ImageDraw.Draw(source_img)
    for i in range(ui_list_saved[index].components.index.size):
        xmin = ui_list_saved[index].components.loc[i].xmin
        ymin = ui_list_saved[index].components.loc[i].ymin
        xmax = ui_list_saved[index].components.loc[i].xmax
        ymax = ui_list_saved[index].components.loc[i].ymax
        draw.rectangle(((xmin, ymin), (xmax, ymax)), outline="red")
        center = (int((xmax - xmin) / 2 + xmin), int((ymax - ymin) / 2 + ymin))
        draw.text(center, ui_list_saved[index].components.loc[i].type, fill=(255, 0, 0, 255))
    source_img.show()


    with open('C:\\Users\\Antoine\\CloudStation\\EPFL\\Master 4\\Master project\\Dataset\\VINS Dataset\\ui_label.json') as f:
        ui_label = json.load(f)

    count=0
    for i in range(len(ui_list_saved)):
        for j in range(len(ui_label)):
            if ui_list_saved[i].name+'.jpg' == ui_label[j]['External ID']:
                count+=1
                ui_list_saved[i].label = ui_label[j]['Label']['classifications'][0]['answer'][0]['title']

    # for i in range(len(ui_list_saved)):
    #     ui_list_saved[i] = crop_popup(ui_list_saved[i])

    for i in range(len(ui_list_saved)):
        if 'CheckBox' in ui_list_saved[i].components.type.values:
            print(ui_list_saved[i].name)

    with open(ui_path, 'wb') as f:
        pickle.dump(ui_list_saved, f)

    ui_df = pd.DataFrame([vars(ui) for ui in ui_list_saved])

    for index, ui in ui_df.iterrows():
        components = ui_df.loc[index].components
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

        if 'Drawer' in components.type.values:
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
        ui_df.at[index, 'components'] = components

    ui_path_json = 'C:\\Users\\Antoine\\CloudStation\\EPFL\\Master 4\\Master project\\Dataset\\VINS Dataset\\ui_list.json'
    ui_df.to_json(ui_path_json)

    list_remove = []
    path = 'C:\\Users\\Antoine\\CloudStation\\EPFL\\Master 4\\Master project\\prototype\\assets\\wireframes\\'
    for i in range(len(ui_list_saved)):
        if ui_list_saved[i].label == 'tutorial':
            list_remove.append(path + ui_list_saved[i].name + '.jpg')

    num_to_select = 750
    list_of_random_items = random.sample(list_remove, num_to_select)

    for i in range(len(list_of_random_items)):
        if os.path.isfile(list_of_random_items[i]):
            os.remove(list_of_random_items[i])

    from collections import Counter
    label_list = []
    for ui in ui_list_saved:
        if ui.label == -1:
            continue
        label_list.append(ui.label)
    counter = Counter(label_list)
    prob_list = []
    for key in counter.keys():
        prob_list.append(counter.get(key)/len(label_list)*100)
    sns.displot(label_list)
    plt.xticks(rotation=60)
    plt.tight_layout()
    plt.show()


    # Fixing random state for reproducibility
    np.random.seed(19680801)
    def randrange(n, vmin, vmax):
        return (vmax - vmin) * np.random.rand(n) + vmin
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    n = 100
    # For each set of style and range settings, plot n random points in the box
    # defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
    for m, zlow, zhigh in [('o', 0, 10), ('^', 0, 10), ('v', 0, 10), ('8', 0, 10), ('h', 0, 10), ('x', 0, 10), ('3', 0, 10)]:
        xs = randrange(n, 0, 10)
        ys = randrange(n, 0, 10)
        zs = randrange(n, zlow, zhigh)
        ax.scatter(xs, ys, zs, marker=m)

    ax.set_xlabel('Nb_button')
    ax.set_ylabel('Nb_image')
    ax.set_zlabel('Nb_input_field')
    plt.show()

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    n = 20
    # For each set of style and range settings, plot n random points in the box
    # defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
    points = np.zeros((n, 3))
    i = 0
    for m, zlow, zhigh in [('o', 0, 10)]:
        xs = randrange(n, 0, 10)
        ys = randrange(n, 0, 10)
        zs = randrange(n, zlow, zhigh)
        ax.scatter(xs, ys, zs, color = [1,0,0], marker=m)
        i += 1
    points[:, 0] = xs
    points[:, 1] = ys
    points[:, 2] = zs
    x_p = 2
    y_p = 1
    z_p = 2
    ax.scatter(x_p, y_p, z_p, color=[0,0,0], marker='o')
    sorted_points = sorted(points, key = lambda K: np.sqrt((K[0]-x_p)**2 + (K[1]-y_p)**2 + (K[2]-z_p)**2))
    for i in range(4):
        ax.plot([x_p, sorted_points[i][0]], [y_p, sorted_points[i][1]], [z_p, sorted_points[i][2]], 'r')


    ax.set_xlabel('Nb_button')
    ax.set_ylabel('Nb_image')
    ax.set_zlabel('Nb_input_field')
    plt.show()