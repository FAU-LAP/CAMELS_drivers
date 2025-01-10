from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_Signal,
    Custom_Function_SignalRO,
)
from ophyd import Device
import cv2


class Opencv_Generic(Device):
    get_FOV = Cpt(
        Custom_Function_SignalRO,
        name="get_FOV",
        metadata={
            "units": "",
            "description": "",
            "h5_data_type": "openCV BGR image",
            "CLASS": "IMAGE",
        },
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
        camera_index=None,
        **kwargs,
    ):
        super().__init__(
            prefix=prefix,
            name=name,
            kind=kind,
            read_attrs=read_attrs,
            configuration_attrs=configuration_attrs,
            parent=parent,
            **kwargs,
        )
        self.camera_index = camera_index
        self.get_FOV.read_function = self.get_FOV_read_function
        if name == "test":
            pass

        # Connect to Camera
        self.cap = cv2.VideoCapture(self.camera_index)

    def get_FOV_read_function(self):
        """
        Gets the current field of view of the camera. Uses openCV and the index that was set in the configuration.
        """
        ret, frame = self.cap.read()
        if ret:
            cv2.imshow("Current camera frame", frame)
            print(frame.shape)
            return frame
        else:
            print("Failed to get frame")
            return None

    def finalize_steps(self):
        self.cap.release()
        cv2.destroyAllWindows()
