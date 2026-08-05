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

# Prueba con diferentes textos
textos_prueba = [
    "¡Me encanta este producto! Funciona perfectamente y llegó muy rápido.",
    "El servicio al cliente fue terrible, nadie me ayudó con mi problema.",
    "El clima está nublado hoy, probablemente llueva más tarde."
]
 
for texto in textos_prueba:
    resultado = chain.invoke(texto)
    print(f"Texto: {texto}")
    print(f"Resultado: {resultado}")
    print("-" * 50)