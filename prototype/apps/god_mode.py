import dash_core_components as dcc
import dash_html_components as html
from dash_devices.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import sys
import re
import num2words

from app import app
from apps import user_mode

sys.path.insert(1, 'C:\\Users\\Antoine\\CloudStation\\EPFL\\Master 4\\Master project\\masterProject')
from UIDatasheet import UIDatasheet
import ui_finder

ui_path = 'C:\\Users\\Antoine\\CloudStation\\EPFL\\Master 4\\Master project\\Dataset\\VINS Dataset\\ui_list.json'
ui_df = pd.read_json(ui_path)

current_page = 0
max_page = 0
filtered_ui = []
image_selected = ''
images = ['', '', '', '', '', '', '', '']

description_layout = html.Div([
    html.Div([
        html.H3('Descriptions'),
        html.P(id='content-description', className='ow'),
        html.Button('Copy description', id='button-copy-description', n_clicks=0),
    ], style={'margin': '15px'}),
    html.Div([
        html.H3('AI search'),
    ], style={'margin': '15px'}),
    html.Div([
        html.Div([
            dcc.Textarea(id='content-text-value', value='', cols=70, placeholder='Text value'),
        ], style={'flex-grow': '1'}),
        html.Div([
            dcc.Input(id='input-topk', type='number', value=16, min=1, placeholder='Top-k value'),
        ], style={'flex-grow': '1'}),
        html.Div([
            html.Button('Run', id='button-run-ai', n_clicks=0),
        ], style={'flex-grow': '1'}),
    ], style={'margin': '15px', 'display': 'flex'}),
    html.Div([
        html.P(id='content-info-retrieved'),
    ], style={'margin': '15px'}),
    html.Div([
        html.Div([
            html.H3('Label'),
            dcc.Dropdown(
                id='dropdown-label',
                options=[
                    {'label': 'Bare', 'value': 'bare'},
                    {'label': 'Shop', 'value': 'shop'},
                    {'label': 'Form', 'value': 'form'},
                    {'label': 'Gallery', 'value': 'gallery'},
                    {'label': 'List', 'value': 'list'},
                    {'label': 'Login', 'value': 'login'},
                    {'label': 'Map', 'value': 'map'},
                    {'label': 'Menu', 'value': 'menu'},
                    {'label': 'Modal', 'value': 'modal'},
                    {'label': 'News', 'value': 'news'},
                    {'label': 'Profile', 'value': 'profile'},
                    {'label': 'Search', 'value': 'search'},
                    {'label': 'Settings', 'value': 'settings'},
                    {'label': 'Terms', 'value': 'terms'},
                    {'label': 'Tutorial', 'value': 'tutorial'},
                    {'label': 'Other', 'value': 'other'},
                ],
            ),
        ], style={'flex-grow': '1', 'margin': '15px'}),
        html.Div([
            html.H3('Number of buttons'),
            dcc.Input(id='input-buttons', type='number', min=0),
        ], style={'flex-grow': '1', 'margin': '15px'}),
        html.Div([
            html.H3('Number of input fields'),
            dcc.Input(id='input-input-fields', type='number', min=0),
        ], style={'flex-grow': '1', 'margin': '15px'}),
        html.Div([
            html.H3('Page indicator'),
            dcc.Dropdown(
                id='dropdown-page-indicator',
                options=[
                    {'label': 'Yes', 'value': 'yes'},
                    {'label': 'No', 'value': 'no'},
                ],
            ),
        ], style={'flex-grow': '1', 'margin': '15px'}),
        html.Div([
            html.H3('Map'),
            dcc.Dropdown(
                id='dropdown-map',
                options=[
                    {'label': 'Yes', 'value': 'yes'},
                    {'label': 'No', 'value': 'no'},
                ],
            ),
        ], style={'flex-grow': '1', 'margin': '15px'}),
        html.Div([
            html.H3('Text filter'),
            dcc.Textarea(id='content-text-filter', value='', rows=7),
        ], style={'flex-grow': '2', 'margin': '15px'}),
    ], style={'display': 'flex'}),
    html.Div([
        html.Button('Clear filters', id='button-clear-filters', n_clicks=0, style={'margin': '15px'}),
        html.Button('Search', id='button-search', n_clicks=0, style={'margin': '15px'}),
    ], style={'margin-bottom': '10px',
              'textAlign': 'center',
              'margin': 'auto'}),
    html.Div([
        html.Progress(id='progress-search', value='0', max=100, style={'width': '30%'}),
        html.P(id='content-search'),
    ], style={'margin-bottom': '10px',
              'textAlign': 'center',
              'margin': 'auto'}),
    html.Div([
        html.Div([
            html.Div([
                html.H3('Image selections'),
                html.Div([
                    html.Img(src=app.get_asset_url('background.png'), id='img_select0', style={'width': '20%'}),
                    html.Button('Select 1st image', id='button-select0', n_clicks=0, style={'height': '10%'}),
                    html.P('None', id='content-select0'),
                    html.Button('Clear', id='button-clear0', n_clicks=0, style={'height': '10%'}),
                ], style={'display': 'flex', 'margin': '15px'}),
                html.Div([
                    html.Img(src=app.get_asset_url('background.png'), id='img_select1', style={'width': '20%'}),
                    html.Button('Select 2nd image', id='button-select1', n_clicks=0, style={'height': '10%'}),
                    html.P('None', id='content-select1'),
                    html.Button('Clear', id='button-clear1', n_clicks=0, style={'height': '10%'}),
                ], style={'display': 'flex', 'margin': '15px'}),
                html.Div([
                    html.Img(src=app.get_asset_url('background.png'), id='img_select2', style={'width': '20%'}),
                    html.Button('Select 3rd image', id='button-select2', n_clicks=0, style={'height': '10%'}),
                    html.P('None', id='content-select2'),
                    html.Button('Clear', id='button-clear2', n_clicks=0, style={'height': '10%'}),
                ], style={'display': 'flex', 'margin': '15px'}),
                html.Div([
                    html.Img(src=app.get_asset_url('background.png'), id='img_select3', style={'width': '20%'}),
                    html.Button('Select 4th image', id='button-select3', n_clicks=0, style={'height': '10%'}),
                    html.P('None', id='content-select3'),
                    html.Button('Clear', id='button-clear3', n_clicks=0, style={'height': '10%'}),
                ], style={'display': 'flex', 'margin': '15px'}),
                # html.Div([
                #     html.Button('Select 5th image', id='button-select4', n_clicks=0),
                #     html.P('None', id='content-select4')
                # ], style={'display': 'flex', 'margin': '15px'}),
                # html.Div([
                #     html.Button('Select 6th image', id='button-select5', n_clicks=0),
                #     html.P('None', id='content-select5')
                # ], style={'display': 'flex', 'margin': '15px'}),
                # html.Div([
                #     html.Button('Select 7th image', id='button-select6', n_clicks=0),
                #     html.P('None', id='content-select6')
                # ], style={'display': 'flex', 'margin': '15px'}),
                # html.Div([
                #     html.Button('Select 8th image', id='button-select7', n_clicks=0),
                #     html.P('None', id='content-select7')
                # ], style={'display': 'flex', 'margin': '15px'}),
                html.Button('Send images', id='button-send-images', n_clicks=0),
            ], style={'margin': '15px'})
        ], style={'float': 'left', 'width': '20%'}),
        html.Div([
            html.Div(
                [
                    html.Div([
                        html.Img(src=app.get_asset_url('background.png'), id='img_god0', className='imageUI',
                                 n_clicks_timestamp=-1),
                    ], style={'flex-grow': '1', 'margin': '15px'}),
                    html.Div([
                        html.Img(src=app.get_asset_url('background.png'), id='img_god1', className='imageUI',
                                 n_clicks_timestamp=-1),
                    ], style={'flex-grow': '1', 'margin': '15px'}),
                    html.Div([
                        html.Img(src=app.get_asset_url('background.png'), id='img_god2', className='imageUI',
                                 n_clicks_timestamp=-1),
                    ], style={'flex-grow': '1', 'margin': '15px'}),
                    html.Div([
                        html.Img(src=app.get_asset_url('background.png'), id='img_god3', className='imageUI',
                                 n_clicks_timestamp=-1),
                    ], style={'flex-grow': '1', 'margin': '15px'}),
                ], style={'display': 'flex'}
            ),
            html.Div(
                [
                    html.Div([
                        html.Img(src=app.get_asset_url('background.png'), id='img_god4', className='imageUI',
                                 n_clicks_timestamp=-1),
                    ], style={'flex-grow': '1', 'margin': '15px'}),
                    html.Div([
                        html.Img(src=app.get_asset_url('background.png'), id='img_god5', className='imageUI',
                                 n_clicks_timestamp=-1),
                    ], style={'flex-grow': '1', 'margin': '15px'}),
                    html.Div([
                        html.Img(src=app.get_asset_url('background.png'), id='img_god6', className='imageUI',
                                 n_clicks_timestamp=-1),
                    ], style={'flex-grow': '1', 'margin': '15px'}),
                    html.Div([
                        html.Img(src=app.get_asset_url('background.png'), id='img_god7', className='imageUI',
                                 n_clicks_timestamp=-1),
                    ], style={'flex-grow': '1', 'margin': '15px'}),
                ], style={'display': 'flex'}
            ),
            html.Div(
                [
                    html.Div([
                        html.Button('Previous page', id='button-previous', n_clicks=0),
                    ], style={'flex-grow': '1', 'textAlign': 'right', 'margin': '15px'}),
                    html.Div([
                        html.Button('Next page', id='button-next-page', n_clicks=0),
                    ], style={'flex-grow': '1', 'textAlign': 'left', 'margin': '15px'}),
                ], style={'display': 'flex'}
            ),
            html.Div(
                [
                    html.P('Page ... out of ...', id='content-page-number'),
                ], style={'textAlign': 'center', 'margin': 'auto'}
            ),
        ], style={'float': 'right', 'width': '80%'}),
    ]),
])

commands_layout = html.Div([
    html.Div([
        html.H3('Selected Images'),
        html.P(id='content-image', className='ow'),
    ], style={'margin': '15px'}),
    html.Div([
        html.H3('Commands'),
        html.P(id='content-command', className='ow'),
    ], style={'margin': '15px'}),
    html.Div(
        [
            html.Button('Send error message', id='button-send-error', n_clicks=0, style={'margin': '15px'}),
            html.Button('Clear error message', id='button-clear-error', n_clicks=0, style={'margin': '15px'}),
        ],
        style={'margin-bottom': '10px',
               'textAlign': 'center',
               'width': '220px',
               'margin': 'auto'}
    ),
])

layout = html.Div([
    dcc.Tabs(id='tabs-god-mode', value='tab-description', children=[
        dcc.Tab(label='User\'s descriptions', value='tab-description', children=description_layout),
        dcc.Tab(label='User\'s commands', value='tab-commands', children=commands_layout),
    ])
])


@app.callback(None,
              [Input('button-send-error', 'n_clicks')])
def send_error(n_clicks):
    if n_clicks:
        app.push_mods({'content-error': {'children': 'Error: the requested command is too complex for the system, please modify your request'}})


@app.callback(None,
              [Input('button-clear-error', 'n_clicks')])
def send_error(n_clicks):
    if n_clicks:
        app.push_mods({'content-error': {'children': ''}})


@app.callback(None,
              [Input('button-select0', 'n_clicks')])
def select_image(n_clicks):
    if n_clicks:
        global image_selected
        if image_selected:
            images[0] = image_selected
            app.push_mods({'content-select0': {'children': image_selected}})
            app.push_mods({'img_select0': {'src': app.get_asset_url('wireframes/' + images[0])}})


@app.callback(None,
              [Input('button-select1', 'n_clicks')])
def select_image(n_clicks):
    if n_clicks:
        global image_selected
        if image_selected:
            images[1] = image_selected
            app.push_mods({'content-select1': {'children': image_selected}})
            app.push_mods({'img_select1': {'src': app.get_asset_url('wireframes/' + images[1])}})


@app.callback(None,
              [Input('button-select2', 'n_clicks')])
def select_image(n_clicks):
    if n_clicks:
        global image_selected
        if image_selected:
            images[2] = image_selected
            app.push_mods({'content-select2': {'children': image_selected}})
            app.push_mods({'img_select2': {'src': app.get_asset_url('wireframes/' + images[2])}})


@app.callback(None,
              [Input('button-select3', 'n_clicks')])
def select_image(n_clicks):
    if n_clicks:
        global image_selected
        if image_selected:
            images[3] = image_selected
            app.push_mods({'content-select3': {'children': image_selected}})
            app.push_mods({'img_select3': {'src': app.get_asset_url('wireframes/' + images[3])}})


@app.callback(None,
              [Input('button-clear0', 'n_clicks')])
def select_image(n_clicks):
    if n_clicks:
        global images
        images[0] = ''
        app.push_mods({'content-select0': {'children': 'None'}})
        app.push_mods({'img_select0': {'src': app.get_asset_url('background.png')}})


@app.callback(None,
              [Input('button-clear1', 'n_clicks')])
def select_image(n_clicks):
    if n_clicks:
        global images
        images[1] = ''
        app.push_mods({'content-select1': {'children': 'None'}})
        app.push_mods({'img_select1': {'src': app.get_asset_url('background.png')}})


@app.callback(None,
              [Input('button-clear2', 'n_clicks')])
def select_image(n_clicks):
    if n_clicks:
        global images
        images[2] = ''
        app.push_mods({'content-select2': {'children': 'None'}})
        app.push_mods({'img_select2': {'src': app.get_asset_url('background.png')}})


@app.callback(None,
              [Input('button-clear3', 'n_clicks')])
def select_image(n_clicks):
    if n_clicks:
        global images
        images[3] = ''
        app.push_mods({'content-select3': {'children': 'None'}})
        app.push_mods({'img_select3': {'src': app.get_asset_url('background.png')}})


@app.callback(None,
              [Input('button-copy-description', 'n_clicks')])
def copy_description(n_clicks):
    if n_clicks:
        if user_mode.data.descriptions:
            description = user_mode.data.descriptions[-1]
            app.push_mods({'content-text-value': {'value': description}})


@app.callback(None,
              [Input('img_god0', 'n_clicks_timestamp'),
               Input('img_god1', 'n_clicks_timestamp'),
               Input('img_god2', 'n_clicks_timestamp'),
               Input('img_god3', 'n_clicks_timestamp'),
               Input('img_god4', 'n_clicks_timestamp'),
               Input('img_god5', 'n_clicks_timestamp'),
               Input('img_god6', 'n_clicks_timestamp'),
               Input('img_god7', 'n_clicks_timestamp')])
def select_image(n_clicks_timestamp0, n_clicks_timestamp1, n_clicks_timestamp2, n_clicks_timestamp3,
                 n_clicks_timestamp4, n_clicks_timestamp5, n_clicks_timestamp6, n_clicks_timestamp7):
    if filtered_ui:
        global current_page
        global image_selected
        list_timestamps = [n_clicks_timestamp0, n_clicks_timestamp1, n_clicks_timestamp2, n_clicks_timestamp3,
                           n_clicks_timestamp4, n_clicks_timestamp5, n_clicks_timestamp6, n_clicks_timestamp7]
        max_idx = np.argmax(list_timestamps)
        if sum(list_timestamps) != -1 * len(list_timestamps):
            if max_idx + current_page * 8 < len(filtered_ui):
                image_selected = filtered_ui[max_idx + current_page * 8]
                app.push_mods({'img_god0': {'className': 'imageUI'}})
                app.push_mods({'img_god1': {'className': 'imageUI'}})
                app.push_mods({'img_god2': {'className': 'imageUI'}})
                app.push_mods({'img_god3': {'className': 'imageUI'}})
                app.push_mods({'img_god4': {'className': 'imageUI'}})
                app.push_mods({'img_god5': {'className': 'imageUI'}})
                app.push_mods({'img_god6': {'className': 'imageUI'}})
                app.push_mods({'img_god7': {'className': 'imageUI'}})

                app.push_mods({'img_god{}'.format(max_idx): {'className': 'imageUIselected'}})


@app.callback(None,
              [Input('button-send-images', 'n_clicks')])
def send_images(n_clicks):
    if n_clicks:
        if images[0]:
            app.push_mods({'img0': {'hidden': False}})
            app.push_mods({'img0': {'src': app.get_asset_url('wireframes/' + images[0])}})
        else:
            app.push_mods({'img0': {'hidden': True}})
        if images[1]:
            app.push_mods({'img1': {'hidden': False}})
            app.push_mods({'img1': {'src': app.get_asset_url('wireframes/' + images[1])}})
        else:
            app.push_mods({'img1': {'hidden': True}})
        if images[2]:
            app.push_mods({'img2': {'hidden': False}})
            app.push_mods({'img2': {'src': app.get_asset_url('wireframes/' + images[2])}})
        else:
            app.push_mods({'img2': {'hidden': True}})
        if images[3]:
            app.push_mods({'img3': {'hidden': False}})
            app.push_mods({'img3': {'src': app.get_asset_url('wireframes/' + images[3])}})
        else:
            app.push_mods({'img3': {'hidden': True}})
        # app.push_mods({'img4': {'src': app.get_asset_url('wireframes/' + images[4])}})
        # app.push_mods({'img5': {'src': app.get_asset_url('wireframes/' + images[5])}})
        # app.push_mods({'img6': {'src': app.get_asset_url('wireframes/' + images[6])}})
        # app.push_mods({'img7': {'src': app.get_asset_url('wireframes/' + images[7])}})
        user_mode.data.images_selected = images
        user_mode.data.image_sent = True


#
# @app.callback(None,
#               [Input('tabs-god-mode', 'value'), ])
# def render_content(tab):
#     if tab == 'tab-description':
#         app.push_mods({'tabs-layout': {'children': [description_layout]}})
#         description_content = ''
#         if user_mode.data.descriptions:
#             nb_desc = len(user_mode.data.descriptions)
#             for i in range(nb_desc):
#                 description_content += '{}: {} <br>'.format(i + 1, user_mode.data.descriptions[i])
#         app.push_mods({'content-description': {'children': DangerouslySetInnerHTML(description_content)}})
#     elif tab == 'tab-commands':
#         app.push_mods({'tabs-layout': {'children': [commands_layout]}})
#         image_content = ''
#         if user_mode.data.images:
#             nb_desc = len(user_mode.data.images)
#             for i in range(nb_desc):
#                 image_content += '{}: {} <br>'.format(i + 1, user_mode.data.images[i].replace('.jpg', ''))
#         app.push_mods({'content-image': {'children': DangerouslySetInnerHTML(image_content)}})
#
#         command_content = ''
#         if user_mode.data.commands:
#             nb_desc = len(user_mode.data.commands)
#             for i in range(nb_desc):
#                 command_content += '{}: {} <br>'. format(i+1, user_mode.data.commands[i])
#         app.push_mods({'content-command': {'children': DangerouslySetInnerHTML(command_content)}})


@app.callback(None,
              [Input('button-previous', 'n_clicks')])
def control_previous(n_clicks_previous):
    global current_page
    global max_page
    global filtered_ui
    if max_page:
        if n_clicks_previous:
            if current_page > 0:
                current_page -= 1
                app.push_mods(
                    {'img_god0': {'src': app.get_asset_url('wireframes/' + filtered_ui[0 + current_page * 8])}})
                app.push_mods(
                    {'img_god1': {'src': app.get_asset_url('wireframes/' + filtered_ui[1 + current_page * 8])}})
                app.push_mods(
                    {'img_god2': {'src': app.get_asset_url('wireframes/' + filtered_ui[2 + current_page * 8])}})
                app.push_mods(
                    {'img_god3': {'src': app.get_asset_url('wireframes/' + filtered_ui[3 + current_page * 8])}})
                app.push_mods(
                    {'img_god4': {'src': app.get_asset_url('wireframes/' + filtered_ui[4 + current_page * 8])}})
                app.push_mods(
                    {'img_god5': {'src': app.get_asset_url('wireframes/' + filtered_ui[5 + current_page * 8])}})
                app.push_mods(
                    {'img_god6': {'src': app.get_asset_url('wireframes/' + filtered_ui[6 + current_page * 8])}})
                app.push_mods(
                    {'img_god7': {'src': app.get_asset_url('wireframes/' + filtered_ui[7 + current_page * 8])}})
                app.push_mods(
                    {'content-page-number': {'children': 'Page {} out of {}'.format(current_page + 1, max_page)}})


@app.callback(None,
              [Input('button-clear-filters', 'n_clicks')])
def clear_filters(n_clicks):
    if n_clicks:
        app.push_mods({'dropdown-label': {'value': ''}})
        app.push_mods({'input-buttons': {'value': ''}})
        app.push_mods({'input-input-fields': {'value': ''}})
        app.push_mods({'dropdown-page-indicator': {'value': ''}})
        app.push_mods({'dropdown-map': {'value': ''}})
        app.push_mods({'content-text-filter': {'value': ''}})
        global max_page
        max_page = 0
        global filtered_ui
        filtered_ui = []


@app.callback(None,
              [Input('button-next-page', 'n_clicks')])
def control_next(n_clicks_next):
    global current_page
    global max_page
    global filtered_ui
    if max_page:
        if n_clicks_next:
            if current_page < max_page - 1:
                current_page += 1
                app.push_mods({'img_god0': {'src': app.get_asset_url('background.png')}})
                app.push_mods({'img_god1': {'src': app.get_asset_url('background.png')}})
                app.push_mods({'img_god2': {'src': app.get_asset_url('background.png')}})
                app.push_mods({'img_god3': {'src': app.get_asset_url('background.png')}})
                app.push_mods({'img_god4': {'src': app.get_asset_url('background.png')}})
                app.push_mods({'img_god5': {'src': app.get_asset_url('background.png')}})
                app.push_mods({'img_god6': {'src': app.get_asset_url('background.png')}})
                app.push_mods({'img_god7': {'src': app.get_asset_url('background.png')}})
                if len(filtered_ui) > 0 + current_page * 8:
                    app.push_mods(
                        {'img_god0': {'src': app.get_asset_url('wireframes/' + filtered_ui[0 + current_page * 8])}})
                if len(filtered_ui) > 1 + current_page * 8:
                    app.push_mods(
                        {'img_god1': {'src': app.get_asset_url('wireframes/' + filtered_ui[1 + current_page * 8])}})
                if len(filtered_ui) > 2 + current_page * 8:
                    app.push_mods(
                        {'img_god2': {'src': app.get_asset_url('wireframes/' + filtered_ui[2 + current_page * 8])}})
                if len(filtered_ui) > 3 + current_page * 8:
                    app.push_mods(
                        {'img_god3': {'src': app.get_asset_url('wireframes/' + filtered_ui[3 + current_page * 8])}})
                if len(filtered_ui) > 4 + current_page * 8:
                    app.push_mods(
                        {'img_god4': {'src': app.get_asset_url('wireframes/' + filtered_ui[4 + current_page * 8])}})
                if len(filtered_ui) > 5 + current_page * 8:
                    app.push_mods(
                        {'img_god5': {'src': app.get_asset_url('wireframes/' + filtered_ui[5 + current_page * 8])}})
                if len(filtered_ui) > 6 + current_page * 8:
                    app.push_mods(
                        {'img_god6': {'src': app.get_asset_url('wireframes/' + filtered_ui[6 + current_page * 8])}})
                if len(filtered_ui) > 7 + current_page * 8:
                    app.push_mods(
                        {'img_god7': {'src': app.get_asset_url('wireframes/' + filtered_ui[7 + current_page * 8])}})
                app.push_mods(
                    {'content-page-number': {'children': 'Page {} out of {}'.format(current_page + 1, max_page)}})


@app.callback(None,
              [Input('button-search', 'n_clicks')],
              [State('dropdown-label', 'value'),
               State('input-buttons', 'value'),
               State('input-input-fields', 'value'),
               State('dropdown-page-indicator', 'value'),
               State('dropdown-map', 'value'),
               State('content-text-filter', 'value')])
def filter_ui(n_clicks, label, nb_buttons, nb_input, page, map_, text_filter):
    if n_clicks:
        index_list = list(range(len(ui_df)))
        global filtered_ui
        filtered_ui = []
        if label:
            drop = []
            count = 0
            app.push_mods({'content-search': {'children': 'Label filtering...'}})
            for index in index_list:
                progress = int((count / len(index_list)) * 100)
                count += 1
                if progress % 10 == 0:
                    app.push_mods({'progress-search': {'value': str(progress)}})
                if ui_df.iloc[index].label != label:
                    drop.append(index)
            index_list = list(set(index_list) - set(drop))
            app.push_mods({'progress-search': {'value': '100'}})
            app.push_mods({'content-search': {'children': ''}})

        if nb_buttons:
            drop = []
            count = 0
            app.push_mods({'content-search': {'children': 'Button filtering...'}})
            for index in index_list:
                progress = int((count / len(index_list)) * 100)
                count += 1
                if progress % 10 == 0:
                    app.push_mods({'progress-search': {'value': str(progress)}})
                components = pd.DataFrame.from_dict(ui_df.iloc[index].components)
                nb_buttons_ui = components.type.str.count('TextButton').sum()
                if nb_buttons_ui != nb_buttons:
                    drop.append(index)
            index_list = list(set(index_list) - set(drop))
            app.push_mods({'progress-search': {'value': '100'}})
            app.push_mods({'content-search': {'children': ''}})

        if nb_input:
            drop = []
            count = 0
            app.push_mods({'content-search': {'children': 'Input fields filtering...'}})
            for index in index_list:
                progress = int((count / len(index_list)) * 100)
                count += 1
                if progress % 10 == 0:
                    app.push_mods({'progress-search': {'value': str(progress)}})
                components = pd.DataFrame.from_dict(ui_df.iloc[index].components)
                nb_input_ui = components.type.str.count('EditText').sum()
                if nb_input_ui != nb_input:
                    drop.append(index)
            index_list = list(set(index_list) - set(drop))
            app.push_mods({'progress-search': {'value': '100'}})
            app.push_mods({'content-search': {'children': ''}})

        if page:
            drop = []
            count = 0
            app.push_mods({'content-search': {'children': 'Page indicator filtering...'}})
            for index in index_list:
                progress = int((count / len(index_list)) * 100)
                count += 1
                if progress % 10 == 0:
                    app.push_mods({'progress-search': {'value': str(progress)}})
                components = pd.DataFrame.from_dict(ui_df.iloc[index].components)
                nb_page_ui = components.type.str.count('PageIndicator').sum()
                if page == 'yes':
                    if nb_page_ui == 0:
                        drop.append(index)
                if page == 'no':
                    if nb_page_ui > 0:
                        drop.append(index)
            index_list = list(set(index_list) - set(drop))
            app.push_mods({'progress-search': {'value': '100'}})
            app.push_mods({'content-search': {'children': ''}})

        if map_:
            drop = []
            count = 0
            app.push_mods({'content-search': {'children': 'Map filtering...'}})
            for index in index_list:
                progress = int((count / len(index_list)) * 100)
                count += 1
                if progress % 10 == 0:
                    app.push_mods({'progress-search': {'value': str(progress)}})
                components = pd.DataFrame.from_dict(ui_df.iloc[index].components)
                nb_map_ui = components.type.str.count('Map').sum()
                if map_ == 'yes':
                    if nb_map_ui == 0:
                        drop.append(index)
                if map_ == 'no':
                    if nb_map_ui > 0:
                        drop.append(index)
            index_list = list(set(index_list) - set(drop))
            app.push_mods({'progress-search': {'value': '100'}})
            app.push_mods({'content-search': {'children': ''}})

        if text_filter:
            drop = []
            count = 0
            app.push_mods({'content-search': {'children': 'Text filtering...'}})
            text_filter_words = text_filter.lower().split()
            for index in index_list:
                progress = int((count / len(index_list)) * 100)
                count += 1
                if progress % 10 == 0:
                    app.push_mods({'progress-search': {'value': str(progress)}})
                components = pd.DataFrame.from_dict(ui_df.iloc[index].components)
                text_ui = ' '.join(components.text.tolist()).lower()
                if not all(text in text_ui for text in text_filter_words):
                    drop.append(index)
            index_list = list(set(index_list) - set(drop))
            app.push_mods({'progress-search': {'value': '100'}})
            app.push_mods({'content-search': {'children': ''}})

        for index in index_list:
            filtered_ui.append(ui_df.iloc[index, 0] + '.jpg')

        app.push_mods({'img_god0': {'src': app.get_asset_url('background.png')}})
        app.push_mods({'img_god1': {'src': app.get_asset_url('background.png')}})
        app.push_mods({'img_god2': {'src': app.get_asset_url('background.png')}})
        app.push_mods({'img_god3': {'src': app.get_asset_url('background.png')}})
        app.push_mods({'img_god4': {'src': app.get_asset_url('background.png')}})
        app.push_mods({'img_god5': {'src': app.get_asset_url('background.png')}})
        app.push_mods({'img_god6': {'src': app.get_asset_url('background.png')}})
        app.push_mods({'img_god7': {'src': app.get_asset_url('background.png')}})

        if len(filtered_ui) == 0:
            app.push_mods({'content-search': {'children': 'No results found for the given filters.'}})
        if len(filtered_ui) > 0:
            app.push_mods({'img_god0': {'src': app.get_asset_url('wireframes/' + filtered_ui[0])}})
        if len(filtered_ui) > 1:
            app.push_mods({'img_god1': {'src': app.get_asset_url('wireframes/' + filtered_ui[1])}})
        if len(filtered_ui) > 2:
            app.push_mods({'img_god2': {'src': app.get_asset_url('wireframes/' + filtered_ui[2])}})
        if len(filtered_ui) > 3:
            app.push_mods({'img_god3': {'src': app.get_asset_url('wireframes/' + filtered_ui[3])}})
        if len(filtered_ui) > 4:
            app.push_mods({'img_god4': {'src': app.get_asset_url('wireframes/' + filtered_ui[4])}})
        if len(filtered_ui) > 5:
            app.push_mods({'img_god5': {'src': app.get_asset_url('wireframes/' + filtered_ui[5])}})
        if len(filtered_ui) > 6:
            app.push_mods({'img_god6': {'src': app.get_asset_url('wireframes/' + filtered_ui[6])}})
        if len(filtered_ui) > 7:
            app.push_mods({'img_god7': {'src': app.get_asset_url('wireframes/' + filtered_ui[7])}})

        page_size = 8
        global max_page
        global current_page
        current_page = 0
        max_page = int((len(filtered_ui) + page_size - 1) / page_size)
        if max_page == 0:
            max_page = 1
        app.push_mods({'content-page-number': {'children': 'Page {} out of {}'.format(current_page + 1, max_page)}})


@app.callback(None,
              [Input('button-run-ai', 'n_clicks')],
              [State('content-text-value', 'value'),
               State('input-topk', 'value')])
def run_ai(n_clicks, description, k):
    if n_clicks and description and k:
        app.push_mods({'content-info-retrieved': {'children': 'Running...'}})
        description = re.sub(r"(\d+)", lambda x: num2words.num2words(int(x.group(0))), description)
        ui_datasheet = UIDatasheet()
        ui_datasheet.description = description
        ui_finder.get_label(ui_datasheet)
        ui_finder.get_components(ui_datasheet)
        info = ui_finder.print_info(ui_datasheet)
        app.push_mods({'content-info-retrieved': {'children': info}})

        wf_list = ui_finder.search_wf(ui_datasheet, k)

        global filtered_ui
        filtered_ui = []
        for wf in wf_list:
            filtered_ui.append(wf + '.jpg')

        app.push_mods({'img_god0': {'src': app.get_asset_url('background.png')}})
        app.push_mods({'img_god1': {'src': app.get_asset_url('background.png')}})
        app.push_mods({'img_god2': {'src': app.get_asset_url('background.png')}})
        app.push_mods({'img_god3': {'src': app.get_asset_url('background.png')}})
        app.push_mods({'img_god4': {'src': app.get_asset_url('background.png')}})
        app.push_mods({'img_god5': {'src': app.get_asset_url('background.png')}})
        app.push_mods({'img_god6': {'src': app.get_asset_url('background.png')}})
        app.push_mods({'img_god7': {'src': app.get_asset_url('background.png')}})

        if len(filtered_ui) == 0:
            app.push_mods({'content-search': {'children': 'No results found for the given filters.'}})
        if len(filtered_ui) > 0:
            app.push_mods({'img_god0': {'src': app.get_asset_url('wireframes/' + filtered_ui[0])}})
        if len(filtered_ui) > 1:
            app.push_mods({'img_god1': {'src': app.get_asset_url('wireframes/' + filtered_ui[1])}})
        if len(filtered_ui) > 2:
            app.push_mods({'img_god2': {'src': app.get_asset_url('wireframes/' + filtered_ui[2])}})
        if len(filtered_ui) > 3:
            app.push_mods({'img_god3': {'src': app.get_asset_url('wireframes/' + filtered_ui[3])}})
        if len(filtered_ui) > 4:
            app.push_mods({'img_god4': {'src': app.get_asset_url('wireframes/' + filtered_ui[4])}})
        if len(filtered_ui) > 5:
            app.push_mods({'img_god5': {'src': app.get_asset_url('wireframes/' + filtered_ui[5])}})
        if len(filtered_ui) > 6:
            app.push_mods({'img_god6': {'src': app.get_asset_url('wireframes/' + filtered_ui[6])}})
        if len(filtered_ui) > 7:
            app.push_mods({'img_god7': {'src': app.get_asset_url('wireframes/' + filtered_ui[7])}})

        page_size = 8
        global max_page
        global current_page
        current_page = 0
        max_page = int((len(filtered_ui) + page_size - 1) / page_size)
        if max_page == 0:
            max_page = 1
        app.push_mods({'content-page-number': {'children': 'Page {} out of {}'.format(current_page + 1, max_page)}})
