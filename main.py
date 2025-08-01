import os
import sys
from urllib import response
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def main():
    print("Hello from agentic!")
    
    # Check if command line argument is provided
    if len(sys.argv) < 2:
        print("Usage: python main.py [--verbose] <your_prompt>")
        sys.exit(1)
    
    # Check for verbose flag
    verbose = False
    args = sys.argv[1:]
    if "--verbose" in args:
        verbose = True
        args.remove("--verbose")
    
    if not args:
        print("Usage: python main.py [--verbose] <your_prompt>")
        sys.exit(1)
    
    # Get the prompt from remaining command line arguments
    prompt = " ".join(args)
    
    if verbose:
        print(f"API Key: {api_key}")
        print(f"User prompt: {prompt}")

    messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),]
    
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=messages,
    )
    print(response.text)
    
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
