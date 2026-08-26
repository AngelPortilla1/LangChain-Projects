from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Eres un asistente útil y amigable llamado ChatBot Pro. Responde de manera clara y concisa."),
        MessagesPlaceholder(variable_name="historial"),
        ("human","{pregunta_actual}")
    ]
)

#simulamos un historial de conversacion con placeholders

historial_conversacion = [
    HumanMessage(content="Hola, ¿cómo estás?"),
    AIMessage(content="¡Hola! Estoy bien, gracias por preguntar. ¿Y tú?"),
    HumanMessage(content="Estoy bien también. ¿Qué has estado haciendo últimamente?"),
    AIMessage(content="He estado trabajando en algunos proyectos interesantes de programación y también he estado leyendo algunos libros sobre inteligencia artificial. ¿Y tú?"),
]

mensajes = chat_prompt.format_messages(
    historial=historial_conversacion,
    pregunta_actual="¿Cuál es tu película favorita?"
)

for m in mensajes:
    print(f"{m.type}: {m.content}")