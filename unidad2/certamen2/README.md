## Uso

Crear ejecutable

```sh
go build -o simulador.exe cmd\main.go
```

Ejecutar simulación

```sh
simulador.exe [opciones]
```

### Opciones

- **-destino string**  
  Archivo de salida de los logs  
  _default:_ `"simulacion.log"`

- **-num_eventos_ext int**  
  Número de eventos externos que se generarán  
  _default:_ `50`

- **-num_workers int**  
  Número de hilos workers  
  _default:_ `4`
