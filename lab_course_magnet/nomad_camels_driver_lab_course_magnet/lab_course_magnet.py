from nomad_camels.main_classes import device_class

from .lab_course_magnet_ophyd import Lab_Course_Magnet


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="lab_course_magnet",
            tags=["valve", "flow"],
            ophyd_device=Lab_Course_Magnet,
            ophyd_class_name="Lab_Course_Magnet",
            **kwargs
        )


class subclass_config(device_class.Simple_Config):
    def __init__(
        self,
        parent=None,
        data="",
        settings_dict=None,
        config_dict=None,
        additional_info=None,
    ):
        super().__init__(
            parent,
            "Lab Course Magnet",
            data,
            settings_dict,
            config_dict,
            additional_info,
        )
        self.comboBox_connection_type.addItem("Local VISA")
        self.load_settings()
