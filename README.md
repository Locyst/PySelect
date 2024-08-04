# PySelect

PySelect is a Python library that provides a flexible selection interface for multiple choices with ease. It allows users to create selection menus with customizable options and associated functions, making it easy to implement interactive selection processes in Python applications.

## How to Use

- Clone the repository.
- Import `selection` class or `PySelect.select` function into your Python environment.
- Follow the example code below to create new selection menus and interact with them.

## Usage

```python
from PySelect.select import select

if __name__ == '__main__':
    var1 = 1
    var2 = 1
    selection = select(
        title=f"What would you like to do with {var1} and {var2}?",
        options={"Add": "add", "Subtract": "subtract", "Multiply": "multiply", "Divide": "divide"}
    )
    
    option = selection["OPTION_SELECTED"]
    if option == "add":
        print(var1 + var2)
    elif option == "subtract":
        print(var1 - var2)
    elif option == "multiply":
        print(var1 * var2)
    elif option == "divide":
        print(var1 / var2)
```

## Paremeters

The python code below shows a dictionary that shows all of the settings that can be used by the selection class (and select function) and what they do.
- Settings have a preset value meaning that you do not need to copy over the whole setting dictionary and instead only the needed parts

```python
settings = {
    'cursor_settings': {
        # Custom settings for cursor appearance and behavior (currently unused)
    },
    'selection_symbols': {
        'selected_symbol': '->',               # Symbol for the selected option
        'unselected_symbol': '  ',             # Symbol for unselected options
    },
    'multiselect_settings': {
        'enabled': False,                      # Enable or disable multiselect
        'cursor_symbol': '>',                  # Symbol for the cursor in multiselect
        'selected_symbol': '●',                # Symbol for selected options in multiselect
        'unselected_symbol': '○',              # Symbol for unselected options in multiselect
        'min': 1                               # Minimum number of options required to be selected
    },
    'display_settings': {
        'multiselect_text': "\n   Use the space bar to select multiple entries\n\n"  # Text that shows when multiselect is enabled
    },
    'defaulted_index': 0,                   # Default cursor position
    'numbered_options': True,               # Whether to number options, starting at 0
    'pick_through_number': True             # Whether to let users select options through their list number, shown with the option above
}

# Example of using the settings dictionary with the select function
selection = select(
    title="Choose an Option",
    options=["Option 1", "Option 2", "Option 3"],
    **settings
)
```
