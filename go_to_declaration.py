"""This tool opens macro variable declaration, it resembles [Go To Declaration] PyCharm feature."""

import re
import subprocess
import sys


def main(
        full_current_path: str,
        current_word: str,
) -> None:
    """Search for a macro variable declaration and open it in Notepad++.

    :param full_current_path: path to a source code file
    :param current_word: SAS macro variable name
    :return: None; opens Notepad++
    """

    def find_line_number() -> int:
        """Find a line where the macro variable is declared."""
        line_number = 0
        regexp = re.compile(fr'%let {current_word}\b')
        with open(full_current_path, encoding='utf-8') as file:
            for line in file.readlines():
                line_number += 1
                if regexp.search(line):
                    return line_number
        return 0

    number = find_line_number()

    if number > 0:
        args: list[str] = [
            'C:/Program Files/Notepad++/notepad++.exe',
            full_current_path,
            f'-n{number}']

        subprocess.Popen(args)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
