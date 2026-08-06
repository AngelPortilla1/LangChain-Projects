from langchain_core.prompts import PromptTemplate

template = "Eres un experto en marketin. Sugiere un eslogan creativo para un producto {producto}"


prompt = PromptTemplate(
    template = template,
    input_variables=["producto"]
)


prompt_lleno = prompt.format(producto = "Zapatos deportivos")

print(prompt_lleno)