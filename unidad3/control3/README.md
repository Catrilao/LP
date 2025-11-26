# Árbol Genealógico en Prolog

Este proyecto implementa un árbol genealógico en Prolog basado en la obra de J.R.R. Tolkien, específicamente la genealogía de los Edain (hombres) y medio-elfos.

## Descripción

El programa define relaciones familiares utilizando hechos y reglas en Prolog, permitiendo realizar consultas sobre parentescos, ancestros, descendientes y otras relaciones familiares.

## Requisitos

- SWI-Prolog (versión 8.0 o superior)
- Sistema operativo: Windows, Linux o macOS

### Instalación de SWI-Prolog

**Windows:**

- Descargar desde: https://www.swi-prolog.org/download/stable
- Ejecutar el instalador y seguir las instrucciones

**Linux:**

```bash
sudo apt-get install swi-prolog
```

**macOS:**

```bash
brew install swi-prolog
```

## Uso

```bash
# Iniciar SWI-Prolog con el archivo
swipl -s arbol.pl
```

## Consultas de Ejemplo

### 1. Consultar padres/madres

```prolog
?- padre(bregor, X).
% X = beor.

?- madre(luthien, X).
% X = dior.
```

### 2. Consultar hijos

```prolog
?- hijo(beren, X).
% X = barahir ;
% X = emeldir.
```

### 3. Consultar hermanos

```prolog
?- hermano(barahir, X).
% X = bregolas.

?- hermano(elrond, X).
% X = elros.
```

### 4. Consultar ancestros (recursivo)

```prolog
?- ancestro(X, elrond).
% X = earendil ;
% X = elwing ;
% X = tuor ;
% X = idril ;
% X = dior ;
% X = beren ;
% ... (todos los ancestros)
```

### 5. Consultar descendientes (recursivo)

```prolog
?- descendiente(X, bregor).
% X = beor ;
% X = barahir ;
% X = beren ;
% ... (todos los descendientes)
```

### 6. Consultar tíos/tías

```prolog
?- tio(X, beren).
% X = bregolas.

?- tia(X, elrond).
% (consulta tías de elrond)
```

### 7. Verificar relaciones específicas

```prolog
?- ancestro(bregor, elrond).
% true.

?- hermano(turin, nienor).
% true.
```

## Estructura de Datos

### Hechos Definidos

- **padre(X, Y)**: X es padre de Y
- **madre(X, Y)**: X es madre de Y

### Reglas Definidas

1. **hijo(X, Y)**: X es hijo de Y

   - Caso 1: Si Y es padre de X
   - Caso 2: Si Y es madre de X

2. **hermano(X, Y)**: X es hermano de Y

   - Comparten el mismo padre O la misma madre
   - X e Y son diferentes

3. **tio(X, Y)**: X es tío de Y

   - X es hermano del padre de Y
   - X es hermano de la madre de Y

4. **tia(X, Y)**: X es tía de Y

   - X es hermana del padre de Y
   - X es hermana de la madre de Y

5. **ancestro(X, Y)**: X es ancestro de Y (RECURSIVO)

   - Caso base: X es padre de Y
   - Caso base: X es madre de Y
   - Caso recursivo: X es padre/madre de alguien que es ancestro de Y

6. **descendiente(X, Y)**: X es descendiente de Y
   - Definido como: Y es ancestro de X

## Genealogía Implementada

```
Nivel 1: bregor
Nivel 2: beor
Nivel 3: barahir, bregolas
Nivel 4: beren, belegund, baragund
Nivel 5: dior, rian, morwen, turin, nienor
Nivel 6: elwing, tuor, earendil
Nivel 7: elrond, elros
```
