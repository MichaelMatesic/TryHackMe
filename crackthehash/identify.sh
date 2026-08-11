#!/bin/bash

src_dir="$HOME/Documents/TryHackMe/crackthehash/"
python="$src_dir.venv/Scripts/python.exe"

while IFS=: read -r mode_number mode_name hash salt; do
    salt=${salt%$'\r'}

    if [[ -n "$salt" ]]; then
        hash_input="$hash:$salt"
    else
        hash_input="$hash"
    fi

    echo -e "\nIdentifying $hash_input ...\n"

    "$python" -m hashid -m "$hash_input"

done < "${src_dir}hashes.txt"