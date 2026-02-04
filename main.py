import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise Exception("Gemini api key not found")

client = genai.Client(api_key=api_key)
print(client.models.generate_content(model='gemini-2.5-flash', contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.").text)

def main():
    print("Hello from my-ai-agent!")


if __name__ == "__main__":
    main()
