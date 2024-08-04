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
  def __init__(self, title, options,
                 cursor_settings=None,
                 selection_symbols=None,
                 multiselect_settings=None,
                 display_settings=None,
                 defaulted_index=0,
                 numbered_options=False,
                 pick_through_number=False):

    cursor_settings = cursor_settings or {}
    selection_symbols = selection_symbols or {}
    multiselect_settings = multiselect_settings or {}
    display_settings = display_settings or {}

    self.title = title
    if isinstance(options, dict): self.options = [Option(name, call_name) for name, call_name in options.items()]
    elif isinstance(options, list): self.options = [Option(name, name) for name in options]

    self.selected_symbol = selection_symbols.get('selected_symbol', '->')
    self.unselected_symbol = selection_symbols.get('unselected_symbol', '  ')

    self.multiselect_cursor_symbol = multiselect_settings.get('cursor_symbol', '>')
    self.multiselect_selected_symbol = multiselect_settings.get('selected_symbol', '●')
    self.multiselect_unselected_symbol = multiselect_settings.get('unselected_symbol', '○')

    self.multiselect = multiselect_settings.get('enabled', False)
    self.min_multiselect = multiselect_settings.get('min', 0)

    self.multiselect_text = display_settings.get('multiselect_text', "\n   Use the space bar to select multiple entries\n\n")

    self.cursor = defaulted_index
    self._normalize_cursor
    self.selected_indexs = []

    self.numbered_options = numbered_options
    self.pick_through_number = pick_through_number

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

  def _normalize_cursor(self):
    self.cursor = max(0, min(self.cursor, len(self.options) - 1))

  def _move_cursor(self, amount):
    self.cursor += amount
    self._normalize_cursor()

  def _draw(self):
    message = str()
    if self.title: message += f"\n   {self.title}\n\n"
    if self.multiselect: message += self.multiselect_text
    for idx, option in enumerate(self.options):
      if self.numbered_options:
        message += f'{idx} {self._selectedcheck(idx)} ' + repr(option) + '\n\n'
      else:
        message += f'{self._selectedcheck(idx)} ' + repr(option) + '\n\n'
    return message

  def _clear(self):
    os.system('clear' if os.name == 'posix' else 'cls')

  def run(self):
    while True:
      self._clear()
      print(self._draw())
      USER_INPUT = input("> ")
      if USER_INPUT == UP_ARROW:
        self._move_cursor(-1)

      elif USER_INPUT == DOWN_ARROW:
        self._move_cursor(1)

      elif (" " in USER_INPUT) and (self.multiselect):
        self.selected_indexs.append(self.cursor)

      elif (self.pick_through_number) and (USER_INPUT.isnumeric()):
        if 0 <= int(USER_INPUT) <= len(self.options) + 1:
          if (self.multiselect):
            self.selected_indexs.append(USER_INPUT)
          else:
            return {"OPTION_SELECTED": repr(self.options[int(USER_INPUT)]),
                                     "INDEX": int(USER_INPUT)}
      elif not USER_INPUT:
        break

    self._clear()
    self._draw()
    if not self.multiselect:
      return {"OPTION_SELECTED": repr(self.options[self.cursor]),
                                     "INDEX": self.cursor}
    return {"OPTION_SELECTED": [repr(self.options[option]) for option in self.selected_indexs],
            "INDEX": self.selected_indexs}

def select(*args, **kwargs):
  _selection = Selection(*args, **kwargs)
  return _selection.run()
