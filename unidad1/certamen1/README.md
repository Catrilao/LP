# Certamen 1

## Integrantes

- Fernanda Fuentes Pizarro – Fernanda.fuentesp@estudiantes.uv.cl
- Angel López Catrilao – angel.lopez@estudiantes.uv.cl

## Requisito

- instalar(`pip install ply`)

## Uso

```sh
python -m src.main <ruta_al_archivo_de_comandos.txt>
```

## Definición de un luchador:

Por cada luchador, se debe poder especificar:

<ol>
    <li>
    Nombre, Puntos de Vida (HP) y Energía (ST): Atributos base del arquetipo.
    </li>
    <li>
    Acciones Atómicas: Conjunto de movimientos básicos disponibles para el luchador.
    <ol type="a">
        <li> Para los golpes de puño y las patadas, se debe poder definir:
            <ul>
                <li>La altura del ataque (alta para la cabeza, media para el tronco, baja para las piernas)</li>
                <li>La forma (frontal o lateral)</li>
                <li>Si es giratoria o no</li>
                <li>Cada acción tendrá además un nombre, un daño y un costo de energía asociados.</li>
            </ul>
        </li>
        <li>El bloqueo se define de una única forma y no posee atributos adicionales más allá de su nombre</li>
    </ol>
    <li>
    Combos: Secuencias nombradas que agrupan varias acciones atómicas de tipo golpe. <br>
    Cada combo debe especificar la energía total (st_req) necesaria para su ejecución.
    </li>
</ol>

## Estrutura declaración

```
luchador <nombre_luchador> {
    stats(hp=<numero>, st=<numero>);
    acciones {
        <tipo_accion>: <nombre_accion>(<estadisticas>[]);
        golpe:
            puño_ligero(daño=5, costo=3, altura=media, forma=frontal, giratoria=no),
            puño_fuerte(daño=10, costo=7, altura=media, forma=frontal, giratoria=no);
        patada: patada_baja(daño=6, costo=4, altura=baja, forma=frontal, giratoria=no);
        bloqueo: bloqueo_alto;
    }
    combos {
        <nombre_combo>(st_req=<numero>) { <acciones>[] }
        Hadouken(st_req=25) { puño_fuerte, puño_ligero }
    }
}
```

## Ejemplo pelea

```
simulacion {
    config {
        luchadores: Ryu vs Ken;
        inicia: Ryu;
        turnos_max: 20;
    }
    pelea {
        turno Ryu {
            si (oponente.hp < 50) {
                usa Shoryuken; // Si falla por ST, usará puño_fuerte.
            } sino {
                usa puño_fuerte;
            }
            usa patada_baja;
        }
        turno Ken {
            usa patada_baja;
            si (self.st > 50) {
                usa Hadouken;
            } sino {
                usa puño_fuerte;
            }
        }
    }
}
```
