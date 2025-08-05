import os
from .config import MAX_FILE_SIZE_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    """
    Read the content of a file within the working directory.
    
    Args:
        working_directory: The base directory that limits file access
        file_path: The relative path to the file within working_directory
    
    Returns:
        String containing file content or error message
    """
    try:
        # Create the full path by joining working_directory and file_path
        full_path = os.path.join(working_directory, file_path)
        
        # Get the absolute path to normalize it (resolve .. and . components)
        abs_full_path = os.path.abspath(full_path)
        abs_working_directory = os.path.abspath(working_directory)
        
        # Check if the resolved path is within the working directory
        if not abs_full_path.startswith(abs_working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # Check if the path exists and is a file
        if not os.path.exists(abs_full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        if not os.path.isfile(abs_full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # Read the file content
        with open(abs_full_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Truncate if necessary
        if len(content) > MAX_FILE_SIZE_CHARS:
            content = content[:MAX_FILE_SIZE_CHARS]
            content += f'[...File "{file_path}" truncated at {MAX_FILE_SIZE_CHARS} characters]'
        
        return content
    
    except Exception as e:
        return f"Error: {str(e)}"

# Function schema for LLM integration
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file within the working directory, with automatic truncation for large files.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)
