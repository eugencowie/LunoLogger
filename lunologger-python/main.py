import flask
import model

app = flask.Flask(__name__)

@app.route('/fetch/')
@app.route('/fetch/<pairs>')
def fetch(pairs='xbtzar+ethxbt'):
    return '\n'.join([model.fetch_ticker(pair.upper()).json for pair in pairs.split('+')])

@app.route('/dump/')
@app.route('/dump/<period>')
@app.route('/dump/<period>/<pairs>')
def dump(period='hourly', pairs='xbtzar+ethxbt'):
    result = []
    if period == 'hourly': result = [''.join([t.json for t in model.retrieve_tickers(pair.upper(), 2000)]) for pair in pairs.split('+')]
    if period == 'daily': result = [''.join([t.json for t in model.retrieve_tickers(pair.upper(), 2000) if t.timestamp.hour == 0]) for pair in pairs.split('+')]
    return '\n'.join(result)

@app.route('/')
@app.route('/show/')
@app.route('/show/<period>')
@app.route('/show/<period>/<pairs>')
def show(period='hourly', pairs='xbtzar+ethxbt'):
    pairs_list = pairs.split('+')
    tickers = []
    if period == 'hourly': tickers = [model.retrieve_tickers_asc(pair.upper(), 50) for pair in pairs_list]
    if period == 'daily': tickers = [[t for t in model.retrieve_tickers_asc(pair.upper(), 50*24) if t.timestamp.hour == 0] for pair in pairs_list]
    return flask.render_template('show.html', columns=len(pairs_list), pairs=tickers)

@app.route('/test/')
@app.route('/test/<pairs>')
def test(pairs='xbtzar+ethxbt'):
    return '\n'.join(['Test ' + pair.upper() for pair in pairs.split('+')])
