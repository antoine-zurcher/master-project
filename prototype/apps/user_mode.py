import json

import dash_core_components as dcc
import dash_html_components as html
from dash_devices.dependencies import Input, Output, State
import numpy as np
import sys
import os
import requests
from requests.structures import CaseInsensitiveDict
import base64
from dash_dangerously_set_inner_html import DangerouslySetInnerHTML
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

sys.path.insert(1, 'C:\\Users\\Antoine\\CloudStation\\EPFL\\dash_react')

from app import app

gauth = GoogleAuth()
gauth.LoadCredentialsFile('credentials.txt')
drive = GoogleDrive(gauth)

rootList = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file in rootList:
    if file['title'] == "MasterProject":
        folderID_mp = file['id']

mpList = drive.ListFile({'q': "'{}' in parents and trashed=false".format(folderID_mp)}).GetList()
for file in mpList:
    if file['title'] == "Wireframes":
        folderID_wf = file['id']

wfList = drive.ListFile({'q': "'{}' in parents and trashed=false".format(folderID_wf)}).GetList()

image_files = os.listdir('./assets/wireframes')
image_names = [i.replace('.jpg', '') for i in image_files]
image_dict = []
for i in range(len(image_names)):
    image_dict.append({'label': image_names[i], 'value': image_names[i]})


class Data:
    def __init__(self):
        self.id_user = ''
        self.image_selected = 'none'
        self.descriptions = []
        self.images = []
        self.images_selected = []
        self.commands = []
        self.image_sent = False
        self.image_url = ''
        self.image_base64 = ''


figma_api_token = '182858-d8d7ecf4-fab9-4bdb-b3dd-a1837bcb036b'
data = Data()

# styling the sidebar
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 80,
    'left': 0,
    'bottom': 0,
    'width': '20rem',
    'padding': '2rem 1rem',
    'background-color': '#f8f9fa',
}

# padding for the page content
CONTENT_STYLE = {
    'margin-left': '22rem',
    'margin-right': '2rem',
    'padding': '2rem 1rem',
}

IMAGE_STYLE = {
    'width': '20%',
    'margin-right': 50,
    'margin-bottom': 50,
    'border': '3px solid white',
}

sidebar_finder = html.Div(
    [
        html.H2('UI', className='display-4'),
        html.Hr(),
        html.P(
            'Please enter your description:', className='lead'
        ),
        dcc.Textarea(
            id='textarea-description',
            value='',
            style={'width': '100%', 'height': 300},
        ),
        html.Div(
            [
                html.Button('Clear', id='button-clear-description', n_clicks=0, style={'margin': '15px'}),
                html.Button('Find', id='button-find', n_clicks=0, style={'margin': '15px'}),
            ],
            style={'margin-bottom': '10px',
                   'textAlign': 'center',
                   'width': '220px',
                   'margin': 'auto'}
        )
    ],
    style=SIDEBAR_STYLE,
)

sidebar_editor = html.Div(
    [
        html.H2('UI', className='display-4'),
        html.Hr(),
        html.P(
            'Please enter your command:', className='lead'
        ),
        dcc.Textarea(
            id='textarea-command',
            value='cmd: ',
            style={'width': '100%', 'height': 300},
        ),
        html.Div(
            [
                html.Button('Clear', id='button-clear-command', n_clicks=0, style={'margin': '15px'}),
                html.Button('Execute', id='button-execute', n_clicks=0, style={'margin': '15px'}),
            ],
            style={'margin-bottom': '10px',
                   'textAlign': 'center',
                   'width': '220px',
                   'margin': 'auto'}
        ),
        html.P('', id='content-error', style={'color': 'red'}),
    ],
    style=SIDEBAR_STYLE,
)

image_gallery = html.Div(
    [
        html.Div(
            [
                html.H1('User interface finder'),
                html.Hr()
            ]
        ),
        html.Div(
            html.P('First enter your description on the left, then select the UI from the list and then click on the next button at the bottom:')
        ),
        html.Div(
            [
                html.Div([
                    html.Img(src=app.get_asset_url('UI_pres.jpg'), id='img0', className='imageUI',
                             n_clicks_timestamp=-1, style={'max-height': '100vh', 'max-width': '60vh'}),
                ], style={'flex-grow': '1', 'margin': '15px'}),
                html.Div([
                    html.Img(src=app.get_asset_url('UI_pres.jpg'), id='img1', className='imageUI',
                             n_clicks_timestamp=-1, style={'max-height': '100vh', 'max-width': '60vh'}),
                ], style={'flex-grow': '1', 'margin': '15px'}),
                html.Div([
                    html.Img(src=app.get_asset_url('UI_pres.jpg'), id='img2', className='imageUI',
                             n_clicks_timestamp=-1, style={'max-height': '100vh', 'max-width': '60vh'}),
                ], style={'flex-grow': '1', 'margin': '15px'}),
                html.Div([
                    html.Img(src=app.get_asset_url('UI_pres.jpg'), id='img3', className='imageUI',
                             n_clicks_timestamp=-1, style={'max-height': '100vh', 'max-width': '60vh'}),
                ], style={'flex-grow': '1', 'margin': '15px'}),
            ], style={'display': 'flex'}
        ),
        html.Div(
            [
                html.Button(id='button-select', n_clicks=0,
                            style={'width': '40px', 'height': '40px', 'position': 'absolute',
                                   'right': '10%', 'padding': '2.5px'},
                            children=[html.Img(src=app.get_asset_url('arrow_right.png'), style={'width': '30px'})]),
            ],
            style={'margin-bottom': '10px',
                   'position': 'relative',
                   'margin': 'auto'}),
        # html.Div(
        #     [
        #         html.Div([
        #             html.Img(src=app.get_asset_url('UI_pres.jpg'), id='img4', className='imageUI',
        #                      n_clicks_timestamp=-1),
        #         ], style={'flex-grow': '1', 'margin': '15px'}),
        #         html.Div([
        #             html.Img(src=app.get_asset_url('UI_pres.jpg'), id='img5', className='imageUI',
        #                      n_clicks_timestamp=-1),
        #         ], style={'flex-grow': '1', 'margin': '15px'}),
        #         html.Div([
        #             html.Img(src=app.get_asset_url('UI_pres.jpg'), id='img6', className='imageUI',
        #                      n_clicks_timestamp=-1),
        #         ], style={'flex-grow': '1', 'margin': '15px'}),
        #         html.Div([
        #             html.Img(src=app.get_asset_url('UI_pres.jpg'), id='img7', className='imageUI',
        #                      n_clicks_timestamp=-1),
        #         ], style={'flex-grow': '1', 'margin': '15px'}),
        #     ], style={'display': 'flex'}
        # ),
    ],
    style=CONTENT_STYLE,
)

finder_layout = [sidebar_finder,
                 image_gallery
                 ]

editor_layout = html.Div([
    html.Div([
        html.Div(
            sidebar_editor,
            style={'width': '22rem', 'display': 'inline-block'}
        ),
        html.Div([
            html.H1('UI Editor'),
            html.P('This interface allows you to edit the layout of the UI by typing a command on the left. Please validate each modification with the button at the bottom:'),
            # dash_react.UIEditor(
            #     id='input',
            #     value='my-value',
            #     label='my-label'),
            html.Img(id='img-loading', hidden=True,
                     style={'width': '100%', 'height': '70vh', 'border': '1px solid rgba(0, 0, 0, 0.1)'}),
            html.Iframe(
                src='https://www.figma.com/embed?embed_host=share&url=https%3A%2F%2Fwww.figma.com%2Ffile%2FYHp4UvwlZfU65BKOOnMnDV%2FUI%3Fnode-id%3D0%253A1',
                style={'width': '100%', 'height': '70vh', 'border': '1px solid rgba(0, 0, 0, 0.1)'}),
            html.Div(
                [
                    html.Button(id='button-back-find', n_clicks=0,
                                style={'width': '40px', 'height': '40px', 'position': 'absolute',
                                       'left': '10%', 'padding': '2.5px'},
                                children=[html.Img(src=app.get_asset_url('arrow_left.png'), style={'width': '30px'})]),
                    html.Button('Validate modification', id='button-validate', n_clicks=0, style={'margin': '15px'}),
                    html.Button(id='button-finish', n_clicks=0,
                                style={'width': '40px', 'height': '40px', 'position': 'absolute',
                                       'right': '10%', 'padding': '2.5px'},
                                children=[html.Img(src=app.get_asset_url('arrow_right.png'), style={'width': '30px'})]),
                ],
                style={'margin-bottom': '10px',
                       'textAlign': 'center',
                       'position': 'relative',
                       'margin': 'auto'}),
        ],
            style={'width': '70%', 'display': 'inline-block'}
        ),
    ]),
])

result_layout = html.Div([
    html.Div([
        html.H1('UI Result'),
        html.Img(id='img-result', src=app.get_asset_url('background.png'),
                 style={'height': '70vh', 'border': '1px solid rgba(0, 0, 0, 0.1)'}),
    ], style={'text-align': 'center'}),
    html.Div(
        [
            html.Button(id='button-back', n_clicks=0,
                        style={'width': '40px', 'height': '40px', 'position': 'absolute',
                               'left': '40%', 'padding': '2.5px'},
                        children=[html.Img(src=app.get_asset_url('arrow_left.png'), style={'width': '30px'})]),
            html.A(html.Button('Export', id='button-export', n_clicks=0, hidden=True,
                               style={'margin': '15px'}),
                   id='download-image', download='UI', href=data.image_base64),
            html.Button(id='button-next', n_clicks=0,
                        style={'width': '40px', 'height': '40px', 'position': 'absolute',
                               'right': '40%', 'padding': '2.5px'},
                        children=[html.Img(src=app.get_asset_url('arrow_right.png'), style={'width': '30px'})]),
        ],
        style={'margin-bottom': '10px',
               'textAlign': 'center',
               'width': '220px',
               'margin': 'auto'}
    ),
])

form_layout = html.Div([
    html.Iframe(
        src='https://docs.google.com/forms/d/e/1FAIpQLScvlYxx6FVUPIwJMXtDmtckbz_dkEZy92rZpC1MzF9m1Z81IQ/viewform?embedded=true',
        style={'width': '100vw', 'height': '100vh', 'frameborder': '0', 'marginheight': '0', 'marginwidth': '0'}),
])

layout = html.Div([
    dcc.Tabs(id='tabs-user', value='tab-finder', children=[
        dcc.Tab(label='UI finder', value='tab-finder', children=finder_layout),
        dcc.Tab(label='UI editor', value='tab-editor', children=editor_layout),
        dcc.Tab(label='UI result', value='tab-result', children=result_layout),
        dcc.Tab(label='Survey', value='tab-form', children=form_layout),
    ])
])


@app.callback(
    [Output('img0', 'className'),
     Output('img1', 'className'),
     Output('img2', 'className'),
     Output('img3', 'className'),
     # Output('img4', 'className'),
     # Output('img5', 'className'),
     # Output('img6', 'className'),
     # Output('img7', 'className')
     ],
    [Input('img0', 'n_clicks_timestamp'),
     Input('img1', 'n_clicks_timestamp'),
     Input('img2', 'n_clicks_timestamp'),
     Input('img3', 'n_clicks_timestamp'),
     # Input('img4', 'n_clicks_timestamp'),
     # Input('img5', 'n_clicks_timestamp'),
     # Input('img6', 'n_clicks_timestamp'),
     # Input('img7', 'n_clicks_timestamp')
     ])
def display_image(n_clicks_timestamp0, n_clicks_timestamp1, n_clicks_timestamp2, n_clicks_timestamp3):
    l = [n_clicks_timestamp0, n_clicks_timestamp1, n_clicks_timestamp2, n_clicks_timestamp3]
    max_idx = np.argmax(l)
    if sum(l) != -1 * len(l) and data.images_selected:
        data.image_selected = data.images_selected[max_idx]
    else:
        return 'imageUI', 'imageUI', 'imageUI', 'imageUI'

    if max_idx == 0:
        return 'imageUIselected', 'imageUI', 'imageUI', 'imageUI'
    elif max_idx == 1:
        return 'imageUI', 'imageUIselected', 'imageUI', 'imageUI'
    elif max_idx == 2:
        return 'imageUI', 'imageUI', 'imageUIselected', 'imageUI'
    elif max_idx == 3:
        return 'imageUI', 'imageUI', 'imageUI', 'imageUIselected'


@app.callback(Output('tabs-user', 'value'),
              [Input('button-select', 'n_clicks')])
def render_content(n_clicks):
    if n_clicks and data.image_sent:
        data.images.append(data.image_selected)
        image_content = ''
        if data.images:
            nb_desc = len(data.images)
            for i in range(nb_desc):
                image_content += '{}: {} <br>'.format(i + 1, data.images[i].replace('.jpg', ''))
        app.push_mods({'content-image': {'children': DangerouslySetInnerHTML(image_content)}})
        return 'tab-editor'
    return 'tab-finder'


@app.callback(
    Output('textarea-description', 'value'),
    [Input('button-find', 'n_clicks')],
    [State('textarea-description', 'value')])
def update_output(n_clicks, description):
    if n_clicks and description:
        data.descriptions.append(description)
        description_content = ''
        if data.descriptions:
            nb_desc = len(data.descriptions)
            for i in range(nb_desc):
                description_content += '{}: {} <br>'.format(i + 1, data.descriptions[i])
        app.push_mods({'content-description': {'children': DangerouslySetInnerHTML(description_content)}})
        app.push_mods({'img0': {'src': app.get_asset_url('UI_load.jpg')}})
        app.push_mods({'img1': {'src': app.get_asset_url('UI_load.jpg')}})
        app.push_mods({'img2': {'src': app.get_asset_url('UI_load.jpg')}})
        app.push_mods({'img3': {'src': app.get_asset_url('UI_load.jpg')}})
        # app.push_mods({'img4': {'src': app.get_asset_url('UI_load.jpg')}})
        # app.push_mods({'img5': {'src': app.get_asset_url('UI_load.jpg')}})
        # app.push_mods({'img6': {'src': app.get_asset_url('UI_load.jpg')}})
        # app.push_mods({'img7': {'src': app.get_asset_url('UI_load.jpg')}})
        return description


@app.callback(
    None,
    [Input('button-execute', 'n_clicks')],
    [State('textarea-command', 'value')])
def execute_command(n_clicks, command):
    if n_clicks:
        data.commands.append(command)
        command_content = ''
        if data.commands:
            nb_desc = len(data.commands)
            for i in range(nb_desc):
                command_content += '{}: {} <br>'.format(i + 1, data.commands[i])
        app.push_mods({'content-command': {'children': DangerouslySetInnerHTML(command_content)}})


@app.callback(
    None,
    [Input('button-validate', 'n_clicks')],
    [State('textarea-command', 'value')])
def validate_command(n_clicks, command):
    if n_clicks:
        app.push_mods({'textarea-command': {'value': command + '\ncmd: '}})


@app.callback(
    None,
    [Input('button-clear-description', 'n_clicks')])
def update_output(n_clicks):
    if n_clicks:
        app.push_mods({'textarea-description': {'value': ''}})


@app.callback(
    None,
    [Input('button-finish', 'n_clicks')])
def update_output(n_clicks):
    if n_clicks:
        url = "https://api.figma.com/v1/images/YHp4UvwlZfU65BKOOnMnDV?ids=743%3A253"

        headers = CaseInsensitiveDict()
        headers["X-FIGMA-TOKEN"] = "214680-f1f99611-f1ed-4d11-bd47-6912a503256c"

        resp = requests.get(url, headers=headers)
        global data
        data.image_url = resp.json()['images'].get('743:253')
        r = requests.get(url=data.image_url)
        # with open("./assets/UI_export.png", 'wb') as f:
        #     f.write(r.content)
        # with open("./assets/UI_export.png", "rb") as img_file:
        #     my_string = base64.b64encode(img_file.read())
        data.image_base64 = 'data:image/png;base64,' + str(base64.b64encode(r.content))[2:-1]
        app.push_mods({'button-export': {'hidden': False}})
        app.push_mods({'tabs-user': {'value': 'tab-result'}})
        app.push_mods({'img-result': {'src': data.image_base64}})
        app.push_mods({'download-image': {'href': data.image_base64}})
        if data.id_user:
            data_json = json.dumps(data.__dict__)
            path_json = 'C:\\Users\\Antoine\\CloudStation\\EPFL\\Master 4\\Master project\\prototype\\assets\\user_data\\'
            data_file = open(path_json + data.id_user + '.json', 'w')
            data_file.write(data_json)
            data_file.close()


@app.callback(
    None,
    [Input('button-back-find', 'n_clicks')])
def go_back_find(n_clicks):
    if n_clicks:
        app.push_mods({'tabs-user': {'value': 'tab-finder'}})


@app.callback(
    None,
    [Input('button-next', 'n_clicks')])
def go_next_form(n_clicks):
    if n_clicks:
        app.push_mods({'tabs-user': {'value': 'tab-form'}})


@app.callback(
    None,
    [Input('button-clear-command', 'n_clicks')])
def update_output(n_clicks):
    if n_clicks:
        app.push_mods({'textarea-command': {'value': ''}})


@app.callback(
    None,
    [Input('button-back', 'n_clicks')])
def update_output(n_clicks):
    if n_clicks:
        app.push_mods({'tabs-user': {'value': 'tab-editor'}})
