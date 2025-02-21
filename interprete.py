from itertools import (
    product,
)  # Importa la función product para generar combinaciones de valores
from typing import (
    Tuple,
    Union,
    Dict,
    List,
)  # Importa tipos para anotaciones de funciones


class InterpreteLógico:
    """
    Clase principal para el análisis y evaluación de proposiciones lógicas.

    Attributes:
        KEY_WORDS (dict): Diccionario de palabras clave y sus tipos de conectores
        LOGICAL_OPERATIONS (dict): Mapeo de tipos de conectores a símbolos lógicos
        NEGATIONS (list): Lista de palabras que indican negación
    """

    def __init__(self):
        """Inicializa el intérprete con sus diccionarios y listas de palabras clave."""

        # Palabras que indican negación
        self.NEGATIONS = [
            "no",
            "nunca",
            "jamás",
            "tampoco",
            "ni",
            "ningún",
            "ninguno",
            "nadie",
            "nada",
            "sin",
            "ni siquiera",
        ]

        # Diccionario de palabras clave y sus tipos
        self.KEY_WORDS = {
            # Conectores condicionales
            "si": "CONDICIONAL",
            "entonces": "CONDICIONAL",
            "siempre que": "CONDICIONAL",
            "a condición de que": "CONDICIONAL",
            # Conectores de conjunción
            "y": "CONJUNCIÓN",
            "además": "CONJUNCIÓN",
            "también": "CONJUNCIÓN",
            "ni": "CONJUNCIÓN",
            # Conectores de disyunción
            "o": "DISYUNCIÓN",
            "o bien": "DISYUNCIÓN",
            "ya sea": "DISYUNCIÓN",
            # Conectores adversativos
            "pero": "ADVERSATIVO",
            "sin embargo": "ADVERSATIVO",
            "no obstante": "ADVERSATIVO",
            "aunque": "ADVERSATIVO",
            # Conectores causales
            "porque": "CAUSAL",
            "puesto que": "CAUSAL",
            "ya que": "CAUSAL",
            "dado que": "CAUSAL",
            # Conectores consecutivos
            "por lo tanto": "CONSECUTIVO",
            "en consecuencia": "CONSECUTIVO",
            "por consiguiente": "CONSECUTIVO",
            "así que": "CONSECUTIVO",
            # Otros conectores
            "es decir": "EXPLICATIVO",
            "o sea": "EXPLICATIVO",
            "por ejemplo": "EJEMPLIFICATIVO",
        }

        # Mapeo de conectores a símbolos lógicos
        self.LOGICAL_OPERATIONS = {
            "CONDICIONAL": "→",
            "CONJUNCIÓN": "∧",
            "DISYUNCIÓN": "∨",
            "ADVERSATIVO": "∧",
            "CAUSAL": "→",
            "CONSECUTIVO": "→",
            "EXPLICATIVO": "↔",
            "EJEMPLIFICATIVO": "→",
        }

    def check_negation(self, proposition: str) -> Tuple[bool, str]:
        """
        Verifica si una proposición contiene una negación y la procesa.

        Args:
            proposition (str): La proposición a analizar

        Returns:
            Tuple[bool, str]: (tiene_negación, proposición_sin_negación)
        """
        proposition = (
            proposition.lower().strip()
        )  # Convierte la proposición a minúsculas y elimina espacios
        is_negated = False  # Inicializa la variable de negación

        for neg in self.NEGATIONS:  # Itera sobre las palabras de negación
            if proposition.startswith(
                neg + " "
            ):  # Verifica si la proposición comienza con una negación
                is_negated = True  # Marca que hay negación
                proposition = proposition[
                    len(neg) :
                ].strip()  # Elimina la negación de la proposición
            elif (
                f" {neg} " in proposition
            ):  # Verifica si hay una negación en medio de la proposición
                is_negated = True  # Marca que hay negación
                proposition = proposition.replace(
                    f" {neg} ", " "
                ).strip()  # Elimina la negación de la proposición

        return (
            is_negated,
            proposition,
        )  # Devuelve si hay negación y la proposición limpia

    def find_connector(self, text: str) -> Union[str, None]:
        """
        Encuentra el primer conector lógico en el texto.

        Args:
            text (str): El texto a analizar

        Returns:
            Union[str, None]: El conector encontrado o None
        """
        text = text.lower()  # Convierte el texto a minúsculas
        sorted_connectors = sorted(
            self.KEY_WORDS.keys(), key=len, reverse=True
        )  # Ordena los conectores por longitud

        for connector in sorted_connectors:  # Itera sobre los conectores ordenados
            if connector in text:  # Verifica si el conector está en el texto
                return connector  # Devuelve el conector encontrado
        return None  # Devuelve None si no se encuentra ningún conector

    def parse_proposition(self, text: str) -> Dict:
        """
        Analiza una proposición y extrae sus componentes.

        Args:
            text (str): La proposición a analizar

        Returns:
            Dict: Diccionario con los componentes de la proposición
        """
        text = text.lower().strip(
            "."
        )  # Convierte el texto a minúsculas y elimina el punto final
        connector = self.find_connector(text)  # Busca el conector en el texto

        if not connector:  # Si no se encuentra un conector
            is_negated, clean_text = self.check_negation(text)  # Verifica la negación
            return {
                "connector": None,  # No hay conector
                "connector_type": None,  # No hay tipo de conector
                "propositions": [text],  # La proposición limpia
                "symbol": None,  # No hay símbolo
                "negations": [is_negated],  # Lista de negaciones
            }

        connector_type = self.KEY_WORDS[connector]  # Obtiene el tipo de conector
        logical_symbol = self.LOGICAL_OPERATIONS[
            connector_type
        ]  # Obtiene el símbolo lógico

        parts = text.split(connector)  # Divide el texto en partes usando el conector
        propositions = []  # Lista para almacenar las proposiciones
        negations = []  # Lista para almacenar las negaciones

        for part in parts:  # Itera sobre las partes
            is_negated, clean_prop = self.check_negation(
                part.strip()
            )  # Verifica la negación de cada parte
            propositions.append(clean_prop)  # Agrega la proposición limpia a la lista
            negations.append(is_negated)  # Agrega la negación a la lista

        return {
            "connector": connector,  # Devuelve el conector encontrado
            "connector_type": connector_type,  # Devuelve el tipo de conector
            "propositions": propositions,  # Devuelve las proposiciones
            "symbol": logical_symbol,  # Devuelve el símbolo lógico
            "negations": negations,  # Devuelve la lista de negaciones
        }

    def evaluate_expression(
        self, values: Tuple[bool, bool], connector_type: str, negations: List[bool]
    ) -> bool:
        """
        Evalúa una expresión lógica considerando negaciones.

        Args:
            values (Tuple[bool, bool]): Valores de verdad de las proposiciones
            connector_type (str): Tipo de conector lógico
            negations (List[bool]): Lista de negaciones para cada proposición

        Returns:
            bool: Resultado de la evaluación
        """
        p, q = values  # Asigna los valores de verdad a p y q

        # Aplicar negaciones si existen
        if negations[0]:  # Si hay negación para p
            p = not p  # Invierte el valor de p
        if len(negations) > 1 and negations[1]:  # Si hay negación para q
            q = not q  # Invierte el valor de q

        # Evalúa la expresión según el tipo de conector
        if connector_type in ["CONDICIONAL", "CAUSAL", "CONSECUTIVO"]:
            return not p or q  # Evalúa la expresión condicional
        elif connector_type in ["CONJUNCIÓN", "ADVERSATIVO"]:
            return p and q  # Evalúa la expresión de conjunción
        elif connector_type == "DISYUNCIÓN":
            return p or q  # Evalúa la expresión de disyunción
        elif connector_type == "EXPLICATIVO":
            return p == q  # Evalúa la expresión explicativa
        elif connector_type == "EJEMPLIFICATIVO":
            return not p or q  # Evalúa la expresión ejemplificativa

        return None  # Devuelve None si no se puede evaluar

    def generate_truth_table(self, parsed_prop: Dict) -> List[List[str]]:
        """
        Genera una tabla de verdad para la proposición.

        Args:
            parsed_prop (Dict): Proposición analizada

        Returns:
            List[List[str]]: Tabla de verdad formateada
        """
        if not parsed_prop["connector_type"] or len(parsed_prop["propositions"]) != 2:
            return "No se pudo generar la tabla de verdad"  # Mensaje de error si no se puede generar la tabla

        combinations = list(
            product([True, False], repeat=2)
        )  # Genera combinaciones de valores de verdad

        # Crear encabezados con negaciones si existen
        p_header = "¬p" if parsed_prop["negations"][0] else "p"  # Encabezado para p
        q_header = "¬q" if parsed_prop["negations"][1] else "q"  # Encabezado para q

        table = []  # Inicializa la tabla
        headers = [
            p_header,
            q_header,
            f"{p_header} {parsed_prop['symbol']} {q_header}",
        ]  # Encabezados de la tabla
        table.append(headers)  # Agrega los encabezados a la tabla

        for values in combinations:  # Itera sobre las combinaciones de valores
            result = self.evaluate_expression(
                values, parsed_prop["connector_type"], parsed_prop["negations"]
            )  # Evalúa la expresión lógica
            row = [
                "V" if v else "F" for v in [values[0], values[1], result]
            ]  # Crea una fila con los resultados
            table.append(row)  # Agrega la fila a la tabla

        return table  # Devuelve la tabla de verdad

    def format_truth_table(self, table: List[List[str]]) -> str:
        """
        Formatea la tabla de verdad para su visualización.

        Args:
            table (List[List[str]]): Tabla de verdad sin formato

        Returns:
            str: Tabla de verdad formateada
        """
        if not isinstance(table, list):  # Verifica si la tabla es una lista
            return table  # Devuelve la tabla si no es una lista

        widths = [
            max(len(str(row[i])) for row in table) for i in range(len(table[0]))
        ]  # Calcula el ancho de cada columna
        lines = []  # Inicializa las líneas de la tabla

        header = (
            "| "
            + " | ".join(str(cell).center(widths[i]) for i, cell in enumerate(table[0]))
            + " |"
        )  # Crea la línea del encabezado
        lines.append("=" * len(header))  # Agrega una línea de separación
        lines.append(header)  # Agrega el encabezado
        lines.append("=" * len(header))  # Agrega otra línea de separación

        for row in table[1:]:  # Itera sobre las filas de la tabla
            lines.append(
                "| "
                + " | ".join(str(cell).center(widths[i]) for i, cell in enumerate(row))
                + " |"
            )  # Formatea cada fila
        lines.append("=" * len(header))  # Agrega una línea de separación al final

        return "\n".join(lines)  # Devuelve la tabla formateada como una cadena
