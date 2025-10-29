package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"path/filepath"

	"github.com/rs/cors"
	_ "modernc.org/sqlite"
)

type CalcResponse struct {
	Error  string  `json:"error,omitempty"`
	Result float64 `json:"result,omitempty"`
}

type CalcRequest struct {
	Op string  `json:"op"`
	A  float64 `json:"a"`
	B  float64 `json:"b"`
}

type History struct {
	Id   string  `json:"id"`
	Ques string  `json:"ques"`
	Ans  float64 `json:"ans"`
}

func writeJson(w http.ResponseWriter, status int, v any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	if err := json.NewEncoder(w).Encode(v); err != nil {
		log.Println("json encode error:", err)
	}
}

func calcHandler(w http.ResponseWriter, r *http.Request, db *sql.DB) {
	if r.Method != http.MethodPost {
		writeJson(w, http.StatusMethodNotAllowed, CalcResponse{Error: "Only POST method allowed"})
		return
	}
	var req CalcRequest
	err := json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		writeJson(w, http.StatusBadRequest, CalcResponse{Error: "Invalid Json" + err.Error()})
		return
	}
	var res CalcResponse
	var ques string
	switch req.Op {
	case "+", "sum", "add":
		res.Result = req.A + req.B
		ques = fmt.Sprintf("%f + %f", req.A, req.B)
	case "-", "sub":
		res.Result = req.A - req.B
		ques = fmt.Sprintf("%f - %f", req.A, req.B)
	case "*", "mul", "x", "X":
		res.Result = req.A * req.B
		ques = fmt.Sprintf("%f * %f", req.A, req.B)
	case "/", "div":
		if req.B == 0 {
			writeJson(w, http.StatusBadRequest, CalcResponse{Error: "Division by zero"})
			return
		}
		res.Result = req.A / req.B
		ques = fmt.Sprintf("%f / %f", req.A, req.B)
	default:
		writeJson(w, http.StatusBadRequest, CalcResponse{Error: "unsupported op; use add, sub, mul, div"})
		return
	}
	writeJson(w, http.StatusOK, res)

	_, err = db.Exec("INSERT INTO history(ques,ans) VALUES(?,?)", ques, res.Result)
	if err != nil {
		log.Fatal(err)
	}
}

func historyHandler(w http.ResponseWriter, r *http.Request, db *sql.DB) {
	rows, err := db.Query("SELECT * FROM history ORDER BY id DESC")
	if err != nil {
		log.Fatal(err)
		http.Error(w, err.Error(), 500)
		return
	}
	var history []History
	defer rows.Close()
	for rows.Next() {
		var h History
		if err := rows.Scan(&h.Id, &h.Ques, &h.Ans); err != nil {
			http.Error(w, err.Error(), 500)
			log.Fatal(err)
			return
		}
		history = append(history, h)
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(history)
}

func create(path string) (*sql.DB, error) {
	abs, err := filepath.Abs(path)
	if err != nil {
		log.Fatal(err)
	}
	flags := "file:" + abs + "?cache=shared&_pragma=journal_mode(WAL)&_busy_timeout=5000"
	db, err := sql.Open("sqlite", flags)
	if err != nil {
		log.Fatal(err)
	}
	db.SetMaxOpenConns(1)
	_, err = db.Exec(`
	CREATE TABLE IF NOT EXISTS history (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		ques REAL NOT NULL,
		ans REAL NOT NULL
	);`)
	if err != nil {
		log.Fatal(err)
	}
	return db, db.Ping()
}

func main() {
	db, err := create("calc.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()
	mux := http.NewServeMux()
	mux.HandleFunc("/calc", func(w http.ResponseWriter, r *http.Request) {
		calcHandler(w, r, db)
	})
	mux.HandleFunc("/hist", func(w http.ResponseWriter, r *http.Request) {
		historyHandler(w, r, db)
	})
	log.Println("server listening on :8080")
	handler := cors.Default().Handler(mux)
	log.Fatal(http.ListenAndServe(":8080", handler))
}

// history function to show the history
// change that ques cuz its doing sum,add ,
