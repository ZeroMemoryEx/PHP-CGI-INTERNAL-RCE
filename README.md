# PHP-CGI-INTERNAL-RCE

<div align="center">
  <img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/cb74a312-7854-471f-ad94-11935f7ed4ae" />
</div>

##
* This PoC demonstrates how an attacker can chain [Orange Tsai's](https://x.com/orange_8361) `CVE-2024-4577` with DNS rebinding to achieve remote code execution on internal network infrastructure directly through the victim’s web browser. By bypassing `Same-Origin Policy (SOP)` and exploiting vulnerable `PHP-CGI` instances running on `local XAMPP servers`, internal development environments, or corporate networks, this attack enables full code execution on systems never intended to be exposed to the internet.

# BLOG 

* https://www.hackandhide.com/your-browser-is-now-your-enemy-delivering-php-rce-to-your-local-servers/

# Setup

* Register at [duckdns](https://www.duckdns.org/)
* Create a subdomain (e.g., example.duckdns.org)
* Note your DuckDNS token from the dashboard
* Configure server.py:

  ```python pythonPUBLIC_IP = "YOUR_PUBLIC_IP"           # Your server's public IP
  DUCKDNS_DOMAIN = "your-subdomain"      # Your DuckDNS subdomain
  DUCKDNS_TOKEN = "your-token-here"      # Your DuckDNS token  
  ```

* to configure a custom payload, locate this line in `client.html` and replace it with your payload.
  ```js
  const payload = `<?php system('calc');?>;echo 1337; die;`;
  ```
* Also, you can modify the list of IPs. As we explained in the article, if you want to implement internal network scanning, you can use the JavaScript snippet I showed there. In this PoC, I’ll be using a predefined list of common IPs to keep it simple and fast
  
##  Dependencies:
  * requests

# VIDEO

https://github.com/user-attachments/assets/90abef27-28d0-4473-88e9-5e285a5cc667

##
* It never needed to be offline… to be safe."
