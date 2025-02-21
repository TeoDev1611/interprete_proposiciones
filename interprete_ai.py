import os
import itertools
import re
import json
import pandas as pd
from dotenv import load_dotenv
from google import genai
from sympy import Symbol, sympify


# Función para interpretar y convertir la proposición de lenguaje natural a lógica simbólica
def interpretar_proposicion_lenguaje_natural(proposicion):
    # Crear Cliente GEMINI
    client = genai.Client(api_key=os.getenv("GEMINI_KEY"))
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Convierte esta proposición lógica en lenguaje natural a lógica formal, usando conectores lógicos: {proposicion}. Devuelve la expresión lógica en formato simbólico. Solo responde con la expresión lógica en formato simbólico y en el caso de que no sea una proposición responde Error",
    )
    return response.text.strip()


def generar_tabla_verdad(expresion_str, formato="dataframe"):
    """
    Genera una tabla de verdad para una expresión lógica.

    Args:
        expresion_str: Expresión lógica en notación simbólica
        formato: Formato de salida ('dataframe', 'dict', 'json')

    Returns:
        Tabla de verdad en el formato especificado
    """
    try:
        # Traducir operadores lógicos a formato SymPy
        expr_sympy = expresion_str.replace("¬", "~")
        expr_sympy = expr_sympy.replace("∧", "&")
        expr_sympy = expr_sympy.replace("∨", "|")
        expr_sympy = expr_sympy.replace("→", ">>")
        expr_sympy = expr_sympy.replace("↔", "==")

        # Detectar automáticamente los símbolos proposicionales
        simbolos_encontrados = set(re.findall(r"([a-zA-Z])", expr_sympy))

        # Crear símbolos SymPy para cada símbolo encontrado
        simbolos_dict = {}
        for s in simbolos_encontrados:
            simbolos_dict[s] = Symbol(s)
            # Definir símbolos en el namespace global
            globals()[s] = simbolos_dict[s]

        # Evaluar la expresión
        expresion = sympify(expr_sympy)

        # Obtener los símbolos ordenados
        simbolos = sorted(expresion.free_symbols, key=lambda x: str(x))

        # Generar todas las combinaciones de valores de verdad
        combinaciones = list(itertools.product([False, True], repeat=len(simbolos)))

        # Crear tabla de verdad
        tabla = []
        for valores in combinaciones:
            asignacion = dict(zip(simbolos, valores))
            resultado_sympy = expresion.subs(asignacion)

            # Convertir valores SymPy a booleanos nativos y luego a enteros
            # En SymPy: True -> BooleanTrue, False -> BooleanFalse
            resultado_bool = bool(
                resultado_sympy
            )  # Convertir a booleano nativo de Python

            # Crear fila con valores booleanos convertidos a enteros
            fila = {}
            for s, v in asignacion.items():
                fila[str(s)] = 1 if v else 0
            fila["resultado"] = 1 if resultado_bool else 0

            tabla.append(fila)

        # Convertir a DataFrame
        df = pd.DataFrame(tabla)

        # Ordenar columnas: primero símbolos, luego resultado
        simbolos_str = [str(s) for s in simbolos]
        columnas_ordenadas = simbolos_str + ["resultado"]
        if not df.empty and all(col in df.columns for col in columnas_ordenadas):
            df = df[columnas_ordenadas]

        # Devolver en el formato solicitado
        if formato == "dataframe":
            return df
        elif formato == "dict":
            return df.to_dict(orient="records")
        elif formato == "json":
            return json.dumps(
                {
                    "expresion": expresion_str,
                    "simbolos": simbolos_str,
                    "filas": df.to_dict(orient="records"),
                },
                ensure_ascii=False,
            )
        else:
            raise ValueError(f"Formato desconocido: {formato}")

    except Exception as e:
        error_msg = f"Error al procesar la expresión: {str(e)}"
        if formato == "json":
            return json.dumps({"error": error_msg})
        return error_msg
