from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_SignalRO,
)
from ophyd import Device
import cv2
import threading
import time


# Global variables for sharing frame data and controlling the loop.
last_frame = None
exit_flag = False


def display_thread():
    """Thread to display the latest frame continuously."""
    window_name = f"Current camera frame {time.time()}"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    global exit_flag # If you intend to modify a global flag

    print("Display thread started. Press 'q' or close the window ('X') to exit.")

    while not exit_flag:
        if last_frame is not None:
            try:
                # Display the frame
                cv2.imshow(window_name, last_frame)
            except cv2.error as e:
                # Catch potential errors if the window is closed abruptly between checks
                print(f"OpenCV error during imshow (window might be closed): {e}")
                break # Exit loop if displaying fails

        # cv2.waitKey is required for the window to update and process events.
        # A delay of 30 ms gives a 30 FPS-like refresh.
        key = cv2.waitKey(30) & 0xFF

        # 1. Check for 'q' key press
        if key == ord("q"):
            print("'q' key pressed. Exiting display loop.")
            # exit_flag = True # Optionally set the global flag if needed elsewhere
            break # Exit the loop

        # 2. Check if the window was closed using the 'X' button
        # cv2.getWindowProperty returns various properties.
        # WND_PROP_VISIBLE or WND_PROP_AUTOSIZE often become < 1 when closed.
        try:
            # Check WND_PROP_VISIBLE first, it's generally reliable
            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                print("Window closed via 'X' button. Exiting display loop.")
                # exit_flag = True # Optionally set the global flag
                break # Exit the loop
        except cv2.error as e:
             # This can happen if the window is destroyed unexpectedly
             print(f"OpenCV error checking window property (window might be closed): {e}")
             break # Assume window is gone and exit loop

        # Add a small sleep if there's no frame to display yet, prevents high CPU usage
        if last_frame is None and not exit_flag:
             time.sleep(0.01) # Sleep 10ms

    print("Display loop finished.")
    # Clean up the window explicitly
    try:
        cv2.destroyWindow(window_name)
        # Adding a small waitKey after destroyWindow helps ensure
        # the window system processes the closure properly on some OS/backends.
        cv2.waitKey(1)
    except cv2.error as e:
        # The window might already be destroyed if an error occurred above
        print(f"OpenCV error during destroyWindow (might be already closed): {e}")



class OpenCV_Instrument(Device):
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
        display_image=True,
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
        self.display_image = display_image
        self.get_FOV.read_function = self.get_FOV_read_function
        if name == "test":
            return

        # Connect to Camera
        self.cap = cv2.VideoCapture(self.camera_index)
        # Start the display thread if display_image is True
        if self.display_image:
            display = threading.Thread(target=display_thread)
            display.daemon = True
            display.start()

    def get_FOV_read_function(self):
        """
        Gets the current field of view of the camera. Uses openCV and the index that was set in the configuration.
        """
        ret, frame = self.cap.read()
        if ret:
            # cv2.imshow("Current camera frame", frame)
            global last_frame
            last_frame = frame
            return frame
        else:
            print("Failed to get frame")
            return None

    def finalize_steps(self):
        self.cap.release()
