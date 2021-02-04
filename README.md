# SPOT STOCK

## Description

Spot Stock is an App designed to intereactively visualize stock prices.\\

The goal is to allow users to consult stock prices by simply typing or selecting the company ticker in a user-friendly input. Furthermore, the user is provided with a set of input selector that allow to make the visualization dynamic. Two different types of visualizations are provided for the user, a time-series stock data visualization and a candlestick visualization. Finally, the user is provided with a Date Range Selector that allows to focus on the performance of the stock in a more specific time frame.\\

There are two different apps:
* app.py: The input is a text box where the user should introduce the company ticker name.
* app2.py The input is a Dropdown Menu where the user can type the name of the company and then select it in the dropdown menu.


## Requirements

* python = 3.7
* libraries
  * dash
  * plotly
  * pandas
  
 ## Execution
 
The script functions.py should be in the same directory as the app.py.\\

In order to run the application the user should should run either app.py or app2py. When executing one of the apps a new tab should open in the browser, if not, just copy the url that prompted after running tha app and paste it in the browser. The url should look like: http://127.0.0.1:8050/

## Examples

![alt text](/slides/example1.PNG "Example app.py")
![alt text](/slides/example2.PNG "Example app2.py")
