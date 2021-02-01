# from alpha_vantage.timeseries import TimeSeries
#import matplotlib.pyplot as plt
import codecs

# ts = TimeSeries(output_format='pandas')
# data, meta_data = ts.get_daily('SAP.FRK')
# open = data['1. open'][0]
# close = data['4. close'][0]
open = 108.52
close = 104.86

template = 'screen-output-weather.svg'
output = codecs.open(template , 'r', encoding='utf-8').read()

output = output.replace('STOCK1','SAP')
output = output.replace('STOCK_CLOSE1', "{:.2f}".format(close))
output = output.replace('STOCK_WINLOSS1', "{:.2f}".format(close-open))

codecs.open('screen-output-weather.svg', 'w', encoding='utf-8').write(output)
