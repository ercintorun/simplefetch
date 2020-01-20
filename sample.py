import simplefetch,logging
logging.basicConfig(filename='info.log', filemode='a', level=logging.INFO,
                    format='%(asctime)s [%(name)s] %(levelname)s (%(threadName)-10s): %(message)s')
					
test_router = simplefetch.SSH("192.168.1.1",22, "admin", "secret", "cisco-ios")
print (test_router.fetchdata("show version"))
test_router.disconnect() 

