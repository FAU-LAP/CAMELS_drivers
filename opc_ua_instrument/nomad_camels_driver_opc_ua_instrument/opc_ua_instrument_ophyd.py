from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_Signal,
    Custom_Function_SignalRO,
    Sequential_Device,
)
from asyncua.sync import Client
from asyncua import ua


def make_ophyd_instance_opc_ua(
    prefix="",
    *args,
    name,
    kind=None,
    read_attrs=None,
    configuration_attrs=None,
    parent=None,
    # These are the arguments you want to pass to the ophyd class
    # These are the settings you defined in the .py file
    # We will pass the number of channels we selected in the drop down and are defined in the .py file
    url=None,
    namespace=None,
    variables=None,
    **kwargs,
):
    ophyd_class = make_ophyd_class(variables)
    return ophyd_class(
        prefix,
        *args,
        name=name,
        kind=kind,
        read_attrs=read_attrs,
        configuration_attrs=configuration_attrs,
        parent=parent,
        # These are the arguments you want to pass to the ophyd class
        # These are the settings you defined in the .py file
        # We will pass the number of channels we selected in the drop down and are defined in the .py file
        url=url,
        namespace=namespace,
        variables=variables,
        **kwargs,
    )


def make_ophyd_class(variables):
    def read_function_generator(name, path):
        def read_function(_self_instance):
            """
            This function returns a lambda function that reads the specified channel.
            the read_function is added to the signal as a read_function.
            The _self_instance will later be resolved to the parent of the instance of the signal.

            Parameters:
            _self_instance (object): The parent instance.

            Returns:
            function: A lambda function that reads the power channel.

            """
            return lambda: _self_instance.parent.read_opc_ua(name=name, path=path)

        return read_function

    def set_function_generator(name, path):
        def set_function(_self_instance, value):
            """
            This function returns a lambda function that sets the opc ua variable.
            The _self_instance will later be resolved to the parent of the instance of the


            Parameters:
            _self_instance (object): The parent instance.
            value (float): The value to set the channel to.

            Returns:
            function: A lambda function that sets the power channel.

            """
            # It is important to pass the value to the lambda function!
            return lambda: _self_instance.parent.set_opc_ua(
                name=name, path=path, value=value
            )

        return set_function

    signal_dictionary = {}
    variables_dict_list = [
        dict(zip(variables.keys(), values)) for values in zip(*variables.values())
    ]
    for variable_dict in variables_dict_list:
        # For each channel add read_power function
        if variable_dict["variable-Type"] == "read-only":
            signal_dictionary[variable_dict["Name"]] = Cpt(
                Custom_Function_SignalRO,
                name=variable_dict["Name"],
                metadata={"units": "", "description": ""},
                read_function=read_function_generator(
                    name=variable_dict["Name"], path=variable_dict["Browse Path"]
                ),
            )
        elif variable_dict["variable-Type"] == "set":
            signal_dictionary[variable_dict["Name"]] = Cpt(
                Custom_Function_Signal,
                name=variable_dict["Name"],
                metadata={"units": "", "description": ""},
                put_function=set_function_generator(
                    name=variable_dict["Name"], path=variable_dict["Browse Path"]
                ),
                read_function=read_function_generator(
                    name=variable_dict["Name"], path=variable_dict["Browse Path"]
                ),
            )

    return type(
        f"OPC_UA_total_channels_{len(variables_dict_list)}",
        (Opc_Ua_instrument,),
        {**signal_dictionary},
    )


class Opc_Ua_instrument(Sequential_Device):
    def __init__(
        self,
        prefix="",
        *,
        name,
        kind=None,
        read_attrs=None,
        configuration_attrs=None,
        parent=None,
        url=None,
        namespace=None,
        variables=None,
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
        self.url = url
        self.namespace = namespace
        self.variables = variables

        # return when calling this during initialization of CAMELS at startup
        if name == "test":
            return

        # The following line forces the channels to wait for others to finish before setting and reading
        # This is because Custom_Function_SignalRO and Custom_Function_Signal are typically run asynchronously
        self.force_sequential = True

        self.client = Client(url=self.url)  # Instantiating the AsyncClient
        # Run the async method to connect to the client
        try:
            self.client.connect()
        except Exception as e:
            print(f"Error connecting to OPC UA server: {e}")

    def read_opc_ua(self, name, path):

        if path != "":
            var = self.client.nodes.root.get_child(path)

        else:
            # Find the namespace index
            nsidx = self.client.get_namespace_index(self.namespace)

            # Get the variable node for read / write
            var = self.client.nodes.root.get_child(
                f"0:Objects/{nsidx}:MyObject/{nsidx}:{name}"
            )
        value = var.read_value()
        return value

    def set_opc_ua(self, name, path, value):
        if path != "":
            var = self.client.nodes.root.get_child(path)
        else:
            # Find the namespace index
            nsidx = self.client.get_namespace_index(self.namespace)

            # Get the variable node for read / write
            var = self.client.nodes.root.get_child(
                f"0:Objects/{nsidx}:MyObject/{nsidx}:{name}"
            )
        # Get the expected data type for the node
        expected_type = var.get_data_type_as_variant_type()
        # Convert the incoming value (which is always a float) to the expected type.
        # You can extend this mapping if needed.
        if expected_type in (ua.VariantType.Int16, ua.VariantType.Int32, ua.VariantType.Int64,
                            ua.VariantType.UInt16, ua.VariantType.UInt32, ua.VariantType.UInt64):
            cast_value = int(value)
        elif expected_type in (ua.VariantType.Float, ua.VariantType.Double):
            cast_value = float(value)
        elif expected_type == ua.VariantType.Boolean:
            # Example conversion: if value is 0.0, then False, otherwise True.
            cast_value = bool(value)
        elif expected_type == ua.VariantType.String:
            cast_value = str(value)
        else:
            # Fallback: if you don't have a conversion defined, just pass the value
            cast_value = value

        # Write the converted value to the OPC UA variable
        data_value = ua.DataValue(ua.Variant(cast_value, expected_type))
        var.write_value(data_value)


    def finalize_steps(self):
        # Disconnect the client when done
        print("Disconnecting...")
        self.client.disconnect()
