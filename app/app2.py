import dash
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output

from functions import get_response, get_df, plot_df_py

# Init. the app
app = dash.Dash(__name__)

# Define the app
app.layout = html.Div(
    children=[
        html.Div(className='row',
                 children=[
                     html.Div(className='three columns div-user-controls',
                              children=[
                                  html.H2('DASH - STOCK PRICES'),
                                  html.P('Visualizing stock time-series prices.'),
                                  html.P('Write the stock you want to visualize.'),
                                  html.Div(
                                      className='div-for-input',
                                      children=[
                                          dcc.Input(id='symbol', type='text', placeholder='Ticker symbol', value='BA', debounce=True)
                                      ]
                                  )
                              ]),
                     html.Div(className='nine columns div-for-charts bg-grey',
                              children=[
                                  dcc.Graph(id='stock-ts', config={'displayModeBar': False}, animate=False)
                              ])
                            ])
                ])

# Callback time series
@app.callback(Output('stock-ts', 'figure'),
              [Input('symbol', 'value')])
def update_graph(symbol):
    url = 'https://www.alphavantage.co/query'
    function = 'TIME_SERIES_DAILY'
    outputsize = 'full'
    response = get_response(url, function, outputsize, symbol)
    df_response = get_df(response)
    fig = plot_df_py(df_response, symbol)
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
