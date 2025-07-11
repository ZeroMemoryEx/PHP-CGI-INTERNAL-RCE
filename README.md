# PHP-CGI-INTERNAL-RCE

* This PoC demonstrates how an attacker can chain [Orange Tsai's](https://x.com/orange_8361) `CVE-2024-4577` with DNS rebinding to achieve remote code execution on internal network infrastructure directly through the victim’s web browser. By bypassing `Same-Origin Policy (SOP)` and exploiting vulnerable `PHP-CGI` instances running on `local XAMPP servers`, internal development environments, or corporate networks, this attack enables full code execution on systems never intended to be exposed to the internet.

# VIDEO



https://github.com/user-attachments/assets/90abef27-28d0-4473-88e9-5e285a5cc667


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

##  Dependencies:
  * requests

