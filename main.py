import os
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv


def main():
    # Load environment / Get API key

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise Exception("Gemini api key not found")

    # Parser setup

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # Client / Prompt setup

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    client = genai.Client(api_key=api_key)
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")
    generate_content(client, messages, args.verbose)
    

def generate_content(client, messages, verbose):
    response = client.models.generate_content(model='gemini-2.5-flash', contents=messages)

    # Response Logic

    if response.usage_metadata == None:
        raise RuntimeError("No metadata recieved")
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Response:")
    print(response.text)

if __name__ == "__main__":
    main()