

# Function to add two numbers
def add(number1, number2):
    return number1 + number2

operator = str(input("Select operations from add, subtract, multiply,divide"))

firstNumber = int(input("Enter first number: "))
secondNumber = int(input("Enter second number: "))

if operator == 'add':
    print(firstNumber, "+", secondNumber, "=", add(firstNumber,secondNumber))

else:
    print("Not valid or implemented input")
