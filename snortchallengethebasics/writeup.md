# [TryHackMe | Snort Challenge - The Basics](https://tryhackme.com/room/snortchallenges1) Challenge Room Solution Writeup

## [Task 1 Introduction](https://tryhackme.com/room/snortchallenges1?taskNo=1)

## [Task 2 Writing IDS Rules (HTTP)](https://tryhackme.com/room/snortchallenges1?taskNo=2)

### Write a rule to detect all TCP packets from or to port 80.

Use `nano` to add the following rule to `local.rules`:
```bash
alert tcp any any <> any 80 (msg:  "TCP traffic involving port 80"; sid: 100002; rev: 1;)
```

Use `snort` with the following arguments (`-l ./` tells `snort` to save in the current working directory):
```bash
sudo snort -c local.rules -r mx-3.pcap -l ./
```

- What is the number of detected packets you got?

    **164** 

To answer the remaining questions of this task, use `snort` to read the saved log:
```bash
sudo snort -r snort.log.XXXXXXXXXX -n 65
```

- What is the destination address of packet 63? 

    **216.239.59.99**

- What is the ACK number of packet 64? 

    **0x2E6B5384**

- What is the SEQ number of packet 62? 

    **0x36C21E28**

- What is the TTL of packet 65? 

    **128**

- What is the source IP of packet 65? 

    **145.254.160.237**

- What is the source port of packet 65? 

    **3372**

## [Task 3 Writing IDS Rules (FTP)](https://tryhackme.com/room/snortchallenges1?taskNo=3)

### Write a single rule to detect "all TCP port 21"  traffic in the given pcap.

Use `nano` to add the following rule to `local.rules`:
```bash
alert tcp any any <> any 21 (msg: "TCP traffic involving port 21"; sid: 100003; rev: 1;)
```

Use `snort` with the following arguments:
```bash
sudo snort -c local.rules -r ftp-png-gif.pcap -l ./
```

- What is the number of detected packets?

    **307** 

Use `grep` with the following arguments:
```bash
grep -a -i ftp ftp-png-gif.pcap
``` 

- What is the FTP service name?

    **Microsoft FTP Service**

### Write a rule to detect failed FTP login attempts in the given pcap.

Use `nano` to add the following rule to `local.rules`:
```bash
alert tcp any 21 -> any any (msg: "FTP failed login attempt"; content: "530"; sid: 100003; rev: 1;)
```

Use `snort` with the following arguments:
```bash
sudo snort -c local.rules -r ftp-png-gif.pcap -l ./
```

- What is the number of detected packets?

    **41**

### Write a rule to detect successful FTP logins in the given pcap.

Use `nano` to add the following rule to `local.rules`:
```bash
alert tcp any 21 -> any any (msg: "FTP successful login"; content: "230"; sid: 100003; rev: 1;)
```

Use `snort` with the following arguments:
```bash
sudo snort -c local.rules -r ftp-png-gif.pcap -l ./
```

- What is the number of detected packets?

    **1**

### Write a rule to detect FTP login attempts with a valid username but no password entered yet.

Use `nano` to add the following rule to `local.rules`:
```bash
alert tcp any 21 -> any any (msg: "FTP valid username, password not yet entered"; content: "331"; sid: 100003; rev: 1;)
```

Use `snort` with the following arguments:
```bash
sudo snort -c local.rules -r ftp-png-gif.pcap -l ./
```

- What is the number of detected packets?

    **42**

### Write a rule to detect FTP login attempts with the "Administrator" username but no password entered yet.

Use `nano` to add the following rule to `local.rules`:
```bash
alert tcp any 21 -> any any (msg: "FTP Administrator username, password not yet entered"; content: "331"; content: "Administrator"; sid: 100003; rev: 1;)
```

Use `snort` with the following arguments:
```bash
sudo snort -c local.rules -r ftp-png-gif.pcap -l ./
```

- What is the number of detected packets?

    **7**

## [Task 4 Writing IDS Rules (PNG)](https://tryhackme.com/room/snortchallenges1?taskNo=4)

### Write a rule to detect the PNG file in the given pcap.

Use `nano` to add the following rule to `local.rules` (wrapping the PNG magic number/file signature of `89 50 4E 47 0D 0A 1A 0A` with `|` tells `snort` to parse for the hex byte sequence):
```bash
alert tcp any any <> any any (msg: "PNG file detected"; content: "|89 50 4E 47 0D 0A 1A 0A|"; sid: 100004; rev: 1)
```

Use the `-X` argument to display the packet payload:
```bash
sudo snort -r snort.log.XXXXXXXXXX -X
```

- Investigate the logs and identify the software name embedded in the packet.

    **Adobe ImageReady**

### Write a rule to detect the GIF file in the given pcap.

Use `nano` to add the following rule to `local.rules`:
```bash
alert tcp any any <> any any (msg: "GIF file detected"; content: "|47 49 46 38|"; sid: 100004; rev: 1)
```

Use the `-X` argument to display the packet payload:
```bash
sudo snort -r snort.log.XXXXXXXXXX -X
```

- Investigate the logs and identify the image format embedded in the packet.

    **GIF89a**

## [Task 5 Writing IDS Rules (Torrent Metafile)](https://tryhackme.com/room/snortchallenges1?taskNo=5)

### Write a rule to detect the torrent metafile in the given pcap.

Use `nano` to add the following rule to `local.rules`:
```bash
alert tcp any any <> any any (msg: "Torrent metafile detected"; content: ".torrent"; sid: 100005; rev: 1;)
```

Use `snort` with the following arguments:
```bash
sudo snort -c local.rules -r torrent.pcap -l ./
```

- What is the number of detected packets?

    **2**

Use the `-X` argument to display the packet payload:
```bash
sudo snort -r snort.log.XXXXXXXXXX -X
```
- What is the name of the torrent application?

    **bittorrent**

- What is the MIME (Multipurpose Internet Mail Extensions) type of the torrent metafile?

    **application/x-bittorrent**

- What is the hostname of the torrent metafile?

    **tracker2.torrentbox.com**

## [Task 6 Troubleshooting Rule Syntax Errors](https://tryhackme.com/room/snortchallenges1?taskNo=6)

### Fix the syntax error in local-1.rules file and make it work smoothly.

Use `nano` to change the following rule in `local-1.rules` from
```bash
alert tcp any 3372 -> any any(msg: "Troubleshooting 1"; sid: 1000001; rev: 1;)
```
to
```bash
alert tcp any 3372 -> any any (msg: "Troubleshooting 1"; sid: 1000001; rev: 1;)
```
fixing the missing space between `any` and `(`.

Use `snort` with the following arguments:
```bash
sudo snort -c local-1.rules -r mx-1.pcap -l ./
```

- What is the number of the detected packets?

    **16**

### Fix the syntax error in local-2.rules file and make it work smoothly.

Use `nano` to change the following rule in `local-2.rules` from
```bash
alert icmp any -> any any (msg: "Troubleshooting 2"; sid: 1000001; rev: 1;)
```
to
```bash
alert icmp any any -> any any (msg: "Troubleshooting 2"; sid: 1000001; rev: 1;)
```
fixing the missing source `any` even though ICMP doesn't use ports.

Use `snort` with the following arguments:
```bash
sudo snort -c local-2.rules -r mx-1.pcap -l ./
```

- What is the number of the detected packets?

    **16**

### Fix the syntax error in local-3.rules file and make it work smoothly.

Use `nano` to change the following rule in `local-3.rules` from
```bash
alert icmp any any -> any any (msg: "ICMP Packet Found"; sid: 1000001; rev: 1;)
alert tcp any any -> any 80,443 (msg: "HTTPX Packet Found"; sid: 1000001; rev: 1;)
```
to
```bash
alert icmp any any -> any any (msg: "ICMP Packet Found"; sid: 1000001; rev: 1;)
alert tcp any any -> any 80,443 (msg: "HTTPX Packet Found"; sid: 1000002; rev: 1;)
```
fixing the duplicate sid.

Use `snort` with the following arguments:
```bash
sudo snort -c local-3.rules -r mx-1.pcap -l ./
```

- What is the number of the detected packets?

    **87**

### Fix the syntax error in local-4.rules file and make it work smoothly.

Use `nano` to change the following rule in `local-4.rules` from
```bash
alert icmp any any -> any any (msg: "ICMP Packet Found"; sid: 1000001; rev: 1;)
alert tcp any 80,443 -> any any (msg: "HTTPX Packet Found": sid: 1000001; rev: 1;)
```
to
```bash
alert icmp any any -> any any (msg: "ICMP Packet Found"; sid: 1000001; rev: 1;)
alert tcp any 80,443 -> any any (msg: "HTTPX Packet Found"; sid: 1000002; rev: 1;)
```
fixing the `:`-`;` mismatch and duplicate sid.

Use `snort` with the following arguments:
```bash
sudo snort -c local-4.rules -r mx-1.pcap -l ./
```

- What is the number of the detected packets?

    **90**

### Fix the syntax error in local-5.rules file and make it work smoothly.

Use `nano` to change the following rule in `local-5.rules` from
```bash
alert icmp any any <> any any (msg: "ICMP Packet Found"; sid: 1000001; rev: 1;)
alert icmp any any <- any any (msg: "Inbound ICMP Packet Found"; sid; 1000002; rev: 1;)
alert tcp any any -> any 80,443 (msg: "HTTPX Packet Found": sid: 1000003; rev: 1;)
```
to
```bash
alert icmp any any <> any any (msg: "ICMP Packet Found"; sid: 1000001; rev: 1;)
alert icmp any any -> any any (msg: "Inbound ICMP Packet Found"; sid: 1000002; rev: 1;)
alert tcp any any -> any 80,443 (msg: "HTTPX Packet Found"; sid: 1000003; rev: 1;)
```
fixing the inbound direction error and `:`-`;` mismatches.

Use `snort` with the following arguments:
```bash
sudo snort -c local-5.rules -r mx-1.pcap -l ./
```

- What is the number of the detected packets?

    **155**

### Fix the logical error in local-6.rules file and make it work smoothly to create alerts.

Use `nano` to change the following rule in `local-6.rules` from
```bash
alert tcp any any <> any 80  (msg: "GET Request Found"; content: "|67 65 74|"; sid: 100001; rev: 1;)
```
to
```bash
alert tcp any any <> any 80  (msg: "GET Request Found"; content: "|47 45 54|"; sid: 100001; rev: 1;)
```
fixing the lower case hex for "get" to upper case hex for "GET".

Use `snort` with the following arguments:
```bash
sudo snort -c local-6.rules -r mx-1.pcap -l ./
```

- What is the number of the detected packets?

    **2**

### Fix the logical error in local-7.rules file and make it work smoothly to create alerts.

Use `nano` to change the following rule in `local-7.rules` from
```bash
alert tcp any any <> any 80  (content:"|2E 68 74 6D 6C|"; sid: 100001; rev: 1;)
```
to
```bash
alert tcp any any <> any 80 (msg: ".html detected"; content: "|2E 68 74 6D 6C|"; sid: 100001; rev:1;)
```
fixing the extra space between `80` and `(` as well as the missing `msg` parameter.

Use `snort` with the following arguments:
```bash
sudo snort -c local-7.rules -r mx-1.pcap -l ./
```

- What is the name of the required option:

    **msg**

## [Task 7 Using External Rules (MS17-010)](https://tryhackme.com/room/snortchallenges1?taskNo=7)


```bash

```

## [Task 8 Using External Rules (Log4j)](https://tryhackme.com/room/snortchallenges1?taskNo=8)


```bash

```

## [Task 9 Conclusion](https://tryhackme.com/room/snortchallenges1?taskNo=9)


```bash

```