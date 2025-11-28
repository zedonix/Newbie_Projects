package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strconv"
	"strings"
	"unicode"
)

func main() {
	if len(os.Args) != 4 {
		printUsage()
		os.Exit(2)
	}
	amount, err := strconv.ParseFloat(os.Args[1], 64)
	base := os.Args[2]
	to := os.Args[3]
	if err != nil {
		fmt.Println("Amount should be an number")
		fmt.Println()
		printUsage()
		os.Exit(2)
	}
	converted := amount
	if base != to {
		converted, err = convertAmount(amount, base, to)
		if err != nil {
			fmt.Println(err)
			fmt.Println()
			printUsage()
			os.Exit(2)
		}
	}
	fmt.Printf("%v %v is %f in %v\n", amount, base, converted, to)
}

func printUsage() {
	fmt.Println(`Usage: currency <amount> <base currency> <convert to currency>
example: currency 10 usd inr
	This converts 10 usd to the equivalent inr`)
}

func convertAmount(amount float64, base string, to string) (float64, error) {
	if len(base) != 3 || len(to) != 3 {
		return 0, fmt.Errorf("currency codes should be 3-letter ISO codes")
	}
	base = upper(base)
	to = upper(to)

	url := fmt.Sprintf("https://api.fxratesapi.com/latest?base=%s&currencies=%s", base, to)
	resp, err := http.Get(url)
	if err != nil {
		return 0, fmt.Errorf("request error: %v", err)
	}
	defer resp.Body.Close()
	if resp.StatusCode == 400 {
		return 0, fmt.Errorf("one of the currency code is wrong")
	} else if resp.StatusCode != 200 {
		return 0, fmt.Errorf("api returned status %d", resp.StatusCode)
	}

	var data struct {
		Success bool               `json:"success"`
		Rates   map[string]float64 `json:"rates"`
	}

	if err := json.NewDecoder(resp.Body).Decode(&data); err != nil {
		return 0, fmt.Errorf("json decode: %v", err)
	}

	if !data.Success {
		return 0, fmt.Errorf("api returned success=false")
	}

	result, ok := data.Rates[to]
	if !ok {
		return 0, fmt.Errorf("invalid currency code: %s", to)
	}
	return result * amount, nil
}

func upper(s string) string {
	for _, r := range s {
		if !unicode.IsLetter(r) {
			return s
		}
	}
	return strings.ToUpper(s)
}
