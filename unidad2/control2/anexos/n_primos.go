package anexos

import "context"

// EncontrarPrimos busca todos los números primos hasta un entero max.
// Utiliza un enfoque de prueba por división, cuya complejidad es alta (aprox. O(n^1.5)).
func EncontrarPrimos(ctx context.Context, max int) []int {
	var primes []int
	for i := 2; i < max; i++ {
		if ctx.Err() != nil {
			return primes
		}

		isPrime := true
		for j := 2; j*j <= i; j++ {
			if i%j == 0 {
				isPrime = false
				break
			}
		}
		if isPrime {
			primes = append(primes, i)
		}
	}
	return primes
}
