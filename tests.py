from functions.run_python import run_python_file

def test_run_python_file():
    """Test the run_python_file function with various scenarios"""
    
    # Test 1: Run main.py without arguments (should print usage instructions)
    print("run_python_file(\"calculator\", \"main.py\"):")
    result1 = run_python_file("calculator", "main.py")
    print("Result:")
    print(result1)
    print()
    
    # Test 2: Run main.py with calculation argument
    print("run_python_file(\"calculator\", \"main.py\", [\"3 + 5\"]):")
    result2 = run_python_file("calculator", "main.py", ["3 + 5"])
    print("Result:")
    print(result2)
    print()
    
    # Test 3: Run tests.py
    print("run_python_file(\"calculator\", \"tests.py\"):")
    result3 = run_python_file("calculator", "tests.py")
    print("Result:")
    print(result3)
    print()
    
    # Test 4: Try to run file outside working directory (should be blocked)
    print("run_python_file(\"calculator\", \"../main.py\"):")
    result4 = run_python_file("calculator", "../main.py")
    print("Result:")
    print(f"    {result4}")
    print()
    
    # Test 5: Try to run non-existent file (should return error)
    print("run_python_file(\"calculator\", \"nonexistent.py\"):")
    result5 = run_python_file("calculator", "nonexistent.py")
    print("Result:")
    print(f"    {result5}")

if __name__ == "__main__":
    test_run_python_file()
