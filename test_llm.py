from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    model_name="mistralai/mixtral-8x7b-instruct",
    temperature=0.9
)

response = llm([HumanMessage(content="Scrivimi una email ironica per un sito obsoleto.")])
print(response.content)
