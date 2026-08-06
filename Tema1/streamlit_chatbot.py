from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
)

import streamlit as st
load_dotenv()

#configurar la pagina de la aplicacion

st.set_page_config(page_title = "Chatbot Básico", page_icon = "🤖")
st.title("Chatbot Básico con LangChain y Streamlit")
st.markdown("Este es un chatbot básico creado con LangChain y Streamlit.")


#sidebar para configurar el modelo y la temperatura    
with st.sidebar:
    st.header("Configuración")
    temperature = st.slider("Temperatura", 0.0, 1.0, 0.5, 0.1)
    model_name = st.selectbox("Modelo", ["deepseek-v4-pro", "deepseek-v4-flash"])


    #Nueva personalidad configurables 

    personalidad = st.select_box("Selecciona la personalidad del chatbot:", ["Amigable", "Profesional", "Experto", "Divertido"])
    
    #recreando el modelo con los parametros seleccionados
    chat_model = ChatOpenAI(model=model_name,
    base_url="https://api.deepseek.com",
    temperature=temperature)
    idioma = st.radio("Selecciona el idioma de respuesta:", ["Español", "Inglés", "Francés"])


    system_message =   {"Útil y amigable": "Eres un asistente útil y amigable llamado ChatBot Pro. Responde de manera clara y concisa.",
                        "Profesional y formal": "Eres un asistente profesional y formal. Proporciona respuestas precisas y bien estructuradas.",
                        "Casual y relajado": "Eres un asistente casual y relajado. Habla de forma natural y amigable, como un buen amigo.",
                        "Experto técnico": "Eres un asistente experto técnico. Proporciona respuestas detalladas con precisión técnica.",
                        "Creativo y divertido": "Eres un asistente creativo y divertido. Usa analogías, ejemplos creativos y mantén un tono alegre."
}
#Inicializar el historial de mensajes
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

    chat_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message[personalidad]),
            ("human", "Historial de conversación:\n{historial}\n\nResponde de manera clara y sobre todo amigable a la siguiente pregunta: {mensaje}")
        ]
    )
    

    # nueva forma de encadenar el prompt y el modelo
    cadena = chat_prompt | chat_model


    

#Mostrar mensajes previos en la interfaz
for msg in st.session_state.mensajes:
    if isinstance(msg, SystemMessage):
        #no muestro el mensaje por pantalla
        continue

    role = "assistant" if isinstance(msg, AIMessage) else "user"

    with st.chat_message(role):
        st.markdown(msg.content)

if st.button("🗑️ Nueva conversación"):
    st.session_state.mensajes = []
    st.rerun()  # Esto refresca la página y reinicia la conversación

#cuadro de entrada de texto de usuario
pregunta = st.chat_input("Escribe tu mensaje")

if pregunta:
    #mostrar inmediatamente el mensaje del usuario en la interfaz
    with st.chat_message("user"):
        st.markdown(pregunta)

    try:
        with st.chat_message("assistant"):
            response_placeholder = st.empty() #se va a ir actualizando en tiempo de ejecucion
            full_response = ""
 
            # streaming! de la respuesta
            for chunk in cadena.stream({"mensaje": pregunta, "historial": st.session_state.mensajes,"idioma": idioma}):
                full_response += chunk.content
                response_placeholder.markdown(full_response + "▌")  # El cursor parpadeante
            
            response_placeholder.markdown(full_response)
        
        # almacenar los mensajes en el historial de la sesión
        st.session_state.mensajes.append(HumanMessage(content=pregunta))
        st.session_state.mensajes.append(AIMessage(content=full_response))
        
    except Exception as e:

        st.error(f"Error al generar respuesta: {str(e)}")
        st.info("Verifica que tu API Key de OpenAI esté configurada correctamente.")

