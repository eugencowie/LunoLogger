package pages

import "net/http"
import "model"
import "fmt"

func ShowXbtZar(response http.ResponseWriter, request *http.Request) {
	tickers := model.RetrieveTickers(request, "XBTZAR", "-Time")
	for _, ticker := range tickers {
		fmt.Fprint(response, ticker.Json)
	}
}

func ShowEthXbt(response http.ResponseWriter, request *http.Request) {
	tickers := model.RetrieveTickers(request, "ETHXBT", "-Time")
	for _, ticker := range tickers {
		fmt.Fprint(response, ticker.Json)
	}
}

func Show(response http.ResponseWriter, request *http.Request) {
	ShowXbtZar(response, request)
	ShowEthXbt(response, request)
}
