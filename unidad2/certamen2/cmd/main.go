package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"simulador/internal"
	"sync"
	"time"
)

func main() {
	numWorkers := flag.Int("num_workers", 4, "Número de hilos workers")
	totalEventosExternos := flag.Int("num_eventos_ext", 50, "Número de eventos externos que se generarán")
	archivoDestino := flag.String("destino", "simulacion.log", "Archivo de salida de los logs")

	flag.Usage = func() {
		fmt.Fprintf(os.Stderr, "Uso: simulador [opciones]\n")
		fmt.Fprintf(os.Stderr, "Opciones:\n")
		flag.PrintDefaults()
	}

	flag.Parse()
	inicio := time.Now()

	logFile, err := os.Create(*archivoDestino)
	if err != nil {
		log.Fatalf("Error al crear archivo de logs")
	}
	defer logFile.Close()

	logger := internal.NewLogger(logFile)

	var wg sync.WaitGroup

	workerChannels := make([]chan *internal.Event, *numWorkers)
	schedulerSendChans := make([]chan<- *internal.Event, *numWorkers)

	for i := 0; i < *numWorkers; i++ {
		ch := make(chan *internal.Event, 10)
		workerChannels[i] = ch
		schedulerSendChans[i] = ch
	}

	for i := 0; i < *numWorkers; i++ {
		workerInstance := internal.NewWorker(i, logger)
		wg.Add(1)
		go workerInstance.Run(&wg, workerChannels[i])
	}

	schedulerInstance := internal.NewScheduler(schedulerSendChans, *totalEventosExternos, logger)
	wg.Add(1)
	go schedulerInstance.Run(&wg)
	wg.Wait()
	duracion := time.Since(inicio)
	fmt.Printf("Tiempo total de simulación con %d workers: %v\n", *numWorkers, duracion)
}
