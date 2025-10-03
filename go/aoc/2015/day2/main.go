package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	data, err := os.ReadFile("input")
	if err != nil {
		panic(err)
	}
	str := string(data)
	lines := strings.Split(strings.TrimSpace(str), "\n")
	total := first(lines)
	fmt.Println(total)
	total = second(lines)
	fmt.Println(total)
}

func first(lines []string) int {
	total := 0
	for _, ch := range lines {
		data := strings.Split(ch, "x")
		l, _ := strconv.Atoi(data[0])
		w, _ := strconv.Atoi(data[1])
		h, _ := strconv.Atoi(data[2])
		side1 := l * w
		side2 := w * h
		side3 := h * l
		smallest := min(side1, side2, side3)
		total += 2*side1 + 2*side2 + 2*side3 + smallest
	}
	return total
}

func second(lines []string) int {
	total := 0
	for _, ch := range lines {
		data := strings.Split(ch, "x")
		l, _ := strconv.Atoi(data[0])
		w, _ := strconv.Atoi(data[1])
		h, _ := strconv.Atoi(data[2])
		side1 := l + w
		side2 := w + h
		side3 := h + l
		smallest := min(side1, side2, side3)
		smallest *= 2
		volume := l * w * h
		total += volume + smallest
	}
	return total
}
