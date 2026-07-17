from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat",
    base_url="https://api.deepseek.com",
    temperature=0.7,)

pregunta = "En que año se descubrió América?"

print("Pregunta:", pregunta)

respuesta = llm.invoke(pregunta)
print("Respuesta:", respuesta.content)