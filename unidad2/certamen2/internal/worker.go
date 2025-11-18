package internal

import (
	"fmt"
	"sync"
	"time"
)

type Worker struct {
	ID          int
	LVT         time.Time
	Historial   []*Event
	Checkpoints []time.Time

	mu     sync.Mutex
	logger *Logger
}

func NewWorker(id int, logger *Logger) *Worker {
	checkpoints := make([]time.Time, 0)
	initialTime := time.Unix(0, 0)
	checkpoints = append(checkpoints, initialTime)

	return &Worker{
		ID:          id,
		LVT:         initialTime,
		Historial:   make([]*Event, 0),
		Checkpoints: checkpoints,
		logger:      logger,
	}
}

func (w *Worker) Run(wg *sync.WaitGroup, ch <-chan *Event) {
	defer wg.Done()

	for evento := range ch {
		if evento.Tipo == TipoEventoExterno {
			w.logger.Log(
				fmt.Sprintf("Worker-%d", w.ID),
				w.LVT,
				"RecepcionExterno",
				fmt.Sprintf("Recibido (T_Evento: %s)", evento.Timestamp.Format(time.Kitchen)),
			)
		}
		w.RecibirEvento(evento)
	}
}

func (w *Worker) RecibirEvento(e *Event) {
	w.mu.Lock()
	defer w.mu.Unlock()

	if e.Tipo == TipoEventoExterno && e.Timestamp.Before(w.LVT) {
		checkpoints_LVT := w.buscarCheckpointAnterior(e.Timestamp)

		w.logger.Log(
			fmt.Sprintf("Worker-%d", w.ID),
			w.LVT,
			"RollbackInicio",
			fmt.Sprintf("Straggler (T=%s). Volviendo a LVT=%s", e.Timestamp.Format(time.Kitchen), checkpoints_LVT.Format(time.Kitchen)),
		)

		w.LVT = checkpoints_LVT

		historialValido := make([]*Event, 0)
		eventosAReprocesar := make([]*Event, 0)

		for _, ev := range w.Historial {
			if !ev.Timestamp.After(w.LVT) {
				historialValido = append(historialValido, ev)
			} else if ev.Timestamp.Before(e.Timestamp) {
				eventosAReprocesar = append(eventosAReprocesar, ev)
			}
		}

		for _, ev := range eventosAReprocesar {
			w.ProcesarEvento(ev)
			eventosInternos := w.generarEventosInternos(ev)
			for _, interno := range eventosInternos {
				w.ProcesarEvento(interno)
			}
		}

		w.logger.Log(
			fmt.Sprintf("Worker-%d", w.ID),
			w.LVT,
			"RollbackFin",
			"ReprocesamientoFinalizado",
		)

		w.Historial = append(historialValido, eventosAReprocesar...)
		w.podarCheckpoints(checkpoints_LVT)

	}

	if e.Tipo == TipoEventoExterno {
		w.logger.Log(
			fmt.Sprintf("Worker-%d", w.ID),
			w.LVT,
			"Checkpoint",
			fmt.Sprintf("Checkpoint creado en T=%s", w.LVT.Format(time.Kitchen)),
		)

		w.Checkpoints = append(w.Checkpoints, w.LVT)
		w.Historial = append(w.Historial, e)
	}

	w.ProcesarEvento(e)

	if e.Tipo == TipoEventoExterno {
		eventosInternos := w.generarEventosInternos(e)
		for _, interno := range eventosInternos {
			w.logger.Log(
				fmt.Sprintf("Worker-%d", w.ID),
				w.LVT,
				"ProcesoInterno",
				fmt.Sprintf("Procesando evento interno (T=%s)", interno.Timestamp.Format(time.Kitchen)),
			)

			w.ProcesarEvento(interno)
		}
	}
}

func (w *Worker) buscarCheckpointAnterior(timestamp time.Time) time.Time {
	var checkpoint time.Time
	for _, chk := range w.Checkpoints {
		if chk.Before(timestamp) {
			checkpoint = chk
		} else {
			break
		}
	}
	return checkpoint
}

func (w *Worker) podarCheckpoints(timestamp time.Time) {
	var idx = -1
	for i, chk := range w.Checkpoints {
		if !chk.After(timestamp) {
			idx = i
		} else {
			break
		}
	}
	w.Checkpoints = w.Checkpoints[:idx+1]
}

func (w *Worker) ProcesarEvento(e *Event) {
	if e.Timestamp.After(w.LVT) {
		w.LVT = e.Timestamp
	}
}

func (w *Worker) generarEventosInternos(e *Event) []*Event {
	listaInternos := make([]*Event, 0)
	tiempoInterno1 := e.Timestamp.Add(15 * time.Second)
	listaInternos = append(listaInternos, &Event{
		Tipo:      TipoEventoInterno,
		Timestamp: tiempoInterno1,
	})
	return listaInternos
}
