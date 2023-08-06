from math import inf
import sys
from console_element import line_type, console_element
from dynamic_element import DynamicElement
import asyncio
from typing import Any
from aioconsole import ainput
import colorama
import time

colorama.init(wrap=False)


def inf_div(v1, v2):
    if v2 == 0:
        return inf
    else:
        return v1 / v2


def ansi_move(number: int, action: str, offset=0, ending=""):
    if number > 0:
        return f"\033[{number + offset}{action}{ending}"
    else:
        return ""


def lmap(func, lst: list):
    return list(map(func, lst))


class Screen:
    def __init__(self, content=[""]) -> None:
        self._total: int = 0
        self._previous_content: list[str] = [""]
        self.current_content: list[line_type] = content
        self.speed = 8
        self._status = False
        self._changed = True
        if self.current_content != [""]:
            self.draw()

    async def start(self):
        self._status = True
        while self._status:
            if self.speed <= 0:
                raise ValueError("Speed cannot be 0 or Negative")
            if self._changed:
                self.draw()
            await asyncio.sleep(1 / self.speed)

    def update(self, new_content: list[line_type], now=False):
        self.current_content = new_content
        self._changed = True
        if now:
            self.draw()

    def insert(self, lines: list, index, now=True):
        self.current_content = (
            self.current_content[:index]
            + lmap(str, lines)
            + self.current_content[index:]
        )
        self._changed = True

    def stop(self):
        self._status = False

    async def input(self, append=True, now: bool = True):
        content = await ainput()
        print("\033[F\033[K", end="")
        if append:
            self.print(content, now=now)
        return content

    def print(self, *values: str, now: bool = True):
        self.current_content.extend(values)
        self._changed = True
        if now:
            self.draw()

    def change(self, value, index: int, now=False):
        self.current_content[index] = str(value)
        self._changed = True
        if now:
            self.draw()

    def draw(self):
        def append_if_needed(lst: list[Any], index: int, value: Any, empty: Any):
            needed_amount = index - len(lst) + 1
            if needed_amount > 0:
                lst.extend([empty for _ in range(needed_amount)])
            lst[index] = value

        def append_if_not_empty(lst: list[str], value: str):
            if value != "":
                lst.append(value)

        def render_line(line: line_type) -> str:
            def render_console_element(element: console_element) -> str:
                if type(element) is str:
                    return element
                elif type(element) is DynamicElement:
                    element.increment_frame()
                    return element.render()
                else:
                    return str(line_type)

            if type(line) is str:
                return line
            else:
                return "".join([render_console_element(element) for element in line])

        start_time = time.time()
        self._changed = False
        rendered_content = [render_line(v) for v in self.current_content]

        previous_total = self._total

        changed: list[int] = []
        for i, (line, current_line) in enumerate(
            zip(
                rendered_content,
                self._previous_content
                + [
                    ""
                    for _ in range(
                        max(0, len(rendered_content) - len(self._previous_content))
                    )
                ],
            )
        ):
            if line != current_line:
                changed.append(i)
        removed_lines = max(0, self._total - len(rendered_content))
        self._total -= removed_lines
        change_string_list: list[str] = ["\0337"]
        append_if_not_empty(change_string_list, "\033[F\033[K" * removed_lines)
        self._previous_content = self._previous_content[: self._total]
        if len(changed) > 0:
            append_if_not_empty(
                change_string_list, ansi_move(self._total - changed[0], "F")
            )
            current_location: int = changed[0]
            for change in changed:
                append_if_not_empty(
                    change_string_list, "\n" * (change - current_location)
                )
                if len(rendered_content) > change:
                    if change < len(self._previous_content) and len(
                        self._previous_content[change]
                    ) > len(rendered_content[change]):
                        append_if_not_empty(change_string_list, "\033[K")
                    append_if_not_empty(change_string_list, rendered_content[change])
                    append_if_needed(
                        self._previous_content, change, rendered_content[change], ""
                    )
                current_location = change
            current_amount = previous_total - current_location
            added_amount = self._total - current_location - current_amount
            append_if_not_empty(
                change_string_list, ansi_move(current_amount, "E", offset=-1)
            )
            append_if_not_empty(change_string_list, added_amount * "\n")
        if self._previous_content == []:
            change_string_list.append("\033[F")
        self._total = len(rendered_content)
        change_string_list.append("\n")
        change_string_list.append("\0338")
        append_if_not_empty(
            change_string_list, ansi_move(self._total - previous_total, "B")
        )

        change_string = "".join(change_string_list)
        if change_string != "\0337\n\0338":
            if False:
                for change_string in change_string_list:
                    print(change_string, end="")
                    sys.stdout.flush()
                    # open("log.txt", "a").write(repr(change_string) + "\n")
                # open("log.txt", "a").write("END\n")
            else:
                calc_time = time.time()
                print(change_string, end="")
                sys.stdout.flush()
                now = time.time()
                open("log.txt", "a").write(
                    f"calc: {calc_time - start_time} print: {now - calc_time} mfps: {inf_div(1, now - start_time)} {repr(change_string)}\n"
                )
