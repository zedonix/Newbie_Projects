package main

import (
	"math/rand"
	"net/http"
	"strings"
	"time"
)

type Link struct {
	Id   string
	Link string
}

var linkMap = map[string]*Link{"example": {Id: "example", Link: "https://example.com"}}

func main() {
	http.HandleFunc("/submit", submitHandler)
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path == "/" {
			htmlHandler(w)
			return
		}
		redirectHandler(w, r)
	})
	if err := http.ListenAndServe(":8080", nil); err != nil {
		panic(err)
	}
}

func redirectHandler(w http.ResponseWriter, r *http.Request) {
	id := r.URL.Path
	if len(id) > 0 && id[0] == '/' {
		id = id[1:]
	}
	link, found := linkMap[id]
	if !found {
		http.Error(w, "Link not found", http.StatusNotFound)
		return
	}
	http.Redirect(w, r, link.Link, http.StatusMovedPermanently)
}

func submitHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}
	if err := r.ParseForm(); err != nil {
		http.Error(w, "Bad request", http.StatusBadRequest)
		return
	}
	url := r.FormValue("url")
	if url == "" {
		http.Error(w, "Url is required", http.StatusBadRequest)
		return
	}
	if !(strings.HasPrefix(url, "http://") || strings.HasPrefix(url, "https://")) {
		url = "https://" + url
	}
	id := generateId(8)
	linkMap[id] = &Link{Id: id, Link: url}
	http.Redirect(w, r, "/", http.StatusSeeOther)
}

func generateId(length int) string {
	const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	seededRand := rand.New(rand.NewSource(time.Now().UnixNano()))

	var result []byte

	for range length {
		index := seededRand.Intn(len(charset))
		result = append(result, charset[index])
	}

	return string(result)
}

func htmlHandler(w http.ResponseWriter) {
	html := `
	<h1>Just freaking give the link </h1>
	<form action="/submit" method="POST">
	<label for="url">Website URL:</label>
	<input id="url" type="text" name="url">
	<input type="submit" value="Submit">
	</form>
	<ul>
`
	for _, link := range linkMap {
		html += `<li><a href="/` + link.Id + `">` + link.Id + `</a></li>`
	}
	html += `</ul>`
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	w.WriteHeader(http.StatusOK)
	_, _ = w.Write([]byte(html))
}
