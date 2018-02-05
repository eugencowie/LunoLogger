package model

import "net/http"
import "google.golang.org/appengine"
import "google.golang.org/appengine/urlfetch"
import "google.golang.org/appengine/datastore"
import "io/ioutil"
import "encoding/json"
import "time"
import "github.com/shopspring/decimal"

type Ticker struct {
	Json      string
	Pair      string `json:"pair"`
	Time      int64  `json:"timestamp"`
	LastTrade string `json:"last_trade"`
	Bid       string `json:"bid"`
	Ask       string `json:"ask"`
	Volume24h string `json:"rolling_24_hour_volume"`
}

type TickerData struct {
	Json      string
	Pair      string
	Time      time.Time
	LastTrade decimal.Decimal
	Bid       decimal.Decimal
	Ask       decimal.Decimal
	Volume24h decimal.Decimal
}

func (t Ticker) Data() TickerData {
	data := TickerData{}
	data.Json = t.Json
	data.Pair = t.Pair
	data.Time = time.Unix(t.Time / 1000, 0)
	err := error(nil)
	data.LastTrade, err = decimal.NewFromString(t.LastTrade)
	if err != nil { panic(err) }
	data.Bid, err = decimal.NewFromString(t.Bid)
	data.Ask, err = decimal.NewFromString(t.Ask)
	data.Volume24h, err = decimal.NewFromString(t.Volume24h)
	return data
}

func webRequest(request *http.Request, url string) []byte {
	context := appengine.NewContext(request)
	client := urlfetch.Client(context)
	response, err := client.Get(url)
	if err != nil { panic(err) }
	defer response.Body.Close()
	body, err := ioutil.ReadAll(response.Body)
	if err != nil { panic(err) }
	return body
}

func FetchTicker(request *http.Request, pair string) Ticker {
	result := webRequest(request, "https://api.mybitx.com/api/1/ticker?pair="+pair)
	ticker := Ticker{Json: string(result)}
	json.Unmarshal(result, &ticker)
	return ticker
}

func StoreTicker(request *http.Request, ticker Ticker) {
	context := appengine.NewContext(request)
	key := datastore.NewIncompleteKey(context, "Ticker", nil)
	_, err := datastore.Put(context, key, &ticker)
	if err != nil { panic(err) }
}

func RetrieveTickers(request *http.Request, pair string, order string) []Ticker {
	context := appengine.NewContext(request)
	query := datastore.NewQuery("Ticker").Filter("Pair =", pair).Order(order)
	var results []Ticker
	for it := query.Run(context); ; {
		var ticker Ticker
		_, err := it.Next(&ticker)
		if err == datastore.Done { break }
		if err != nil { panic(err) }
		results = append(results, ticker)
	}
	return results
}

func RetrieveTickersData(request *http.Request, pair string, order string) []TickerData {
	context := appengine.NewContext(request)
	query := datastore.NewQuery("Ticker").Filter("Pair =", pair).Order(order)
	var results []TickerData
	for it := query.Run(context); ; {
		var ticker Ticker
		_, err := it.Next(&ticker)
		if err == datastore.Done { break }
		if err != nil { panic(err) }
		results = append(results, ticker.Data())
	}
	return results
}
