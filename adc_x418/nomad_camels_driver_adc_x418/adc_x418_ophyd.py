from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.custom_function_signal import Custom_Function_Signal, Custom_Function_SignalRO
from ophyd import Device
import socket
import re
import json
import base64
import time
from functools import partial
import tkinter as tk
from tkinter import simpledialog

class Adc_X418(Device):
	sleep_time = 0.05

	read_channel_1 = Cpt(
		Custom_Function_SignalRO,
		name="read_channel_1",
		metadata={"units": "V", "description": "Read value measured at channel 1"},
	)

	read_channel_2 = Cpt(
		Custom_Function_SignalRO,
		name="read_channel_2",
		metadata={"units": "V", "description": "Read value measured at channel 2"},
	)

	read_channel_3 = Cpt(
		Custom_Function_SignalRO,
		name="read_channel_3",
		metadata={"units": "V", "description": "Read value measured at channel 3"},
	)

	read_channel_4 = Cpt(
		Custom_Function_SignalRO,
		name="read_channel_4",
		metadata={"units": "V", "description": "Read value measured at channel 4"},
	)

	read_channel_5 = Cpt(
		Custom_Function_SignalRO,
		name="read_channel_5",
		metadata={"units": "V", "description": "Read value measured at channel 5"},
	)

	read_channel_6 = Cpt(
		Custom_Function_SignalRO,
		name="read_channel_6",
		metadata={"units": "V", "description": "Read value measured at channel 6"},
	)

	read_channel_7 = Cpt(
		Custom_Function_SignalRO,
		name="read_channel_7",
		metadata={"units": "V", "description": "Read value measured at channel 7"},
	)

	read_channel_8 = Cpt(
		Custom_Function_SignalRO,
		name="read_channel_8",
		metadata={"units": "V", "description": "Read value measured at channel 8"},
	)

	read_status_channel_1 = Cpt(
		Custom_Function_SignalRO,
		name="read_status_channel_1",
		metadata={"units": "", "description": "Read range of channel 1"},
	)

	read_status_channel_2 = Cpt(
		Custom_Function_SignalRO,
		name="read_status_channel_2",
		metadata={"units": "", "description": "Read range of channel 2"},
	)

	read_status_channel_3 = Cpt(
		Custom_Function_SignalRO,
		name="read_status_channel_3",
		metadata={"units": "", "description": "Read range of channel 3"},
	)

	read_status_channel_4 = Cpt(
		Custom_Function_SignalRO,
		name="read_status_channel_4",
		metadata={"units": "", "description": "Read range of channel 4"},
	)

	read_status_channel_5 = Cpt(
		Custom_Function_SignalRO,
		name="read_status_channel_5",
		metadata={"units": "", "description": "Read range of channel 5"},
	)

	read_status_channel_6 = Cpt(
		Custom_Function_SignalRO,
		name="read_status_channel_6",
		metadata={"units": "", "description": "Read range of channel 6"},
	)

	read_status_channel_7 = Cpt(
		Custom_Function_SignalRO,
		name="read_status_channel_7",
		metadata={"units": "", "description": "Read range of channel 7"},
	)

	read_status_channel_8 = Cpt(
		Custom_Function_SignalRO,
		name="read_status_channel_8",
		metadata={"units": "", "description": "Read range of channel 8"},
	)

	set_decimal_places_all_channels = Cpt(
		Custom_Function_Signal,
		name="set_decimal_places_all_channels",
        kind="config",
		metadata={"units": "", "description": "Set number of digits after . shown for all channels, max 4"},
	)

	set_range_channel_1 = Cpt(
		Custom_Function_Signal,
		name="set_range_channel_1",
        kind="config",
		metadata={"units": "", "description": "Set range of the channel 1"},
	)

	set_range_channel_2 = Cpt(
		Custom_Function_Signal,
		name="set_range_channel_2",
        kind="config",
		metadata={"units": "", "description": "Set range of the channel 2"},
	)

	set_range_channel_3 = Cpt(
		Custom_Function_Signal,
		name="set_range_channel_3",
        kind="config",
		metadata={"units": "", "description": "Set range of the channel 3"},
	)

	set_range_channel_4 = Cpt(
		Custom_Function_Signal,
		name="set_range_channel_4",
        kind="config",
		metadata={"units": "", "description": "Set range of the channel 4"},
	)

	set_range_channel_5 = Cpt(
		Custom_Function_Signal,
		name="set_range_channel_5",
        kind="config",
		metadata={"units": "", "description": "Set range of the channel 5"},
	)

	set_range_channel_6 = Cpt(
		Custom_Function_Signal,
		name="set_range_channel_6",
        kind="config",
		metadata={"units": "", "description": "Set range of the channel 6"},
	)

	set_range_channel_7 = Cpt(
		Custom_Function_Signal,
		name="set_range_channel_7",
        kind="config",
		metadata={"units": "", "description": "Set range of the channel 7"},
	)

	set_range_channel_8 = Cpt(
		Custom_Function_Signal,
		name="set_range_channel_8",
        kind="config",
		metadata={"units": "", "description": "Set range of the channel 8"},
	)

	def __init__(
		self,
		prefix="",
		*,
		name,
		kind=None,
		read_attrs=None,
		configuration_attrs=None,
		parent=None,
		host_ip="192.168.1.2",
        port=80,
        byte_length=10000,
		use_admin_credentials = True,
		user_password = False,
		**kwargs,
	):
		super().__init__(prefix=prefix,
			name=name,
			kind=kind,
			read_attrs=read_attrs,
			configuration_attrs=configuration_attrs,
			parent=parent,
			**kwargs,
		)
		self.host_ip = host_ip
		self.port = port
		self.byte_length = byte_length
		self.use_admin_credentials = use_admin_credentials
		self.user_password = user_password
		self.read_channel_1.read_function = partial(self.read_channel_n_read_function, channel_num=1)
		self.read_channel_2.read_function = partial(self.read_channel_n_read_function, channel_num=2)
		self.read_channel_3.read_function = partial(self.read_channel_n_read_function, channel_num=3)
		self.read_channel_4.read_function = partial(self.read_channel_n_read_function, channel_num=4)
		self.read_channel_5.read_function = partial(self.read_channel_n_read_function, channel_num=5)
		self.read_channel_6.read_function = partial(self.read_channel_n_read_function, channel_num=6)
		self.read_channel_7.read_function = partial(self.read_channel_n_read_function, channel_num=7)
		self.read_channel_8.read_function = partial(self.read_channel_n_read_function, channel_num=8)
		self.read_status_channel_1.read_function = partial(self.read_status_channel_n_read_function, channel_num=1)
		self.read_status_channel_2.read_function = partial(self.read_status_channel_n_read_function, channel_num=2)
		self.read_status_channel_3.read_function = partial(self.read_status_channel_n_read_function, channel_num=3)
		self.read_status_channel_4.read_function = partial(self.read_status_channel_n_read_function, channel_num=4)
		self.read_status_channel_5.read_function = partial(self.read_status_channel_n_read_function, channel_num=5)
		self.read_status_channel_6.read_function = partial(self.read_status_channel_n_read_function, channel_num=6)
		self.read_status_channel_7.read_function = partial(self.read_status_channel_n_read_function, channel_num=7)
		self.read_status_channel_8.read_function = partial(self.read_status_channel_n_read_function, channel_num=8)
		self.set_range_channel_1.put_function = partial(self.set_range_channel_n_put_function, channel_num=1)
		self.set_range_channel_2.put_function = partial(self.set_range_channel_n_put_function, channel_num=2)
		self.set_range_channel_3.put_function = partial(self.set_range_channel_n_put_function, channel_num=3)
		self.set_range_channel_4.put_function = partial(self.set_range_channel_n_put_function, channel_num=4)
		self.set_range_channel_5.put_function = partial(self.set_range_channel_n_put_function, channel_num=5)
		self.set_range_channel_6.put_function = partial(self.set_range_channel_n_put_function, channel_num=6)
		self.set_range_channel_7.put_function = partial(self.set_range_channel_n_put_function, channel_num=7)
		self.set_range_channel_8.put_function = partial(self.set_range_channel_n_put_function, channel_num=8)
		self.set_decimal_places_all_channels.put_function = self.set_decimal_places_all_channels_put_function

		# This if statement prevents the lines of the init below to be run when starting up CAMELS.
		if name == "test":
			return
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((self.host_ip, self.port))
		time.sleep(self.sleep_time)
		if self.use_admin_credentials:
			self.encoded_auth_str = self.check_authorization()
		else:
			print("Unable to change settings of ADC without admin credentials. All corresponding commands will be ignored. Use \'Configure Instruments\' dialog window to change this.")
		if self.user_password and not(self.use_admin_credentials):
			self.encoded_auth_str = self.check_authorization()

	def read_channel_n_read_function(self, channel_num):
		## request state.json file from ADC, then parse it to extract measured value at channel number 'channel_num'
		message = "GET /state.json HTTP/1.1\r\n"
		if self.use_admin_credentials or self.user_password:										## authorisation if needed
			message = message + "Authorization: Basic " + self.encoded_auth_str + "\r\n"
		message = message + "\r\n"
		self.sock.sendall(message.encode())
		time.sleep(self.sleep_time)																	## seems to have random problems from time to time if no waiting after sendall / recv
		response = self.sock.recv(self.byte_length)
		time.sleep(self.sleep_time)
		response_readable=response.decode()
		response_match = re.search(r'{.*?}', response_readable, re.DOTALL)							## searching for .json -like part of the response
		if response_match:
			response_dict = json.loads(response_match.group(0))
			reply = response_dict["analogInput"+str(channel_num)]
			return reply
		else:
			print(f"no json string received from X418")
			if len(response_readable.split())>1:
				code_http = response_readable.split()[1]
				print("ADC response code returned: " + code_http)
			return
	
	def read_status_channel_n_read_function(self, channel_num):
		## request full status file from ADC, then extract range of channel_num
		message = "GET /io.data?spc0_ioTypeID=9 HTTP/1.1\r\n"
		if self.use_admin_credentials or self.user_password:										## authorisation if needed
			message = message + "Authorization: Basic " + self.encoded_auth_str + "\r\n"
		message = message + "\r\n"
		self.sock.sendall(message.encode())
		time.sleep(self.sleep_time)
		response = self.sock.recv(self.byte_length)
		time.sleep(self.sleep_time)
		response_readable=response.decode()
		if len(response_readable.split())>1:
			code_http = response_readable.split()[1]
			if code_http != "200":
				print("ADC response code returned: " + code_http)
				return
		response_data = re.findall(r'\r\nenabled.*', response_readable, re.DOTALL)					## everything after header
		response_lines = response_data[0].splitlines(keepends=False)								## line 0 - names of the fields, line 1 - full of zeroes, lines 2 - 9 correspond to channels 1 - 8
		response_values = response_lines[2+channel_num].split(',')									## element number 44 describes the range
		if response_values[44] == '1':
			return 10.24
		elif response_values[44] == '2':
			return 5.12
		elif response_values[44] == '3':
			return 2.56
		elif response_values[44] == '4':
			return 1.28
		else:
			return 0

	def set_range_channel_n_put_function(self, value, channel_num):
		if not(self.use_admin_credentials):
			print("Can not change ADC range without admin credentials")
			return
		## choose range from available list by rounding up
		if value > 10.24:
			print("range can not be set that high; setting to max = 10.24V")
			value_range = '1'
		elif value > 5.12:
			value_range = '1'
		elif value > 2.56:
			value_range = '2'
		elif value > 1.28:
			value_range = '3'
		elif value > 0:
			value_range = '4'
		else:
			print("range can not be that low, setting to min = 1.28V")
			value_range = '4'
		## reading out current status
		message = "GET /io.data?spc0_ioTypeID=9 HTTP/1.1\r\n" + "Authorization: Basic " + self.encoded_auth_str + "\r\n\r\n"
		self.sock.sendall(message.encode())
		time.sleep(self.sleep_time)
		response = self.sock.recv(self.byte_length)
		time.sleep(self.sleep_time)
		## make new status string to send to ADC
		response_readable=response.decode()
		response_data = re.findall(r'\r\nenabled.*', response_readable, re.DOTALL)
		response_lines = response_data[0].splitlines(keepends=False)
		response_fields = response_lines[1].split(',')
		response_values = response_lines[2+channel_num].split(',')
		fields_index=[43, 0, 6, 44, 12, 9, 10, 11, 3, 1, 2]											##replace values for num 44 for range and num 12 for decimal places
		line_to_post = 'spc0_settingsTableNum=' + str(channel_num) + '&spc0_settingsTableType=4'
		for i in fields_index:
			if i == 44:
				line_to_post = line_to_post + '&'+'ios0_'+response_fields[i]+'='+value_range		## copying everything needed except for the range, which is replaced with the new one
			else:
				line_to_post = line_to_post + '&'+'ios0_'+response_fields[i]+'='+response_values[i].replace(' ', '+')
		## sending new status string
		message = "POST /ioUpdate.srv HTTP/1.1\r\n" + "Content-Type: application/x-www-form-urlencoded; charset=UTF-8\r\n" + "Content-Length: " + str(len(line_to_post)) + "\r\n" + "Authorization: Basic " + self.encoded_auth_str + "\r\n\r\n" + line_to_post
		self.sock.sendall(message.encode())
		time.sleep(self.sleep_time)
		response = self.sock.recv(self.byte_length)
		time.sleep(self.sleep_time)

	def set_decimal_places_all_channels_put_function(self, value=4):
		if not(self.use_admin_credentials):
			print("Can not change ADC settings without admin credentials")
			return
		## choose decimal place from available list
		if value > 4:
			print("number of digits can not be set that high; setting to max = 4")
			value_range = '4'
		elif value > 3:
			value_range = '4'
		elif value > 2:
			value_range = '3'
		elif value > 1:
			value_range = '2'
		elif value > 0:
			value_range = '1'
		elif value == 0:
			value_range = '0'
		else:
			print("number of digits can not be that low, setting to min = 0")
			value_range = '0'
		## reading out current status
		message = "GET /io.data?spc0_ioTypeID=9 HTTP/1.1\r\n" + "Authorization: Basic " + self.encoded_auth_str + "\r\n\r\n"
		self.sock.sendall(message.encode())
		time.sleep(self.sleep_time)
		response = self.sock.recv(self.byte_length)
		time.sleep(self.sleep_time)
		## make new status string to send to ADC
		response_readable=response.decode()
		response_data = re.findall(r'\r\nenabled.*', response_readable, re.DOTALL)
		response_lines = response_data[0].splitlines(keepends=False)
		response_fields = response_lines[1].split(',')
		fields_index=[43, 0, 6, 44, 12, 9, 10, 11, 3, 1, 2]											##replace values for num 44 for range and num 12 for decimal places
		for j in range(1,9):
			response_values = response_lines[2+j].split(',')
			line_to_post = 'spc0_settingsTableNum=' + str(j) + '&spc0_settingsTableType=4'
			for i in fields_index:
				if i == 12:
					line_to_post = line_to_post + '&'+'ios0_'+response_fields[i]+'='+value_range
				else:
					line_to_post = line_to_post + '&'+'ios0_'+response_fields[i]+'='+response_values[i].replace(' ', '+')
			## sending new status string
			message = "POST /ioUpdate.srv HTTP/1.1\r\n" + "Content-Type: application/x-www-form-urlencoded; charset=UTF-8\r\n" + "Content-Length: " + str(len(line_to_post)) + "\r\n" + "Authorization: Basic " + self.encoded_auth_str + "\r\n\r\n" + line_to_post
			self.sock.sendall(message.encode())
			time.sleep(self.sleep_time)
			response = self.sock.recv(self.byte_length)
			time.sleep(self.sleep_time)

	def check_authorization(self):
		max_num_attempts = 5
		for i in range(1,max_num_attempts+1):
			## request credentials
			username, password = self.get_credentials()
			if not((isinstance(username, str)) and (isinstance(password, str))):
				print("Unexpected failure acquiring login and/or password")
				return
			encoded_auth_str = self.authorization_str(username, password)
			## if user == admin, try getting time from the device (for whatever reason, requires admin credentials)
			## if user == user, try reading some data
			if self.use_admin_credentials:
				message = "GET /date-time.json HTTP/1.1\r\n" + "Authorization: Basic " + encoded_auth_str + "\r\n\r\n"
			else:
				message = "GET /state.json HTTP/1.1\r\n" + "Authorization: Basic " + encoded_auth_str + "\r\n\r\n"
			self.sock.sendall(message.encode())
			time.sleep(self.sleep_time)
			response = self.sock.recv(self.byte_length)
			time.sleep(self.sleep_time)
			## parse ADC response and check if the credentials are OK from returned http code in the header
			response_readable=response.decode().split()
			if len(response_readable) < 2:
				print("failed to receive parseable response from ADC")
				return
			code_http = response_readable[1]
			if code_http == "200":																	## 200 = OK
				return encoded_auth_str
			elif (code_http == "401") or (code_http == "403"):										## 401 = unauthorized, 403 = forbidden
				print("ADC response: " + code_http)
				continue
			else:
				print("Unexpected response from ADC")
				return
		if (code_http == "401") or (code_http == "403"):
			print("Authentication failed")
			return
		return encoded_auth_str

	def get_credentials(self):
    	## Create the root window
		root_window = tk.Tk()
		root_window.withdraw()  # Hide the root window
		## Get password, choose username (three fixed options are available in X418, ignoring option "manager" as it is not different from "user" for our purposes)
		# username = simpledialog.askstring("Login", "Enter login for ADC X418:", initialvalue="admin")
		if self.use_admin_credentials:
			username = "admin"
			password = simpledialog.askstring("Password", "Enter admin password for ADC X418:", show='*')
		else:
			username = "user"
			password = simpledialog.askstring("Password", "Enter user password for ADC X418:", show='*')
		root_window.destroy()
		return username, password

	def authorization_str(self, username, password):
		authorization_str_input = username + ":" + password
		encoded_str = base64.b64encode(authorization_str_input.encode())
		return encoded_str.decode()
	
	def finalize_steps(self):
		self.sock.close()
		time.sleep(self.sleep_time)