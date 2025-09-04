from dotenv import load_dotenv
import os
import requests
from agents import Agent, Runner, RunConfig, OpenAIChatCompletionsModel, AsyncOpenAI, function_tool
#Load Environment Variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") 

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please check your .env file.")
# Setup OpenAI or Gemini Client
external_client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"  
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",  
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)
