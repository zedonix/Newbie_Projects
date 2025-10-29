package main

import (
	"fmt"
	"log"
	"net/http"
)

func headers(w http.ResponseWriter, req *http.Request) {
	for name, headers := range req.Header {
		for _, h := range headers {
			fmt.Fprintf(w, "%v: %v\n", name, h)
		}
	}
}

func hello(w http.ResponseWriter, req *http.Request) {
	fmt.Fprintf(w, "hello")
}

func handler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	w.Write([]byte(`{"ok":true}`))
}

func root(w http.ResponseWriter, req *http.Request) {
	fmt.Fprintf(w, "nothing here right now")
}

func logging(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		log.Println(r.Method, r.URL.Path)
		next.ServeHTTP(w, r)
	})
}

func main() {
	mux := http.NewServeMux()
	mux.Handle("/", logging(http.HandlerFunc(hello)))
	mux.HandleFunc("/header", headers)
	mux.HandleFunc("/handler", handler)
	mux.HandleFunc("/hello", hello)
	mux.HandleFunc("/root", root)
	log.Fatal(http.ListenAndServe(":8080", mux))
}
