import codecs
import time
import os.path
import time
import sys
import os
import json
from alpha_vantage.timeseries import TimeSeries

stale=True
stocks_filepath = '/stocks.json'
stock1_symbol = 'SAP.FRK'
stock1_name = 'SAP'
data={}
refreshDelay = 24*60*60  # for daily data

if (os.path.isfile(os.getcwd() + stocks_filepath)):
    with open(os.getcwd() + stocks_filepath, 'r') as content_file:
        data = json.load(content_file)
    stale=time.time() - os.path.getmtime(os.getcwd() + stocks_filepath) > refreshDelay

if stale:
    try:
        print('Stock data is stale, calling provider')
        ts = TimeSeries(output_format='json')
        data,_ = ts.get_daily(stock1_symbol)
        with open(os.getcwd() + stocks_filepath, 'w') as text_file:
            text_file.write(json.dumps(data))
    except:
        print('Failed to get new API response, will use older response')
        with open(os.getcwd() + stocks_filepath, 'r') as content_file:
          data = json.load(content_file)

first = next(iter(data.values()))
print (first)
open = float(first['1. open'])
close = float(first['4. close'])
diff = close - open

template = 'screen-output-weather.svg'
output = codecs.open(template , 'r', encoding='utf-8').read()

output = output.replace('STOCK1', stock1_name)
output = output.replace('STOCK_CLOSE1', '{:.2f}'.format(close))
diffText = '{:.2f}'.format(diff)
if diff >= 0:
    diffText = '+' + diffText
output = output.replace('STOCK_WINLOSS1', diffText)

codecs.open('screen-output-weather.svg', 'w', encoding='utf-8').write(output)
