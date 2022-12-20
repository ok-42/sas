"""Get back to macro variable or function usage from its declaration.

Similar to 'Navigate - Last Edit Location'.
"""

import subprocess
from pathlib import Path


def main(current_directory: str, filename: str = '.sas_navigation') -> None:
    """Read info about the last position from a text file.

    The file should be excluded from version control. Its structure should be as following:

    - 1st line: path to the file where you found a macro usage; relative to ``current_directory``
    - 2nd line: line number where that macro was used

    Example: for a project with the following structure

    - /root/project/macro_declaration.sas
    - /root/project/macro_usage.sas
    - /root/project/.sas_navigation

    proper argument values are:

    - ``current_directory`` is ``/root/project``
    - ``filename`` is ``.sas_navigation``

    :param current_directory: path to a directory that contains SAS files
    :param filename: file that contains info on the last position
    :return: None; opens a file in Notepad++
    """

    current_path = Path(current_directory)

    with open(current_path / filename, encoding='utf-8') as file:
        content: list[str] = file.read().split('\n')

    sas_file: str = content[0]
    line_number = int(content[1])

    npp_path = 'C:/Program Files/Notepad++/notepad++.exe'
    args: list[str] = [
        npp_path,
        current_path / sas_file,
        f'-n{line_number}']

    subprocess.Popen(args)
