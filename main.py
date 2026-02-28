import os
import argparse
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompts import system_prompt
from functions.call_functions import available_functions, call_function

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
    MAX_ITERS = 20
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")
    for _ in range(MAX_ITERS):
        text = generate_content(client, messages, args.verbose)
        if text is not None:
            print("Final response:")
            print(text)
            return
    print(f"Maximum iterations ({MAX_ITERS}) reached")
    sys.exit(1)
        
        
    

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )

    

    # Response Logic

    ## Raise error if no metadata is present

    if response.usage_metadata == None:
        raise RuntimeError("No metadata recieved")
    
    ## Adds candidates to messages list if there are any

    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    ## Returns the response if no tools are used

    if not response.function_calls:
        return response.text
    
    ## Run tools and raise errors if anything is empty

    function_results = []
    if response.function_calls != None:
        for function in response.function_calls:
            function_call_results = call_function(function, verbose)
            if function_call_results.parts == None:
                raise Exception(f"Error: {function.name}.parts is empty")
            if function_call_results.parts[0].function_response == None:
                raise Exception(f"Error: {function.name}.parts[0].function_response returned None")
            if function_call_results.parts[0].function_response.response == None:
                raise Exception(f"Error: {function.name}.parts[0].function_response.response returned None")
            function_results.append(function_call_results.parts[0])
            if verbose:
                print(f"-> {function_call_results.parts[0].function_response.response}")
    
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    messages.append(types.Content(role="user", parts=function_results))

if __name__ == "__main__":
    main()