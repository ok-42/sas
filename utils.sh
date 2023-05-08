# Find a macro definition and open it in Notepad++
function sm() {
    result=$(grep -nr "%macro $1" .)
    echo "$result"
    [ -n "$result" ] && echo "$result" | awk -F':' '{print $1 " -n" $2}' | xargs start notepad++
}


# Check a SAS log file for common errors
function log() {

    # TODO read default path from a config file
    local log_file=${1:-test.log}

    local pattern_1="Syntax error"
    local pattern_2="ERROR:"

    local line_number_1
    local line_number_2

    # The line number where the first syntax error appears in the log; written with ChatGPT
    # If a syntax error was found, output message will be orange
    line_number_1=$(grep -n "$pattern_1" "$log_file" | head -n 1 | cut -d ':' -f 1)
    if [[ -n "$line_number_1" ]]; then
        echo -e "\e[33mSyntax error found on line $line_number_1\e[0m"
    fi

    # If an ERROR: message was found, it's red
    line_number_2=$(grep -n "$pattern_2" "$log_file" | head -n 1 | cut -d ':' -f 1)
    if [[ -n "$line_number_2" ]]; then
        echo -e "\e[31mError found on line $line_number_2\e[0m"
    fi

    # If no error messages were found, it's green
    if [[ -z $line_number_1 && -z $line_number_2 ]]; then
        echo -e "\e[32mNo errors found\e[0m"
    fi

    # The first error in the log file
    local line_number
    line_number=$((line_number_1 < line_number_2 ? line_number_1 : line_number_2))

    start notepad++ "$log_file" -n"$line_number"
}

# Search for a given substring or retrieve a search result
# Takes one argument that should be either a string (to search for) or a number (of a search result)
function g() {

    # Temporary text file that stores results of grep search
    GREP_OUTPUT=grep_output.txt

    # https://stackoverflow.com/a/806923
    REGEXP='^[0-9]+$'

    # String: Search in the current directory and save results to a text file
    if ! [[ $1 =~ $REGEXP ]] ; then
       grep -nr --color --exclude-dir=.git --exclude=$GREP_OUTPUT "$1" . > $GREP_OUTPUT
       cat -n $GREP_OUTPUT

    # Number: Open the n-th line from the previous search results
    else
        n=1;
        while read line; do
            if [ $n == $1 ]; then
                echo "$line";
                SEARCH_RESULT=$line
            fi
        n=$((n+1));
        done < $GREP_OUTPUT;

        # Structure of $line: file name, line number, and a line with found occurrence.
        # These parts are separated by colon
        echo $SEARCH_RESULT | awk -F':' '{print $1 " -n" $2}' | xargs start notepad++
    fi
}
