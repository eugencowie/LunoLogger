import flask
import model

app = flask.Flask(__name__)

@app.route('/fetch/')
@app.route('/fetch/<pairs>')
def fetch(pairs='xbtzar+ethxbt'):
    return '\n'.join([model.fetch_ticker(pair.upper()).json for pair in pairs.split('+')])

@app.route('/dump/')
@app.route('/dump/<pairs>')
def dump(pairs='xbtzar+ethxbt'):
    return '\n'.join([''.join([t.json for t in model.retrieve_tickers(pair.upper(), 2000)]) for pair in pairs.split('+')])

@app.route('/')
@app.route('/show/')
@app.route('/show/<raw_pairs>')
def show(raw_pairs='xbtzar+ethxbt'):
    pairs = raw_pairs.split('+')
    tickers = [model.retrieve_tickers_asc(pair.upper(), 50) for pair in pairs]
    return flask.render_template('show.html', columns=len(pairs), pairs=tickers)

@app.route('/test/')
@app.route('/test/<pairs>')
def test(pairs='xbtzar+ethxbt'):
    return '\n'.join(['Test ' + pair.upper() for pair in pairs.split('+')])
