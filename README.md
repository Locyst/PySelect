# PySelect

**PySelect** is a small Python library for creating interactive selection menus in the console using the `curses` module.

## How to Use

- Clone the repository.
- Import the `pyselect` function function into your Python environment.
- Follow the example code below to create new selection menus and interact with them.

## Usage

```
>>> from PySelect import pyselect

>>> title = "Which of the following hobbies interests you the most?"
>>> options = ["Gardening", "Painting", "Coding", "Hiking"]

>>> option, index = pyselect(title=title, options=options)

>>> print(option)
>>> print(index)
```

**Outputs**

```
>>> Painting
>>> 1
```

## Paremeters

- `options`: A list of options to pick from.
- `title`: (optional) a title above the list of options
- `indicator`: (optional) the selection indicator, defaults to `->`
- `default_index`: (optional) determines the default selected option if it is not the first one
- `multiselect`: (optional) if this is set to `True`, users will be able to select more than one option.
- `min_multiselect`: (optional) the minimum amount of options the user can select before allowing them to continue
- `screen`; (optional) set this to your pre-existing curses screen object, assuming that it has been initialised in the standard way

## Notes

This is a major rewrite of the `PySelect` library, using curses instead of just the normal console. Many functions used in the PySelect class are refactored similarly to the ones in the [pick](https://github.com/aisk/pick) library due to how much easier they to read while keeping the same functionality.
