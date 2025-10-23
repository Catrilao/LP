class Simbolo:
    def __init__(self, nombre, tipo, scope) -> None:
        self.nombre = nombre
        self.tipo = tipo
        self.scope = scope

    def __repr__(self) -> str:
        return f"Simbolo('{self.nombre}', tipo={self.tipo}, scope={self.scope})"


class TablaSimbolos:
    def __init__(self) -> None:
        self.tabla = {"global": {}}
        self.scope_actual = "global"
        self.pila_scopes = ["global"]
        self.errores = []

    def scope_entrar(self, nombre_scope) -> bool:
        if nombre_scope not in self.tabla:
            self.tabla[nombre_scope] = {}

        self.scope_actual = nombre_scope
        self.pila_scopes.append(nombre_scope)
        return True

    def scope_salir(self):
        if len(self.pila_scopes) <= 1:
            self.scope_actual = "global"
            return
        self.pila_scopes.pop()
        self.scope_actual = self.pila_scopes[-1]

    def insertar(self, nombre, tipo):
        if nombre in self.tabla[self.scope_actual]:
            self.errores.append(
                f"Símbolo '{nombre}' duplicado en scope '{self.scope_actual}' "
                f"(tipo: {self.tabla[self.scope_actual][nombre].tipo})"
            )
            return False

        simbolo = Simbolo(nombre, tipo, self.scope_actual)
        self.tabla[self.scope_actual][nombre] = simbolo
        return True

    def buscar(self, nombre: str, scope_busqueda=None):
        scope_busqueda = scope_busqueda or self.scope_actual

        if scope_busqueda in self.tabla:
            if nombre in self.tabla[scope_busqueda]:
                return self.tabla[scope_busqueda][nombre]

        if scope_busqueda != "global" and nombre in self.tabla["global"]:
            return self.tabla["global"][nombre]

        return None

    def existe(self, nombre, scope_busqueda=None):
        return self.buscar(nombre, scope_busqueda) is not None

    def __str__(self):
        result = []
        result.append("=" * 60)
        result.append("TABLA DE SÍMBOLOS")
        result.append("=" * 60)

        for scope, simbolos in self.tabla.items():
            if simbolos:
                result.append(f"\n[Scope: {scope}]")
                result.append("-" * 60)
                for nombre, simbolo in simbolos.items():
                    result.append(f"  {nombre:20} | tipo: {simbolo.tipo:10}")

        if self.errores:
            result.append("\n" + "=" * 60)
            result.append("ERRORES")
            result.append("=" * 60)
            for error in self.errores:
                result.append(f"\t- {error}")
        result.append("=" * 60)

        return "\n".join(result)
