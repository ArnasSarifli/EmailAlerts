import plotly.graph_objects as go
import yfinance as yf
import os

class Graph():
    def drawGraph(akcija):
        success = False
        data = yf.download(tickers=akcija, period='30d', interval='1d')
        if data.empty:
            return success

        sma50 = data.Close.rolling(window=50, min_periods=1).mean()

        fig = go.Figure(data=[go.Candlestick(x=data.index,
                                         open=data['Open'],
                                         high=data['High'],
                                         low=data['Low'],
                                         close=data['Close'])])

        fig.add_trace(go.Scatter(x=data.index, y=sma50, name='Moving Avg 50',
                             line=dict(color='green', width=1.5)))

        fig.update_layout(
        title=f"{akcija} 30 dienų kainos kaita",
        yaxis_title="Kaina (USD)")

        fig.update(layout_xaxis_rangeslider_visible=False)

        if not os.path.exists("Images"):
            os.mkdir("Images")

        fig.write_image("Images/graph1.png")
        success = True
        return success

