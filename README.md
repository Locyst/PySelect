# PySelect

PySelect is a Python library that provides a flexible selection interface for multiple choices with ease. It allows users to create selection menus with customizable options and associated functions, making it easy to implement interactive selection processes in Python applications.

## How to Use

- Clone the repository.
- Import the `select` class into your Python environment.
- Follow the example code below to create new selection menus and interact with them.

## Usage

```python
from PySelect import select

if __name__ == '__main__':
     var1=1
     var2=1
     selection = select(title=f"What would you like to do with {var1} and {var2}?", options={"Add": "add", "Subtract": "subtract", "Multiply": "multiply", "Divide": "divide"})
     if selection["OPTION_SELECTED"] == "add":
          print(var1+var2)
     elif selection["OPTION_SELECTED"] == "subtract":
          print(var1+var2)
     elif selection["OPTION_SELECTED"] == "multiply":
          print(var1*var2)
     elif selection["OPTION_SELECTED"] == "divide":
          print(var1/var2)
```
