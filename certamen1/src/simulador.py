from src.luchador import Luchador


class Simulador:
    def __init__(self, ast, logs_activos) -> None:
        self.ast = ast
        self.luchadores = {}
        self.config = {}
        self.turnos = None
        self.historial = []
        self.logs_activos = logs_activos

    def inicializar(self):
        self.config = self.ast["simulacion"]["config"]
        self.turnos = self.ast["simulacion"]["turnos"]

        luchadores_ast = self.ast.get("luchadores")

        for luchadores_data in luchadores_ast:
            luchador_nombre = luchadores_data.get("nombre")
            luchador_stats = luchadores_data.get("stats")

            acciones = {}
            acciones_ast = luchadores_data.get("acciones")

            for _, lista_acciones in acciones_ast.items():
                for accion in lista_acciones:
                    accion_nombre = accion.get("nombre")
                    accion_config = accion.get("config")

                    acciones[accion_nombre] = {
                        "daño": accion_config.get("daño", 0),
                        "costo": accion_config.get("costo", 0),
                        "altura": accion_config.get("altura", ""),
                        "forma": accion_config.get("forma", ""),
                        "giratoria": accion_config.get("giratoria", False),
                    }

            combos = {}
            combos_ast = luchadores_data.get("combos")

            for combo in combos_ast:
                combo_nombre = combo.get("nombre")
                combo_st_req = combo.get("st_req")
                combo_acciones = combo.get("acciones")

                daño_total = sum(
                    acciones.get(acc, {}).get("daño", 0) for acc in combo_acciones
                )

                combos[combo_nombre] = {
                    "st_req": combo_st_req,
                    "acciones": combo_acciones,
                    "daño_total": daño_total,
                }

            luchador = Luchador(
                nombre=luchador_nombre,
                acciones=acciones,
                combos=combos,
                hp=luchador_stats.get("hp"),
                st=luchador_stats.get("st"),
            )

            self.luchadores[luchador_nombre] = luchador

    def simular(self):
        self.inicializar()

        luchador_inicial = self.config["inicia"]
        luchador1_nombre = self.config["luchador1"]
        luchador2_nombre = self.config["luchador2"]

        luchador1 = self.luchadores[luchador1_nombre]
        luchador2 = self.luchadores[luchador2_nombre]

        luchador_actual = None
        turno_actual = 0
        while (
            turno_actual < self.config["turnos_max"]
            and luchador1.esta_vivo()
            and luchador2.esta_vivo()
        ):
            if turno_actual == 0:
                if luchador_inicial == luchador1_nombre:
                    luchador_actual = luchador1
                    oponente = luchador2
                else:
                    luchador_actual = luchador2
                    oponente = luchador1
            else:
                if luchador_actual == luchador1:
                    luchador_actual = luchador2
                    oponente = luchador1
                else:
                    luchador_actual = luchador1
                    oponente = luchador2

            self.log(f"\n TURNO {turno_actual + 1} - {luchador_actual.nombre}")

            self.ejecutar_turno(luchador_actual, oponente)

            self.log(f"Estado: {luchador1}")
            self.log(f"Estado: {luchador2}")

            turno_actual += 1

        return self.generar_resumen()

    def ejecutar_turno(self, luchador_actual: Luchador, oponente: Luchador):
        if self.turnos is None:
            return

        instrucciones = self.turnos.get(luchador_actual.nombre)
        for instruccion in instrucciones:
            if not luchador_actual.esta_vivo() or not oponente.esta_vivo():
                break
            self.ejecutar_instruccion(instruccion, luchador_actual, oponente)

    def ejecutar_instruccion(
        self, instruccion, luchador_actual: Luchador, oponente: Luchador
    ):
        tipo = instruccion.get("tipo")

        if tipo == "usa":
            accion = instruccion.get("accion")
            if accion in luchador_actual.combos:
                luchador_actual.ejecutar_combo(accion, oponente)
            else:
                luchador_actual.ejecutar_accion(accion, oponente)
        elif tipo == "condicional":
            condicion = instruccion.get("condicion")
            bloque_si = instruccion.get("bloque_si")
            bloque_no = instruccion.get("bloque_no")

            if self.evaluar_condicion(condicion, luchador_actual, oponente):
                self.ejecutar_instruccion(bloque_si, luchador_actual, oponente)
            else:
                self.ejecutar_instruccion(bloque_no, luchador_actual, oponente)

    def evaluar_condicion(
        self, condicion, luchador_actual: Luchador, oponente: Luchador
    ):
        referencia = condicion["izquierda"]["entidad"]
        atributo = condicion["izquierda"]["atributo"]
        operador = condicion["operador"]
        valor_condicion = condicion["derecha"]

        valor_atributo = 0
        if referencia == "self":
            valor_atributo = getattr(luchador_actual, atributo)
        elif referencia == "oponente":
            valor_atributo = getattr(oponente, atributo)

        operadores = {
            ">": lambda a, b: a > b,
            "<": lambda a, b: a < b,
            ">=": lambda a, b: a >= b,
            "<=": lambda a, b: a <= b,
            "==": lambda a, b: a == b,
            "!=": lambda a, b: a != b,
        }

        return operadores[operador](valor_atributo, valor_condicion)

    def generar_resumen(self):
        resumen = []
        resumen.append("\n" + "=" * 50 + "\n")
        resumen.append("RESUMEN")

        resumen.append("\nConfiguración")
        resumen.append(f"  Luchador 1: {self.config['luchador1']}")
        resumen.append(f"  Luchador 2: {self.config['luchador2']}")
        resumen.append(f"  Inicia: {self.config['inicia']}")
        resumen.append(f"  Turnos máximos: {self.config['turnos_max']}")

        resumen.append("\nEstado Final De Luchadores")
        luchador1_nombre = self.config["luchador1"]
        luchador2_nombre = self.config["luchador2"]
        luchador1 = self.luchadores[luchador1_nombre]
        luchador2 = self.luchadores[luchador2_nombre]

        resumen.append(f"  {luchador1.nombre}:")
        resumen.append(f"    HP: {luchador1.hp}")
        resumen.append(f"    ST: {luchador1.st}")
        resumen.append(
            f"    Estado: {'Vivo' if luchador1.esta_vivo() else 'Derrotado'}"
        )

        resumen.append(f"  {luchador2.nombre}:")
        resumen.append(f"    HP: {luchador2.hp}")
        resumen.append(f"    ST: {luchador2.st}")
        resumen.append(
            f"    Estado: {'Vivo' if luchador2.esta_vivo() else 'Derrotado'}"
        )

        resumen.append("\nResultado")
        if luchador1.esta_vivo() and not luchador2.esta_vivo():
            ganador = luchador1.nombre
            resumen.append(f"  Ganador: {ganador}")
        elif not luchador1.esta_vivo() and luchador2.esta_vivo():
            ganador = luchador2.nombre
            resumen.append(f"  Ganador: {ganador}")
        else:
            if luchador1.hp > luchador2.hp:
                ganador = luchador1.nombre
                resumen.append(f"  Ganador por HP: {ganador}")
            elif luchador2.hp > luchador1.hp:
                ganador = luchador2.nombre
                resumen.append(f"  Ganado por HP: {ganador}")
            else:
                resumen.append("  Empate")

        return "\n".join(resumen)

    def log(self, mensaje):
        if self.logs_activos:
            print(mensaje)
        self.historial.append(mensaje)
