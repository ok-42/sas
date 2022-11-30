"""This tool opens macro variable declaration, it resembles [Go To Declaration] PyCharm feature."""

import re
import subprocess
import sys
from pathlib import Path


def main(
        full_current_path: str,
        current_word: str,
) -> None:
    """Search for a macro variable declaration and open it in Notepad++.

    :param full_current_path: path to a source code file
    :param current_word: SAS macro variable name
    :return: None; opens Notepad++
    """

    def find_line_number(file_path: str) -> int:
        """Find a line where the macro variable or function is declared.

        :param file_path: path to a SAS file
        :return: line number; 0 if there is no occurrence
        """
        line_number = 0

        # TODO determine whether that is &variable or %function using CURRENT_LINESTR
        regexp_var = re.compile(fr'%let {current_word}\b')
        regexp_fun = re.compile(fr'%macro {current_word}\b')
        with open(file_path, encoding='utf-8') as file:
            for line in file.readlines():
                line_number += 1
                if regexp_var.search(line) or regexp_fun.search(line):
                    return line_number
        return 0

    number = find_line_number(full_current_path)

    # Use NPP_FULL_FILE_PATH
    npp_path = 'C:/Program Files/Notepad++/notepad++.exe'

    # If a macro variable or function was declared in the current file
    if number > 0:
        args: list[str] = [
            npp_path,
            full_current_path,
            f'-n{number}']

        subprocess.Popen(args)

    # Otherwise, that name was declared in another file
    else:

        # Directory containing the current file
        current_dir: Path = Path(full_current_path).parent

        # All its subdirectories and files
        for path in current_dir.iterdir():

            # Ignore non-SAS files and current file
            if path.suffix == '.sas' and path.as_posix() != full_current_path:

                # Line number in another file
                number_ext = find_line_number(path.as_posix())

                # If the name was found in that file
                if number_ext > 0:
                    args: list[str] = [
                        npp_path,
                        path,
                        f'-n{number_ext}']
                    subprocess.Popen(args)


if __name__ == '__main__':

    # Corresponding Notepad++ variables are $(FULL_CURRENT_PATH) and $(CURRENT_WORD)
    # https://npp-user-manual.org/docs/config-files/#userdefinedcommands
    main(full_current_path=sys.argv[1], current_word=sys.argv[2])
