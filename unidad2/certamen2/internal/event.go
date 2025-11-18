package internal

import (
	"fmt"
	"time"
)

const (
	TipoEventoExterno = iota
	TipoEventoInterno
)

type Event struct {
	Tipo      int
	Timestamp time.Time
}

func NewEvent(tipo int) *Event {
	return &Event{
		Tipo:      tipo,
		Timestamp: time.Now(),
	}
}

func (e *Event) String() string {
	tipo := "Sin tipo"
	if e.Tipo == TipoEventoExterno {
		tipo = "Externo"
	} else {
		tipo = "Interno"
	}

	return fmt.Sprintf("[Evento] Tipo: %s, Timestamp: %s", tipo, e.Timestamp)
}
