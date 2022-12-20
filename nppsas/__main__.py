import sys

from nppsas.go_backward import main as go_backward
from nppsas.go_to_declaration import main as go_to_declaration

# Corresponding Notepad++ variables are $(FULL_CURRENT_PATH), $(CURRENT_WORD), and $(CURRENT_LINE)
# https://npp-user-manual.org/docs/config-files/#userdefinedcommands
if sys.argv[1] == 'go_to_declaration':
    go_to_declaration(
        full_current_path=sys.argv[2],
        current_word=sys.argv[3],
        current_line=sys.argv[4],
    )

if sys.argv[1] == 'go_backward':
    go_backward(
        current_directory=sys.argv[2],
    )
