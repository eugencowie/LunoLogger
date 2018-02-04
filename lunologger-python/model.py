from google.appengine.ext import ndb
from datetime import datetime
import urllib2
import json

class Ticker(ndb.Model):
    json = ndb.StringProperty()
    pair = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty()
    last_trade = ndb.StringProperty()
    bid = ndb.StringProperty()
    ask = ndb.StringProperty()
    rolling_24_hour_volume = ndb.StringProperty()

def ticker(pair):
    json_str = urllib2.urlopen('https://api.mybitx.com/api/1/ticker?pair={}'.format(pair)).read()
    json_dict = json.loads(json_str)
    tickers = ndb.Key('tickers', '{}'.format(pair))
    ticker = Ticker(parent=tickers, json=json_str, pair=json_dict['pair'],
        timestamp=datetime.fromtimestamp(json_dict['timestamp']/1000),
        last_trade=json_dict['last_trade'], bid=json_dict['bid'], ask=json_dict['ask'],
        rolling_24_hour_volume=json_dict['rolling_24_hour_volume'])
    return ticker
