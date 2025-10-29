from src.tabla_simbolos import TablaSimbolos


class ErrorSemantico(Exception):
    pass


class AnalizadorSemantico:
    def __init__(self) -> None:
        self.warnings = []
        self.tabla_simbolos = TablaSimbolos()

    def analizar(self, ast):
        self.errores = []
        self.warnings = []
        self.tabla_simbolos = TablaSimbolos()

        luchadores = ast.get("luchadores")

        for luchador in luchadores:
            self._construir_tabla(luchador)

        for luchador in luchadores:
            self._validar_luchador(luchador)

    def _construir_tabla(self, luchador):
        luchador_nombre = luchador.get("nombre")

        self.tabla_simbolos.insertar(luchador_nombre, "luchador")
        self.tabla_simbolos.scope_entrar(luchador_nombre)

        for _, lista_acciones in luchador.get("acciones", {}).items():
            for accion in lista_acciones:
                accion_nombre = accion.get("nombre")
                self.tabla_simbolos.insertar(accion_nombre, "accion")

        for combo in luchador.get("combos", []):
            combo_nombre = combo.get("nombre")
            self.tabla_simbolos.insertar(combo_nombre, "combo")

        self.tabla_simbolos.scope_salir()

    def _validar_luchador(self, luchador):
        luchador_nombre = luchador.get("nombre")

        self.tabla_simbolos.scope_actual = luchador_nombre

        self._validar_stats(luchador.get("stats", {}), luchador_nombre)
        acciones = self._validar_acciones(luchador.get("acciones", {}), luchador_nombre)
        self._validar_combos(luchador.get("combos", {}), acciones, luchador_nombre)

        self.tabla_simbolos.scope_salir()

    def _validar_stats(self, stats, luchador_nombre):
        if "hp" not in stats:
            self._levantar_excepcion_error(
                f"({luchador_nombre}): Falta el parámetro 'hp' en stats"
            )
        elif stats["hp"] <= 0:
            self._levantar_excepcion_error(
                f"({luchador_nombre}): 'hp' debe ser un número positivo, actual: {stats['hp']}"
            )

        if "st" not in stats:
            self._levantar_excepcion_error(
                f"({luchador_nombre}): Falta el parámetro 'st' en stats"
            )
        elif stats["st"] <= 0:
            self._levantar_excepcion_error(
                f"({luchador_nombre}): 'st' debe ser un número positivo, actual: {stats['st']}"
            )

    def _validar_acciones(self, acciones, luchador_nombre):
        acciones_dict = {}

        for tipo_accion, lista_acciones in acciones.items():
            for accion in lista_acciones:
                accion_nombre = accion.get("nombre")
                config = accion.get("config", {})

                if accion_nombre in acciones_dict:
                    self._levantar_excepcion_error(
                        f"({luchador_nombre}): Acción duplicada: '{accion_nombre}'"
                    )

                if tipo_accion == "bloqueo":
                    if config:
                        self._levantar_excepcion_error(
                            f"({luchador_nombre}): Bloqueo '{accion_nombre}' no debe llevar configuración"
                        )
                else:
                    NUMERO_ACCIONES_CONFIG = 5
                    if len(config) != NUMERO_ACCIONES_CONFIG:
                        self._levantar_excepcion_error(
                            f"({luchador_nombre}): '{accion_nombre}' debe tener {NUMERO_ACCIONES_CONFIG} configuraciones"
                        )

                    self._validar_parametros_accion(
                        config, accion_nombre, luchador_nombre
                    )

                acciones_dict[accion_nombre] = {
                    "tipo": tipo_accion,
                    "config": config,
                }

        return acciones_dict

    def _validar_parametros_accion(self, config, accion_nombre, luchador_nombre):
        parametros_obligatorios = [
            "daño",
            "costo",
            "altura",
            "forma",
            "giratoria",
        ]

        for parametro in parametros_obligatorios:
            if parametro not in config:
                self._levantar_excepcion_error(
                    f"({luchador_nombre}): Acción '{accion_nombre}' no tiene el parámetro: '{parametro}'"
                )

        if config["daño"] <= 0:
            self._levantar_excepcion_error(
                f"({luchador_nombre}): 'daño' debe ser un número positivo, actual: {config['daño']}"
            )

        if config["costo"] <= 0:
            self._levantar_excepcion_error(
                f"({luchador_nombre}): 'costo' debe ser un número positivo, actual: {config['costo']}"
            )

    def _validar_combos(self, combos, acciones_dict, luchador_nombre):
        nombres_combos = set()

        for combo in combos:
            nombre_combo = combo.get("nombre")
            st_req = combo.get("st_req")
            acciones = combo.get("acciones")

            if nombre_combo in nombres_combos:
                self._levantar_excepcion_error(
                    f"({luchador_nombre}): Combo duplicado: '{nombre_combo}'"
                )
            nombres_combos.add(nombre_combo)

            if st_req <= 0:
                self._levantar_excepcion_error(
                    f"({luchador_nombre}): 'st_req' debe ser un número positivo, actual: {st_req}"
                )

            costo_total = 0
            for accion_nombre in acciones:
                simbolo = self.tabla_simbolos.buscar(accion_nombre, luchador_nombre)

                if not simbolo:
                    self._levantar_excepcion_error(
                        f"({luchador_nombre}): Combo '{nombre_combo}': "
                        f"acción '{accion_nombre}' no existe"
                    )
                elif accion_nombre in acciones_dict:
                    accion_info = acciones_dict[accion_nombre]
                    if accion_info["tipo"] == "bloqueo":
                        self._levantar_excepcion_error(
                            f"({luchador_nombre}): Combo '{nombre_combo}': "
                            f"no puede incluir bloqueos ('{accion_nombre}')"
                        )
                    else:
                        costo_total += accion_info["config"].get("costo")

            if costo_total != st_req:
                self._agregar_warning(
                    f"({luchador_nombre}): Combo '{nombre_combo}': "
                    f"costo total ({costo_total}) es diferente de st_req ({st_req})"
                )

    def _levantar_excepcion_error(self, mensaje):
        raise ErrorSemantico(f"[Error Semántico] {mensaje}")

    def _agregar_warning(self, mensaje):
        self.warnings.append(mensaje)
