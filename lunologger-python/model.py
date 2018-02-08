from google.appengine.ext import ndb
from datetime import datetime
import urllib2
import json as json_loader

class Ticker(ndb.Model):
    json = ndb.StringProperty()
    pair = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty()
    last_trade = ndb.StringProperty()
    bid = ndb.StringProperty()
    ask = ndb.StringProperty()
    rolling_24_hour_volume = ndb.StringProperty()

def fetch_ticker(pair):
    text = urllib2.urlopen('https://api.mybitx.com/api/1/ticker?pair={}'.format(pair)).read()
    json = json_loader.loads(text)
    ticker = Ticker(
        json = text,
        pair = json['pair'],
        timestamp = datetime.fromtimestamp(json['timestamp'] / 1000),
        last_trade = (json['last_trade']),
        bid = (json['bid']),
        ask = (json['ask']),
        rolling_24_hour_volume = (json['rolling_24_hour_volume'])
    )
    ticker.put()
    return ticker

def retrieve_tickers(pair, max=2000):
    return Ticker.query().filter(Ticker.pair == pair).order(Ticker.timestamp).fetch(max)

def retrieve_tickers_asc(pair, max=50):
    return Ticker.query().filter(Ticker.pair == pair).order(-Ticker.timestamp).fetch(max)
