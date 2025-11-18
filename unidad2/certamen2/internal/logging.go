package internal

import (
	"encoding/json"
	"fmt"
	"io"
	"sync"
	"time"
)

type LogEntry struct {
	Timestamp time.Time `json:"timestamp"`
	HiloID    string    `json:"hilo_id"`
	LVT       time.Time `json:"lvt"`
	Evento    string    `json:"evento"`
	Mensaje   string    `json:"mensaje"`
}

type Logger struct {
	encoder *json.Encoder
	mu      sync.Mutex
}

func NewLogger(out io.Writer) *Logger {
	return &Logger{
		encoder: json.NewEncoder(out),
	}
}

func (l *Logger) Log(hiloID string, lvt time.Time, evento string, mensaje string) {
	entry := LogEntry{
		Timestamp: time.Now(),
		HiloID:    hiloID,
		LVT:       lvt,
		Evento:    evento,
		Mensaje:   mensaje,
	}

	l.mu.Lock()
	defer l.mu.Unlock()

	if err := l.encoder.Encode(entry); err != nil {
		fmt.Println("Error escribiendo log:", err)
	}
}
