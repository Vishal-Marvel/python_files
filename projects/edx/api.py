from pycoingecko import CoinGeckoAPI
import pandas as pd
cg = CoinGeckoAPI()
bitcon_data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency = 'usd', days=30)
data = pd.DataFrame(bitcon_data, columns=['TimeStamp' ,'Price'])
data['Date'] = pd.to_datetime(data['TimeStamp'], unit='ms')
# candlestick_data = data.groupby(data.Date.dt.date).agg({'Price': ['min','max','first','last']})
# fig = go.Figure()
print(data.head(5))