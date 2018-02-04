package pages

import "net/http"
import "model"
import "fmt"

func FetchXbtZar(response http.ResponseWriter, request *http.Request) {
	ticker := model.FetchTicker(request, "XBTZAR")
	model.StoreTicker(request, ticker)
	fmt.Fprint(response, ticker.Json)
}

func FetchEthXbt(response http.ResponseWriter, request *http.Request) {
	ticker := model.FetchTicker(request, "ETHXBT")
	model.StoreTicker(request, ticker)
	fmt.Fprint(response, ticker.Json)
}

func Fetch(response http.ResponseWriter, request *http.Request) {
	FetchXbtZar(response, request)
	FetchEthXbt(response, request)
}
