package main

import (
	"fmt"
	"os"
)

func main() {
	data, err := os.ReadFile("input")
	if err != nil {
		panic(err)
	}
	str := string(data)
	first(str)
	second(str)
}

func first(str string) {
	floor := 0
	for i, ch := range str {
		_ = i
		if ch == '(' {
			floor += 1
		} else {
			floor -= 1
		}
	}
	fmt.Println(floor)
}

func second(str string) {
	floor := 0
	position := 0
	for i, chr := range str {
		if chr == '(' {
			floor += 1
		} else {
			floor -= 1
		}
		if floor == -1 {
			position = i + 1
			break
		}
	}
	fmt.Println(position)
}
