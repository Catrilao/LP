package main

import (
	"context"
	"control2/anexos"
	"flag"
	"fmt"
	"os"
	"time"
)

func main() {
	n := flag.Int("n", 2500, "Es la dimensión de dos matrices que se multiplican.\nSe supone que la evaluación de la condición toma un tiempo considerable,\npor lo que su tiempo se simula de esta forma.")
	umbral := flag.Int("umbral", 5000000, "Valor utilizado para determinar si se ejecuta una u otra rama")
	secuencial := flag.Bool("secuencial", true, "Tipo de ejecución. Secuencial o Concurrente")
	nombreArchivo := flag.String("nombre_archivo", "./resultados/salida.txt", "nombre del archivo donde se registran las métricas de interés.")
	ramaGanadora := flag.String("rama_ganadora", "a", "Rama que se ejecutara siempre, a(n Primos), b(Proof of Work)")
	flag.Parse()

	// Se fuerza a que siempre se ejecute la función `EncontrarPrimos`
	switch *ramaGanadora {
	case "a":
		*umbral = -10
	case "b":
		*umbral = 1000000000
	}

	start := time.Now()
	if *secuencial {
		ctx := context.Background()
		ejecucionSecuencial(ctx, *n, *umbral)
	} else {
		ctx, cancel := context.WithCancel(context.Background())
		defer cancel()
		ejecucionEspeculativa(ctx, *n, *umbral)
	}
	elapsed := time.Since(start)

	f, err := os.OpenFile(*nombreArchivo, os.O_APPEND|os.O_CREATE, 0644)
	if err != nil {
		return
	}
	defer f.Close()

	fmt.Printf("El código tardo %dms", elapsed.Milliseconds())

	texto := fmt.Sprintf("%d\n", elapsed.Milliseconds())
	if _, err := f.WriteString(texto); err != nil {
		fmt.Printf("Error escribiendo archivo: %v\n", err)
	}
}

func ejecucionSecuencial(ctx context.Context, n int, umbral int) {
	fmt.Printf("Ejecución secuencial\n")

	traza := anexos.CalcularTrazaDeProductoDeMatrices(n)
	fmt.Printf("n: %d\n", n)

	if umbral <= traza {
		numPrimos := anexos.EncontrarPrimos(ctx, 5000000)
		fmt.Printf("Número de primos antes de 500000: %d\n", len(numPrimos))
	} else {
		hash, nonce := anexos.SimularProofOfWork(ctx, "qwerty", 5)
		fmt.Printf("Hash: %q, nonce: %d\n", hash, nonce)
	}
}

func ejecucionEspeculativa(ctx context.Context, n int, umbral int) {
	fmt.Printf("Ejecución NO secuencial\n")

	ctxPrimos, cancelPrimos := context.WithCancel(ctx)
	ctxPOW, cancelPOW := context.WithCancel(ctx)

	defer cancelPrimos()
	defer cancelPOW()

	primosCh := make(chan []int, 1)
	powCh := make(chan struct {
		hash  string
		nonce int
	}, 1)

	go func() {
		primos := anexos.EncontrarPrimos(ctxPrimos, 5000000)
		primosCh <- primos
	}()

	go func() {
		hash, nonce := anexos.SimularProofOfWork(ctxPOW, "qwerty", 5)
		powCh <- struct {
			hash  string
			nonce int
		}{hash, nonce}
	}()

	traza := anexos.CalcularTrazaDeProductoDeMatrices(n)
	fmt.Printf("n: %d\n", n)

	if umbral <= traza {
		cancelPOW()
		primos := <-primosCh
		fmt.Printf("Número de primos antes de 5000000: %d\n", len(primos))
	} else {
		res := <-powCh
		cancelPrimos()
		fmt.Printf("Hash: %q, nonce: %d\n", res.hash, res.nonce)
	}
}
