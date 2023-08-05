# Vats_Proxy
Free Proxy library for Python to use with requests library.

### Installation
```
pip install vats_proxy
```

### Get started
How to initiate ProxyManager and Use it:

```Python
from vats_proxy import ProxyManager

# Initialize Manager
proxy_manager = ProxyManager(count=1)

# Make request with proxy
proxy = proxy_manager.proxies.pop()
request = requests.get("https://google.com", proxies=proxy)

```