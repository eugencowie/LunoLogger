package pages

import "net/http"
import "model"
import "fmt"

func DumpXbtZar(response http.ResponseWriter, request *http.Request) {
	tickers := model.RetrieveTickers(request, "XBTZAR", "-Time")
	for _, ticker := range tickers {
		fmt.Fprint(response, ticker.Json)
	}
}

func DumpEthXbt(response http.ResponseWriter, request *http.Request) {
	tickers := model.RetrieveTickers(request, "ETHXBT", "-Time")
	for _, ticker := range tickers {
		fmt.Fprint(response, ticker.Json)
	}
}

func Dump(response http.ResponseWriter, request *http.Request) {
	DumpXbtZar(response, request)
	DumpEthXbt(response, request)
}
