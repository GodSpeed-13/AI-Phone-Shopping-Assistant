import os
from groq import Groq
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


def get_llm_client(provider="openai"):
    if provider == "openai":
        return OpenAI()

    if provider == "groq":
        return Groq(api_key=os.environ.get("GROQ_API_KEY"))

    raise ValueError(f"Unknown LLM provider: {provider}")
