from functions.write_file import write_file

def test_write_file():
    """Test the write_file function with various scenarios"""
    
    # Test 1: Write to lorem.txt file (should overwrite existing content)
    print("write_file(\"calculator\", \"lorem.txt\", \"wait, this isn't lorem ipsum\"):")
    result1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print("Result:")
    print(f"    {result1}")
    print()
    
    # Test 2: Write to a new file in pkg directory
    print("write_file(\"calculator\", \"pkg/morelorem.txt\", \"lorem ipsum dolor sit amet\"):")
    result2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print("Result:")
    print(f"    {result2}")
    print()
    
    # Test 3: Try to write outside the working directory (should be blocked)
    print("write_file(\"calculator\", \"/tmp/temp.txt\", \"this should not be allowed\"):")
    result3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print("Result:")
    print(f"    {result3}")

if __name__ == "__main__":
    test_write_file()
