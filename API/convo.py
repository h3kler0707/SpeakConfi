from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
from tts import TTS

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

SYSTEM_INSTRUCTION = """
You are a good speaker and teach how to keep up conversations.
Keep the level of English simple and easy to understand.
Always keep the conversation going naturally.
Ask follow-up questions ONLY when appropriate.
You may invent stories and characters.
You must answer in 1 to 1.5 lines and maximum 2 until super necessary.
"""

history = []

topic = "trip planning"

history.append(
    types.Content(
        role="user",
        parts=[
            types.Part(
                text=f"Start the conversation with topic: {topic}"
            )
        ],
    )
)

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=history,
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        temperature=0.7,
    ),
)

history.append(
    types.Content(
        role="model",
        parts=[types.Part(text=response.text)],
    )
)

TTS(response.text)
print("AI:", response.text)

while True:
    user = input("You: ")

    if user.lower() in {"exit", "quit"}:
        break

    history.append(
        types.Content(
            role="user",
            parts=[types.Part(text=user)],
        )
    )

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=history,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.7,
        ),
    )

    history.append(
        types.Content(
            role="model",
            parts=[types.Part(text=response.text)],
        )
    )

    TTS(response.text)
    print("AI:", response.text)