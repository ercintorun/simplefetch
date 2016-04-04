# -*- coding: UTF-8 -*
import paramiko, logging, socket, time, re

line_break = " \n"
ios_any_cli_length = "terminal length 0"
vrp6_cli_length = "screen-length 0 temporary"
junos_cli_length = "set cli screen-length 0"

class SSH:
    def __init__( self, host, port, user, passwd, os):
		self.os = os
		self.host = str(host)+":"+str(port)
		self.connectionsuccess = False
		"""Connecting to Host"""
		try:
			self.ssh = paramiko.SSHClient()
			self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			logging.info("Connecting to "+self.host)
			self.ssh.connect(host, username=user, password=passwd, port=port, compress=True, allow_agent=False, look_for_keys=False, timeout=10)
			logging.info("Connected to "+self.host)
			
			"""Invoking Shell and Pagination"""
			try:
				self.chan = self.ssh.invoke_shell(width=255,width_pixels=0, height_pixels=0)
				time.sleep(2)
				resp = self.chan.recv(9999)
				if "failed" in resp:
					logging.warning ("connecting to "+ self.host + " failed, this log is send by the host:" +resp)
					raise ValueError("connecting to "+ self.host + " failed, this log is send by the host:" +resp)
					return
				self.prompt= re.sub('[><#]', '', resp.split()[-1])
			except:
				logging.warning("could not invoke a shell to %s" % self.host)
				raise ValueError("could not invoke a shell to %s" % self.host)
				return
			logging.info("Invoked a shell to %s , now sending pagination commands" % self.host)
 
			resp = ""
			buff = ""
			if os in ("cisco-ios" ,"cisco-nxos","cisco-iosxe","cisco-iosxr"):
				self.chan.send(ios_any_cli_length+line_break)
			elif os=="huawei-vrp6":
				self.chan.send(vrp6_cli_length+line_break)
			elif os=="junos":
				self.chan.send(junos_cli_length+line_break)
			else:
				logging.warning("device software type '%s' is unkown" % os)
				raise ValueError("device software type '%s' is unkown" % os)
				return	
			time.sleep(1)
			self.timeout_start = time.time()
			self.timeout = 10
			while buff.find(self.prompt) == -1:
				resp=self.chan.recv(9999)
				buff+= resp
				if time.time() > self.timeout_start + self.timeout:
					logging.warning("10 seconds timeout after sending terminal length command to %s" % self.host)
					return
			self.connectionsuccess = True

		except paramiko.ssh_exception.AuthenticationException:
			logging.warning("Authentication failure on "+self.host)
			raise ValueError("Authentication failure on "+self.host)
			return
		except socket.timeout:
			logging.warning("Timed out on "+self.host)
			raise ValueError("Authentication failure on "+self.host)
			return
		except socket.error:
			logging.warning("Connection refused on "+self.host)
			raise ValueError("Connection refused on "+self.host)
			return
			
    def fetchdata(self, cmd):
		if self.connectionsuccess:
			logging.info("running "+ str(cmd)+" on host "+self.host)
			resp = ""
			buff = ""
			if self.os in ("cisco-ios", "cisco-nxos", "cisco-iosxe", "huawei-vrp6", "cisco-iosxr", "junos"):
				self.chan.send(cmd+line_break)
				time.sleep(1)
				self.timeout_start = time.time()
				self.timeout = 40
				while buff.find(self.prompt) == -1:
					resp=self.chan.recv(9999)
					buff+= resp
					if time.time() > self.timeout_start + self.timeout:
						logging.warning("40 seconds timeout after sending command '"+str(cmd)+"' to %s" % self.host)
						raise ValueError("40 seconds timeout after sending command '"+str(cmd)+"' to %s" % self.host)
						return
				logging.info("["+self.host+"] > All initial commands ran.")
				return str(buff).split(self.prompt)[0].split(cmd)[-1]
			else:
				logging.warning("device software type '%s' is unkown" % os)
				raise ValueError("device software type '%s' is unkown" % os)
				return	
		else:
			logging.warning("No connection has been established to %s therefore command could not be executed" % self.host)
			return
			
    def disconnect (self):
		if self.connectionsuccess:	
			self.ssh.close()
			logging.info("["+self.host+"] < Disconnected")
		else:
			logging.warning("No connection exist to %s therefore no need to close" % self.host)
			raise ValueError("No connection exist to %s therefore no need to close" % self.host)
			return