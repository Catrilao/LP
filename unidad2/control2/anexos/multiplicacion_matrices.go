package anexos

import "math/rand"

// CalcularTrazaDeProductoDeMatrices multiplica dos matrices NxN y devuelve la traza
// de la matriz resultante. La complejidad del cómputo es O(n^3).
func CalcularTrazaDeProductoDeMatrices(n int) int {
	// Se crean dos matrices con valores aleatorios para la multiplicación.
	m1 := make([][]int, n)
	m2 := make([][]int, n)
	for i := 0; i < n; i++ {
		m1[i] = make([]int, n)
		m2[i] = make([]int, n)
		for j := 0; j < n; j++ {
			m1[i][j] = rand.Intn(10)
			m2[i][j] = rand.Intn(10)
		}
	}
	// Se realiza la multiplicación y se calcula la traza en el proceso.
	trace := 0
	for i := 0; i < n; i++ {
		sum := 0
		for k := 0; k < n; k++ {
			sum += m1[i][k] * m2[k][i]
		}
		trace += sum
	}
	return trace
}
