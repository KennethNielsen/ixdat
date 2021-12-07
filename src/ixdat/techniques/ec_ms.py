"""Module for representation and analysis of EC-MS measurements"""
import numpy as np
from ..constants import FARADAY_CONSTANT
from .ec import ECMeasurement, ECCalibration
from .ms import MSMeasurement, MSCalResult, MSCalibration
from .cv import CyclicVoltammagram
from ..exporters.ecms_exporter import ECMSExporter
from ..plotters.ecms_plotter import ECMSPlotter
from ..plotters.ms_plotter import STANDARD_COLORS
import json  # FIXME: doesn't belong here.


class ECMSMeasurement(ECMeasurement, MSMeasurement):
    """Class for raw EC-MS functionality. Parents: ECMeasurement and MSMeasurement"""

    extra_column_attrs = {
        # FIXME: It would be more elegant if this carried over from both parents
        #   That might require some custom inheritance definition...
        "ecms_meaurements": {
            "mass_aliases",
            "signal_bgs",
            "ec_technique",
        },
    }
    default_plotter = ECMSPlotter
    default_exporter = ECMSExporter

    def __init__(self, **kwargs):
        """FIXME: Passing the right key-word arguments on is a mess"""
        ec_kwargs = {
            k: v for k, v in kwargs.items() if k in ECMeasurement.get_all_column_attrs()
        }
        ms_kwargs = {
            k: v for k, v in kwargs.items() if k in MSMeasurement.get_all_column_attrs()
        }
        # ms_kwargs["ms_calibration"] = self.ms_calibration  # FIXME: This is a mess.
        # FIXME: I think the lines below could be avoided with a PlaceHolderObject that
        #  works together with MemoryBackend
        if "series_list" in kwargs:
            ec_kwargs.update(series_list=kwargs["series_list"])
            ms_kwargs.update(series_list=kwargs["series_list"])
        if "component_measurements" in kwargs:
            ec_kwargs.update(component_measurements=kwargs["component_measurements"])
            ms_kwargs.update(component_measurements=kwargs["component_measurements"])
        ECMeasurement.__init__(self, **ec_kwargs)
        MSMeasurement.__init__(self, **ms_kwargs)

    def as_dict(self):
        self_as_dict = super().as_dict()

        if self.ms_calibration:
            self_as_dict["ms_calibration"] = self.ms_calibration.as_dict()
            # FIXME: necessary because an ECMSCalibration is not serializeable
            #   If it it was it would go into extra_column_attrs
        return self_as_dict

    @classmethod
    def from_dict(cls, obj_as_dict):
        """Unpack the ECMSCalibration when initiating from a dict"""
        if "ms_calibration" in obj_as_dict:
            if isinstance(obj_as_dict["ms_calibration"], dict):
                # FIXME: This is a mess
                obj_as_dict["ms_calibration"] = ECMSCalibration.from_dict(
                    obj_as_dict["ms_calibration"]
                )
        obj = super(ECMSMeasurement, cls).from_dict(obj_as_dict)
        return obj

    def as_cv(self):
        self_as_dict = self.as_dict()

        # FIXME: The following lines are only necessary because
        #  PlaceHolderObject.get_object isn't able to find things in the MemoryBackend
        del self_as_dict["s_ids"]
        self_as_dict["series_list"] = self.series_list

        return ECMSCyclicVoltammogram.from_dict(self_as_dict)

    def ecms_calibration(self, mol, mass, n_el, tspan, tspan_bg=None):
        """Calibrate for mol and mass based on one period of steady electrolysis

        Args:
            mol (str): Name of the molecule to calibrate
            mass (str): Name of the mass at which to calibrate
            n_el (str): Number of electrons passed per molecule produced (remember the
                sign! e.g. +4 for O2 by OER and -2 for H2 by HER)
            tspan (tspan): The timespan of steady electrolysis
            tspan_bg (tspan): The time to use as a background

        Return MSCalResult: The result of the ms_calibration
        """
        Y = self.integrate_signal(mass, tspan=tspan, tspan_bg=tspan_bg)
        Q = self.integrate("raw current / [mA]", tspan=tspan) * 1e-3
        n = Q / (n_el * FARADAY_CONSTANT)
        F = Y / n
        cal = MSCalResult(
            name=f"{mol}_{mass}",
            mol=mol,
            mass=mass,
            cal_type="ecms_calibration",
            F=F,
        )
        return cal

    def ecms_calibration_curve(
        self,
        mol,
        mass,
        n_el,
        tspan_list=None,
        tspan_bg=None,
        ax="new",
        axes_measurement=None,
    ):
        """Fit mol's sensitivity at mass based on steady periods of EC production

        Args:
            mol (str): Name of the molecule to calibrate
            mass (str): Name of the mass at which to calibrate
            n_el (str): Number of electrons passed per molecule produced (remember the
                sign! e.g. +4 for O2 by OER and -2 for H2 by HER)
            tspan_list (list of tspan): THe timespans of steady electrolysis
            tspan_bg (tspan): The time to use as a background
            ax (Axis): The axis on which to plot the ms_calibration curve result. Defaults
                to a new axis.
            axes_measurement (list of Axes): The EC-MS plot axes to highlight the
                ms_calibration on. Defaults to None.

        Return MSCalResult(, Axis(, Axis)): The result of the ms_calibration
            (and requested axes)
        """
        axis_ms = axes_measurement[0] if axes_measurement else None
        axis_current = axes_measurement[0] if axes_measurement else None
        Y_list = []
        n_list = []
        for tspan in tspan_list:
            Y = self.integrate_signal(mass, tspan=tspan, tspan_bg=tspan_bg, ax=axis_ms)
            # FIXME: plotting current by giving integrate() an axis doesn't work great.
            Q = self.integrate("raw current / [mA]", tspan=tspan, axis=axis_current)
            Q *= 1e-3  # mC --> [C]
            n = Q / (n_el * FARADAY_CONSTANT)
            Y_list.append(Y)
            n_list.append(n)
        n_vec = np.array(n_list)
        Y_vec = np.array(Y_list)
        pfit = np.polyfit(n_vec, Y_vec, deg=1)
        F = pfit[0]
        if ax:
            color = STANDARD_COLORS[mass]
            if ax == "new":
                ax = self.plotter.new_ax()
                ax.set_xlabel("amount produced / [nmol]")
                ax.set_ylabel("integrated signal / [nC]")
            ax.plot(n_vec * 1e9, Y_vec * 1e9, "o", color=color)
            n_fit = np.array([0, max(n_vec)])
            Y_fit = n_fit * pfit[0] + pfit[1]
            ax.plot(n_fit * 1e9, Y_fit * 1e9, "--", color=color)
        cal = MSCalResult(
            name=f"{mol}_{mass}",
            mol=mol,
            mass=mass,
            cal_type="ecms_calibration_curve",
            F=F,
        )
        if ax:
            if axes_measurement:
                return cal, ax, axes_measurement
            return cal, ax
        return cal


class ECMSCyclicVoltammogram(CyclicVoltammagram, MSMeasurement):
    """Class for raw EC-MS functionality. Parents: CyclicVoltammogram, MSMeasurement

    FIXME: Maybe this class should instead inherit from ECMSMeasurement and
        just add the CyclicVoltammogram functionality?
    """

    extra_column_attrs = {
        # FIXME: It would be more elegant if this carried over from both parents
        #   That might require some custom inheritance definition...
        "ecms_meaurements": {
            "mass_aliases",
            "signal_bgs",
            "ec_technique",
        },
    }
    default_plotter = ECMSPlotter
    default_exporter = ECMSExporter

    def __init__(self, **kwargs):
        """FIXME: Passing the right key-word arguments on is a mess"""
        ec_kwargs = {
            k: v for k, v in kwargs.items() if k in ECMeasurement.get_all_column_attrs()
        }
        ec_kwargs.update(series_list=kwargs["series_list"])
        ECMeasurement.__init__(self, **ec_kwargs)
        ms_kwargs = {
            k: v for k, v in kwargs.items() if k in MSMeasurement.get_all_column_attrs()
        }
        ms_kwargs.update(series_list=kwargs["series_list"])
        MSMeasurement.__init__(self, **ms_kwargs)
        self.plot = self.plotter.plot_vs_potential

    def as_dict(self):
        self_as_dict = super().as_dict()

        if self.ms_calibration:
            self_as_dict["ms_calibration"] = self.ms_calibration.as_dict()
            # FIXME: now that ECMSCalibration should be seriealizeable, it could
            #  go into extra_column_attrs. But it should be a reference.
        return self_as_dict

    @classmethod
    def from_dict(cls, obj_as_dict):
        """Unpack the ECMSCalibration when initiating from a dict"""
        if "ms_calibration" in obj_as_dict:
            if isinstance(obj_as_dict["ms_calibration"], dict):
                # FIXME: This is a mess
                obj_as_dict["ms_calibration"] = ECMSCalibration.from_dict(
                    obj_as_dict["ms_calibration"]
                )
        obj = super(ECMSCyclicVoltammogram, cls).from_dict(obj_as_dict)
        return obj


class ECMSCalibration(ECCalibration, MSCalibration):
    """Class for calibrations useful for ECMSMeasurements"""

    extra_column_attrs = {
        "ecms_calibrations": {"date", "setup", "RE_vs_RHE", "A_el", "L"}
    }
    # FIXME: The above should be covered by the parent classes. Needs metaprogramming!
    # NOTE: technique, name, and tstamp in column_attrs are inherited from Calibration
    # NOTE: ms_results_ids in extra_linkers is inherited from MSCalibration.
    # NOTE: signal_bgs is left out

    def __init__(
        self,
        name=None,
        date=None,
        tstamp=None,
        setup=None,
        ms_cal_results=None,
        signal_bgs=None,
        RE_vs_RHE=None,
        A_el=None,
        L=None,
        technique="EC-MS",
    ):
        """
        Args:
            name (str): Name of the ms_calibration
            date (str): Date of the ms_calibration
            setup (str): Name of the setup where the ms_calibration is made
            ms_cal_results (list of MSCalResult): The mass spec calibrations
            RE_vs_RHE (float): the RE potential in [V]
            A_el (float): the geometric electrode area in [cm^2]
            L (float): the working distance in [m]
        """
        ECCalibration.__init__(self, name=name, A_el=A_el, RE_vs_RHE=RE_vs_RHE)
        MSCalibration.__init__(
            self,
            date=date,
            tstamp=tstamp,
            setup=setup,
            ms_cal_results=ms_cal_results,
            signal_bgs=signal_bgs,
        )
        self.technique = technique
        self.L = L

    @classmethod
    def from_dict(cls, obj_as_dict):
        """Unpack the MSCalResults when initiating from a dict"""
        obj = super(ECMSCalibration, cls).from_dict(obj_as_dict)
        obj.ms_cal_results = [
            MSCalResult.from_dict(cal_as_dict) for cal_as_dict in obj.ms_cal_results
        ]
        return obj

    def export(self, path_to_file=None):
        """Export an ECMSCalibration as a json-formatted text file"""
        path_to_file = path_to_file or (self.name + ".ix")
        self_as_dict = self.as_dict()
        del self_as_dict["ms_cal_result_ids"]
        self_as_dict["ms_cal_results"] = [cal.as_dict() for cal in self.ms_cal_results]
        with open(path_to_file, "w") as f:
            json.dump(self_as_dict, f, indent=4)

    @classmethod
    def read(cls, path_to_file):
        """Read an ECMSCalibration from a json-formatted text file"""
        with open(path_to_file) as f:
            obj_as_dict = json.load(f)
        return cls.from_dict(obj_as_dict)

    @property
    def mol_list(self):
        return list({cal.mol for cal in self.ms_cal_results})

    @property
    def mass_list(self):
        return list({cal.mass for cal in self.ms_cal_results})

    @property
    def name_list(self):
        return list({cal.name for cal in self.ms_cal_results})

    def __contains__(self, mol):
        return mol in self.mol_list or mol in self.name_list

    def __iter__(self):
        yield from self.ms_cal_results

    def get_mass_and_F(self, mol):
        """Return the mass and sensitivity factor to use for simple quant. of mol"""
        cal_list_for_mol = [cal for cal in self if cal.mol == mol or cal.name == mol]
        Fs = [cal.F for cal in cal_list_for_mol]
        index = np.argmax(np.array(Fs))

        the_good_cal = cal_list_for_mol[index]
        return the_good_cal.mass, the_good_cal.F

    def get_F(self, mol, mass):
        """Return the sensitivity factor for mol at mass"""
        cal_list_for_mol_at_mass = [
            cal
            for cal in self
            if (cal.mol == mol or cal.name == mol) and cal.mass == mass
        ]
        F_list = [cal.F for cal in cal_list_for_mol_at_mass]
        return np.mean(np.array(F_list))

    def scaled_to(self, ms_cal_result):
        """Return a new ms_calibration w scaled sensitivity factors to match one given"""
        F_0 = self.get_F(ms_cal_result.mol, ms_cal_result.mass)
        scale_factor = ms_cal_result.F / F_0
        calibration_as_dict = self.as_dict()
        new_cal_list = []
        for cal in self.ms_cal_results:
            cal = MSCalResult(
                name=cal.name,
                mass=cal.mass,
                mol=cal.mol,
                F=cal.F * scale_factor,
                cal_type=cal.cal_type + " scaled",
            )
            new_cal_list.append(cal)
        calibration_as_dict["ms_cal_results"] = [cal.as_dict() for cal in new_cal_list]
        calibration_as_dict["name"] = calibration_as_dict["name"] + " scaled"
        return self.__class__.from_dict(calibration_as_dict)
