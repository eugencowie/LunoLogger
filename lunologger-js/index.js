const request = require('request-promise');
const datastore = require('@google-cloud/datastore')();

exports.fetch = ({}, res) => {
  request.get({uri: 'https://api.mybitx.com/api/1/ticker', qs: {pair: 'XBTZAR'}, json: true}).then(ticker => {
    ticker.timestamp = new Date(ticker.timestamp);
    datastore.save({key: datastore.key(['Ticker']), data: ticker}).then(() => {
      res.status(200).send(JSON.stringify(ticker));
    });
  });
};
