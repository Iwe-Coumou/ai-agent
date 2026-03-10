import os
from dotenv import load_dotenv
import argparse
from prompts import system_prompt
from functions.call_function import available_functions, call_function
from google import genai
from google.genai import types



def main(client):
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=messages, 
            config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions])
            )

        if response.usage_metadata is None:
            raise RuntimeError("No response usage_metadate available")

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)


        function_results = []
        if response.function_calls:
            for function_call in response.function_calls:
                result = call_function(function_call, True)
                if not result.parts:
                    raise Exception(f"Error: no parts in function call {function_call.name}({function_call.args})")
                if result.parts[0].function_response.response == None:
                    raise Exception(f"Error: Function response of parts[0] is None")
                function_results.append(result.parts[0])
                if args.verbose:
                    print(f"-> {result.parts[0].function_response.response}")
                
        messages.append(types.Content(role="User", parts=function_results))
        
        if not response.function_calls:
            print(response.text)
            break
        
    else:
        print(f"No response within {20} loops")
        exit(1)
        
if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not retreival failed.")
    client = genai.Client(api_key=api_key)
    
    main(client)
