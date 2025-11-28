package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strconv"
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
	website := "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/"
	website += base + ".json"
	resp, err := http.Get(website)
	if err != nil {
		return 0, err
	}
	defer resp.Body.Close()
	if resp.StatusCode == http.StatusNotFound {
		return 0, fmt.Errorf("%q in not a currency code", to)
	} else if resp.StatusCode != http.StatusOK {
		return 0, fmt.Errorf("unexpected status: %v", resp.StatusCode)
	}

	var raw map[string]json.RawMessage
	if err := json.NewDecoder(resp.Body).Decode(&raw); err != nil {
		return 0, fmt.Errorf("json decode error: %v", err)
	}

	baseFind := raw[base]
	if baseFind == nil {
		return 0, fmt.Errorf("%q in not a currency code", base)
	}

	var rates map[string]float64
	if err := json.Unmarshal(baseFind, &rates); err != nil {
		return 0, fmt.Errorf("json unmarshal error: %v", err)
	}

	result, ok := rates[to]
	if !ok {
		return 0, fmt.Errorf("%q in not a currency code", to)
	}
	return result * float64(amount), nil
}
