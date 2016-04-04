# simplefetch
Simplified Paramiko Library to Fetch Data From MultiVendor Network Devices

# Supports

* Cisco IOS
* Cisco IOS-XE
* Cisco NX-OS
* Cisco IOS-XR
* Juniper Junos

Script is based on paramiko and catches device-prompt to understand the output is fetched, thus there is a strong possibility that script could work with many network devices from different vendors, i  only do not have the chance to test.

# Accepted Network Device OS Types
* huawei-vrp6
* cisco-ios
* cisco-iosxe
* cisco-iosxr
* cisco-nxos
* junos

# Simple Example
```
import simplefetch, logging

logging.basicConfig(filename='warning.log', filemode='a', level=logging.WARNING,
                    format='%(asctime)s [%(name)s] %(levelname)s (%(threadName)-10s): %(message)s')
					
test_router = simplefetch.SSH("192.168.1.0", 22, "admin", "secret", "cisco-ios")
print test_router.fetchData("show version")
test_router.disconnect()
```
