import dash
import dash_html_components as html
import dash_core_components as dcc
from datetime import date, timedelta

from dash.dependencies import Input, Output

from functions import get_response, get_df, plot_df_py, plot_candlestick, csv_to_dict, date_filter_df

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
                                  html.P('Escriba el símbolo ticker de la acción que quiere visualizar:'),
                                  html.Div(
                                      dcc.Input(
                                            id='symbol',
                                            type='text',
                                            placeholder='Ticker symbol',
                                            value='AMZN',
                                            debounce=True)
                                       ),
                                  html.Br(),
                                  html.Br(),
                                  html.P('Escoge el tipo de gráfico:'),
                                  html.Div(
                                      dcc.RadioItems(
                                          id='type',
                                          value='ts',
                                          options=[
                                                {'label': 'Time series', 'value': 'ts'},
                                                {'label': 'Candlestick', 'value': 'cs'}
                                            ]
                                       ),
                                      style={'color': 'white',
                                             'fontSize': 18}
                                  ),
                                  html.Br(),
                                  html.Br(),
                                  html.P('Escoge el intervalo de fechas:'),
                                  html.Div(
                                      dcc.DatePickerRange(
                                          id='date-range',
                                          day_size=45,
                                          number_of_months_shown=2,
                                          updatemode='bothdates',
                                          clearable=True,
                                          start_date=date(1999, 1, 1),
                                          start_date_placeholder_text='Fecha Inicial',
                                          end_date=date.today(),
                                          end_date_placeholder_text='Fecha Final',
                                          initial_visible_month=date.today() - timedelta(days=31)
                                      ),
                                      style={'fontSize': 18,
                                             'background-color': 'white',
                                             'width': '100%',
                                             'position': 'relative',
                                             'box-sizing': 'border-box'
                                             }
                                         ),
                                  html.Br(),
                                  html.Button('Reset', id='button')
                              ]),
                     html.Div(className='nine columns div-for-charts bg-soft-grey',
                              children=[
                                  dcc.Graph(id='stock-ts', config={'displayModeBar': False}, animate=False)
                              ])
                            ])
                ])


# Callback time series
@app.callback(Output('stock-ts', 'figure'),
              [Input('symbol', 'value'),
               Input('type', 'value'),
               Input('date-range', 'start_date'),
               Input('date-range', 'end_date')])
def update_graph(symbol, type, start_date, end_date, dict_tickers=dict_tickers):
    url = 'https://www.alphavantage.co/query'
    function = 'TIME_SERIES_DAILY'
    outputsize = 'full'
    response = get_response(url, function, outputsize, symbol)
    df_response = get_df(response)
    df_response = date_filter_df(df_response, start_date, end_date)
    if type=='ts':
        if symbol in dict_tickers:
            fig = plot_df_py(df_response, dict_tickers[symbol])
        else:
            fig = plot_df_py(df_response, symbol)
    else:
        if symbol in dict_tickers:
            fig = plot_candlestick(df_response, dict_tickers[symbol])
        else:
            fig = plot_candlestick(df_response, symbol)
    return fig


@app.callback([Output('date-range', 'start_date'),
               Output('date-range', 'end_date')],
              Input('button', 'n_clicks'))
def reset_date(button):
    start_date = date(1999, 1, 1)
    end_date = date.today()
    return start_date, end_date


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
