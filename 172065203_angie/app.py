import dash
import dash_core_components as dcc
import dash_html_components as html
import wc
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Plot
wordList = wc.popularWords
c1_keys = [wordList[i][0] for i in range(5)] # Assumes that there are at least five words.
c1_values = [wordList[i][1] for i in range(5)]

maxCount = int(wordList[0][1])

# Creation of the chart
c1 = go.Figure([go.Bar(
    x = c1_keys,
    y = c1_values,
    )
])

# Prettifying the bar chart
c1.update_layout(
    title = f'Top words in {wc.title} at ({wc.dt_string} Eastern Standard Time)',
    title_x = 0.5, # Centralizing the title
    yaxis = dict(
        range = [0, maxCount],
        dtick = maxCount/9,
        autorange = False
        ),
    )

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1('Word Counts'),
        html.Div('''
            A graphical, visual illustration of used words in Misc threads with stop words removed.
        '''),
        html.Div([
            html.A(html.H3(wc.webpage), wc.webpage),
            dcc.Graph(id='Chart 1', figure = c1)
        ], className='nine columns'),
    ], className='column')
])

if __name__ == '__main__':
    app.run_server(debug=True)
