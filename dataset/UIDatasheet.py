import pickle


class UIDatasheet:
    def __init__(self):
        self.description = None
        self.name = None

        self.label = None
        self.button_text = ''

        self.nb_buttons = None
        self.nb_images = None
        self.nb_checkbox = None
        self.nb_input_fields = None
        self.nb_map = None

        self.button1_x = None
        self.button1_y = None
        self.button2_x = None
        self.button2_y = None
        self.button3_x = None
        self.button3_y = None
        self.button4_x = None
        self.button4_y = None
        self.button5_x = None
        self.button5_y = None

        self.image1_x = None
        self.image1_y = None
        self.image2_x = None
        self.image2_y = None
        self.image3_x = None
        self.image3_y = None
        self.image4_x = None
        self.image4_y = None
        self.image5_x = None
        self.image5_y = None
        self.image6_x = None
        self.image6_y = None
        self.image7_x = None
        self.image7_y = None
        self.image8_x = None
        self.image8_y = None
        self.image9_x = None
        self.image9_y = None
        self.image10_x = None
        self.image10_y = None

        self.checkbox1_x = None
        self.checkbox1_y = None
        self.checkbox2_x = None
        self.checkbox2_y = None
        self.checkbox3_x = None
        self.checkbox3_y = None
        self.checkbox4_x = None
        self.checkbox4_y = None
        self.checkbox5_x = None
        self.checkbox5_y = None

        self.input_field1_x = None
        self.input_field1_y = None
        self.input_field2_x = None
        self.input_field2_y = None
        self.input_field3_x = None
        self.input_field3_y = None
        self.input_field4_x = None
        self.input_field4_y = None
        self.input_field5_x = None
        self.input_field5_y = None

        self.map1_x = None
        self.map1_y = None



ui_path = 'C:\\Users\\Antoine\\CloudStation\\EPFL\\Master 4\\Master project\\Dataset\\VINS Dataset\\ui_list.dat'
wf_path = 'C:\\Users\\Antoine\\CloudStation\\EPFL\\Master 4\\Master project\\prototype\\assets\\wireframes\\'

with open(ui_path, 'rb') as f:
    ui_list_saved = pickle.load(f)

ui_datasheet_list = [None] * len(ui_list_saved)

for i in range(len(ui_list_saved)):
    ui_datasheet_list[i] = UIDatasheet()
    ui_datasheet_list[i].label = ui_list_saved[i].label
    ui_datasheet_list[i].name = ui_list_saved[i].name
    button_text = ''
    for j, component in ui_list_saved[i].components.iterrows():
        if component.type == 'TextButton':
            button_text += component.text + ' '
    ui_datasheet_list[i].button_text = button_text
    ui_datasheet_list[i].nb_buttons = ui_list_saved[i].components.type.str.count('TextButton').sum()
    ui_datasheet_list[i].nb_images = ui_list_saved[i].components.type.str.count('Image').sum()
    ui_datasheet_list[i].nb_checkbox = ui_list_saved[i].components.type.str.count('CheckedTextView').sum()
    ui_datasheet_list[i].nb_input_fields = ui_list_saved[i].components.type.str.count('EditText').sum()
    ui_datasheet_list[i].nb_map = ui_list_saved[i].components.type.str.count('Map').sum()

with open('C:\\Users\\Antoine\\CloudStation\\EPFL\\Master 4\\Master project\\Dataset\\VINS Dataset\\ui_datasheet_list.dat', 'wb') as f:
        pickle.dump(ui_datasheet_list, f)