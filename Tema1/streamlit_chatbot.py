from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
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


#Inicializar el historial de mensajes

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

#sidebar para configurar el modelo y la temperatura    
with st.sidebar:
    st.header("Configuración")
    temperature = st.slider("Temperatura", 0.0, 1.0, 0.5, 0.1)
    model_name = st.selectbox("Modelo", ["deepseek-v4-pro", "deepseek-v4-flash"])
    
    #recreando el modelo con los parametros seleccionados
    chat_model = ChatOpenAI(model=model_name,
    base_url="https://api.deepseek.com",
    temperature=temperature)
    idioma = st.radio("Selecciona el idioma de respuesta:", ["Español", "Inglés", "Francés"])

    prompt_template = PromptTemplate(
    input_variables=["mensaje", "historial"],
    template="""Eres un asistente útil y amigable llamado ChatBot StreamlitProSaber. 
    Historial de conversación:
    {historial}
    Responde de manera clara y sobre todo amigable a la siguiente pregunta: {mensaje}"""
    )

    # nueva forma de encadenar el prompt y el modelo
    cadena = prompt_template | chat_model
    if st.button("🗑️ Nueva conversación"):
        # ¿Qué necesitas limpiar?
        st.session_state.mensajes = []
        st.rerun()  # Esto refresca la página y reinicia la conversación

    

#Mostrar mensajes previos en la interfaz
for msg in st.session_state.mensajes:
    if isinstance(msg, SystemMessage):
        #no muestro el mensaje por pantalla
        continue

    role = "assistant" if isinstance(msg, AIMessage) else "user"


    with st.chat_message(role):
        st.markdown(msg.content)


#cuadro de entrada de texto de usuario
pregunta = st.chat_input("Escribe tu mensaje")

if pregunta:
    #mostrar inmediatamente el mensaje del usuario en la interfaz
    with st.chat_message("user"):
        st.markdown(pregunta)

    try:
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
 
            # ¡Aquí está la magia del streaming!
            for chunk in cadena.stream({"mensaje": pregunta, "historial": st.session_state.mensajes,"idioma": idioma}):
                full_response += chunk.content
                response_placeholder.markdown(full_response + "▌")  # El cursor parpadeante
            
            response_placeholder.markdown(full_response)
        
        # No olvides almacenar los mensajes
        st.session_state.mensajes.append(HumanMessage(content=pregunta))
        st.session_state.mensajes.append(AIMessage(content=full_response))
        
    except Exception as e:
        # ¿Qué tipo de errores podrían ocurrir aquí?
        st.error(f"Error al generar respuesta: {str(e)}")
        st.info("Verifica que tu API Key de OpenAI esté configurada correctamente.")

