# [TryHackMe | Crack the hash](https://tryhackme.com/room/crackthehash) Challenge Room Solution Writeup

## General Approach Structure

- Create ```hashes.txt``` then manually append hashes and salts to it.
- Feed each hash through [HashID](https://pypi.org/project/hashID/) and cross-reference against the [Hashcat Wiki](https://hashcat.net/wiki/doku.php?id=example_hashes).
- Identification can be (partially) automated as follows with ```identify.sh``` seen below.

```bash
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
```

- Append modes to ```hashes.txt```, which finally should look like this.

```txt
0:MD5:48bb6e862e54f2a795ffc4e541caed4d:
100:SHA1:CBFDAC6008F9CAB4083784CBD1874F76618D2A97:
1400:SHA2-256:1C8BFE8F801D79745C4631D09FFF36C82AA37FC4CCE4FC946683D7B336B63032:
3200:bcrypt $2*$, Blowfish (Unix):$2y$12$Dwt1BZj6pcyc3Dy1FWZ5ieeUznr71EeNkJkUlypTsgbX1H68wsRom:
900:MD4:279412f945939ba78ce0758d3fd83daa:
1400:SHA2-256:F09EDCB1FCEFC6DFB23DC3505A882655FF77375ED8AA2D1C13F640FCCC2D0C85:
1000:NTLM:1DFECA0C002AE40B8619ECF94819CC1B:
1800:sha512crypt $6$, SHA512 (Unix) 2:$6$aReallyHardSalt$6WKUTqzq.UQQmrm0p/T7MPpMbGNnzXPMAXi4bJMl9be.cfi3/qxIf.hsGpS41BqMhSrHVXgMpdjS6xeKZAs02.:
160:HMAC-SHA1 (key = $salt):e5d8870e5bdd26602cab8dbe07a942c8669e56d6:tryhackme

```

- Feed ```hashes.txt``` through ```crack.sh``` seen below.

```bash
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
```

- View output in ```cracked.txt``` (see below) and manually cross-reference results against [CrackStation](https://crackstation.net/).
- Note that ```rockyou.txt``` does not have ```Eternity22``` and therefore ```hashcat``` will exhaust for ```279412f945939ba78ce0758d3fd83daa```.

```txt
48bb6e862e54f2a795ffc4e541caed4d:easy
cbfdac6008f9cab4083784cbd1874f76618d2a97:password123
1c8bfe8f801d79745c4631d09fff36c82aa37fc4cce4fc946683d7b336b63032:letmein
$2y$12$Dwt1BZj6pcyc3Dy1FWZ5ieeUznr71EeNkJkUlypTsgbX1H68wsRom:bleh
279412f945939ba78ce0758d3fd83daa:Eternity22
f09edcb1fcefc6dfb23dc3505a882655ff77375ed8aa2d1c13f640fccc2d0c85:paule
1dfeca0c002ae40b8619ecf94819cc1b:n63umy8lkf4i
$6$aReallyHardSalt$6WKUTqzq.UQQmrm0p/T7MPpMbGNnzXPMAXi4bJMl9be.cfi3/qxIf.hsGpS41BqMhSrHVXgMpdjS6xeKZAs02.:waka99
e5d8870e5bdd26602cab8dbe07a942c8669e56d6:tryhackme:481616481616
```

## [Task 1 Level 1](https://tryhackme.com/room/crackthehash?taskNo=1)

- From the aforementioned ```cracked.txt``` we have:

```txt
48bb6e862e54f2a795ffc4e541caed4d:easy
cbfdac6008f9cab4083784cbd1874f76618d2a97:password123
1c8bfe8f801d79745c4631d09fff36c82aa37fc4cce4fc946683d7b336b63032:letmein
$2y$12$Dwt1BZj6pcyc3Dy1FWZ5ieeUznr71EeNkJkUlypTsgbX1H68wsRom:bleh
279412f945939ba78ce0758d3fd83daa:Eternity22
```

## [Task 2 Level 2](https://tryhackme.com/room/crackthehash?taskNo=2)

- From the aforementioned ```cracked.txt``` we have:

```txt
f09edcb1fcefc6dfb23dc3505a882655ff77375ed8aa2d1c13f640fccc2d0c85:paule
1dfeca0c002ae40b8619ecf94819cc1b:n63umy8lkf4i
$6$aReallyHardSalt$6WKUTqzq.UQQmrm0p/T7MPpMbGNnzXPMAXi4bJMl9be.cfi3/qxIf.hsGpS41BqMhSrHVXgMpdjS6xeKZAs02.:waka99
e5d8870e5bdd26602cab8dbe07a942c8669e56d6:tryhackme:481616481616
```