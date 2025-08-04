from functions.get_files_info import get_files_info

def test_get_files_info():
    """Test the get_files_info function with various scenarios"""
    
    # Test 1: List current directory in calculator
    print("get_files_info(\"calculator\", \".\"):")
    result1 = get_files_info("calculator", ".")
    print("Result for current directory:")
    print(result1)
    print()
    
    # Test 2: List pkg subdirectory
    print("get_files_info(\"calculator\", \"pkg\"):")
    result2 = get_files_info("calculator", "pkg")
    print("Result for 'pkg' directory:")
    print(result2)
    print()
    
    # Test 3: Try to access /bin (should be blocked)
    print("get_files_info(\"calculator\", \"/bin\"):")
    result3 = get_files_info("calculator", "/bin")
    print("Result for '/bin' directory:")
    print(f"    {result3}")
    print()
    
    # Test 4: Try to access parent directory (should be blocked)
    print("get_files_info(\"calculator\", \"../\"):")
    result4 = get_files_info("calculator", "../")
    print("Result for '../' directory:")
    print(f"    {result4}")

if __name__ == "__main__":
    test_get_files_info()
