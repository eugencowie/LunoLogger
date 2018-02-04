from model import Ticker, ticker
from html import *
from google.appengine.ext import ndb
from webapp2 import RequestHandler
from decimal import *

class FetchPage(RequestHandler):
    def get(self):
        xbt_zar = ticker('XBTZAR')
        eth_xbt = ticker('ETHXBT')
        xbt_zar.put()
        eth_xbt.put()
        self.response.write(''.join([xbt_zar.json, eth_xbt.json]))
        
class DumpPage(RequestHandler):
    def get(self):
        xbt_zar = Ticker.query(ancestor=ndb.Key('tickers', 'XBTZAR')).order(-Ticker.timestamp).fetch(100)
        eth_xbt = Ticker.query(ancestor=ndb.Key('tickers', 'ETHXBT')).order(-Ticker.timestamp).fetch(100)
        self.response.write(''.join([t.json for t in xbt_zar+eth_xbt]))

def ticker_html_inner(t):
    return td(t.pair) + td('{:%Y-%m-%d %H:%M}'.format(t.timestamp)) + td(t.last_trade) + td(t.bid) + td(t.ask) # + td(t.rolling_24_hour_volume)

def ticker_html(t, attr='style="color:white;background-color:dimgray"'):
    return tr(ticker_html_inner(t), attr)

def ticker_html_prev(t, prev):
    if float(t.last_trade) > float(prev.last_trade):
        return ticker_html(t, 'style="color:white;background-color:darkgreen"')
    elif float(t.last_trade) < float(prev.last_trade):
        return ticker_html(t, 'style="color:white;background-color:darkred"')
    else:
        return ticker_html(t)

class MainPage(RequestHandler):
    def get(self):
        xbtzar = Ticker.query(ancestor=ndb.Key('tickers', 'XBTZAR')).order(-Ticker.timestamp).fetch(20)
        ethxbt = Ticker.query(ancestor=ndb.Key('tickers', 'ETHXBT')).order(-Ticker.timestamp).fetch(20)
        table_head = tr(th('Pair') + th('Time') + th('Last trade') + th('Bid') + th('Ask'))# + th('24h volume'))
        xbtzar_rows = [ticker_html_prev(t,xbtzar[i+1]) if i<len(xbtzar)-1 else ticker_html(t) for i,t in enumerate(xbtzar)]
        ethxbt_rows = [ticker_html_prev(t,ethxbt[i+1]) if i<len(ethxbt)-1 else ticker_html(t) for i,t in enumerate(ethxbt)]
        self.response.write(
            html(
                head(
                    link('stylesheet', '/public/bootstrap.min.css') +
                    style('table{float:left!important;width:49%!important;border:2px solid black!important;margin:5px!important}')
                ) +
                body(
                    table(table_head + '\n'.join(xbtzar_rows), 'class="table table-hover"') +
                    table(table_head + '\n'.join(ethxbt_rows), 'class="table table-hover"')
                )
            )
        )

class Wallet:
    currency = Decimal(1000)
    asset = Decimal(0)
    position = 'sell'
    def buy(self, t, cost, fee=Decimal(0.01)):
        if self.position == 'sell':
            self.asset += ((self.currency - (self.currency * fee)) / cost)
            self.currency = Decimal(0)
            self.position = 'buy'
            return tr(ticker_html_inner(t) + td('Buy') + td('{0:.2f}'.format(self.currency)) + td('{0:.8f}'.format(self.asset)), 'style="color:white;background-color:darkgreen"')
        else:
            return tr(ticker_html_inner(t) + td('') + td('{0:.2f}'.format(self.currency)) + td('{0:.8f}'.format(self.asset)), 'style="color:white;background-color:darkgreen"')
    def sell(self, t, cost, fee=Decimal(0.01)):
        if self.position == 'buy':
            self.currency = ((self.asset - (self.asset * fee)) * cost)
            self.asset = Decimal(0)
            self.position = 'sell'
            return tr(ticker_html_inner(t) + td('Sell') + td('{0:.2f}'.format(self.currency)) + td('{0:.8f}'.format(self.asset)), 'style="color:white;background-color:darkred"')
        else:
            return tr(ticker_html_inner(t) + td('') + td('{0:.2f}'.format(self.currency)) + td('{0:.8f}'.format(self.asset)), 'style="color:white;background-color:darkred"')
    def none(self, t):
        return tr(ticker_html_inner(t) + td('') + td('{0:.2f}'.format(self.currency)) + td('{0:.8f}'.format(self.asset)), 'style="color:white;background-color:dimgray"')

class BacktestPage(RequestHandler):
    def get(self):
        xbtzar = Ticker.query(ancestor=ndb.Key('tickers', 'XBTZAR')).order(Ticker.timestamp).fetch(20)
        wallet = Wallet()
        xbtzar_rows = []
        for i,t in enumerate(xbtzar):
            if i>0:
                prev = xbtzar[i-1]
                action = 'None'
                if float(t.last_trade) > float(prev.last_trade):
                    xbtzar_rows.append(wallet.buy(t, Decimal(t.last_trade), Decimal(0)))
                elif float(t.last_trade) < float(prev.last_trade):
                    xbtzar_rows.append(wallet.sell(t, Decimal(t.last_trade), Decimal(0)))
                else:
                    xbtzar_rows.append(wallet.none(t))
        wallet.sell(t, Decimal(xbtzar[len(xbtzar)-1].last_trade), Decimal(0))
        table_head = tr(th('Pair') + th('Time') + th('Last trade') + th('Bid') + th('Ask') + th('Action') + th('Currency') + th('Asset'))
        self.response.write(
            html(
                head(link('stylesheet', '/public/bootstrap.min.css')) +
                body(table(table_head + '\n'.join(xbtzar_rows), 'class="table table-hover"'))
            )
        )
