#!/bin/bash

type=`echo "$1" | cut -d '.' -f 2`

if [ $type = "c" ];then
    gcc $1 && ./a.out
    rm a.out
elif [ $type = "cpp" ];then
    g++ $1 && ./a.out
    rm a.out
else
    echo "Not .c or .cpp file"
fi
