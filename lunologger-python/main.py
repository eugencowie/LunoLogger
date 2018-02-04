from pages import FetchPage, DumpPage, MainPage, BacktestPage
from webapp2 import WSGIApplication

app = WSGIApplication([
    ('/fetch', FetchPage),
    ('/dump', DumpPage),
    ('/', MainPage),
    ('/test', BacktestPage)
], debug=True)
