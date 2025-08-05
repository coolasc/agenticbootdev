import os
from .config import MAX_FILE_SIZE_CHARS
from google.genai import types

def write_file(working_directory, file_path, content):
    """
    Write content to a file within the working directory.
    
    Args:
        working_directory: The base directory that limits file access
        file_path: The relative path to the file within working_directory
        content: The content to write to the file
    
    Returns:
        String containing success message or error message
    """
    try:
        # Create the full path by joining working_directory and file_path
        full_path = os.path.join(working_directory, file_path)
        
        # Get the absolute path to normalize it (resolve .. and . components)
        abs_full_path = os.path.abspath(full_path)
        abs_working_directory = os.path.abspath(working_directory)
        
        # Check if the resolved path is within the working directory
        if not abs_full_path.startswith(abs_working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # Create the directory if it doesn't exist
        directory = os.path.dirname(abs_full_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        # Write the content to the file
        with open(abs_full_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        # Return success message
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {str(e)}"

# Function schema for LLM integration
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites content to a file within the working directory, creating directories as needed.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)
