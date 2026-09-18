# [TryHackMe | Masterminds](https://tryhackme.com/room/mastermindsxlq) Challenge Room Solution Writeup

## [Task 2 | [Infection 1]](https://tryhackme.com/room/mastermindsxlq?taskNo=2)

Open `infection1.pcap` in `Brim`.

### Provide the victim's IP address.

Inspect `id.orig_h` to find **192[.]168[.]75[.]249**.

### The victim attempted to make HTTP connections to two suspicious domains with the status '404 Not Found'. Provide the hosts/domains requested. 

Query `status_code==404` to find **cambiasuhistoria[.]growlab[.]es,www[.]letscompareonline[.]com**.

### The victim made a successful HTTP connection to one of the domains and received the response_body_len of 1,309 (uncompressed content size of the data transferred from the server). Provide the domain and the destination IP address.

Query `status_code==200 and response_body_len==1309` to find **ww25[.]gocphongthe[.]com,199[.]59[.]242[.]153**.

### How many unique DNS requests were made to cab[.]myfkn[.]com domain (including the capitalized domain)? 

Click `Unique DNS Queries` to find **7** unique requests.

### Provide the URI of the domain bhaktivrind[.]com that the victim reached out over HTTP. 

Query `host=="bhaktivrind.com"` to find **/cgi-bin/JBbb8/**.

### Provide the IP address of the malicious server and the executable that the victim downloaded from the server. 

Query `.exe` to find **185[.]239[.]243[.]112,catzx[.]exe**.

### Based on the information gathered from the second question, provide the name of the malware using [VirusTotal (opens in new tab)](https://www.virustotal.com/gui/home/upload). 

Research the various domains to find multiple mentions of **Emotet**.

## [Task 2 | [Infection 2]](https://tryhackme.com/room/mastermindsxlq?taskNo=3)

Open `infection2.pcap` in `Brim`.

### Provide the IP address of the victim machine. 

Inspect `id.orig_h` to find **192[.]168[.]75[.]146**

### Provide the IP address the victim made the POST connections to. 

Click `HTTP Requests` to find **5[.]181[.]156[.]252**.

### How many POST connections were made to the IP address in the previous question?

From the previous query, **3**.

### Provide the domain where the binary was downloaded from. 

Query `.exe` to find **hypercustom[.]top**.

### Provide the name of the binary including the full URI.

From the previous query, **/jollion/apines[.]exe**.

### Provide the IP address of the domain that hosts the binary.

From the previous query, **45[.]95[.]203[.]28**.

### There were 2 Suricata "A Network Trojan was detected" alerts. What were the source and destination IP addresses? 

Click `Suricata Alerts by Source and Destination` to find **192[.]168[.]75[.]146,45[.]95[.]203[.]28**.

### Taking a look at .top domain in HTTP requests, provide the name of the stealer (Trojan that gathers information from a system) involved in this packet capture using [URLhaus Database (opens in new tab)](https://urlhaus.abuse.ch/). 

Research [http[:]//hypercustom[.]top/jollion/apines[.]exe on URLhaus](https://urlhaus.abuse.ch/url/1552560/) to find **Redline Stealer**.

## [Task 2 | [Infection 3]](https://tryhackme.com/room/mastermindsxlq?taskNo=4)

Open `infection3.pcapng` in `Brim`.

### Provide the IP address of the victim machine.

Inspect `id.orig_h` to find **192[.]168[.]75[.]232**

### Provide three C2 domains from which the binaries were downloaded (starting from the earliest to the latest in the timestamp)

Click `HTTP Requests` then read through to find **efhoahegue[.]ru,afhoahegue[.]ru,xfhoahegue[.]ru**.

### Provide the IP addresses for all three domains in the previous question.

From the previous query, **162[.]217[.]98[.]146,199[.]21[.]76[.]77,63[.]251[.]106[.]25**.

### How many unique DNS queries were made to the domain associated from the first IP address from the previous answer? 

Click `Unique DNS Queries` to find **2** unique requests.

### How many binaries were downloaded from the above domain in total? 

Query `host=="efhoahegue.ru"` to find **5** binaries.

### Provided the user-agent listed to download the binaries. 

From the previous query, **Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0**.

### Provide the amount of DNS connections made in total for this packet capture.

Query `_path=="dns" | count()` to find **986**.

### With some OSINT skills, provide the name of the worm using the first domain you have managed to collect from Question 2. (Please use quotation marks for Google searches, don't use .ru in your search, and DO NOT interact with the domain directly).

Research [efhoahegue[.]ru on VirusTotal](https://www.virustotal.com/gui/domain/efhoahegue.ru/) to find **Phorphiex**.