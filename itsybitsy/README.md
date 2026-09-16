# [TryHackMe | ItsyBitsy](https://tryhackme.com/room/itsybitsy) Challenge Room Solution Writeup

## [Task 2 | Scenario - Investigate a Potential C2 Communication Alert](https://tryhackme.com/room/itsybitsy?taskNo=2)

During normal SOC monitoring, Analyst John observed an alert on an IDS solution indicating a potential C2 communication from a user Browne from the HR department. A suspicious file was accessed containing a malicious pattern THM:{ ________ }. A week-long HTTP connection logs have been pulled to investigate. Due to limited resources, only the connection logs could be pulled out and are ingested into the connection_logs index in Kibana.

### How many events were returned for the month of March 2022?

Filtering the dates accordingly shows **1482** events.

### What is the IP associated with the suspected user in the logs?

Most logs are associated with another IP, but inspecting the logs for `source_ip:` **192.166.65.54** reveals suspicious activity.

### The user’s machine used a legit windows binary to download a file from the C2 server. What is the name of the binary?

The associated logs show `user_agent:` **bitsadmin**.

### The infected machine connected with a famous filesharing site in this period, which also acts as a C2 server used by the malware authors to communicate. What is the name of the filesharing site?

The associated logs show `host:` **pastebin.com**.

### What is the full URL of the C2 to which the infected host is connected?

The associated logs show `uri: /yTg0Ah6a`, from which **pastebin.com/yTg0Ah6a** may be reconstructed.

### A file was accessed on the filesharing site. What is the name of the file accessed?

Visiting the above [URL](https://pastebin.com/yTg0Ah6a) reveals a hosted file named **secret.txt**.

### The file contains a secret code with the format THM{_____}.

The file itself contains **THM{SECRET__CODE}**.