# Find a macro definition and open it in Notepad++
function sm() {
    result=$(grep -nr "%macro $1" .)
    echo $result
    [ ! -z "$result" ] && echo $result | awk -F':' '{print $1 " -n" $2}' | xargs start notepad++
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
