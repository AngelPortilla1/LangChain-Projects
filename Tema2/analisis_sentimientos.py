from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnableSequence
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pathlib import Path
import json
import os

dotenv_path = Path(__file__).parent.parent / "Tema1" / ".env"
load_dotenv(dotenv_path)




print(os.getenv("OPENAI_API_KEY"))


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


summary_branc = RunnableLambda(generate_summary)

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


sentiment_branch = RunnableLambda(analyze_sentiment)

def merge_results(data):
    """Combina los resultados de ambas ramas en un formato unificado"""
    return {
        "resumen": data["resumen"],
        "sentimiento": data["sentimiento_data"]["sentimiento"],
        "razon": data["sentimiento_data"]["razon"]
    }


merger = RunnableLambda(merge_results)



parallel_analysis = RunnableParallel({
    "resumen" :summary_branc,
    "sentimiento_data" :sentiment_branch
})


chain = preprocessor | parallel_analysis | merger

reviews_batch = [
    "Me encantó el producto, superó mis expectativas.",
    "El servicio fue terrible, no lo recomiendo.",
    "Es un producto promedio, nada especial.",
    "Excelente calidad y atención al cliente.",
    "No me gustó, esperaba más por el precio."
]


#Con .batch langchain va a procesar muchos elementos al tiempo
resultado_batch = chain.batch(reviews_batch)



#json.dumps() significa "dump string": convierte un objeto de Python en una cadena de texto (string) con formato JSON.

print(json.dumps(resultado_batch, indent=4, ensure_ascii=False))