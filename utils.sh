# Find a macro definition and open it in Notepad++
function sm() {
    result=$(grep -nr "%macro $1" .)
    echo $result
    [ ! -z "$result" ] && echo $result | awk -F':' '{print $1 " -n" $2}' | xargs start notepad++
}
