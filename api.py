import json
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from interprete_ai import generar_tabla_verdad, interpretar_proposicion_lenguaje_natural
from interprete import InterpreteLógico

# Inicializa FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()


def api_response(expresion_str):
    """
    Función para usar en una API que genera la tabla de verdad
    y devuelve una respuesta JSON estructurada.
    """
    try:
        # Generar tabla en formato dict
        resultado = generar_tabla_verdad(expresion_str, formato="dict")

        # Verificar si hay error (si es string, asumimos que es un mensaje de error)
        if isinstance(resultado, str):
            return json.dumps(
                {"success": False, "error": resultado}, ensure_ascii=False
            )

        # Crear respuesta API
        response = {
            "success": True,
            "expresion_original": expresion_str,
            "tabla_verdad": resultado,
            "num_filas": len(resultado),
        }

        return json.dumps(response, ensure_ascii=False)

    except Exception as e:
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)


@app.post("/analizar_ai")
async def analizar_proposicion_ai(prop: str):
    expresion = interpretar_proposicion_lenguaje_natural(prop)
    resultado = json.loads(api_response(expresion))
    print("SE HA CONSULTADO IA")
    if not resultado.get("success"):
        raise HTTPException(status_code=400, detail=resultado.get("error"))
    return resultado


@app.post("/analizar")
async def analizar_proposicion(prop: str):
    client = InterpreteLógico()
    resultado = client.parse_proposition(prop)
    if not resultado["connector"]:
        raise HTTPException(status_code=400, detail="No se ha encontrado un conector")
    return {
        "análisis": resultado,
        "tabla_verdad": client.generate_truth_table(resultado),
    }


@app.get("/")
async def read_root():
    return {"estado_servidor": "Ok"}
