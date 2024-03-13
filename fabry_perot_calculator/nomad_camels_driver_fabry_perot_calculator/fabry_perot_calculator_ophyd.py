from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_Signal,
    Custom_Function_SignalRO,
)
from ophyd import Device
import pandas as pd
import ratter
import numpy as np
from scipy.interpolate import interp1d
import sympy as sp
import lmfit
from lmfit import Parameters


def fit_gap_thickness(params, lamb, I_normed, R_of_wavelength_and_gap_function):
    def optimize_function(params):
        reflectivity = R_of_wavelength_and_gap_function(lamb, params["gap"])
        return (I_normed / np.max(I_normed) - reflectivity / np.max(reflectivity)) ** 2

    brute_params = lmfit.minimize(
        fcn=optimize_function, params=params, method="brute", keep=5
    )
    fit = lmfit.minimize(
        optimize_function, brute_params.candidates[0].params, max_nfev=200
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
        **kwargs
    ):
        super().__init__(
            prefix=prefix,
            name=name,
            kind=kind,
            read_attrs=read_attrs,
            configuration_attrs=configuration_attrs,
            parent=parent,
            **kwargs
        )
        self.background_data_path = background_data_path
        self.reflectivity_data_path = reflectivity_data_path
        self.calculate_distance_from_spectrum.read_function = (
            self.calculate_distance_from_spectrum_read_function
        )
        self.spectrometer.put_function = self.spectrometer_function
        if name == "test":
            return
        # Get the background data that is located at the path given in  the settings window
        self.background_spectrum_dataset = pd.read_csv(
            self.background_data_path,
            delimiter="\t",
            decimal=",",
            names=["Wavelength", "Intensity", "empty"],
            usecols=["Wavelength", "Intensity"],
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
        self.air = ratter.Material("air", refractive_index_value=1.00027698)
        self.SiC = ratter.Material("SiC", refractive_index_value=2.66)

        # define the layers
        self.gap = ratter.Layer("gap", self.air)
        self.SiC_top = ratter.Layer("SiC_top", self.SiC, thickness_value=np.inf)
        self.SiC_bottom = ratter.Layer("SiC_bottom", self.SiC, thickness_value=np.inf)
        # create the stack out of the layers
        self.stack = ratter.Layerstack([self.SiC_top, self.gap, self.SiC_bottom])
        # calculate the reflectance amplitude
        self.r = self.stack.reflectance_amplitude()
        self.R = sp.conjugate(self.r) * self.r
        # create callable function depending on wavelength and gap thickness between the two SiC chips
        self.R_of_wavelength_and_gap = ratter.as_function_of(
            self.R, [ratter.LAMBDA_VAC, self.gap.thickness_symbol]
        )

    def calculate_distance_from_spectrum_read_function(self):
        self.measured_spectrum = self.spectrometer.spectrum.get()
        self.wavelength = self.spectrometer.wavelength.get()

        # subtract 340 as this is the dark count rate of the camera
        self.corrected_spectrum = self.measured_spectrum - 340

        # normalize the spectrum to go from 0 to 1
        # the Fabry-Perot fit is also normalized to go from 0 to 1
        # This is done as most of the information is in the spacing of the peaks, not in the actual height of the peaks
        self.corrected_spectrum = (
            self.corrected_spectrum / self.background_intensity
            - np.min(self.corrected_spectrum / self.background_intensity)
        ) / np.max(self.corrected_spectrum / self.background_intensity)
        self.params = Parameters()
        # vary the parameters here!
        self.params.add("gap", 10e3, min=8e3, max=15e3, vary=True)
        self.fit_results = fit_gap_thickness(
            self.params, self.wavelength, self.corrected_spectrum
        )
        return self.fit_results["gap"]

    def spectrometer_function(self, value):
        if isinstance(value, str):
            from nomad_camels.utility import device_handling

            self.spectrometer = device_handling.running_devices[value]
        else:
            self.spectrometer = value
