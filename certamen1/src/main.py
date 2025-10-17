from src.lexer import lexer
from src.parser import parser
from src.analizador_semantico import AnalizadorSemantico
from src.simulador import Simulador
import json
import sys

MOSTRAR_AST = "--ast" in sys.argv
MOSTRAR_TABLA = "--tabla" in sys.argv
MOSTRAR_LOGS = "--no_logs" not in sys.argv


def mostrar_ast(ast):
    print("=" * 60)
    print("ÁRBOL DE SINTAXIS ABSTRACTA (MOSTRAR_AST)")
    print("=" * 60)
    print(json.dumps(ast, indent=2, ensure_ascii=False))
    print()


def mostrar_errores_warnings(errores, warnings):
    if errores:
        print(f"\n{len(errores)} error(es) encontrado(s):")
        for error in errores:
            print(f"\t- {error}")

    if warnings:
        print(f"\n{len(warnings)} warning(s):")
        for warning in warnings:
            print(f"\t - {warning}")


def main(ruta_archivo: str) -> None:
    with open(ruta_archivo, "r", encoding="utf-8") as file:
        contenido = file.read()

    ast = parser.parse(contenido, lexer=lexer)
    if not ast:
        print("ERROR: Análisis sintáctico falló")
        exit(1)

    if MOSTRAR_AST:
        mostrar_ast(ast)

    analizador = AnalizadorSemantico()
    analizador.analizar(ast)

    if MOSTRAR_TABLA:
        print(analizador.tabla_simbolos)

    mostrar_errores_warnings(analizador.errores, analizador.warnings)

    if analizador.errores:
        sys.exit(1)

    if MOSTRAR_LOGS:
        print("\nTURNOS")
        print("=" * 50)

    simulador = Simulador(ast, MOSTRAR_LOGS)
    reporte = simulador.simular()
    print(reporte)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python -m src.main <ruta_al_archivo_de_comandos.txt>", end="")
        print(" [--ast] [--tabla] [--no_logs]")
        print("\nOpciones:")
        print("  --ast       Mostrar el Árbol de Sintaxis Abstracta")
        print("  --tabla     Mostrar la tabla de símbolos")
        print("  --no_logs   Desactivar logs de turnos")
        sys.exit(1)
    main(sys.argv[1])
