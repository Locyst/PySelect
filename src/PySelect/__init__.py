import curses
from dataclasses import dataclass, field
from typing import List, Optional, Union

__all__ = ["PySelect", "pyselect"]

####################
## PySelect Library
## A utility for creating console-based menu screens using the curses module.
##
## Features:
## - Navigate through options using arrow keys (k/j) and Enter.
## - Support for single or multi-selection modes.
## - Customizable indicator symbols and titles.
##
## Inspired by the pick Python tool for similar functionality.
##
## Key Bindings:
## - Up: k or arrow up
## - Down: j or arrow down
## - Select: space
## - Enter: Enter key
####################

KEYS_ENTER = [curses.KEY_ENTER, ord("\n"), ord("\r")]
KEYS_UP = [curses.KEY_UP, ord("k")]
KEYS_DOWN = [curses.KEY_DOWN, ord("j")]
KEYS_SELECT = [ord(" ")]

SYMBOL_FILLED_CIRCLE = "●"
SYMBOL_UNFILLED_CIRCLE = "○"

@dataclass
class PySelect:
    options: List[str]
    title: Optional[str] = None
    screen: Optional[curses.window] = None
    indicator: str = "->"
    default_index: int = 0
    multiselect: bool = False
    min_multiselect: int = 1
    selected_indexes: List[int] = field(default_factory=list)

    def __post_init__(self):
        if not isinstance(self.options, list) or not self.options:
            raise ValueError("Options must be an non-empty list.")

        if not (0 <= self.default_index < len(self.options)):
            raise ValueError("Default index must be within the range of options.")

        if self.min_multiselect < 1:
            raise ValueError("Minimum multiselect must be at least 1.")

        if self.min_multiselect > len(self.options):
            raise ValueError("Minimum multiselect cannot be greater than the number of options.")

        self.index = self.default_index

        if self.screen is None:
            self._initialize_screen()

    def _initialize_screen(self):
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.screen.keypad(True)

    def move_up(self):
        self.index = max(self.index - 1, 0)

    def move_down(self):
        self.index = min(self.index + 1, len(self.options) - 1)

    def mark_index(self):
        if self.index not in self.selected_indexes:
            self.selected_indexes.append(self.index)
        else:
            self.selected_indexes.remove(self.index)

    def get_indexes(self) -> Union[tuple, List[tuple]]:
        if not self.multiselect:
            return (self.options[self.index], self.index)
        return [(self.options[idx], idx) for idx in self.selected_indexes]

    def get_option_lines(self) -> List[str]:
        lines = []

        for idx, option in enumerate(self.options):
            if idx == self.index:
                prefix = self.indicator
            else:
                prefix = len(self.indicator) * " "

            if self.multiselect:
                symbol = (
                    SYMBOL_FILLED_CIRCLE
                    if idx in self.selected_indexes
                    else SYMBOL_UNFILLED_CIRCLE
                )

                prefix = f"{prefix} {symbol}"

            lines.append(f"{prefix} {option}")

        return lines

    def run(self) -> Union[tuple, List[tuple]]:
        try:
            while True:
                self.screen.clear()

                lines = self.get_option_lines()

                if self.title:
                    title_message = len(self.indicator) * " " + self.title
                    self.screen.addstr(0, 0, title_message)

                for idx, line in enumerate(lines):
                    self.screen.addstr(idx + 2, 0, line)

                key = self.screen.getch()

                if key in KEYS_UP:
                    self.move_up()
                elif key in KEYS_DOWN:
                    self.move_down()
                elif key in KEYS_ENTER:
                    if (self.multiselect and len(self.selected_indexes) < self.min_multiselect):
                        continue
                    return self.get_indexes()
                elif key in KEYS_SELECT:
                    if self.multiselect:
                        self.mark_index()

                self.screen.refresh()
        finally:
            self.screen.clear()
            curses.curs_set(1)
            curses.endwin()

def pyselect(
    options: List[str],
    title: Optional[str] = None,
    screen: Optional[curses.window] = None,
    indicator: str = "->",
    default_index: int = 0,
    multiselect: bool = False,
    min_multiselect: int = 1,
    ):

    pyselect: PySelect = PySelect(
        options,
        title,
        screen,
        indicator,
        default_index,
        multiselect,
        min_multiselect,
        )

    return pyselect.run()
