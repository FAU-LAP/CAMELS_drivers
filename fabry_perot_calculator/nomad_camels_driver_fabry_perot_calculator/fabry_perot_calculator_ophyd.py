from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_Signal,
    Custom_Function_SignalRO,
)
import os
from ophyd import Device
import pandas as pd
import ratter
import numpy as np
from scipy.interpolate import interp1d
import sympy as sp
import lmfit
from lmfit import Parameters
import matplotlib.pyplot as plt


def fit_gap_thickness(params, lamb, I_normed, R_of_wavelength_and_gap_function):
    def optimize_function(params):
        params_values = [param.value for key, param in params.items()]
        reflectivity = R_of_wavelength_and_gap_function(lamb, *params_values)
        return (I_normed / np.max(I_normed) - reflectivity / np.max(reflectivity)) ** 2

    brute_params = lmfit.minimize(
        fcn=optimize_function, params=params, method="brute", Ns=100, keep=5
    )
    fit = lmfit.minimize(
        optimize_function,
        brute_params.candidates[0].params,
    )
    return fit.params.valuesdict()


class Fabry_Perot_Calculator(Device):
    calculate_distance_from_spectrum = Cpt(
        Custom_Function_SignalRO,
        name="calculate_distance_from_spectrum",
        metadata={
            "units": "",
            "description": "connects to the spectrometer to take a spectrum and performs Fabry-Perot fit to determine the distance",
        },
    )
    spectrometer = Cpt(Custom_Function_Signal, name="spectrometer", kind="config")

    def __init__(
        self,
        prefix="",
        *,
        name,
        kind=None,
        read_attrs=None,
        configuration_attrs=None,
        parent=None,
        background_data_path="",
        reflectivity_data_path="",
        plot_savepath="",
        materials="",
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
        self.background_data_path = background_data_path
        self.reflectivity_data_path = reflectivity_data_path
        self.plot_savepath = plot_savepath
        self.spectrometer_device = None
        self.material_dict = materials
        self.calculate_distance_from_spectrum.read_function = (
            self.calculate_distance_from_spectrum_read_function
        )
        self.spectrometer.put_function = self.spectrometer_function
        if name == "test":
            return
        # Get the background data that is located at the path given in  the settings window
        try:
            self.background_spectrum_dataset = pd.read_csv(
                self.background_data_path,
                delimiter="\t",
                decimal=",",
                names=["Wavelength", "Intensity", "empty"],
                usecols=["Wavelength", "Intensity"],
            )
        except:
            try:
                self.background_spectrum_dataset = pd.read_csv(
                    self.background_data_path,
                    delimiter="\t",
                    decimal=".",
                    skiprows=1,
                    names=["Wavelength", "Intensity"],
                    usecols=["Wavelength", "Intensity"],
                )
            except Exception as e:
                raise Exception(
                    f"Could not read the background data from the path {self.background_data_path}. The error is {e}"
                )

        # get actual arrays from the pandas datasets
        self.background_wavelength, self.background_intensity = (
            self.background_spectrum_dataset["Wavelength"].values,
            self.background_spectrum_dataset["Intensity"].values,
        )
        # Interpolate the reflectivity if a path is given to correct the data later on
        if self.reflectivity_data_path:
            self.reflectivity_data = pd.read_csv(
                self.reflectivity_data_path,
                delimiter=";",
                decimal=",",
                names=["Wavelength", "Reflectivity"],
                usecols=["Wavelength", "Reflectivity"],
            )
            self.reflectivity = interp1d(
                self.reflectivity_data["Wavelength"],
                self.reflectivity_data["Reflectivity"],
                fill_value=(
                    np.min(self.reflectivity_data["Reflectivity"]),
                    np.max(self.reflectivity_data["Reflectivity"]),
                ),
                bounds_error=False,
            )

        # determine the ratter model to calculate the symbolic expression for the Fabry-Perot fit
        # define materials used
        # Create a list to store the materials and layers
        self.materials = []
        self.layers = []
        self.fit_symbols = []
        self.params = Parameters()

        # Iterate over the dictionary
        for i in range(len(self.material_dict["Material"])):
            # Create a Material object
            material = ratter.Material(
                self.material_dict["Material"][i],
                refractive_index_value=self.material_dict["Refractive Index"][i],
            )
            self.materials.append(material)

            # Create a Layer object
            thickness_value = self.material_dict["Thickness (m)"][i]
            if thickness_value == "fit":
                thickness_value = None
            elif thickness_value == "inf" or thickness_value == "np.inf":
                thickness_value = np.inf
            else:
                thickness_value = float(thickness_value)
            layer = ratter.Layer(
                f"layer_{i}", material, thickness_value=thickness_value
            )
            if thickness_value == None:
                self.fit_symbols.append(layer.thickness_symbol)
                self.params.add(
                    f"layer_{i}",
                    self.material_dict["Fit start"][i],
                    min=self.material_dict["Fit min"][i],
                    max=self.material_dict["Fit max"][i],
                )

            self.layers.append(layer)

        # create the stack out of the layers
        self.stack = ratter.Layerstack(self.layers)
        # calculate the reflectance amplitude
        self.r = self.stack.reflectance_amplitude()
        self.R = sp.conjugate(self.r) * self.r
        # create callable function depending on wavelength and gap thickness between the two SiC chips
        self.R_of_wavelength_and_open_parameters = ratter.as_function_of(
            self.R, [ratter.LAMBDA_VAC] + self.fit_symbols
        )

    def calculate_distance_from_spectrum_read_function(self):
        self.measured_spectrum = self.spectrometer_device.spectrum.get()
        self.wavelength = self.spectrometer_device.wavelength.get()

        # subtract 340 as this is the dark count rate of the camera
        self.corrected_spectrum = self.measured_spectrum - 340
        if self.reflectivity:
            self.corrected_spectrum = self.corrected_spectrum / self.reflectivity(
                self.wavelength
            )

        # normalize the spectrum to go from 0 to 1
        # the Fabry-Perot fit is also normalized to go from 0 to 1
        # This is done as most of the information is in the spacing of the peaks, not in the actual height of the peaks
        self.corrected_spectrum = (
            self.corrected_spectrum / self.background_intensity
            - np.min(self.corrected_spectrum / self.background_intensity)
        ) / np.max(self.corrected_spectrum / self.background_intensity)
        self.fit_results = fit_gap_thickness(
            self.params,
            self.wavelength,
            self.corrected_spectrum,
            self.R_of_wavelength_and_open_parameters,
        )
        print(self.fit_results)
        self.fit_result_intensity = np.real(
            self.R_of_wavelength_and_open_parameters(
                self.wavelength, *self.fit_results.values()
            )
        )
        if self.plot_savepath:
            try:
                fig, ax = plt.subplots()
                ax.plot(
                    self.wavelength,
                    self.corrected_spectrum / np.max(self.corrected_spectrum),
                )
                ax.plot(self.wavelength, self.fit_result_intensity/np.max(self.fit_result_intensity))
                ax.set_title(f"Distance = {int(self.fit_results['layer_1'])} nm")
                time_stamp = (pd.Timestamp.now()).strftime("%Y-%m-%d_%H-%M-%S")
                fig.savefig(os.path.join(self.plot_savepath, f"fit_{time_stamp}.png"))
                plt.close(fig)
            except:
                print(
                    "Could not save the fit plot to the desktop. Make sure the path exists and is accessible."
                )

        results_array = np.array(
            [
                np.full_like(self.wavelength, value)
                for value in self.fit_results.values()
            ]
        )
        return np.concatenate(
            (
                results_array,
                self.wavelength[None, :],
                self.corrected_spectrum[None, :],
                self.fit_result_intensity[None, :],
            ),
            axis=0,
        )

    def spectrometer_function(self, value):
        if isinstance(value, str):
            from nomad_camels.utility import device_handling

            self.spectrometer_device = device_handling.running_devices[value]
        else:
            self.spectrometer_device = value
