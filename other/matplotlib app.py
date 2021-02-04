from functions import get_response, get_df, plot_df, plot_df_py

url = 'https://www.alphavantage.co/query'
function = 'TIME_SERIES_DAILY'
symbol = 'BA'
outputsize = 'full'

response = get_response(url, function, outputsize, symbol)
df_response = get_df(response)

# Plot with matplotlib
plot_df(df_response, symbol)

