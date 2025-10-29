from src.lexer import tokens  # noqa: F401 - Requerida por YACC
import ply.yacc as yacc
import sys


def p_inicio(p):
    """inicio : lista_luchadores simulacion_inicio"""
    p[0] = {
        "luchadores": p[1],
        "simulacion": p[2],
    }


def p_lista_luchadores(p):
    """lista_luchadores : lista_luchadores luchador_def
    | luchador_def"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_luchador_def(p):
    """luchador_def : LUCHADOR ID ILLAVE stats_def acciones_def combos_def DLLAVE"""
    p[0] = {
        "nombre": p[2],
        "stats": p[4],
        "acciones": p[5],
        "combos": p[6],
    }


def p_stats_def(p):
    """stats_def : STATS IPAREN stats_lista DPAREN PUNCOM"""
    p[0] = p[3]


def p_stats_lista(p):
    """stats_lista : stats_lista COMA stat
    | stat"""
    if len(p) == 4:
        p[0] = {**p[1], **p[3]}
    else:
        p[0] = p[1]


def p_stat(p):
    """stat : hp_def
    | st_def"""
    p[0] = {**p[1]}


def p_hp_def(p):
    """hp_def : HP IGUAL NUMBER"""
    p[0] = {"hp": p[3]}


def p_st_def(p):
    """st_def : ST IGUAL NUMBER"""
    p[0] = {"st": p[3]}


def p_acciones_def(p):
    """acciones_def : ACCIONES ILLAVE acciones_grupo DLLAVE"""
    p[0] = p[3]


def p_acciones_grupo(p):
    """acciones_grupo : acciones_grupo encabezado_acciones
    | encabezado_acciones"""
    if len(p) == 3:
        p[0] = {**p[1], **p[2]}
    else:
        p[0] = p[1]


def p_encabezado_acciones(p):
    """encabezado_acciones : accion_tipo DOSPUN acciones_subgrupo PUNCOM"""
    p[0] = {p[1]: p[3]}


def p_accion_tipo(p):
    """accion_tipo : GOLPE
    | PATADA
    | BLOQUEO"""
    p[0] = p[1]


def p_acciones_subgrupo(p):
    """acciones_subgrupo : acciones_subgrupo COMA accion
    | accion"""
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_accion_config(p):
    """accion : ID IPAREN config_lista DPAREN"""
    p[0] = {"nombre": p[1], "config": p[3]}


def p_bloqueo(p):
    """accion : ID"""
    p[0] = {"nombre": p[1], "config": {}}


def p_config_lista(p):
    """config_lista : config_lista COMA config_accion
    | config_accion"""
    if len(p) == 4:
        p[0] = {**p[1], **p[3]}
    else:
        p[0] = p[1]


def p_config_accion(p):
    """config_accion : dano_config
    | costo_config
    | altura_config
    | forma_config
    | giratoria_config"""
    p[0] = {**p[1]}


def p_dano_config(p):
    """dano_config : DANO IGUAL NUMBER"""
    p[0] = {"daño": p[3]}


def p_costo_config(p):
    """costo_config : COSTO IGUAL NUMBER"""
    p[0] = {"costo": p[3]}


def p_altura_config(p):
    """altura_config : ALTURA IGUAL tipo_altura"""
    p[0] = {"altura": p[3]}


def p_forma_config(p):
    """forma_config : FORMA IGUAL tipo_forma"""
    p[0] = {"forma": p[3]}


def p_giratoria_config(p):
    """giratoria_config : GIRATORIA IGUAL bool"""
    p[0] = {"giratoria": p[3]}


def p_tipo_altura(p):
    """tipo_altura : ALTA
    | MEDIA
    | BAJA"""
    p[0] = p[1]


def p_tipo_forma(p):
    """tipo_forma : FRONTAL
    | LATERAL"""
    p[0] = p[1]


def p_bool(p):
    """bool : SI
    | NO"""
    p[0] = p[1].upper() == "SI"


def p_combos_def(p):
    """combos_def : COMBOS ILLAVE combos_grupo DLLAVE"""
    p[0] = p[3]


def p_combos_grupo(p):
    """combos_grupo : combos_grupo combo
    | combo"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_combo(p):
    """combo : ID IPAREN ST_REQ IGUAL NUMBER DPAREN ILLAVE lista_acciones DLLAVE"""
    p[0] = {
        "nombre": p[1],
        "st_req": p[5],
        "acciones": p[8],
    }


def p_lista_acciones(p):
    """lista_acciones : lista_acciones COMA ID
    | ID"""
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_simulacion_inicio(p):
    """simulacion_inicio : SIMULACION ILLAVE config_simulacion turnos DLLAVE"""
    p[0] = {
        "config": p[3],
        "turnos": p[4],
    }


def p_config_simulacion(p):
    """config_simulacion : CONFIG ILLAVE LUCHADORES DOSPUN ID VS ID PUNCOM INICIA DOSPUN ID PUNCOM TURNOS_MAX DOSPUN NUMBER PUNCOM DLLAVE"""
    p[0] = {
        "luchador1": p[5],
        "luchador2": p[7],
        "inicia": p[11],
        "turnos_max": p[15],
    }


def p_turnos(p):
    """turnos : PELEA ILLAVE TURNO ID ILLAVE turno_luchador DLLAVE TURNO ID ILLAVE turno_luchador DLLAVE DLLAVE"""
    p[0] = {
        p[4]: p[6],
        p[9]: p[11],
    }


def p_turno_luchador(p):
    """turno_luchador : turno_luchador ataque
    | ataque"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_ataque(p):
    """ataque : ataque_condicional
    | ataque_directo"""
    p[0] = p[1]


def p_ataque_condicional(p):
    """ataque_condicional : SI IPAREN condicion DPAREN ILLAVE ataque_directo DLLAVE SINO ILLAVE ataque_directo DLLAVE"""
    p[0] = {
        "tipo": "condicional",
        "condicion": p[3],
        "bloque_si": p[6],
        "bloque_no": p[10],
    }


def p_ataque_directo(p):
    """ataque_directo : USA ID PUNCOM"""
    p[0] = {
        "tipo": "usa",
        "accion": p[2],
    }


def p_condicion(p):
    """condicion : atributo_condicional operador_logico NUMBER"""
    p[0] = {
        "izquierda": p[1],
        "operador": p[2],
        "derecha": p[3],
    }


def p_atributo_condicional(p):
    """atributo_condicional : SELF PUNTO atributo
    | OPONENTE PUNTO atributo"""
    p[0] = {
        "entidad": p[1],
        "atributo": p[3],
    }


def p_atributo(p):
    """atributo : HP
    | ST"""
    p[0] = p[1]


def p_operador_logico(p):
    """operador_logico : DIST
    | COMP
    | MAYIG
    | MENIG
    | MAYOR
    | MENOR
    """
    p[0] = p[1]


class ParseError(Exception):
    pass


def p_error(p):
    if p:
        msg = f"[Error Sintáctico] Token inesperado '{p.value}' (tipo: {p.type}) en línea {p.lineno}'"
    else:
        msg = "[Error Sintáctico] Fin de archivo inesperado"
    raise ParseError(msg)


DEBUG_MODE = "--debug" in sys.argv
parser = yacc.yacc(debug=DEBUG_MODE)
