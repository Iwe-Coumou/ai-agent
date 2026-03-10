import os
from dotenv import load_dotenv
import argparse
from prompts import system_prompt
from functions.call_function import available_functions

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("GEMINI_API_KEY not retreival failed.")

from google import genai
from google.genai import types

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
# Now we can access `args.user_prompt`

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

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

if response.function_calls:
    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({(function_call.args)})")

if response.text:
    print(f"{response.text}")
