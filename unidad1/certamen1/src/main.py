from src.lexer import lexer
from src.parser import parser, ParseError
from src.analizador_semantico import AnalizadorSemantico, ErrorSemantico
from src.simulador import Simulador
import json
import sys
import argparse


def mostrar_ast(ast):
    print("=" * 60)
    print("ÁRBOL DE SINTAXIS ABSTRACTA (MOSTRAR_AST)")
    print("=" * 60)
    print(json.dumps(ast, indent=4, ensure_ascii=False))


def mostrar_errores_warnings(errores, warnings, mostrar_warnings):
    if errores:
        print(f"\n{len(errores)} error(es) encontrado(s):")
        for error in errores:
            print(f"\t- {error}")

    if warnings and mostrar_warnings:
        print(f"\n{len(warnings)} warning(s):")
        for warning in warnings:
            print(f"\t - {warning}")


def main(
    ruta_archivo, mostrar_ast_flag, mostrar_tabla, mostrar_logs, mostrar_warnings
) -> None:
    with open(ruta_archivo, "r", encoding="utf-8") as file:
        contenido = file.read()

    try:
        ast = parser.parse(contenido, lexer=lexer)
        analizador = AnalizadorSemantico()
        analizador.analizar(ast)
    except ParseError as e:
        print(e)
        sys.exit(2)
    except ErrorSemantico as e:
        print(e)
        sys.exit(20)

    if mostrar_ast_flag:
        mostrar_ast(ast)

    if mostrar_tabla:
        print(analizador.tabla_simbolos)

    mostrar_errores_warnings(analizador.errores, analizador.warnings, mostrar_warnings)

    if analizador.errores:
        sys.exit(1)

    if mostrar_logs:
        print("\nTURNOS")
        print("=" * 50)

    simulador = Simulador(ast, mostrar_logs)
    reporte = simulador.simular()
    print(reporte)


def parse_args():
    parser_arg = argparse.ArgumentParser(prog="python -m src.main")
    parser_arg.add_argument("ruta_archivo", help="ruta al archivo de comandos (.txt)")
    parser_arg.add_argument(
        "--ast", action="store_true", help="Mostrar el Árbol de Sintaxis Abstracta"
    )
    parser_arg.add_argument(
        "--tabla", action="store_true", help="Mostrar la tabla de símbolos"
    )
    parser_arg.add_argument(
        "--no_logs", action="store_true", help="Desactivar logs de turnos"
    )
    parser_arg.add_argument(
        "--no_warnings", action="store_true", help="Desactivar warnings"
    )
    return parser_arg.parse_args()


if __name__ == "__main__":
    args = parse_args()
    mostrar_logs = not args.no_logs
    mostrar_warnings = not args.no_warnings
    main(args.ruta_archivo, args.ast, args.tabla, mostrar_logs, mostrar_warnings)
