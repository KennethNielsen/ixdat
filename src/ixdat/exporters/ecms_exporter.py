from .ec_exporter import ECExporter


class ECMSExporter(ECExporter):
    """A CSVExporter that by default exports potential, current, selector, and all MID"""

    @property
    def default_export_columns(self):
        """The default v_list for ECExporter is V_str, J_str, and sel_str"""
        v_list = (
            ECExporter(measurement=self.measurement).default_export_columns
            + self.measurement.mass_list
        )

        return v_list

    def export(
        self,
        path_to_file=None,
        measurement=None,
        v_list=None,
        tspan=None,
        mass_list=None,
        mol_list=None,
    ):
        if not v_list:
            if mass_list:
                v_list = ECExporter(measurement=self.measurement).default_export_columns
            else:
                v_list = self.default_export_columns
        if mass_list:
            v_list += mass_list
        if mol_list:
            v_list += [f"n_dot_{mol}" for mol in mol_list]
        return super().export(path_to_file, measurement, v_list, tspan)
