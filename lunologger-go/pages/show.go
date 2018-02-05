package pages

import "net/http"
import "io/ioutil"
import "html/template"
import "model"

type ShowTemplate struct {
	Columns int
	XbtZarTickers []model.Ticker
	EthXbtTickers []model.Ticker
}

func ShowXbtZar(response http.ResponseWriter, request *http.Request) {
	funcs := template.FuncMap{"divide": func(a, b int) int { return a / b }}
	contents, err := ioutil.ReadFile("pages/show.html")
	if err != nil { panic(err) }
	templ, err := template.New("show").Funcs(funcs).Parse(string(contents))
	if err != nil { panic(err) }
	tickers := model.RetrieveTickers(request, "XBTZAR", "-Time")
	data := ShowTemplate{1,tickers,nil}
	err = templ.Execute(response, data)
	if err != nil { panic(err) }
}

func ShowEthXbt(response http.ResponseWriter, request *http.Request) {
	funcs := template.FuncMap{"divide": func(a, b int) int { return a / b }}
	contents, err := ioutil.ReadFile("pages/show.html")
	if err != nil { panic(err) }
	templ, err := template.New("show").Funcs(funcs).Parse(string(contents))
	if err != nil { panic(err) }
	tickers := model.RetrieveTickers(request, "ETHXBT", "-Time")
	data := ShowTemplate{1,nil,tickers}
	err = templ.Execute(response, data)
	if err != nil { panic(err) }
}

func Show(response http.ResponseWriter, request *http.Request) {
	funcs := template.FuncMap{"divide": func(a, b int) int { return a / b }}
	contents, err := ioutil.ReadFile("pages/show.html")
	if err != nil { panic(err) }
	templ, err := template.New("show").Funcs(funcs).Parse(string(contents))
	if err != nil { panic(err) }
	xbtzar := model.RetrieveTickers(request, "XBTZAR", "-Time")
	ethxbt := model.RetrieveTickers(request, "ETHXBT", "-Time")
	data := ShowTemplate{2,xbtzar,ethxbt}
	err = templ.Execute(response, data)
	if err != nil { panic(err) }
}
