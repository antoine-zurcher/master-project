import dash_devices

app = dash_devices.Dash(__name__, suppress_callback_exceptions=True)
server = app.server
app.title = 'UI generator'

