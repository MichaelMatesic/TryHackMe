# [TryHackMe | Invite Only](https://tryhackme.com/room/invite-only) Challenge Room Solution Writeup

## [Task 1 Invite Only](https://tryhackme.com/room/invite-only?taskNo=1)

The following information will be used for investigation:
- Flagged IP: `101[.]99[.]76[.]120`
- Flagged SHA256 hash: `5d0509f68a9b7c415a726be75a078180e3f02e59866f193b0a99eee8e39c874f`

### What is the name of the file identified with the flagged SHA256 hash?

Search [VirusTotal](https://www.virustotal.com/gui/home/upload) for `5d0509f68a9b7c415a726be75a078180e3f02e59866f193b0a99eee8e39c874f` to find the name **syshelpers.exe**.

### What is the file type associated with the flagged SHA256 hash?

Navigate to Details > File type to find **Win32 EXE**.

### What are the execution parents of the flagged hash? List the names chronologically, using a comma as a separator. Note down the hashes for later use.

Navigate to Relations > Execution Parents to find **361GJX7J,installer.exe** with SHA-256 hashes `047c5eec0445746862710d20e50a5dd04510b7e625fa5c1f5d48ce078001c0de` and `fa102d4e3cfbe85f5189da70a52c1d266925f3efd122091cdc8fe0fc39033942`. 

### What is the name of the file being dropped? Note down the hash value for later use.

Navigate to Relations > Dropped Files to find **Aclient.exe** with SHA-256 hash `dd02c105809e4ca41a5489e585ba025eddb89a91703b73a566c9903e6406a08c`.

### Research the second hash in question 3 and list the four malicious dropped files in the order they appear (from up to down), separated by commas.

Search [VirusTotal](https://www.virustotal.com/gui/home/upload) for `fa102d4e3cfbe85f5189da70a52c1d266925f3efd122091cdc8fe0fc39033942`, then navigate to Relations > Dropped Files (and check the respective pages if necessary) to find **searchhost.exe,syshelpers.exe,nat.vbs,runsys.vbs** with SHA-256 hashes `59feea18dc45bbe2b9798c9549983d79cc4788a9a0dafe2b0a930c60c7d2d6d7`, `5d0509f68a9b7c415a726be75a078180e3f02e59866f193b0a99eee8e39c874f`, `87be7b4336367083ca9fcb1c7b9d0459659f2ffafde51f7236960f6032512409`,  and `cb567a26c9aa7b023bd713756035530e56330ea87c3adbd26c83a5c8dc1cf9b9`.

### Analyse the files related to the flagged IP. What is the malware family that links these files?

Search [VirusTotal](https://www.virustotal.com/gui/home/upload) for `101[.]99[.]76[.]120`, then navigate to Community > Comments to find **asyncrat**.

### What is the title of the original report where these flagged indicators are mentioned? Use Google to find the report.

Navigate to Community > Comments to find **[From Trust to Threat: Hijacked Discord Invites Used for Multi-Stage Malware Delivery](https://research.checkpoint.com/2025/from-trust-to-threat-hijacked-discord-invites-used-for-multi-stage-malware-delivery/)**.

### Which tool did the attackers use to steal cookies from the Google Chrome browser?

Reading the report reveals **ChromeKatz** as the tool used for cookie theft.

### Which phishing technique did the attackers use? Use the report to answer the question.

Reading the report reveals **ClickFix** as the technique used for phishing.

### What is the name of the platform that was used to redirect a user to malicious servers?

Reading the report reveals **Discord** as the platform used for redirection.