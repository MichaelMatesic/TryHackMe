#!/bin/bash

src_dir="$HOME/Documents/TryHackMe/crackthehash/"

while IFS=: read -r mode_number mode_name hash salt; do
    salt=${salt%$'\r'}

    if [[ -n "$salt" ]]; then
        hash_input="$hash:$salt"
    else
        hash_input="$hash"
    fi

    echo -e "\nCracking $hash_input with mode $mode_number ($mode_name) ...\n";

    ./hashcat -m "$mode_number" -a 0 -o "${src_dir}cracked.txt" "$hash_input" "${src_dir}rockyou.txt"

done < "${src_dir}hashes.txt"
