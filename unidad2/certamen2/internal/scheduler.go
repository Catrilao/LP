package internal

import (
	"fmt"
	"math/rand"
	"sync"
	"time"
)

type Scheduler struct {
	LVT         time.Time
	workers     []chan<- *Event
	rand        *rand.Rand
	totalEvents int
	logger      *Logger
}

func NewScheduler(workerChans []chan<- *Event, totalEvents int, logger *Logger) *Scheduler {
	source := rand.NewSource(time.Now().UnixNano())

	return &Scheduler{
		LVT:         time.Unix(0, 0),
		workers:     workerChans,
		rand:        rand.New(source),
		totalEvents: totalEvents,
		logger:      logger,
	}
}

func (s *Scheduler) Run(wg *sync.WaitGroup) {
	defer wg.Done()

	for i := 0; i < s.totalEvents; i++ {
		incremento := time.Duration(s.rand.Intn(10)+1) * time.Second
		nuevoTimestamp := s.LVT.Add(incremento)

		s.LVT = nuevoTimestamp

		evento := &Event{
			Tipo:      TipoEventoExterno,
			Timestamp: nuevoTimestamp,
		}

		workerIndex := s.rand.Intn(len(s.workers))
		canalDestino := s.workers[workerIndex]

		s.logger.Log(
			"Scheduler",
			s.LVT,
			"EnvioExterno",
			fmt.Sprintf("Enviando a Worker %d (T_Evento: %s)", workerIndex, evento.Timestamp.Format(time.Kitchen)),
		)

		canalDestino <- evento
	}

	for _, ch := range s.workers {
		close(ch)
	}
}
