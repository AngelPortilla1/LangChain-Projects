from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pathlib import Path
import json
dotenv_path = Path(__file__).parent.parent / "Tema1" / ".env"
load_dotenv(dotenv_path)
#configuracion del modelo: 

chat = ChatOpenAI(model="deepseek-chat",
    base_url="https://api.deepseek.com",
    temperature=0)

def preprocess_text(text):
    """Limpia el texto eliminando espacios extras y limitando longitud"""
    text = text.strip()
    text = text[:500]
    return text

preprocessor = RunnableLambda(preprocess_text)


def generate_summary(text):
    """Genera un resumen conciso del texto"""
    prompt = f'Resume en una sola oracion {text}'
    response= chat.invoke(prompt)
    return response.content


def analyze_sentiment(text):
    """Analiza el sentimiento y devuelve el resultado estructurado"""
    prompt = f"""Analiza el sentimiento del siguiente texto.
    Responde ÚNICAMENTE en formato JSON válido:
    {{"sentimiento": "positivo|negativo|neutro", "razon": "justificación breve"}}
        
    Texto: {text}"""
    
    response = chat.invoke(prompt)
    try:
        return json.loads(response.content)
    except json.JSONDecodeError:
        return {"sentimiento": "neutro", "razon": "Error en análisis"}


def merge_results(data):
    """Combina los resultados de ambas ramas en un formato unificado"""
    return {
        "resumen": data["resumen"],
        "sentimiento": data["sentimiento_data"]["sentimiento"],
        "razon": data["sentimiento_data"]["razon"]
    }
def process_one(t):
    resumen = generate_summary(t)              # Llamada 1 al LLM
    sentimiento_data = analyze_sentiment(t)    # Llamada 2 al LLM
    return merge_results({
        "resumen": resumen,
        "sentimiento_data": sentimiento_data
    })
 
# Convertir en Runnable
process = RunnableLambda(process_one)


chain = preprocessor | process

