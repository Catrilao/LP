import re
import ply.lex as lex
import sys

keywords = {
    "simulacion": "SIMULACION",
    "config": "CONFIG",
    "luchadores": "LUCHADORES",
    "vs": "VS",
    "inicia": "INICIA",
    "turnos_max": "TURNOS_MAX",
    "pelea": "PELEA",
    "turno": "TURNO",
    "usa": "USA",
    "self": "SELF",
    "oponente": "OPONENTE",
    "luchador": "LUCHADOR",
    "stats": "STATS",
    "acciones": "ACCIONES",
    "combos": "COMBOS",
    "golpe": "GOLPE",
    "patada": "PATADA",
    "bloqueo": "BLOQUEO",
    "daño": "DANO",
    "costo": "COSTO",
    "altura": "ALTURA",
    "forma": "FORMA",
    "giratoria": "GIRATORIA",
    "frontal": "FRONTAL",
    "lateral": "LATERAL",
    "si": "SI",
    "no": "NO",
    "hp": "HP",
    "st": "ST",
    "st_req": "ST_REQ",
    "alta": "ALTA",
    "media": "MEDIA",
    "baja": "BAJA",
    "sino": "SINO",
}

tokens = [
    "ID",
    "NUMBER",
    "ILLAVE",  # {
    "DLLAVE",  # }
    "IPAREN",  # (
    "DPAREN",  # )
    "DOSPUN",  # :
    "PUNCOM",  # ;
    "IGUAL",  # =
    "COMA",  # ,
    "MENOR",  # <
    "MAYOR",  # >
    "COMP",  # ==
    "MAYIG",  # >=
    "MENIG",  # <=
    "DIST",  # !=
    "PUNTO",  # .
] + list(keywords.values())


# Ignorar espacios y tabulaciones
t_ignore = " \t"


# Ignorar comentarios
def t_COMMENT(t):
    r"//.*"
    pass


def t_ID(t):
    r"[a-zA-ZñÑ_][a-zA-ZñÑ_0-9]*"
    t.type = keywords.get(t.value.lower(), "ID")
    return t


def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t


# Regla para tener el número de línea
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


# Delimitadores
t_ILLAVE = r"\{"
t_DLLAVE = r"\}"
t_IPAREN = r"\("
t_DPAREN = r"\)"

# Comparaciones
t_DIST = r"!="
t_COMP = r"=="
t_MAYIG = r">="
t_MENIG = r"<="
t_MAYOR = r">"
t_MENOR = r"<"

# Separadores
t_DOSPUN = r":"
t_PUNCOM = r";"
t_IGUAL = r"="
t_COMA = r","

t_PUNTO = r"."


# Errores léxicos
def t_error(t):
    print(f"[Error Léxico] Carácter invalido {t.value[0]} en línea {t.lexer.lineno}")
    t.lexer.skip(1)


DEBUG_MODE = "--debug" in sys.argv
lexer = lex.lex(debug=DEBUG_MODE, reflags=re.UNICODE)

if __name__ == "__main__":
    test_input = """
    luchador Ryu {
        stats(hp=100, st=100);
        acciones {
            golpe:
                puño_ligero(daño=5, costo=3, altura=media, forma=frontal, giratoria=no),
                puño_fuerte(daño=10, costo=7, altura=media, forma=frontal, giratoria=no);
            patada:
                patada_baja(daño=6, costo=4, altura=baja, forma=frontal, giratoria=no);
            bloqueo:
                bloqueo_alto;
        }
        combos {
            Shoryuken(st_req=20) { puño_fuerte, puño_fuerte, puño_ligero }
            Hadouken(st_req=25) { puño_fuerte, puño_ligero }
        }
    }
    """
    lexer.input(test_input)
    for tok in lexer:
        print(tok)
