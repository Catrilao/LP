from __future__ import annotations


class Luchador:
    def __init__(self, nombre, hp, st, acciones, combos, logs_activos) -> None:
        self.nombre = nombre
        self.hp_inicial = hp
        self.hp = hp
        self.st_inicial = st
        self.st = st
        self.acciones = acciones
        self.combos = combos
        self.logs_activos = logs_activos

    def esta_vivo(self):
        return self.hp > 0

    def ejecutar_accion(self, nombre_accion: str, oponente: Luchador) -> None:
        if nombre_accion not in self.acciones:
            self.log(f"Error. {self.nombre} no tiene {nombre_accion}.")

        costo_accion = self.acciones[nombre_accion]["costo"]
        daño_accion = self.acciones[nombre_accion]["daño"]

        if self.st < costo_accion:
            self.log(
                f"Error. {self.nombre} no tiene energia suficiente para {nombre_accion}."
            )

        self._gastar_energia(costo_accion)
        oponente._recibir_daño(daño_accion)

    def ejecutar_combo(self, nombre_combo: str, oponente: Luchador) -> None:
        if nombre_combo not in self.combos:
            self.log(f"Error. {self.nombre} no tiene el combo {nombre_combo}")
            return

        combo = self.combos[nombre_combo]
        combo_acciones = combo["acciones"]
        combo_costo = combo["st_req"]
        combo_daño = combo["daño_total"]

        for accion in combo_acciones:
            if accion not in self.acciones:
                self.log(f"Error. {accion} no existe en el combo {nombre_combo}")
                return

        if self.st < combo_costo:
            primera_accion = combo_acciones[0]
            self.log(
                f"Warning: Energía insuficiente para el combo {nombre_combo}\n"
                f"Ejecutando primera acción simple: {primera_accion}\n"
            )
            self.ejecutar_accion(primera_accion, oponente)
            return

        self.st = max(0, self.st - combo_costo)
        for accion in combo_acciones:
            oponente._recibir_daño(combo_daño)

    def _recibir_daño(self, cantidad: int) -> None:
        self.hp = max(0, self.hp - cantidad)

    def _gastar_energia(self, cantidad: int) -> None:
        self.st = max(0, self.st - cantidad)

    def __str__(self) -> str:
        return f"{self.nombre}: HP={self.hp}/{self.hp_inicial}. ST={self.st}/{self.st_inicial}"

    def log(self, mensaje):
        if self.logs_activos:
            print(mensaje)
