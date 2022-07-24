import dash
import dash_ace
import dash_html_components as html
from dash.dependencies import Input, Output
import flask
from flask import request, jsonify
from flask_cors import CORS

server = flask.Flask(__name__)
CORS(server)

app = dash.Dash(__name__,
                server=server,
                routes_pathname_prefix='/dash/'
                )

ace_editor = dash_ace.DashAceEditor(
        id='demo-editor',
        value="""
# This is a TOML document

title = "TOML Example"

[owner]
name = "Tom Preston-Werner"
dob = 1979-05-27T07:32:00-08:00

[database]
enabled = true
ports = [ 8000, 8001, 8002 ]
data = [ ["delta", "phi"], [3.14] ]
temp_targets = { cpu = 79.5, case = 72.0 }

[servers]

[servers.alpha]
ip = "10.0.0.1"
role = "frontend"

[servers.beta]
ip = "10.0.0.2"
role = "backend"        
            """,
        theme='github',
        mode='toml',
        tabSize=2,
        enableBasicAutocompletion=True,
        enableLiveAutocompletion=True,
        autocompleter='/autocompleter?prefix=',
        prefixLine=True,
        triggerWords=[':', '\\.', '::'],
        placeholder='Norm code ...',
    )

app.layout = html.Div([
    ace_editor,
    html.Div(id='output')
])


@app.callback(
    Output('output', 'children'),
    Input('demo-editor', 'value')
)
def update_output_editor(value):
    return value


@server.route('/autocompleter', methods=['GET'])
def autocompleter():
    server.logger.info('receiving auto completing request with prefix: ' + request.args.get('prefix'))
    return jsonify([{"name": "Completed", "value": "Completed", "score": 300, "meta": "test"}])


if __name__ == '__main__':
    app.run_server(debug=True)
