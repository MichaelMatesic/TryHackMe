# [TryHackMe | Snort Challenge - Live Attacks](https://tryhackme.com/room/snortchallenges2) Challenge Room Solution Writeup

## [Task 2 Scenario 1 | Brute-Force](https://tryhackme.com/room/snortchallenges2?taskNo=2)

Run `snort` in packet-sniffing mode for about a minute and save the log for inspection using `sudo snort -l.`. Then inspect the log using `sudo snort -r snort.log.XXXXXXXXXX -X`. Noticing repeated `SSH` attempts, filter the log accordingly using `sudo snort -r snort.log.XXXXXXXXXX -X 'tcp[13] & 2 != 0 and tcp[13] & 16 == 0`, which searches for `SYN` attempts and excludes `SYN ACK` responses. Doing so will reveal many packets like this:

```bash
=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

WARNING: No preprocessors configured for policy 0.
09/07-15:00:04.872488 ATTACKER_IP:46852 -> VICTIM_IP:22
TCP TTL:64 TOS:0x0 ID:23770 IpLen:20 DgmLen:60 DF
******S* Seq: 0x72ED7BF5  Ack: 0x0  Win: 0xF507  TcpLen: 40
TCP Options (5) => MSS: 8961 SackOK TS: 1884614478 0 NOP WS: 7 
0x0000: 02 6D 84 B4 B4 1B 02 67 7A 27 40 23 08 00 45 00  .m.....gz"'"@#..E.
0x0010: 00 3C 5C DA 40 00 40 06 48 8C 0A 0A F5 24 0A 0A  .<\.@.@.H....$..
0x0020: 8C 1D B7 04 00 16 72 ED 7B F5 00 00 00 00 A0 02  ......r.{.......
0x0030: F5 07 9A B4 00 00 02 04 23 01 04 02 08 0A 70 54  ........#.....pT
0x0040: EF 4E 00 00 00 00 01 03 03 07                    .N........

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
```

This is indicative of a brute-force `SSH` attack, which we can defend against with the following `snort` rule (run `nano local.rules` to write the rule into):

```bash
reject ip ATTACKER_IP.0/24 any <> VICTIM_IP.0/24 22 (msg:"Unauthorized SSH attempt";sid:1000001;rev:1;)
```

Now run `sudo snort -A full -c local.rules` for about a minute until the flag file appears on your `Desktop`.

### Stop the attack and get the flag (which will appear on your Desktop).

**THM{81b7fef657f8aaa6e4e200d616738254}**

### What is the name of the service under attack?

**SSH**

### What is the used protocol/port in the attack?

**TCP/22**

## [Task 3 Scenario 2 | Reverse-Shell](https://tryhackme.com/room/snortchallenges2?taskNo=3)

Run `snort` in packet-sniffing mode for about a minute and save the log for inspection using `sudo snort -l.`. Then inspect the log using `sudo snort -r snort.log.XXXXXXXXXX -X`. Notice the following sequence of packets:

```bash
=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

09/07-15:39:09.459796 ATTACKER_IP:54366 -> VICTIM_IP:4444
TCP TTL:64 TOS:0x0 ID:53196 IpLen:20 DgmLen:60 DF
******S* Seq: 0xCBC44D22  Ack: 0x0  Win: 0xF507  TcpLen: 40
TCP Options (5) => MSS: 8961 SackOK TS: 2359074715 0 NOP WS: 7 
0x0000: 02 15 8B 5C 4F EF 02 7C 9A 93 DF DD 08 00 45 00  ...\O..|......E.
0x0010: 00 3C CF CC 40 00 40 06 02 08 0A 0A C4 37 0A 0A  .<..@.@......7..
0x0020: 90 9C D4 5E 11 5C CB C4 4D 22 00 00 00 00 A0 02  ...^.\..M\"......
0x0030: F5 07 69 16 00 00 02 04 23 01 04 02 08 0A 8C 9C  ..i.....#.......
0x0040: 9F 9B 00 00 00 00 01 03 03 07                    ..........

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

WARNING: No preprocessors configured for policy 0.
09/07-15:39:09.471636 VICTIM_IP:4444 -> ATTACKER_IP:54366
TCP TTL:64 TOS:0x0 ID:0 IpLen:20 DgmLen:60 DF
***A**S* Seq: 0x4093A761  Ack: 0xCBC44D23  Win: 0xF4B3  TcpLen: 40
TCP Options (5) => MSS: 8961 SackOK TS: 1981242415 2359074715 NOP WS: 7 
0x0000: 02 7C 9A 93 DF DD 02 15 8B 5C 4F EF 08 00 45 00  .|.......\O...E.
0x0010: 00 3C 00 00 40 00 40 06 D1 D4 0A 0A 90 9C 0A 0A  .<..@.@.........
0x0020: C4 37 11 5C D4 5E 40 93 A7 61 CB C4 4D 23 A0 12  .7.\.^@..a..M#..
0x0030: F4 B3 E7 F0 00 00 02 04 23 01 04 02 08 0A 76 17  ........#.....v.
0x0040: 5C 2F 8C 9C 9F 9B 01 03 03 07                    \/........

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

09/07-15:39:09.482194 ATTACKER_IP:54366 -> VICTIM_IP:4444
TCP TTL:64 TOS:0x0 ID:53197 IpLen:20 DgmLen:52 DF
***A**** Seq: 0xCBC44D23  Ack: 0x4093A762  Win: 0x1EB  TcpLen: 32
TCP Options (3) => NOP NOP TS: 2359074715 1981242415 
0x0000: 02 15 8B 5C 4F EF 02 7C 9A 93 DF DD 08 00 45 00  ...\O..|......E.
0x0010: 00 34 CF CD 40 00 40 06 02 0F 0A 0A C4 37 0A 0A  .4..@.@......7..
0x0020: 90 9C D4 5E 11 5C CB C4 4D 23 40 93 A7 62 80 10  ...^.\..M#@..b..
0x0030: 01 EB 69 0E 00 00 01 01 08 0A 8C 9C 9F 9B 76 17  ..i...........v.
0x0040: 5C 2F                                            \/

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

WARNING: No preprocessors configured for policy 0.
WARNING: No preprocessors configured for policy 0.
WARNING: No preprocessors configured for policy 0.
09/07-15:39:09.505876 ATTACKER_IP:54366 -> VICTIM_IP:4444
TCP TTL:64 TOS:0x0 ID:53198 IpLen:20 DgmLen:134 DF
***AP*** Seq: 0xCBC44D23  Ack: 0x4093A762  Win: 0x1EB  TcpLen: 32
TCP Options (3) => NOP NOP TS: 2359074740 1981242415 
0x0000: 02 15 8B 5C 4F EF 02 7C 9A 93 DF DD 08 00 45 00  ...\O..|......E.
0x0010: 00 86 CF CE 40 00 40 06 01 BC 0A 0A C4 37 0A 0A  ....@.@......7..
0x0020: 90 9C D4 5E 11 5C CB C4 4D 23 40 93 A7 62 80 18  ...^.\..M#@..b..
0x0030: 01 EB 69 60 00 00 01 01 08 0A 8C 9C 9F B4 76 17  ..i\`..........v.
0x0040: 5C 2F 1B 5D 30 3B 75 62 75 6E 74 75 40 69 70 2D  \/.]0;ubuntu@ip-
0x0050: 31 30 2D 31 30 2D 31 39 36 2D 35 35 3A 20 7E 07  ATTACKER_IP: ~.
0x0060: 1B 5B 30 31 3B 33 32 6D 75 62 75 6E 74 75 40 69  .[01;32mubuntu@i
0x0070: 70 2D 31 30 2D 31 30 2D 31 39 36 2D 35 35 1B 5B  p-ATTACKER_IP.[
0x0080: 30 30 6D 3A 1B 5B 30 31 3B 33 34 6D 7E 1B 5B 30  00m:.[01;34m~.[0
0x0090: 30 6D 24 20                                      0m$ 

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

WARNING: No preprocessors configured for policy 0.
09/07-15:39:09.516443 VICTIM_IP:4444 -> ATTACKER_IP:54366
TCP TTL:64 TOS:0x0 ID:9999 IpLen:20 DgmLen:52 DF
***A**** Seq: 0x4093A762  Ack: 0xCBC44D75  Win: 0x1E9  TcpLen: 32
TCP Options (3) => NOP NOP TS: 1981242440 2359074740 
0x0000: 02 7C 9A 93 DF DD 02 15 8B 5C 4F EF 08 00 45 00  .|.......\O...E.
0x0010: 00 34 27 0F 40 00 40 06 AA CD 0A 0A 90 9C 0A 0A  .4"'".@.@.........
0x0020: C4 37 11 5C D4 5E 40 93 A7 62 CB C4 4D 75 80 10  .7.\.^@..b..Mu..
0x0030: 01 E9 26 51 00 00 01 01 08 0A 76 17 5C 48 8C 9C  ..&Q......v.\H..
0x0040: 9F B4                                            ..

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

WARNING: No preprocessors configured for policy 0.
09/07-15:39:09.526995 VICTIM_IP:4444 -> ATTACKER_IP:54366
TCP TTL:64 TOS:0x0 ID:9999 IpLen:20 DgmLen:52 DF
***A***F Seq: 0x4093A762  Ack: 0xCBC44D75  Win: 0x1E9  TcpLen: 32
TCP Options (3) => NOP NOP TS: 1981265127 2359074740 
0x0000: 02 7C 9A 93 DF DD 02 15 8B 5C 4F EF 08 00 45 00  .|.......\O...E.
0x0010: 00 34 27 0F 40 00 40 06 AA CD 0A 0A 90 9C 0A 0A  .4"'".@.@.........
0x0020: C4 37 11 5C D4 5E 40 93 A7 62 CB C4 4D 75 80 11  .7.\.^@..b..Mu..
0x0030: 01 E9 CD B0 00 00 01 01 08 0A 76 17 B4 E7 8C 9C  ..........v.....
0x0040: 9F B4                                            ..

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

WARNING: No preprocessors configured for policy 0.
09/07-15:39:09.538355 ATTACKER_IP:54366 -> VICTIM_IP:4444
TCP TTL:64 TOS:0x0 ID:9999 IpLen:20 DgmLen:57 DF
***AP*** Seq: 0xCBC44D75  Ack: 0x4093A763  Win: 0x1EB  TcpLen: 32
TCP Options (3) => NOP NOP TS: 2359097427 1981265127 
0x0000: 02 15 8B 5C 4F EF 02 7C 9A 93 DF DD 08 00 45 00  ...\O..|......E.
0x0010: 00 39 27 0F 40 00 40 06 AA C8 0A 0A C4 37 0A 0A  .9"'".@.@......7..
0x0020: 90 9C D4 5E 11 5C CB C4 4D 75 40 93 A7 63 80 18  ...^.\..Mu@..c..
0x0030: 01 EB 9C 15 00 00 01 01 08 0A 8C 9C F8 53 76 17  .............Sv.
0x0040: B4 E7 65 78 69 74 0A                             ..exit.

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

WARNING: No preprocessors configured for policy 0.
09/07-15:39:09.548914 ATTACKER_IP:54366 -> VICTIM_IP:4444
TCP TTL:64 TOS:0x0 ID:9999 IpLen:20 DgmLen:52 DF
***A***F Seq: 0xCBC44D7A  Ack: 0x4093A763  Win: 0x1EB  TcpLen: 32
TCP Options (3) => NOP NOP TS: 2359097427 1981265127 
0x0000: 02 15 8B 5C 4F EF 02 7C 9A 93 DF DD 08 00 45 00  ...\O..|......E.
0x0010: 00 34 27 0F 40 00 40 06 AA CD 0A 0A C4 37 0A 0A  .4"'".@.@......7..
0x0020: 90 9C D4 5E 11 5C CB C4 4D 7A 40 93 A7 63 80 11  ...^.\..Mz@..c..
0x0030: 01 EB 75 09 00 00 01 01 08 0A 8C 9C F8 53 76 17  ..u..........Sv.
0x0040: B4 E7                                            ..

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

WARNING: No preprocessors configured for policy 0.
09/07-15:39:09.557554 VICTIM_IP:4444 -> ATTACKER_IP:54366
TCP TTL:64 TOS:0x0 ID:9999 IpLen:20 DgmLen:40 DF
*****R** Seq: 0x4093A763  Ack: 0x0  Win: 0x0  TcpLen: 20
0x0000: 02 7C 9A 93 DF DD 02 15 8B 5C 4F EF 08 00 45 00  .|.......\O...E.
0x0010: 00 28 27 0F 40 00 40 06 AA D9 0A 0A 90 9C 0A 0A  .("'".@.@.........
0x0020: C4 37 11 5C D4 5E 40 93 A7 63 00 00 00 00 50 04  .7.\.^@..c....P.
0x0030: 00 00 79 47 00 00                                ..yG..

=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
```

This is indicative of a reverse-shell attack, which we can defend against with the following `snort` rule (run `nano local.rules` to write the rule into):

```bash
reject ip ATTACKER_IP.0/24 any <> VICTIM_IP.0/24 any (msg:"Known reverse-shell attacker";sid:1000001;rev:1;)
```

Note that unlike with the `SSH` attack (port `22`), the reverse-shell exploit can choose ports other than `4444`, so we cover them all with `any`.

Now run `sudo snort -A full -c local.rules` for about a minute until the flag file appears on your `Desktop`.

### Stop the attack and get the flag (which will appear on your Desktop)

**THM{0ead8c494861079b1b74ec2380d2cd24}**

### What is the used protocol/port in the attack?

**TCP/4444**

### Which tool is highly associated with this specific port number?

**Metasploit**