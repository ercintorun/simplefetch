# simplefetch
Simplified Paramiko Library to Fetch Data From MultiVendor Network Devices

# Supports

* Cisco IOS
* Cisco IOS-XE
* Cisco NX-OS
* Cisco IOS-XR
* Juniper Junos
* Huawei VRP5/8

Script is based on paramiko and catches device-prompt to understand the output is fetched, thus there is a strong possibility that script could work with many network devices from different vendors, i  only do not have the chance to test.

# Accepted Network Device OS Types
* huawei-vrp
* cisco-ios
* cisco-iosxe
* cisco-iosxr
* cisco-nxos
* junos
* dell-os10
* zte-zxros 
* ericsson-ipos
* nokia-sros

For the above device type pagination commands (e.g. "terminal length 0") send automatically. 

# Simple Example
```
import simplefetch

test_router = simplefetch.SSH("192.168.1.1", 22, "admin", "secret", "cisco-ios")
print test_router.fetchdata("show version")
test_router.disconnect()
```

# Example with Logging 

```
import simplefetch,logging
logging.basicConfig(filename='info.log', filemode='a', level=logging.INFO,
                    format='%(asctime)s [%(name)s] %(levelname)s (%(threadName)-10s): %(message)s')
					
test_router = simplefetch.SSH("192.168.1.1", 22, "admin", "secret", "cisco-ios")
print (test_router.fetchdata("show version"))
test_router.disconnect() 
```
# Example with Multithreading Python3

import simplefetch
import logging, time
from threading import Thread
timestr = time.strftime("%Y%m%d-%H%M%S")
log_filename="basarisiz_baglanti_loglari_"+str(timestr)+".txt"

logging.basicConfig(filename=log_filename, filemode='a', level=logging.INFO,
                    format='%(asctime)s [%(name)s] %(levelname)s (%(threadName)-10s): %(message)s')


username= "username"
password="password"
router_list=["router_name1","192.168.1.1"]

def get_memory_usages(router_name):
	try:
		connection = simplefetch.SSH(user=username, passwd=password, network_os="huawei-vrp")
		try:
			display_health_raw= connection.fetchdata("display startup")
			print (router_name)
			print (display_health_raw)
		except:
			logging.warning ("could not get output of command from %s",router_name)
			connection.disconnect()
	except:
		logging.warning ("connection unsuccessful to %s",router_name)


import concurrent.futures 
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor: 
	for items in router_list:
		executor.submit(get_memory_usages,items) 
executor.shutdown(wait=True)
