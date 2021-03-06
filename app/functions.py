from datetime import datetime

import requests
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import plotly.graph_objects as go

import csv

def csv_to_dict(csv_name='tickers.csv'):
    '''
    :param csv_name: name of the csv file to be converted in list
    :return: list
    '''
    with open(csv_name, mode='r') as infile:
        reader = csv.reader(infile)
        list_names = [{'label': line[1], 'value': line[0]} for line in reader]
    with open(csv_name, mode='r') as infile:
        reader = csv.reader(infile)
        list_tickers = [{'label': line[0], 'value': line[0]} for line in reader]
    with open(csv_name, mode='r') as infile:
        reader = csv.reader(infile)
        dict_tickers = {line[0]: line[1] for line in reader}

    list_fin = list_names + list_tickers
    return list_fin, dict_tickers

def get_response(url, function, outputsize, symbol='GOOG', key='Y6GDRF92F1KZUF4O'):
    '''
    :param url: The url of the API
    :param function: The function of the API. Ex: TIME_SERIES_DAILY for daily stock data
    :param symbol: Market symbol of the company.
    :param outputsize: size of the response (compact: 100 samples, full: all data)
    :param key: API key
    :return: dictionary with API response
    '''
    params = {'function': function, 'symbol': symbol, 'outputsize': outputsize, 'apikey': key}
    response = requests.get(url, params=params)
    return response


def get_df(response):
    '''
    :param response: API response
    :return: API response converted to df
    '''
    dict_response = {'Date': [], 'Open': [], 'High': [], 'Low': [], 'Close': [], 'Volume': []}
    response_json = response.json()
    ts = response_json['Time Series (Daily)']
    for a in reversed(list(ts.keys())):
        dict_response['Date'].append(datetime.strptime(a, '%Y-%m-%d'))
        dict_response['Open'].append(float(ts[a]['1. open']))
        dict_response['High'].append(float(ts[a]['2. high']))
        dict_response['Low'].append(float(ts[a]['3. low']))
        dict_response['Close'].append(float(ts[a]['4. close']))
        dict_response['Volume'].append(float(ts[a]['5. volume']))
    df_response = pd.DataFrame(dict_response)
    return df_response

def date_filter_df(df_response, start_date, end_date):
    '''
    :param df_response: df to be filtered by date
    :param start_date: start date to filter from
    :param end_date: start date to filter to
    :return: filtered by date df
    '''
    df_filtered = df_response[(df_response['Date'] >= start_date) & (df_response['Date'] <= end_date)]
    return df_filtered

def plot_df(df, symbol):
    '''
    :param df: dataframe with the data to plot
    :param symbol: symbol of the company to plot stock value
    :return: plot the trend of the stock using matplotlib
    '''
    # Figure object, figure size
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.fill_between(df['Date'], df['Close'], color="skyblue", alpha=0.2)
    ax.plot(df['Date'], df['Close'], color='dodgerblue')

    # figure grids
    ax.grid()

    # y-axis limits (a bit lower and a bit higher than min and max ranges of plot
    ax.set_ylim((min(df['Close']) * 0.95, max(df['Close']) * 1.05))

    # axis titles
    ax.set(ylabel='USD ($)', title=symbol)
    # dates interval, we want 12 tickers in the axis so we divided df length by 15
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=round(len(df['Date'])/12)))
    # format x-axis
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')

    plt.show()


def plot_df_py(df, symbol):
    trace1 = {
        'line': {'color': 'rgba(30, 166, 220, 1)'},
        'mode': 'lines',
        'name': symbol,
        'type': 'scatter',
        'x': df['Date'],
        'y': df['Close'],
        'xaxis': 'x',
        'yaxis': 'y',
        'fill': 'tozeroy',
        'fillcolor': 'rgba(30, 166, 220, 0.2)'
    }
    data = [trace1]

    layout = {
        "title": {'text': symbol, 'font': {'color': 'black', 'size': 28}, 'x': 0.5},
        "template": "seaborn",
        "autosize": True,
        "xaxis": {
            "domain": [0, 1],
            'range': [min(df['Date']), max(df['Date'])],
            'tickmode': 'auto',
            'rangeslider_visible': True,
            'nticks': 20,
            "rangeselector": {"buttons": [
                {
                    "step": "month",
                    "count": 3,
                    "label": "3 mo",
                    "stepmode": "backward"
                },
                {
                    "step": "month",
                    "count": 6,
                    "label": "6 mo",
                    "stepmode": "backward"
                },
                {
                    "step": "year",
                    "count": 1,
                    "label": "1 yr",
                    "stepmode": "backward"
                },
                {
                    "step": "year",
                    "count": 1,
                    "label": "YTD",
                    "stepmode": "todate"
                },
                {"step": "all"}
            ],
            }
        },
        "yaxis": {
            "title": "USD",
            "domain": [0, 1],
            'tickprefix': '$',
            'range': [min(df['Close']) * 0.95, max(df['Close']) * 1.05]
        },
        "margin": {
            "b": 50,
            "l": 70,
            "r": 30,
            "t": 40
        }
    }

    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(height=920)
    return fig

def plot_candlestick(df, symbol):
    trace1 = go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])

    data = [trace1]

    layout = {
        "title": {'text': symbol, 'font': {'color': 'black', 'size': 28}, 'x': 0.5},
        "template": "seaborn",
        "autosize": True,
        "xaxis": {
            "domain": [0, 1],
            'range': [min(df['Date']), max(df['Date'])],
            'tickmode': 'auto',
            'nticks': 20,
            "rangeselector": {"buttons": [
                {
                    "step": "month",
                    "count": 3,
                    "label": "3 mo",
                    "stepmode": "backward"
                },
                {
                    "step": "month",
                    "count": 6,
                    "label": "6 mo",
                    "stepmode": "backward"
                },
                {
                    "step": "year",
                    "count": 1,
                    "label": "1 yr",
                    "stepmode": "backward"
                },
                {
                    "step": "year",
                    "count": 1,
                    "label": "YTD",
                    "stepmode": "todate"
                },
                {"step": "all"}
            ],
            }
        },
        "yaxis": {
            "title": "USD",
            "domain": [0, 1],
            'tickprefix': '$',
            'range': [min(df['Low']) * 0.95, max(df['High']) * 1.05]
        },
        "margin": {
            "b": 50,
            "l": 70,
            "r": 30,
            "t": 40
        }
    }

    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(height=920)
    return fig

