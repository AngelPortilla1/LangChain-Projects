from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI

import json

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
    