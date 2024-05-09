import os

UP_ARROW = '\x1b[A'
LEFT_ARROW = '\x1b[D'
DOWN_ARROW = '\x1b[B'
RIGHT_ARROW = '\x1b[C'

class Option(object):
  def __init__(self, name, call_name, type='default'):
    self.name = name
    self.call_name = call_name
    self.type = type

  def __repr__(self):
    return self.call_name

  def __str__(self):
    return self.name

class Selection(object):
  def __init__(self, title, options, *, selected_symbol='->', unselected_symbol='  ',
                multiselect=False, min_multiselect=0, multiselect_cursor_symbol='>',
               multiselect_selected_symbol='●', multiselect_unselected_symbol='○',
              defaulted_index=0):
    self.title = title
    if isinstance(options, dict): self.options = [Option(name, call_name) for name, call_name in options.items()]
    elif isinstance(options, list): self.options = [Option(name, name) for name in options]

    self.selected_symbol = selected_symbol
    self.unselected_symbol = unselected_symbol

    self.multiselect_cursor_symbol = multiselect_cursor_symbol
    self.multiselect_selected_symbol = multiselect_selected_symbol
    self.multiselect_unselected_symbol = multiselect_unselected_symbol

    self.multiselect = multiselect
    self.min_multiselect = min_multiselect

    self.cursor = defaulted_index
    self.selected_indexs = []

  def _selectedcheck(self, idx):
    symbol = ''
    if self.cursor == idx:
      if self.multiselect: symbol += self.multiselect_cursor_symbol
      else: symbol += self.selected_symbol
    else:
      symbol += self.unselected_symbol
    if self.multiselect:
      if idx in self.selected_indexs:
        symbol += self.multiselect_selected_symbol
      else:
        symbol += self.multiselect_unselected_symbol

    return symbol


  def _move_cursor(self, amount):
    self.cursor += amount
    self.cursor = max(0, min(self.cursor, len(self.options) - 1))

  def _draw(self):
    message = str()
    if self.title: message += f"\n   {self.title}\n\n"
    if self.multiselect: message += "\n   Use the space bar to select multiple entries\n\n"
    for idx, option in enumerate(self.options):
      message += f'{self._selectedcheck(idx)} ' + repr(option) + '\n\n'
    return message

  def run(self):
    while True:
      os.system('clear' if os.name == 'posix' else 'cls')
      print(self._draw())
      move = input("> ")
      if move == UP_ARROW:
        self._move_cursor(-1)
      elif move == DOWN_ARROW:
        self._move_cursor(1)
      elif " " in move:
        if self.multiselect:
          self.selected_indexs.append(self.cursor)
      elif not move:
        break

    os.system('clear' if os.name == 'posix' else 'cls')
    self._draw()
    if not self.multiselect:
      return {"OPTION_SELECTED": repr(self.options[self.cursor]),
                                     "INDEX": self.cursor}
    return {"OPTION_SELECTED": [repr(self.options[option]) for option in self.selected_indexs],
            "INDEX": self.selected_indexs}

def select(*args, **kwargs):
  _selection = Selection(*args, **kwargs)
  return _selection.run()
