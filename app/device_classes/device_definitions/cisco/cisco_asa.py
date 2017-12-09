from ..cisco_base_device import CiscoBaseDevice

class CiscoASA(CiscoBaseDevice):

	def cmd_run_config(self):
		command = 'show running-config'
		return command

	def cmd_start_config(self):
		command = 'show startup-config'
		return command

	def cmd_cdp_neighbor(self):
		command = ''
		return command

	def pull_run_config(self): #required
		command = self.cmd_run_config()
		return self.get_cmd_output(command)

	def pull_start_config(self): #required
		command = self.cmd_start_config()
		return self.get_cmd_output(command)

	def pull_cdp_neighbor(self): #required
		command = self.cmd_cdp_neighbor()
		return self.get_cmd_output(command)

	def pull_interface_config(self):
		command = "show run interface %s | exclude configuration|!" % (self.interface)
		return self.get_cmd_output(command)

	# Not supported on ASA's
	def pull_interface_mac_addresses(self):
		return ''

	def pull_interface_statistics(self):
		command = "show interface %s" % (self.interface)
		return self.get_cmd_output(command)

	def pull_interface_info(self):
		intConfig = self.pull_interface_config()
		intMac = self.pull_interface_mac_addresses()
		intStats = self.pull_interface_statistics()

		return intConfig, intMac, intStats

	def pull_device_uptime(self):
		command = 'show version | include up'
		return self.get_cmd_output(command)
		for x in uptime:
			if 'failover' in x:
				break
			else:
				uptimeOutput = x.split(' ', 2)[-1]
		return output

	def pull_host_interfaces(self):
		command = "show ip interface brief"
		result = self.run_ssh_command(command)
		# Returns False if nothing was returned
		if not result:
			return result
		return self.split_on_newline(self.cleanup_ios_output(result))

	def count_interface_status(self, interfaces): #required
		up, down, disabled, total = 0
		for interface in interfaces:
			if not 'Interface' in interface:
				if 'administratively down,down' in interface:
					disabled += 1
				elif 'down,down' in interface:
					down += 1
				elif 'up,down' in interface:
					down += 1
				elif 'up,up' in interface:
					up += 1
				elif 'manual deleted' in interface:
					total -= 1

				total += 1

		return up, down, disabled, total
		
