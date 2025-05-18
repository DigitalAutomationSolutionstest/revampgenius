import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    model_name="openai/gpt-4o",  # ✅ modello top qualità/prezzo
    temperature=0.9
)

def generate_email(report: str) -> str:
    prompt = f"""
Sei un esperto di marketing AI ironico e pungente.
Hai generato il seguente report tecnico su un sito obsoleto:

{report}

Scrivi un'email ironica ma professionale per proporre un restyling AI-powered con MiniAIApps.tech.
Tono amichevole, divertente ma elegante. Concludi con una CTA chiara.
    """
    response = llm([HumanMessage(content=prompt)])
    return response.content
