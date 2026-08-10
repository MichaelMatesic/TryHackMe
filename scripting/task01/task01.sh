#!/bin/bash

b64_encoded=$(< "b64_1550406728131.txt")

for i in $(seq 1 50); do
    b64_encoded=$(base64 --decode <<< "$b64_encoded")
done

b64_decoded=$b64_encoded

echo "Decoded: $b64_decoded"