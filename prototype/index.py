import dash_core_components as dcc
import dash_html_components as html
from dash_devices.dependencies import Input, Output, State

from app import app
from apps import user_mode, god_mode

app.layout = html.Div([
    dcc.Location(id='url'),
    html.Div(id='page-content')
])

start_layout = html.Div([
    html.Div([
        html.H1('UI design prototype'),
        html.Hr(),
        html.P('Please enter your ID code:'),
    ], style={'textAlign': 'center', 'margin': 'auto'}),
    html.Div([
        dcc.Input(id='input-id', type='text'),
    ], style={'textAlign': 'center', 'margin': 'auto'}),
    html.Div([
        dcc.Link(
            html.Button('Start', id='button-start', n_clicks=0, style={'margin': '15px'}),
            href='/generator')
    ], style={'textAlign': 'center', 'margin': 'auto'}),
])


@app.callback(None,
              [Input('button-start', 'n_clicks')],
              [State('input-id', 'value')])
def start(n_clicks, id_user):
    if n_clicks:
        user_mode.data.id_user = id_user


# Update the page content
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return start_layout
    elif pathname == '/generator':
        return user_mode.layout
    elif pathname == '/god-mode':
        return god_mode.layout

    else:
        return html.H1('404 Error: URL not found')


if __name__ == '__main__':
    app.run_server(debug=True)
