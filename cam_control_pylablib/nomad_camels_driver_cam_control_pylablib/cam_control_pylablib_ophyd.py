from ophyd import Component as Cpt
from ophyd import Device
import socket
import re
import numpy as np
import time
import json
from nomad_camels.bluesky_handling.custom_function_signal import \
    Custom_Function_Signal, Custom_Function_SignalRO


class Cam_Control_Pylablib(Device):
    # host_ip = Cpt(Custom_Function_Signal, name='host_ip',
    #               kind='config', metadata={'description': 'Host IP given in the settings.cfg file.'})
    # port = Cpt(Custom_Function_Signal, name='port',
    #            kind='config', metadata={'description': 'Port given in the settings.cfg file.'})
    # byte_length = Cpt(Custom_Function_Signal, name='byte_length',
    #                   kind='config', metadata={'description': 'Maximum byte length that can be read.'})
    exposure_time = Cpt(Custom_Function_Signal, name='exposure_time',
                        kind='config', metadata={'unit': 'ms',
                                                 'description': 'Camera exposure time in ms.'})

    get_single_frame = Cpt(Custom_Function_SignalRO, name='get_single_frame',
                           metadata={'description': 'Get data of single frame with parameters of the GUI.'})
    get_background_frame = Cpt(Custom_Function_SignalRO, name='get_background_frame',
                               metadata={'description': 'Get data of background frame with parameters of the GUI.'})

    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None,
                 host_ip='127.0.0.1',
                 port=18923,
                 byte_length=9000000,
                 read_wait=1000,
                 **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind,
                         read_attrs=read_attrs,
                         configuration_attrs=configuration_attrs, parent=parent,
                         **kwargs)
        self.host_ip = host_ip
        self.port = port
        self.byte_length = byte_length
        self.read_wait = float(read_wait)/1000
        self.exposure_time.put_function = lambda x: self.exposure_time_function(exposure_time=x)
        self.get_single_frame.read_function = self.get_single_frame_function
        self.get_background_frame.read_function = self.get_background_frame_function

        # This if statement prevents the lines of the init below to be run when starting up CAMELS.
        if name == 'test':
            return
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host_ip, self.port))
        self.sock.sendall(bytes(
            r'{    "id": 0,    "purpose": "request",    "parameters": {        "name": "stream/buffer/setup"   }}' + "\n",
            "utf-8"))
        self.sock.recv(self.byte_length)
        time.sleep(5)

    def exposure_time_function(self, exposure_time=100):
        self.sock.sendall(bytes(
            r'{    "id": 0,    "purpose": "request",    "parameters": {"name": "gui/set/value", "args": {"name": "cam/cam/exposure", "value": ' + f'{exposure_time}' + '}}}' + "\n",
            "utf-8"))
        received = self.sock.recv(self.byte_length)

    def get_single_frame_function(self, ):
        self.sock.sendall(bytes(
            r'{    "id": 0,    "purpose": "request",    "parameters": {        "name": "stream/buffer/status"   }}',
            'utf-8'))
        status = self.sock.recv(self.byte_length)
        if json.loads(str(status, 'utf-8'))['parameters']['args']['filled'] >= 1:
        # if True:
            self.sock.sendall(bytes(
                r'{    "id": 2,    "purpose": "request",    "parameters": {        "name": "stream/buffer/read" , "args": {"n": 1}  }}',
                'utf-8'))
            time.sleep(self.read_wait+self.exposure_time/1000)
            full_read = self.sock.recv(self.byte_length)
            print(len(full_read))
            match = re.match(rb'^.*"nbytes": \d*}}', full_read)
            data = full_read[match.span()[1]:]
            read = full_read[:match.span()[1]]
            # print('len read ', len(read))
            # time.sleep(1)
            # data = self.sock.recv(self.byte_length)
            # print('len data ', len(data))
            size_match = re.match(r'^.*\"shape\": \[1, (\d*), (\d*)], \"dtype\": \"<u2\", \"nbytes\": (\d*)}}.*$',
                                  str(read, 'utf-8'))
            print('Succeeded to read from buffer')
            # print('data len: ', len(data))
            return np.frombuffer(data, dtype='<u2').reshape(int(size_match.group(1)), int(size_match.group(2)))
        else:
            print('Failed to read from buffer')
            return None

    def get_background_frame_function(self, ):
        self.sock.sendall(bytes(
            r'{    "id": 0,    "purpose": "request",    "parameters": {        "name": "proc/bgsub/get_status"    }}',
            'utf-8'))
        status = self.sock.recv(self.byte_length)
        status_dict = json.loads(str(status, 'utf-8'))
        if (status_dict['parameters']['args']['enabled']) and (
                status_dict['parameters']['args']['snapshot/background/state'] == 'valid'):
            self.sock.sendall(bytes(
                r'{    "id": 0,    "purpose": "request",    "parameters": {  "name": "proc/bgsub/get_snapshot_background"   }}',
                'utf-8'))
            time.sleep(self.read_wait+self.exposure_time/1000)
            full_read = self.sock.recv(self.byte_length)
            match = re.match(rb'^.*"nbytes": \d*}}', full_read)
            data = full_read[match.span()[1]:]
            read = full_read[:match.span()[1]]
            size_match = re.match(r'^.*\"shape\": \[(\d*), (\d*)], \"dtype\": \"<i4\", \"nbytes\": (\d*)}}.*$',
                                  str(read, 'utf-8'))
            return np.frombuffer(data, dtype='<i4').reshape(int(size_match.group(1)), int(size_match.group(2)))
        else:
            print('Failed to get background. Background currently disabled or not valid.')

    def save_snapshot(self):
        self.sock.sendall(bytes(
                r'{    "id": 0,    "purpose": "request",    "parameters": {  "name": "save/snap"  }}',
                'utf-8'))
        self.sock.recv(self.byte_length)

    def start_saving(self):
        self.sock.sendall(bytes(
            r'{    "id": 0,    "purpose": "request",    "parameters": {  "name": "save/start"   }}',
            'utf-8'))
        self.sock.recv(self.byte_length)

    def stop_saving(self):
        self.sock.sendall(bytes(
            r'{    "id": 0,    "purpose": "request",    "parameters": {  "name": "save/stop"   }}',
            'utf-8'))
        self.sock.recv(self.byte_length)

    def finalize_steps(self):
        self.sock.close()

