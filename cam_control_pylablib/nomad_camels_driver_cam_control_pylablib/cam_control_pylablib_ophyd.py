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
    exposure_time = Cpt(Custom_Function_Signal, name='exposure_time',
                        kind='config', metadata={'unit': 'ms',
                                                 'description': 'Camera exposure time in ms.'})
    path_suffix = Cpt(Custom_Function_Signal, name='path_suffix',
                      metadata={'description': 'Suffix that is added to all saved snapshots, should be some variable '
                                               'or changed value. Set "None" if the standard saving of the GUI should be used.'})

    frame_average = Cpt(Custom_Function_SignalRO, name='frame_average',
                      metadata={'description': 'Calculates the frame average of the latest frame. '
                                               'Works only after using get_single_frame.'})
    get_single_frame = Cpt(Custom_Function_SignalRO, name='get_single_frame',
                           metadata={'description': 'Get data of single frame with parameters of the GUI.'})
    get_background_frame = Cpt(Custom_Function_SignalRO, name='get_background_frame',
                               metadata={'description': 'Get data of background frame with parameters of the GUI.'})
    complete_settings = Cpt(Custom_Function_SignalRO, name='complete_settings',
                            kind='config', metadata={'description': 'Reads the complete GUI settings of cam control.'})
    set_roi = Cpt(Custom_Function_Signal, name='set_roi',
                      metadata={'description': 'Set the ROI. Write "[x_min, x_max, y_min, y_max]"'})
    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None,
                 host_ip='127.0.0.1',
                 port=18923,
                 byte_length=9000000,
                 overwrite_exposure_time=True,
                 **kwargs):
        super().__init__(prefix=prefix, name=name, kind=kind,
                         read_attrs=read_attrs,
                         configuration_attrs=configuration_attrs, parent=parent,
                         **kwargs)
        self.host_ip = host_ip
        self.port = port
        self.byte_length = byte_length
        self.overwrite_exposure_time = overwrite_exposure_time
        self.exposure_time.put_function = lambda x: self.exposure_time_function(exposure_time=x)
        self.get_single_frame.read_function = self.get_single_frame_function
        self.get_background_frame.read_function = self.get_background_frame_function
        self.frame_average.read_function = self.frame_average_function
        self.complete_settings.read_function = self.complete_settings_function
        self.set_roi.put_function = lambda x: self.set_roi_function(x)
        self.path_suffix.put(None)

        # This if statement prevents the lines of the init below to be run when starting up CAMELS.
        if name == 'test':
            return
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host_ip, self.port))
        self.sock.sendall(bytes(
            r'{    "id": 0,    "purpose": "request",    "parameters": {        "name": "gui/get/value", "args": {"name": "cam/save/path"}   }}' + "\n",
            "utf-8"))
        self.default_save_path = json.loads(str(self.sock.recv(self.byte_length), 'utf-8'))['parameters']['args']['value']
        self.sock.sendall(bytes(
            r'{    "id": 0,    "purpose": "request",    "parameters": {        "name": "stream/buffer/setup"   }}' + "\n",
            "utf-8"))
        self.sock.recv(self.byte_length)
        # Get the ROI and the size of the ROI so that we know how large the read frame from buffer should be
        self.sock.sendall(bytes(
                r'{    "id": 0,    "purpose": "request",    "parameters": { "name": "cam/param/get", "args": {"name": "roi"}  }}',
                "utf-8"))
        time.sleep(0.1)
        self.roi_string = (self.sock.recv(self.byte_length)).decode('utf-8')
        self.roi_matches = re.findall(r'\[\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\s*\]', self.roi_string)
        self.roi = np.array([int(num) for match in self.roi_matches for num in match])
        self.roi_length = float((self.roi[1]-self.roi[0])*(self.roi[3]-self.roi[2]))
        

    def exposure_time_function(self, exposure_time=100):
        if self.overwrite_exposure_time:
            self.sock.sendall(bytes(
                r'{    "id": 0,    "purpose": "request",    "parameters": {"name": "gui/set/value", "args": {"name": "cam/cam/exposure", "value": ' + f'{exposure_time}' + '}}}' + "\n",
                "utf-8"))
            received = self.sock.recv(self.byte_length)

    def get_single_frame_function(self, ):
        self.sock.sendall(bytes(
            r'{    "id": 0,    "purpose": "request",    "parameters": {        "name": "stream/buffer/status"   }}',
            'utf-8'))
        status = self.sock.recv(self.byte_length)
        while json.loads(str(status, 'utf-8'))['parameters']['args']['filled'] == 0:
            self.sock.sendall(bytes(
                r'{    "id": 0,    "purpose": "request",    "parameters": {        "name": "stream/buffer/status"   }}',
                'utf-8'))
            status = self.sock.recv(self.byte_length)
        self.sock.sendall(bytes(
            r'{    "id": 2,    "purpose": "request",    "parameters": {        "name": "stream/buffer/read" , "args": {"n": 1}  }}',
            'utf-8'))
        full_read = self.sock.recv(self.byte_length)
        while len(full_read) < self.roi_length*2:
            full_read += self.sock.recv(self.byte_length)

        match = re.match(rb'^.*"nbytes": \d*}}', full_read)
        data = full_read[match.span()[1]:]
        read = full_read[:match.span()[1]]
        size_match = re.match(r'^.*\"shape\": \[1, (\d*), (\d*)], \"dtype\": \"<u2\", \"nbytes\": (\d*)}}.*$',
                              str(read, 'utf-8'))
        return np.frombuffer(data, dtype='<u2').reshape(int(size_match.group(1)), int(size_match.group(2)))

    def get_background_frame_function(self, ):
        self.sock.sendall(bytes(
            r'{    "id": 0,    "purpose": "request",    "parameters": {        "name": "proc/bgsub/get_status"    }}',
            'utf-8'))
        status = self.sock.recv(self.byte_length)
        status_dict = json.loads(str(status, 'utf-8'))
        while status_dict['parameters']['args']['snapshot/background/state'] == 'acquiring':
            self.sock.sendall(bytes(
                r'{    "id": 0,    "purpose": "request",    "parameters": {        "name": "proc/bgsub/get_status"    }}',
                'utf-8'))
            status = self.sock.recv(self.byte_length)
            status_dict = json.loads(str(status, 'utf-8'))
        if status_dict['parameters']['args']['snapshot/background/state'] == 'valid':
            self.sock.sendall(bytes(
                r'{    "id": 0,    "purpose": "request",    "parameters": {  "name": "proc/bgsub/get_snapshot_background"   }}',
                'utf-8'))
            time.sleep(0.1)
            full_read = self.sock.recv(self.byte_length)
            match = re.match(rb'^.*"nbytes": \d*}}', full_read)
            data = full_read[match.span()[1]:]
            read = full_read[:match.span()[1]]
            size_match = re.match(r'^.*\"shape\": \[(\d*), (\d*)], \"dtype\": \"<i4\", \"nbytes\": (\d*)}}.*$',
                                  str(read, 'utf-8'))
            return np.frombuffer(data, dtype='<i4').reshape(int(size_match.group(1)), int(size_match.group(2)))
        else:
            print('Failed to get background. Background not valid.')

    def frame_average_function(self,):
        frame = self.get_single_frame.get()
        if len(frame) > 0:
            return np.average(frame)
    def save_snapshot(self):
        # If path_suffix is set with Set_Channels than this name is used to save the file.
        if self.path_suffix.get() != None:
            self.sock.sendall(bytes(
                r'{    "id": 0,    "purpose": "request",    "parameters": {  "name": "save/snap", "args": {"path": ' f'"{self.default_save_path}_{self.path_suffix.get()}_{time.time()}"' '}  }}',
                'utf-8'))
            self.sock.recv(self.byte_length)
        # If no path_suffix is set, then the regular snap saving behaviour of the GUI is used
        else:
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

    def complete_settings_function(self):
        self.sock.sendall(bytes(
            r'{    "id": 0,    "purpose": "request",    "parameters": { "name": "gui/get/value"  }}',
            "utf-8"))
        complete_settings_string = str(self.sock.recv(self.byte_length), 'utf-8')
        complete_settings_dict = json.loads(complete_settings_string)
        pretty_string_complete_settings = json.dumps(complete_settings_dict, sort_keys=True, indent=4)
        return pretty_string_complete_settings

    def set_roi_function(self, value):
        self.sock.sendall(bytes(
            r'{    "id": 0,    "purpose": "request",    "parameters": {"name": "cam/param/set", "args": {"roi": ' f'{value}' '}}}',
            "utf-8"))
        self.sock.recv(self.byte_length)

    def grab_background(self,):
        self.sock.sendall(bytes(
        r'{    "id": 0,    "purpose": "request",    "parameters": {"name": "gui/set/value", "args": {"name": "proc/grab_background", "value": "True"}}}',
        "utf-8"))
        self.sock.recv(self.byte_length)
        time.sleep(0.5)
        self.sock.sendall(bytes(
            r'{    "id": 0,    "purpose": "request",    "parameters": { "name": "gui/get/value"  , "args": {"name": "proc/background_state"}}}',
            "utf-8"))
        status = self.sock.recv(self.byte_length)
        status_dict = json.loads(str(status, 'utf-8'))
        while status_dict['parameters']['args']['value'] == 'Accumulating':
            self.sock.sendall(bytes(
                r'{    "id": 0,    "purpose": "request",    "parameters": { "name": "gui/get/value"  , "args": {"name": "proc/background_state"}}}',
                "utf-8"))
            status = self.sock.recv(self.byte_length)
            status_dict = json.loads(str(status, 'utf-8'))



    def finalize_steps(self):
        self.sock.close()

