from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate


load_dotenv()

chat = ChatOpenAI(model="deepseek-chat",
    base_url="https://api.deepseek.com",
    temperature=0.7,)

plantilla = PromptTemplate(
    input_variables=["nombre"],
    template="Saluda al usuario con su nombre \n Nombre del usuario: {nombre}\n Asistente:"

)
#Deprecado
#LLMChain(llm=chat, prompt=plantilla)

chain = plantilla | chat

resultado = chain.invoke({"nombre": "Juan"})

print(resultado.content)
 