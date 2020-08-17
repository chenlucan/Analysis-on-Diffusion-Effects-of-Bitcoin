import pandas as pd
from math import pow, sqrt
import sys

n1 = sys.argv[1]
n2 = sys.argv[2]

def get_file(asset):
    f = ''
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
    return f

def cal_r(s1, s2):
    s1 = pd.Series(s1)
    s2 = pd.Series(s2)

    xm = s1.mean()
    ym = s2.mean()
    stdx = s1.std()
    stdy = s2.std()

    print(xm, stdx)
    print(ym, stdy)

    cov = 0.0
    for p in range(0, len(s1)):
        x = s1[p]
        y = s2[p]
        cov = cov + (x-xm)*(y-ym)

    cov = cov / (len(s1)-1)
    r = cov / (stdx * stdy)
    # print('cov==========',cov, r)
    return (cov, r)


f1 = get_file(n1)
f2 = get_file(n2)
d = '/Users/lucan/Dropbox/MPA/Capstone paper/data/'

df1 = pd.read_csv(d+f1)
df2 = pd.read_csv(d+f2)

df1 = df1[['Date','Price']]
df2 = df2[['Date','Price']]

if n1 == 'jpy':
    df1['Price'] = 1/df1['Price']

if n2 == 'jpy':
    df2['Price'] = 1/df2['Price']

df1 = df1.rename(columns={"Price": "X"})
df2 = df2.rename(columns={"Price": "Y"})

print(df1)
print(df2)

df1.set_index('Date')
df2.set_index('Date')

df = pd.merge(df1, df2, how='inner', left_index=True, right_index=True)

df['X_return'] = 0.0
df['Y_return'] = 0.0

l = len(df)

for p in range(0, l):
    vx = df.loc[p]['X']
    vy =  df.loc[p]['Y']
    if isinstance(vx, str):
        df.at[p, 'X'] = float(vx.replace(',',''))
    if isinstance(vy, str):
        df.at[p, 'Y'] = float(vy.replace(',',''))

for p in range(0, l-1):
    v1 = df.loc[p]['X']
    v2 = df.loc[p+1]['X']
    df.at[p+1, 'X_return'] = (v2-v1)/v1*100.0

    v1 = df.loc[p]['Y']
    v2 = df.loc[p+1]['Y']
    df.at[p+1, 'Y_return'] = (v2-v1)/v1*100.0

df['X_return_7_mean'] = 0.0
df['Y_return_7_mean'] = 0.0

for p in range(6, l-1):
    df.at[p, 'X_return_7_mean'] = df['X_return'][p-6: p+1].mean()
    df.at[p, 'Y_return_7_mean'] = df['Y_return'][p-6: p+1].mean()

df['X_7_mean'] = 0.0
df['Y_7_mean'] = 0.0

for p in range(6, l-1):
    df.at[p, 'X_7_mean'] = df['X'][p-6: p+1].mean()
    df.at[p, 'Y_7_mean'] = df['Y'][p-6: p+1].mean()


print (df.head(20))

# cal_r(df['X'], df['Y'])
# cal_r(df['X_7_mean'], df['Y_7_mean'])
# cal_r(df['X_return'], df['Y_return'])
# cal_r(df['X_return_7_mean'], df['Y_return_7_mean'])

days = 7
df['R_price'] = 0.0
df['R_return'] = 0.0
for p in range(days, l):
    df.at[p-1, 'R_price'] = cal_r(df['X'][p-days:p].tolist(), df['Y'][p-days:p].tolist())[1]
    df.at[p-1, 'R_return'] = cal_r(df['X_return'][p-days:p].tolist(), df['Y_return'][p-days:p].tolist())[1]

print(df.tail(20))
print(df['R_price'][days-1:].mean())
print(df['R_return'][days-1:].mean())
