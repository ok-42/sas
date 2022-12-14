"""This tool opens macro variable declaration, it resembles [Go To Declaration] PyCharm feature."""

import re
import subprocess
from pathlib import Path


def save_last_position(
        macro_file: str,
        line_number: int,
        settings_file_path: str
):
    """Save current cursor position before going to macro declaration.

    :param macro_file: path to a file with macro usage; relative to the current directory
    :param line_number: number of line where a macro was used
    :param settings_file_path: full path to a file where these settings would be stored
    :return: None; overrides file content
    """

    with open(settings_file_path, mode='w', encoding='utf-8') as file:
        file.write(f'{macro_file}\n{line_number}')


def find_macro_parameter(
        lines: list[str],
        parameter_name: str,
        occurrence_line_number: int
) -> int:
    """Find parameter name in a ``%macro`` statement if the parameter was declared as a keyword argument.

    Example:

    >>> sas_code = [
    ...     '%macro func(param_1=, param_2=);',
    ...     '%put &param_2.;'
    ...     '%mend func;']
    >>> find_macro_parameter(
    ...     lines=sas_code,
    ...     parameter_name='param_2',  # Find this parameter ...
    ...     occurrence_line_number=3   # ... that was used on the line 2 of SAS code
    ... )

    The expected result is 1 because that is the line that contains ``param_2`` declaration as a kwarg. That also
    works when a signature takes multiple lines.

    How the function works:

    [1] Iterate all the lines before the 2nd line ``'%put &param_2.;'`` and look for ``%macro`` statement.

    [2] Look for the ``param_2=`` text token within each ``%macro`` statement found in step [1].

    :param lines: file content, list of str
    :param parameter_name: macro variable name from a source code
    :param occurrence_line_number: line number where a macro variable was used
    :return: line number that refers to %macro statement
    """

    regexp_macro_definition = re.compile('%macro')
    regexp_close_brackets = re.compile(r'\)\s*;')
    regexp_whole_word = re.compile(fr'\b{parameter_name}\s*=')

    # [1] Iterate lines before the macro variable occurrence
    for i, line in enumerate(reversed(lines[:occurrence_line_number])):

        # [2] If a macro function declaration started, ...
        if regexp_macro_definition.search(line):

            # (loop counter `i` is the offset of a %macro statement)
            for j, line_2 in enumerate(lines[occurrence_line_number-i:occurrence_line_number]):

                # ... look for a macro parameter in its signature until its closing bracket is found
                if regexp_whole_word.search(line_2):
                    return occurrence_line_number - i + j + 1

                if regexp_close_brackets.search(line):
                    break

    # If no matching macro parameters were found
    return 0


def main(
        full_current_path: str,
        current_word: str,
        current_line: str,
) -> None:
    """Search for a macro variable declaration and open it in Notepad++.

    :param full_current_path: path to a source code file
    :param current_word: SAS macro variable name
    :param current_line: line number where SAS macro is used
    :return: None; opens Notepad++
    """

    settings_path = Path(full_current_path).parent / '.sas_navigation'

    # Notepad++ variable CURRENT_LINE is less by one than actual value
    current_line_adj = int(current_line) + 1

    save_last_position(
        macro_file=Path(full_current_path).name,
        line_number=current_line_adj,
        settings_file_path=settings_path.as_posix())

    def find_line_number(file_path: str) -> int:
        """Find a line where the macro variable or function is declared.

        :param file_path: path to a SAS file
        :return: line number; 0 if there is no occurrence
        """
        line_number = 0

        # TODO determine whether that is &variable or %function using CURRENT_LINESTR
        regexp_var = re.compile(fr'%let {current_word}\b')
        regexp_fun = re.compile(fr'%macro {current_word}\b')

        # [1] Try to find either '%let' or '%macro' statements
        with open(file_path, encoding='utf-8') as file:
            lines: list[str] = file.readlines()
            for line in lines:
                line_number += 1
                if regexp_var.search(line) or regexp_fun.search(line):
                    return line_number

        # [2] Try to find any '%macro' statement that is followed by the param declaration
        return find_macro_parameter(
            lines=lines,
            parameter_name=current_word,
            occurrence_line_number=current_line_adj)

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
