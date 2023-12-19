import yfinance as yf
from flask import request, render_template, jsonify, Flask
from newsapi import NewsApiClient

app = Flask(__name__, template_folder='templates')
newsapi = NewsApiClient(api_key='7e3fdf7d04574899a01f037d3b1e4567')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_stock_data', methods = ['POST'])
def get_stock_data():
    ticker = request.get_json()['ticker']
    data = yf.Ticker(ticker).history(period='1y')
    return jsonify({'currentPrice':data.iloc[-1].Close, 'openPrice':data.iloc[-1].Open})

def get_company_name(ticker):
   stock = yf.Ticker(ticker)
   return stock.info['longName']

@app.route('/get_news', methods = ['POST'])
def get_news():
    ticker = request.get_json()['ticker']
    company_name = get_company_name(ticker)
    query = company_name + " financial"
    news = newsapi.get_everything(q=query, language='en', sort_by='relevancy')
    return jsonify(news['articles'])

if __name__ == '__main__':
    app.run(debug=True)