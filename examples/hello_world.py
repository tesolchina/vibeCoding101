"""
Simple Hello World Example
This is a basic Python script that students can reference or run.
"""

def main():
    """Main function to run the program"""
    print("Hello, World!")
    print("Welcome to Python programming!")
    
    # Get user input
    name = input("What's your name? ")
    print(f"Nice to meet you, {name}!")
    
    # Simple calculation
    age = int(input("How old are you? "))
    print(f"In 10 years, you will be {age + 10} years old!")

if __name__ == "__main__":
    main()
