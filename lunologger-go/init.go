package lunologger

import "net/http"
import "pages"

func init() {
	http.HandleFunc("/fetch/xbtzar", pages.FetchXbtZar)
	http.HandleFunc("/fetch/ethxbt", pages.FetchEthXbt)
	http.HandleFunc("/fetch", pages.Fetch)
	http.HandleFunc("/dump/xbtzar", pages.DumpXbtZar)
	http.HandleFunc("/dump/ethxbt", pages.DumpEthXbt)
	http.HandleFunc("/dump", pages.Dump)
	http.HandleFunc("/show/xbtzar", pages.ShowXbtZar)
	http.HandleFunc("/show/ethxbt", pages.ShowEthXbt)
	http.HandleFunc("/show", pages.Show)
	http.HandleFunc("/", pages.Show)
}
