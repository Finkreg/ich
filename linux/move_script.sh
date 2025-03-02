#~/bin/bash
#

directory="Dir1"

for file in "$directory"/*
do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        number="${filename//[^0-9]/}"

        if [ $((number % 2)) -eq 0 ]; then
            mv "$file" "Dir2/"
        fi
    fi
done

