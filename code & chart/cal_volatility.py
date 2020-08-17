import pandas as pd
from math import pow, sqrt
import sys

if len(sys.argv) <= 1:
    sys.exit(0)

f = ''
d = '/Users/lucan/Dropbox/MPA/Capstone paper/data/'
asset = sys.argv[1]
print (asset)
if asset == 'bitcoin':
    f = 'Bitcoin Historical Data - Investing.com.csv'
elif asset == 'jpy':
    f = 'USD_JPY Historical Data.csv'
elif asset == 'eur':
    f = 'EUR_USD Historical Data.csv'
elif asset == 'sgd':
    f = 'SGD_USD Historical Data.csv'
elif asset == 'gold':
    f = 'Gold Futures Historical Data.csv'
elif asset == 'oil':
    f = 'Crude Oil WTI Futures Historical Data.csv'
else:
    sys.exit(0)

df = pd.read_csv(d+f)
df['volatility'] = 0.0
N = 7
l = len(df)

for p in range(0, l-N+1):
    c = 0
    for i in range(0, N):
        v1 = df.loc[p]['Price']
        v2 = df.loc[p+i]['Price']
        if isinstance(v1, str):
            v1 = float(v1.replace(',',''))
            v2 = float(v2.replace(',',''))

        c = c + pow((v1-v2)/v1*100, 2)
    c = c * 1.0 / N
    c = sqrt(c)
    df.at[p, 'volatility'] = c

df.to_csv(d+'volatility_'+f)
