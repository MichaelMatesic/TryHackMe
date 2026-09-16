# [TryHackMe | Dunkle Materie](https://tryhackme.com/room/dunklematerieptxc9) Challenge Room Solution Writeup

## [Task 1 | Ransomware Investigation](https://tryhackme.com/room/dunklematerieptxc9?taskNo=1)

Run `C:\Users\Administrator\Desktop\procdot_1_22_57_windows\win64\procdot.exe`, load `C:\Users\Administrator\Desktop\Analysis Files\Logfile.CSV` into the `Procmon` variable and `C:\Users\Administrator\Desktop\Analysis Files\traffic.pcap` into the `Windump` variable. 

### Provide the two PIDs spawned from the malicious executable. (In the order as they appear in the analysis tool)

Click the three dots under `Render Configuration` then notice the suspicious process `exploreer.exe`. Two `PID`s are associated with this: **8644,7128**.

### Provide the full path where the ransomware initially got executed? (Include the full path in your answer)

By selecting `PID` `7128` for `exploreer.exe` in the `Render Configuration` popup from the previous question, then allowing `ProcDot` to refresh, a graph will appear. Search this graph for the red box showing the execution path associated with this process: **c:\users\sales\appdata\local\temp\exploreer.exe**.

### This ransomware transfers the information about the compromised system and the encryption results to two domains over HTTP POST. What are the two C2 domains? (no space in the answer)

On the same graph as the previous question, searching the blue bubbles will reveal two suspicious domains associated with `exploreer.exe` `PID` `7128`: **mojobiden.com,paymenthacks.com**.

### What are the IPs of the malicious domains? (no space in the answer)

From the previous question, their `IP`s are **146.112.61.108,206.188.197.206**.

### Provide the user-agent used to transfer the encrypted data to the C2 channel. 

Open `C:\Users\Administrator\Desktop\Analysis Files\traffic.pcap` with `WireShark`. Run the search `http.host contains "mojobiden.com" || http.host contains "paymenthacks.com"` then investigate the POST request packet for the `User-Agent` field: **Firefox/89.0**.

### Provide the cloud security service that blocked the malicious domain. 

Now run the search `http.response.code==403` and investigate the packet for the `Server` field: **Cisco Umbrella**. This makes sense since Cisco also appeared in the `ProcDot` graph from the earlier `PID` investigation. 

### Provide the name of the bitmap that the ransomware set up as a desktop wallpaper. 

Returning to the `ProcDot` graph, search the connected yellow boxes for `HKCU\Control Panel\Desktop\Wallpaper` then right click for details. Viewing the data field shows **LEY9kpI9R.bmp**.

### Find the PID (Process ID) of the process which attempted to change the background wallpaper on the victim's machine.

From the graph the associated `PID` is **4892**.

### The ransomware mounted a drive and assigned it the letter. Provide the registry key path to the mounted drive, including the drive letter.

Searching the graph's connected yellow boxes reveals **HKLM\SYSTEM\MountedDevices\DosDevices\Z:**.

### Now you have collected some IOCs from this investigation. Provide the name of the ransomware used in the attack. (external research required)

Searching [VirusTotal](https://www.virustotal.com/gui/home/upload) for mojobiden[.]com and paymenthacks[.]com reveal many results about **BlackMatter Ransomware**.