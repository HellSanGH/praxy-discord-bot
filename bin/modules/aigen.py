from openai import OpenAI
from pydantic import BaseModel

from os import environ

from dotenv import load_dotenv

load_dotenv()

openai_key = environ["OPENAIKEY"]

def aigen(message):
    global openai_key
    clientai = OpenAI(api_key = openai_key)
    completion = clientai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "Your name is Praxy Nivora. You are a discord friendly bot who's ready to help, answer questions and chat. Use chat expressions like 'u', 'lol', 'lmao', 'alr', 'sup', 'ye', 'nah', 'ngl', 'y', ':)', 'bruh'."},
        {"role": "user", "content": message}
        ]
    )
    return completion.choices[0].message.content