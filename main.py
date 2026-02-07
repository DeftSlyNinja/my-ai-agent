import os
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise Exception("Gemini api key not found")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

client = genai.Client(api_key=api_key)
response = client.models.generate_content(model='gemini-2.5-flash', contents=messages)
if response.usage_metadata == None:
    raise RuntimeError("No metadata recieved")
else:
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
print("Response:")
print(response.text)

