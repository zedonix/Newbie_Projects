package add

import (
	"encoding/csv"
	"fmt"
	"os"
	"strconv"
	"time"

	"github.com/olekukonko/tablewriter"
)

const path = "data/data.csv"

func List() {
	_, err := os.Stat(path)
	fileExists := err == nil
	if !fileExists {
		fmt.Println("No records, Use todo add to add a new todo")
		return
	}
	file, err := os.Open(path)
	if err != nil {
		panic(err)
	}
	defer file.Close()
	reader := csv.NewReader(file)
	records, err := reader.ReadAll()
	if err != nil {
		panic(err)
	}
	if len(records) == 1 {
		fmt.Println("No records")
	} else {
		table := tablewriter.NewWriter(os.Stdout)
		table.Header(records[0])
		table.Bulk(records[1:])
		table.Render()
	}
}

func Add(record []string) {
	_, err := os.Stat(path)
	fileExists := err == nil
	file, err := os.OpenFile(path, os.O_RDWR|os.O_CREATE, 0o644)
	if err != nil {
		panic(err)
	}

	defer file.Close()
	writer := csv.NewWriter(file)
	reader := csv.NewReader(file)
	defer writer.Flush()

	now := time.Now()
	id := 1
	if fileExists {
		records, err := reader.ReadAll()
		if err != nil {
			panic(err)
		}
		idPrev := 0
		if len(records) != 1 {
			idPrev, err = strconv.Atoi(records[len(records)-1][0])
			if err != nil {
				panic(err)
			}
		}
		id = idPrev + 1
	} else {
		head := []string{"ID", "Discription", "Created on", "Completed"}
		writer.Write(head)
	}

	record = append([]string{strconv.Itoa(id)}, record...)
	record = append(record, now.Format("2006-01-02 15:04"))
	record = append(record, "false")
	writer.Write(record)
	fmt.Println("Added")
}

func Delete(id []string) {
	file, err := os.Open(path)
	if err != nil {
		panic(err)
	}
	reader := csv.NewReader(file)
	data, err := reader.ReadAll()
	file.Close()
	if err != nil {
		panic(err)
	}
	done := false
	for i, records := range data {
		if records[0] == id[0] {
			done = true
			data = append(data[:i], data[i+1:]...)
			break
		}
	}
	if !done {
		fmt.Println("No such id")
		return
	}
	file, err = os.OpenFile(path, os.O_WRONLY|os.O_TRUNC, 0o644)
	writer := csv.NewWriter(file)
	defer writer.Flush()
	writer.WriteAll(data)
	fmt.Println("Deleted todo")
	file.Close()
}

func Complete(id []string) {
	file, err := os.Open(path)
	if err != nil {
		panic(err)
	}
	reader := csv.NewReader(file)
	data, err := reader.ReadAll()
	file.Close()
	if err != nil {
		panic(err)
	}
	done := false
	for i, records := range data {
		if records[0] == id[0] {
			done = true
			addMe := data[i]
			if addMe[3] == "true" {
				fmt.Println("Already Marked as complete")
				return
			} else {
				addMe[3] = "true"
			}
			data = append(data[:i], data[i+1:]...)
			data = append(data, addMe)
			break
		}
	}
	if !done {
		fmt.Println("No such id")
		return
	}
	file, err = os.OpenFile(path, os.O_WRONLY|os.O_TRUNC, 0o644)
	writer := csv.NewWriter(file)
	defer writer.Flush()
	writer.WriteAll(data)
	fmt.Println("Marked as Complete")
	file.Close()
}
