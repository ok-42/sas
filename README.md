# What is it

A collection of utilities that facilitate SAS code development.


# Prerequisite

- Windows
- Notepad++
- Python
- Git for Windows


# Installation

1. Clone the project.
2. Add `source utils.sh` to your `.bashrc` using actual path to the [file](utils.sh).
3. Incorporate [`<Command>`](notepad_settings.xml) tag into your Notepad++ settings file
   [(how to find it)](https://github.com/ok-42/settings/tree/master/notepad-plus-plus). It adds run configuration and 
   assigns <kbd>Ctrl</kbd> + <kbd>B</kbd> shortcut for that action.
4. Set actual path to the cloned directory in the `<Command>` tag.
5. Make sure that the shortcut has no other assignment (*Settings &mdash; Shortcut Mapper...*). By default, that is 
   *Go to matching brace*. Otherwise, you need to assign another keyboard shortcut for the action.


# Usage

> Note: As of now, that only works if all SAS files you search in are located in the same directory.
 
## Go to macro variable or function declaration (Notepad++)

1. Open SAS file with Notepad++.
2. Either select a variable or function name or put caret there.
3. Invoke *Run &mdash; SAS macro search*. Its default keyboard shortcut is <kbd>Ctrl</kbd> + <kbd>B</kbd>.

## Go to macro function declaration (Git for Windows)

1. Open Git Bash.
2. Navigate to a directory that contains your SAS files.
3. Put the actual macro function name into the command below. Quotes are optional.

```bash
sm 'macro_function_name'
```
