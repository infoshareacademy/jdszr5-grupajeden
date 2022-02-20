import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import base64
import io
import pandas as pd
from datetime import datetime
import dash_table

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_excel(r'.\input_1.xlsx')
df1 = pd.read_excel(r'.\input_2.xlsx')
df2 = pd.read_excel(r'.\input_3.xlsx')

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# main page
index_page = html.Div([
    html.H2('MENU:', style={'font-family': 'Times New Roman, Times, serif',
                                                              'font-weight': 'bold',
                                                              'font-size':'40px'}),
    dcc.Link('Wczytaj dane', href='/data_upload',style={'font-family': 'Times New Roman, Times, serif',
                                                              'font-weight': 'bold',
                                                              'font-size':'40px'}),
    html.Br(),
    dcc.Link('Wykresy zużycia energii',href='/energy', style={'font-family': 'Times New Roman, Times, serif',
                                                              'font-weight': 'bold',
                                                              'font-size':'40px'}),
    html.Br(),
    dcc.Link('Tabela z danymi', href='/tab_data', style={'font-family': 'Times New Roman, Times, serif',
                                                              'font-weight': 'bold',
                                                              'font-size':'40px'})

])

# upload page
upload_page = html.Div([
    html.H4('Wczytaj dane CSV lub XLSX'),
    dcc.Link('Wykresy zużycia energii',href='/energy'),
    html.Br(),
    dcc.Link('Tabela z danymi', href='/tab_data'),
    html.Br(),
    dcc.Link('Wróć do MENU', href='/'),
    dcc.Upload(
        id='upload-1',
        children=html.Div([
            'Drag and drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'textAlign': 'center',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'lineHeight': '60px'
        },
        multiple=True
    ),
    html.Div(id='upload-1-div'),
    html.Br()
])

# energy page
energy_page = html.Div([
    html.Div([
    html.H4('Wykres przedstawiający zużycie energii na podstawie wczytanych danych'),
    dcc.Link('Wczytaj dane', href='/data_upload'),
    html.Br(),
    dcc.Link('Tabela z danymi', href='/tab_data'),
    html.Br(),
    dcc.Link('Wróć do MENU', href='/'),
    dcc.Graph(id='graph-1'),
    dcc.Slider(
        id='bar-1',
        min=df.Year.min(),
        max=df.Year.max(),
        value=df.Year.min(),
        marks={str(Year): str(Year) for Year in df.Year.unique()},
        step=None
    )]),
    html.Br(),
    html.Div([
        dcc.Graph(id='graph-3', style={
                                       'width': '50%',
                                       'height': '100%',
                                       'margin-left': '+1050px'
        }),
    ]),
    html.Div([
        dcc.Graph(id='graph-2', style={
                                       'width': '50%',
                                       'height': '100%',
                                       "margin-top": "-450px"
        }),
    ])
])

# tab data page
tab_data_page = html.Div([
    html.H4('Tabela do przeglądu danych'),
    dcc.Link('Wczytaj dane', href='/data_upload'),
    html.Br(),
    dcc.Link('Wykresy zużycia energii', href='/energy'),
    html.Br(),
    dcc.Link('Wróć do MENU', href='/'),
    dash_table.DataTable(
        id='table-1',
        columns=[{'name': col, 'id': col, 'deletable': True, 'selectable': True} for col in df.columns],
        data=df.to_dict('records'),
        export_format='xlsx',
        export_headers='display',
        editable=True,
        filter_action='native',
        sort_action='native',
        page_action='native',
        page_current=0,
        page_size=200,
        column_selectable='multi',
        row_selectable='multi',
        row_deletable=True,
        selected_columns=[],
        selected_rows=[]
    )
])

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/data_upload':
        return upload_page
    elif pathname == '/energy':
        return energy_page
    elif pathname == '/tab_data':
        return tab_data_page
    else:
        return index_page

def parse_contents(content, name, date):
    content_type, content_string = content.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in name:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in name:
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'Wystąpił błąd podczas przetwarzania pliku.'
        ])

    return html.Div([
        html.H5(name),
        html.H6(datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': col, 'id': col} for col in df.columns]
        ),
        html.Hr(),
        html.Div('Raw Content'),
        html.Pre(content[:300] + '...')
    ])

@app.callback(
    Output('upload-1-div', 'children'),
    [Input('upload-1', 'contents')],
    [State('upload-1', 'filename'),
     State('upload-1', 'last_modified')]
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    print(list_of_contents)
    print(list_of_names)
    print(list_of_dates)
    if list_of_contents is not None:
        children = [
            parse_contents(content, name, date) for content, name, date in zip(list_of_contents,
                                                                               list_of_names,
                                                                               list_of_dates)
        ]
        return children

@app.callback(
    Output('graph-1', 'figure'),
    [Input('bar-1', 'value')]
)
def update_graph(selected_Year):
    dff = df.query(f'Year == {selected_Year}')
    traces = []
    for room in df.Room.unique():
        dff_room = dff[dff.Room == room]
        traces.append(
            go.Scatter(
                x=dff_room.Date_time,
                y=dff_room.Sum_of_energy,
                name=room,
                opacity=0.6,
                marker={
                    'size': 15,
                    'line': {'width': 1.5, 'color': 'white'}
                }
            )
        )
    return {
        'data': traces,
        'layout': go.Layout(
            # title_text='Wykres'
        )
    }

@app.callback(
    Output('graph-2', 'figure'),
    [Input('bar-1', 'value')]
)
def update_graph(selected_Year):
    dff1 = df1.query(f'Year == {selected_Year}')
    traces = []
    for room in df1.Room.unique():
        dff1_room = dff1[dff1.Room == room]
        traces.append(
            go.Bar(
                x=dff1_room.Month,
                y=dff1_room.Sum_of_energy,
                name=room,
                opacity=0.6
            )
        )
    return {
        'data': traces,
        'layout': go.Layout(
            # title_text='Wykres'
        )
    }

@app.callback(
    Output('graph-3', 'figure'),
    [Input('bar-1', 'value')]
)
def update_graph(selected_Year):
    dff2 = df2.query(f'Year == {selected_Year}')
    traces = []
    for room in df2.Room.unique():
        dff2_room = dff2[dff2.Room == room]
        traces.append(
            go.Bar(
                x=dff2_room.Season,
                y=dff2_room.Sum_of_energy,
                name=room,
                opacity=0.6
            )
        )
    return {
        'data': traces,
        'layout': go.Layout(
            # title_text='Wykres'
        )
    }

@app.callback(
    Output('table-1', 'style_data_conditional'),
    [Input('table-1', 'selected_columns')]
)
def update_style(selected_columns):
    print(selected_columns)
    return [{
        'if': {'column_id': col},
        'background_color': 'lightgrey'
    } for col in selected_columns]

if __name__ == '__main__':
    app.run_server(debug=True)