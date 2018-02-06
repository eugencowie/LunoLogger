import request from 'request-promise';
import Datastore from '@google-cloud/datastore';
const datastore = Datastore()

export function fetch({}, response) {
  request.get({uri: 'https://api.mybitx.com/api/1/ticker', qs: {pair: 'XBTZAR'}, json: true}).then(ticker => {
    ticker.timestamp = new Date(ticker.timestamp);
    datastore.save({key: datastore.key(['Ticker']), data: ticker}).then(() => {
      response.status(200).send(JSON.stringify(ticker));
    });    
  });
}
