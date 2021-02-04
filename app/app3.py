import dash
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output

from functions import get_response, get_df, plot_df_py, csv_to_dict

# Import the tickers data
ticker_list, dict_tickers = csv_to_dict()


# Init. the app
app = dash.Dash(__name__)

# Define the app
app.layout = html.Div(
    children=[
        html.Div(className='row',
                 children=[
                     html.Div(className='three columns div-user-controls bg-grey',
                              children=[
                                  html.H2('PRECIO DE ACCIÓN'),
                                  html.P('Escriba y seleccione en la lista la compañia cuya acción quiera visualizar.'),
                                  html.Div(
                                      className='div-for-input',
                                      children=[
                                          dcc.Dropdown(
                                            options=ticker_list,
                                            value='AMZN',
                                            multi=False,
                                            id='symbol'
                                          )
                                      ]
                                  )
                              ]),
                     html.Div(className='nine columns div-for-charts bg-soft-grey',
                              children=[
                                  dcc.Graph(id='stock-ts', config={'displayModeBar': False}, animate=False)
                              ])
                            ])
                ])


# Callback time series
@app.callback(Output('stock-ts', 'figure'),
              [Input('symbol', 'value')])
def update_graph(symbol, dict_tickers=dict_tickers):
    url = 'https://www.alphavantage.co/query'
    function = 'TIME_SERIES_DAILY'
    outputsize = 'full'
    response = get_response(url, function, outputsize, symbol)
    df_response = get_df(response)
    if dict_tickers[symbol]:
        fig = plot_df_py(df_response, dict_tickers[symbol])
    else:
        fig = plot_df_py(df_response, symbol)
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
