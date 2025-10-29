package anexos

import (
	"context"
	"crypto/sha256"
	"fmt"
	"strings"
)

// SimularProofOfWork simula la búsqueda de una prueba de trabajo de blockchain.
// La dificultad determina el número de ceros iniciales que debe tener el hash.
// La complejidad crece exponencialmente con la dificultad.
// Para un computador personal, dificultad 5-6 suele tardar unos segundos.
func SimularProofOfWork(ctx context.Context, blockData string, dificultad int) (string, int) {
	targetPrefix := strings.Repeat("0", dificultad)
	nonce := 0
	for {
		if ctx.Err() != nil {
			return "", 0
		}

		data := fmt.Sprintf("%s%d", blockData, nonce)
		hashBytes := sha256.Sum256([]byte(data))
		hashString := fmt.Sprintf("%x", hashBytes)

		if strings.HasPrefix(hashString, targetPrefix) {
			return hashString, nonce
		}
		nonce++
	}
}
