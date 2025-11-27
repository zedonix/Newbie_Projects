package main

import (
	"fmt"
	"net/http"
	"net/url"
	"os"
	"strings"

	"golang.org/x/net/html"
)

var visited = make(map[string]bool)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: go run main.go <https://example.com>")
		return
	}
	startURL := os.Args[1]
	parsed, err := url.Parse(startURL)
	if err != nil {
		fmt.Println("Invalid URL:", err)
		return
	}

	fmt.Println("Starting scan:", startURL)
	checkPage(startURL, parsed.Host)
}

func checkPage(link, domain string) {
	if visited[link] {
		return
	}
	visited[link] = true

	resp, err := http.Get(link)
	if err != nil {
		fmt.Printf("[DEAD] %s (error: %v)\n", link, err)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode >= 400 {
		fmt.Printf("[DEAD] %s (status %d)\n", link, resp.StatusCode)
		return
	}
	fmt.Printf("[OK]   %s (status %d)\n", link, resp.StatusCode)

	contentType := resp.Header.Get("Content-Type")
	if !strings.Contains(contentType, "text/html") {
		return
	}

	tokenizer := html.NewTokenizer(resp.Body)
	for {
		tt := tokenizer.Next()
		if tt == html.ErrorToken {
			break
		}
		token := tokenizer.Token()
		if token.Type == html.StartTagToken && token.Data == "a" {
			for _, attr := range token.Attr {
				if attr.Key == "href" {
					href := strings.TrimSpace(attr.Val)
					if href == "" || strings.HasPrefix(href, "#") {
						continue
					}

					newURL := resolveURL(link, href)
					if newURL == "" {
						continue
					}
					u, err := url.Parse(newURL)
					if err != nil {
						continue
					}

					if u.Host == domain {
						checkPage(newURL, domain)
					} else {
						if !visited[newURL] {
							visited[newURL] = true
							checkStatus(newURL)
						}
					}
				}
			}
		}
	}
}

func resolveURL(base, ref string) string {
	b, err := url.Parse(base)
	if err != nil {
		return ""
	}
	r, err := url.Parse(ref)
	if err != nil {
		return ""
	}
	return b.ResolveReference(r).String()
}

func checkStatus(link string) {
	resp, err := http.Head(link)
	if err != nil {
		fmt.Printf("[DEAD] %s (error: %v)\n", link, err)
		return
	}
	defer resp.Body.Close()
	if resp.StatusCode >= 400 {
		fmt.Printf("[DEAD] %s (status %d)\n", link, resp.StatusCode)
	} else {
		fmt.Printf("[OK]   %s (status %d)\n", link, resp.StatusCode)
	}
}
