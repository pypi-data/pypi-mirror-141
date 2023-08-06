import re
import readline  # pylint: disable=unused-import

from rich import box
from rich.console import Console
from rich.style import Style
from rich.table import Table
from rich.theme import Theme

from voltorb_flip.game import (
    CellState,
    GameState,
    UnableToFlipException,
    VoltorbFlip,
)

THEME = Theme(
    {
        "card": "dim cyan",
        "bomb": Style(color="red", bgcolor="white"),
        "point": Style(color="navy_blue", bgcolor="deep_sky_blue1"),
        "prompt_value": Style(bold=True, underline=True, color="black"),
        "flipped_good": Style(color="#123B27", bgcolor="white"),
        "covered": Style(color="#41D98F", bgcolor="#123B27"),
        "header": Style(italic=True),
        "command": Style(bold=True, italic=True),
    }
)

COVERED_CHARACTER = "?"
MARKED_CHARACTER = "M"
BOMB_CHAR = " "
OK_CHAR = " "
COMMAND_REGEX = re.compile(r"(?P<command>[fmq])?(?:(?P<row>[a-z])(?P<column>[\d]))?")


class ConsoleGame:
    def __init__(self):
        self.game = VoltorbFlip()
        self.latest_error = None
        self.console = Console(theme=THEME)

    def get_board(self):
        table_style = {
            "box": box.SIMPLE,
            "padding": 0,
            "safe_box": False,
            "collapse_padding": True,
            "show_lines": False,
            "show_header": False,
            "header_style": None,
            "title_style": None,
            "pad_edge": False,
        }

        # Tables
        table = Table(*[" " for _ in range(self.game.CLASSIC_BOARD_SIZE + 3)], **table_style)

        # Columns
        headers = [" "]
        for row in range(self.game.CLASSIC_BOARD_SIZE):
            headers.append(f"[header]{row + 1}[/header]")
        headers.append(OK_CHAR)
        headers.append(BOMB_CHAR)
        table.add_row(*headers)

        # Rows
        for row in range(self.game.CLASSIC_BOARD_SIZE):
            current_row_label = chr(ord("a") + row)
            column_elements = [f"[header]{current_row_label}[/header]"]
            for column in range(self.game.CLASSIC_BOARD_SIZE):
                value = ConsoleGame._get_cell_value(column, self.game, row)

                if value.isnumeric():
                    value = f"[flipped_good]{value}[/flipped_good]"
                elif value == COVERED_CHARACTER:
                    value = f"[covered]{value}[/covered]"

                column_elements.append(value)

            column_elements.append(f"[point]{self.game.horizontal_points[row]}[/point]")
            column_elements.append(f"[bomb]{self.game.horizontal_bombs[row]}[/bomb]")
            table.add_row(*column_elements)

        # Last rows
        column_elements = [f"{OK_CHAR}\n{BOMB_CHAR}"]
        for row in range(self.game.CLASSIC_BOARD_SIZE):
            column_elements.append(
                f"[point]{self.game.vertical_points[row]}[/point]\n[bomb]{self.game.vertical_bombs[row]}[/bomb]"
            )
        column_elements.append("")
        table.add_row(*column_elements)

        return table

    def draw_game(self):
        self.console.clear()
        board_string = self.get_board()
        self.console.print(board_string)

    def _process_command(self, command):
        action = re.match(COMMAND_REGEX, command)
        if action.start() == action.end():
            self.latest_error = f'"{command}" is not a valid command!'
            return True

        command_dict = action.groupdict()

        action = command_dict.get("command") or "f"
        row = ord(command_dict.get("row") or "a") - ord("a")
        column = int(command_dict.get("column") or -1) - 1

        if action == "q":
            self.game.end_game()
            return False

        if action == "f":
            self.game.flip(row, column)
        elif action == "m":
            if self.game.cell_states[row][column] == CellState.MARKED_0:
                self.game.mark(row, column, cell_state=CellState.COVERED)
            else:
                self.game.mark(row, column, cell_state=CellState.MARKED_0)

        return self.game.state == GameState.IN_PROGRESS

    def process_input(self):
        commands = [
            "Flip [command]f<row><column>[/command]",
            "Mark [command]m<row><column>[/command]",
            "Quit [command]q[/command]",
        ]
        if self.latest_error:
            self.console.print(f"Error! {self.latest_error}")

        self.console.print("Instructions:", ", ".join(commands))
        prompt = " | ".join(
            [
                f"Lv. [prompt_value]{self.game.level}[/prompt_value]",
                f"Score [prompt_value]{self.game.current_score}[/prompt_value]",
            ]
        )
        command_input = self.console.input(prompt + " > ")  # nosec
        try:
            self.latest_error = None
            return self._process_command(command_input)
        except UnableToFlipException as flip_excp:
            self.latest_error = f"That cell can't be uncovered, it is {flip_excp.cell_state.name}"
            return True

        return True

    @staticmethod
    def _get_cell_value(column, game, row):
        cell_state = game.cell_states[row][column]
        value = str(game.board[row][column])
        if cell_state == CellState.COVERED:
            value = COVERED_CHARACTER
        elif cell_state != CellState.UNCOVERED:
            value = MARKED_CHARACTER
        return value
