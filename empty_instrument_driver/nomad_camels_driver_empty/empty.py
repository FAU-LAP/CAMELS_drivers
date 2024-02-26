from .empty_ophyd import Instrument_Name
from nomad_camels.main_classes import device_class


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="instrument_name",
            virtual=False,
            # Change the tags to fit your device
            tags=["Function", "Sine", "Waveform", "Generator", "Voltage"],
            ophyd_device=Instrument_Name,
            ophyd_class_name="instrument_name",
            **kwargs
        )

        # Configs are optional
        # The config settings ona n instrument are changeable in the 'Configure Instrument' window
        # These are the defualt values
        # and tell the automatic UI generator what type of value is expected in the config field
        # It is a simple text edit field where you can enter new numbers
        self.config["custom_signal_config"] = 1
        # This is a checkbox to set to True or uncheck to set false
        self.config["custom_signal_config"] = True
        # This is a combobox
        # the definition of possible elements is done below in the subclass_config
        self.config["Source_Type"] = "Voltage"


class subclass_config(device_class.Simple_Config):
    """
    Automatically creates a GUI for the configuration values given here.
    This is perfect for simple devices with just a few settings.
    """

    def __init__(
        self,
        parent=None,
        data="",
        settings_dict=None,
        config_dict=None,
        additional_info=None,
    ):
        # Change the 'instrument name' string to the name of the instrument
        # this will be displayed when adding the instrument in CAMELS
        # Optional Configs
        # Comboboxes with any number of options
        comboBoxes = {
            "Source_Type": ["Voltage", "Current", "Sweep Voltage", "Sweep Current"]
        }
        # Optional labels for the self.config elements defined above. Useful to add units.
        labels = {"custom_signal_config": "Custom Signal Config (V)"}
        super().__init__(
            parent,
            "instrument name",
            data,
            settings_dict,
            config_dict,
            additional_info,
            comboBoxes=comboBoxes,
            labels=labels,
        )

        # Keep the following line! or you can not set the VISA communication configuration
        self.comboBox_connection_type.addItem("Local VISA")
        self.load_settings()
