import paramiko, logging, socket, time, re, datetime
import sys

python3_usage=True
if sys.version_info[0] < 3:
    python3_usage=False

"""
#v2.0 2020.01.20
#Written by Ercin TORUN
#automates ssh login using paramiko library

"""
#==================some variables
line_break = "\r"
ios_any_cli_length = "terminal length 0"
vrp_cli_length = "screen-length 0 temporary"
junos_cli_length = "set cli screen-length 0"
cli_prompt = ("#", ">")
MAX_BUFFER = 65535
#==================================
def get_command_results(channel, hostname):
	## http://joelinoff.com/blog/?p=905
	interval = 0.1
	maxseconds = 30
	maxcount = maxseconds / interval
	bufsize = 9192
	# Poll until completion or timeout
	# Note that we cannot directly use the stdout file descriptor
	# because it stalls at 64K bytes (65536).
	input_idx = 0
	timeout_flag = False
	start = datetime.datetime.now()
	start_secs = time.mktime(start.timetuple())
	output = ''
	channel.setblocking(0)
	while True:
		if channel.recv_ready():
			data = channel.recv(bufsize).decode('ascii')
			output += data
		if channel.exit_status_ready():
			break
		# Timeout check
		now = datetime.datetime.now()
		now_secs = time.mktime(now.timetuple())
		et_secs = now_secs - start_secs
		if et_secs > maxseconds:
			timeout_flag = True
			break
 
		rbuffer = output.rstrip(' ')
		if len(rbuffer) > 0 and hostname in rbuffer: ## got a Cisco command prompt
			time.sleep(0.5) #sometimes router returns hostname 2 times with an empty line, wait for a short time, example at bottom
			break
		time.sleep(0.200)
	if channel.recv_ready():
		data = channel.recv(bufsize)
		output += data.decode('ascii')

	return output
 
def send_command_and_get_response(channel, cmd, hostname):
	if not cmd.endswith("\n"):
		channel.send(cmd+"\n")
	else:
		channel.send(cmd)
	results = get_command_results(channel, hostname)
	results = results.split(hostname)[-0] # at the end of the output, an empty line with router name comes, remove it 
	results = results.split(cmd)[-1] #router returns the first command that is send, so split and do not display the command that is sent
	if results[-1:] in ["<","["]: #if router is huawei before router name there might be a string  < or [  e.g. <nw_rt_...>
		results = results[:-1]
	return results

class SSH:
	""" Simple shell to run a command on the host """
	def __init__(self, host, port, user, passwd, network_os=None):
		self.os=network_os
		self.host = host
		self.connectionsuccess = False
		self.port=port
		"""Connecting to Host"""
		try:
			self.ssh = paramiko.SSHClient()
			self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			logging.info("Connecting to host "+self.host)
			self.ssh.connect(self.host, username=user, password=passwd, port=self.port, allow_agent=False, look_for_keys=False, timeout=10)
			logging.info("Connected to host "+self.host)
			"""Invoking Shell and Pagination"""
			
			try: 
				self.chan = self.ssh.invoke_shell(width=255,width_pixels=0, height_pixels=0)		
				resp=self.chan.recv(MAX_BUFFER)
				if python3_usage:
					resp=resp.decode()
				if "failed" in resp:
					logging.warning ("connection failed, this log is send by the host:" +resp)
					raise ValueError("connection failed, this log is send by the host:" +resp)
					return	
			except: 
				logging.warning("could not invoke a shell to %s" % self.host)
				raise ValueError("could not invoke a shell to %s" % self.host)
				return
			self.prompt= re.sub('[><#]', '', resp.split()[-1])  #get device hostname
			logging.info("the router name connected is %s" % self.prompt)
			logging.info("Invoked a shell to %s , now sending pagination commands" % self.host)
			
			buff="" 
			resp=""
			
			if self.os in ("cisco-ios" ,"cisco-nxos","cisco-iosxe","cisco-iosxr"):
				send_command_and_get_response(self.chan,ios_any_cli_length, self.prompt)
			elif self.os=="huawei-vrp":
				send_command_and_get_response(self.chan,vrp_cli_length, self.prompt)
			elif self.os=="junos":
				send_command_and_get_response(self.chan,junos_cli_length, self.prompt)
			else:
				logging.info("device software type '%s' is unkown, no pagination command is send to device" % os)
				raise ValueError("device software type '%s' is unkown, no pagination command is send to device" % os)
				return			
	
			time.sleep(1)
			self.connectionsuccess = True			
	
		except paramiko.ssh_exception.AuthenticationException:
			logging.warning("Authentication failure on %s" % self.host)
			raise ValueError("Authentication failure on %s"% self.host)
			return
		except socket.timeout:
			logging.warning("Timed out on %s")
			raise ValueError("Authentication failure on %s" % self.host)
			return
		except socket.error:
			logging.warning("Connection refused on %s" % self.host)
			raise ValueError("Connection refused on %s" %self.host)
			return	

	def fetchdata(self, cmd):
		if self.connectionsuccess:
			logging.info("running "+ str(cmd)+" on host "+self.host)
			resp = ""
			buff = ""
			buff = send_command_and_get_response(self.chan,cmd,self.prompt)
			
			logging.info("["+self.host+"] > All initial commands ran.")

			return buff
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
