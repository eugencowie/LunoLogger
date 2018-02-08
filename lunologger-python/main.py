from pages import FetchPage, DumpPage, MainPage, BacktestXbtZarPage, BacktestEthXbtPage
from webapp2 import WSGIApplication

app = WSGIApplication([
    ('/fetch', FetchPage),
    ('/dump', DumpPage),
    ('/', MainPage),
    ('/test/xbtzar', BacktestXbtZarPage),
    ('/test/ethxbt', BacktestEthXbtPage)
], debug=True)
