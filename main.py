import os
import sys
from urllib import response
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def call_function(function_call_part, verbose=False):
    """
    Handle calling one of our four functions based on the LLM's function call.
    
    Args:
        function_call_part: A types.FunctionCall with .name and .args properties
        verbose: Whether to print detailed output
    
    Returns:
        types.Content with the function result
    """
    # Dictionary mapping function names to actual functions
    available_function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    
    function_name = function_call_part.name
    function_args = dict(function_call_part.args) if function_call_part.args else {}
    
    # Print function call info
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")
    
    # Check if function exists
    if function_name not in available_function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    # Add working directory to arguments
    function_args["working_directory"] = "./calculator"
    
    # Call the function
    try:
        function_to_call = available_function_map[function_name]
        function_result = function_to_call(**function_args)
        
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Error executing function: {str(e)}"},
                )
            ],
        )

# System prompt for AI agent
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# Available functions for the LLM
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

def main():
    print("Hello from agentic!")
    
    # Hardcoded working directory for security
    working_directory = "calculator"
    
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
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]
    
    client = genai.Client(api_key=api_key)
    
    # Conversational loop - limit to 20 iterations
    max_iterations = 20
    iteration = 0
    
    try:
        while iteration < max_iterations:
            iteration += 1
            
            if verbose:
                print(f"\n--- Iteration {iteration} ---")
            
            # Generate content with current messages
            response = client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], 
                    system_instruction=system_prompt
                ),
            )
            
            # Check if we have candidates in the response
            if not response.candidates or not response.candidates[0].content:
                print("No response candidates found")
                break
            
            candidate_content = response.candidates[0].content
            
            # Add the model's response to our conversation
            messages.append(candidate_content)
            
            # Check if this is a final text response (no function calls)
            has_function_calls = False
            has_text_response = False
            
            # Process each part of the response
            for part in candidate_content.parts:
                if hasattr(part, 'function_call') and part.function_call:
                    has_function_calls = True
                    function_call_part = part.function_call
                    
                    # Call the function and get the result
                    function_call_result = call_function(function_call_part, verbose)
                    
                    # Validate the response structure
                    if not (function_call_result.parts and 
                            hasattr(function_call_result.parts[0], 'function_response') and
                            function_call_result.parts[0].function_response and
                            hasattr(function_call_result.parts[0].function_response, 'response')):
                        raise Exception("Invalid function response structure")
                    
                    # Add the tool response to our conversation
                    messages.append(function_call_result)
                    
                    # Print result if verbose
                    if verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                    else:
                        # Print just the result for non-verbose mode
                        response_data = function_call_result.parts[0].function_response.response
                        if "result" in response_data:
                            print(response_data["result"])
                        elif "error" in response_data:
                            print(response_data["error"])
                            
                elif hasattr(part, 'text') and part.text:
                    has_text_response = True
                    if verbose:
                        print(f"Model response: {part.text}")
            
            # If we got a text response and no function calls, we're done
            if has_text_response and not has_function_calls:
                # Print the final response
                final_text = ""
                for part in candidate_content.parts:
                    if hasattr(part, 'text') and part.text:
                        final_text += part.text
                
                if not verbose and final_text:
                    print(final_text)
                break
            
            # If no function calls and no text, something went wrong
            if not has_function_calls and not has_text_response:
                print("No function calls or text response found")
                break
                
        if iteration >= max_iterations:
            print(f"Reached maximum iterations ({max_iterations})")
            
    except Exception as e:
        print(f"Error during conversation loop: {e}")
        if verbose:
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
