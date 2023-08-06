"""
@package lib.data_preprocessor

Data Preprocessor module
"""

# Standard packages
import os
import json
import time
from multiprocessing import Pool
from typing import List, Dict, Tuple, Union

# Third parties packages
import xarray as xr
import numpy as np

# Own package
from mfire.configuration.rules import Rules
from mfire.utils import xr_utils, exception
from mfire.utils.date import Datetime, Timedelta
from mfire.settings import get_logger, RULES_NAMES

# Logging
LOGGER = get_logger(name="data_preprocessor.mod", bind="preprocess")


class DataPreprocessor:
    """ DataPreprocessor
    Class handling the following data preprocessing according to a given config
    file :
        * parameter extraction from multigrib files
        * concatenation of term by parameter
        * FUTURE : accumulations and combinations of files
        * export to netcdf
    """

    grib_param_dtypes: dict = {
        "discipline": int,
        "parameterCategory": int,
        "productDefinitionTemplateNumber": int,
        "parameterNumber": int,
        "typeOfFirstFixedSurface": str,
        "level": int,
        "typeOfStatisticalProcessing": int,
        "derivedForecast": int,
        "percentileValue": int,
        "scaledValueOfLowerLimit": int,
        "lengthOfTimeRange": int,
        "units": str,
    }
    mandatory_grib_param: list = ["name", "units", "startStep", "endStep", "stepRange"]

    def __init__(self, data_config_filename: str, rules: str):
        """__init__

        Args:
            data_config_filename (str): Name of the data config file
            rules (str): Name of the rules convention used for files selection. This
                argument must be an element of the RULES_NAMES tuple.
        """
        # Opening the data config file
        LOGGER.info(f"Opening config '{data_config_filename}'", func="__init__")
        with open(data_config_filename, "r") as data_config_file:
            data_config = json.load(data_config_file)
        self.sources_config = data_config["sources"]
        self.preprocessed_config = data_config["preprocessed"]
        self.missing_gribs = []

        # Checking rules convention
        LOGGER.info("Checking rules convention", func="__init__")
        if rules not in RULES_NAMES:
            raise ValueError(
                f"Given rules '{rules}' not among the available rules : {RULES_NAMES}"
            )

        # Opening rules_xls file (for the grib_param_df)
        self.rules = Rules(name=rules)

    def get_backend_kwargs(
        self, param: str, model: str, indexpath: str = ""
    ) -> Dict[str, Union[List[str], Dict[str, str], str]]:
        """get_backend_kwargs : Method which extract the exact backend_kwargs
        dictionnary for the cfgrib engine corresponding to the given param and
        model

        Args:
            param (str): Param name following the Promethee standard (defined
                in the RULES csv configuration file)
            model (str): Model name following the Promethee standard (defined
                in the RULES csv configuration file)
            indexpath (str, optional): Path to the directory where to store the
                .idx temporary files created by cfgrib. Defaults to ''.

        Returns:
            dict : Backend_kwargs dictionnary for the cfgrib engine :
                * read_keys : list of keys to read
                * filter_by_keys : dict of paired keys/value corresponding
                    to the given (param, model)
                * indexpath : path where to store the .idx files created by
                    cfgrib. Default to ''.
        """
        try:
            raw_dico = self.rules.grib_param_df.loc[(param, model)].dropna().to_dict()
        except KeyError:
            raw_dico = (
                self.rules.grib_param_df.loc[(param, "default")].dropna().to_dict()
            )
            LOGGER.warning(
                f"Using 'default' model to retrieve '{param}' backend_kwargs.",
                param=param,
                model=model,
                func="get_backend_kwargs",
            )
        param_keys = dict()
        for key, value in raw_dico.items():
            if key not in self.grib_param_dtypes:
                raise exception.ConfigurationError(
                    f"Grib param key '{key}' not referenced in the grib_param_dtypes"
                )
            value_type = self.grib_param_dtypes[key]
            param_keys[key] = value_type(value)

        return {
            "read_keys": list(param_keys.keys()) + self.mandatory_grib_param,
            "filter_by_keys": param_keys,
            "indexpath": indexpath,
        }

    @staticmethod
    def extract_param_from_file(
        file_conf: dict,
    ) -> Tuple[str, dict, dict, xr.DataArray]:
        """extract_param_from_file : Extracts a single parameter from a single
        grib file

        Args:
            file_conf (dict): Dictionnary configuring the file to open and the
                param to extract. It contains the following keys :
                * grib_filename : Name of the raw grib file
                * backend_kwargs : backend cfgrib kwargs used to extract the
                    correct parameter
                * preproc_filename : Name of the output netcdf file
                * grib_attrs : Attributes corrections
        """
        dataarray = None
        try:
            dataarray = xr.open_dataarray(
                file_conf["grib_filename"],
                engine="cfgrib",
                backend_kwargs=file_conf["backend_kwargs"],
            )
        except Exception:
            LOGGER.error(
                "Failed to extract parameter from grib file.",
                grib_filename=file_conf["grib_filename"],
                preproc_filename=file_conf["preproc_filename"],
                backend_kwargs=file_conf["backend_kwargs"].get("filter_by_keys"),
                func="extract_param_from_file",
            )
            return None

        # Attributes corrections
        for attr_key, attr_value in file_conf["grib_attrs"].items():
            if attr_key not in dataarray.attrs:
                dataarray.attrs[attr_key] = attr_value
                continue

            if attr_value == dataarray.attrs.get(attr_key):
                continue

            if (
                attr_key == "units"
                and dataarray.attrs[attr_key] != attr_value
                and attr_value is not None
            ):
                LOGGER.debug(
                    f"Found 'units' = { dataarray.attrs[attr_key]} "
                    f"while '{attr_value}' expected. "
                    f"Changing 'units' to '{attr_value}'.",
                    grib_filename=file_conf["grib_filename"],
                    preproc_filename=file_conf["preproc_filename"],
                    func="extract_param_from_file",
                )
                dataarray.attrs[attr_key] = attr_value

        return (
            file_conf["preproc_filename"],
            file_conf["preproc_attrs"],
            file_conf["postproc"],
            dataarray,
        )

    @staticmethod
    def concat_dataarrays(dict_das: dict, preproc_filename: str = None) -> xr.DataArray:
        """concat_dataarrays : concatenate a group of dataarrays into a single
        and apply cumulation preprocessing

        Args:
            dict_das (dict): Dictionary with all the dataarrays

        Returns:
            xr.DataArray: Concatenated and preprocessed dataarray
        """
        # Avant cela on va mettre les fichiers sur la grille désirée
        das = []
        source_steps = []
        GRIB_StepRange = []
        grid_changes = 0
        var_to_delete = set(["heightAboveGround", "time", "step", "surface"])
        for elt in dict_das["file"]:
            source_grid = elt["preproc"].get("source_grid")
            preproc_grid = elt["preproc"].get("preproc_grid")
            source_steps.append(int(elt["preproc"].get("source_step", 1)))
            # On etend du nombre de step present dans le fichier en entree.
            GRIB_StepRange.extend(
                [elt["da"].attrs["GRIB_endStep"] - elt["da"].attrs["GRIB_startStep"]]
                * elt["da"].step.size
            )
            # On vire certaine variables
            drop_var = set(elt["da"].coords).intersection(var_to_delete)
            elt["da"] = elt["da"].drop_vars(list(drop_var))
            if source_grid != preproc_grid:
                grid_changes += 1
                da = xr_utils.change_grid(elt["da"], preproc_grid)
                das.append(da)
            else:
                das.append(elt["da"])
        LOGGER.debug(
            "Changement de grilles effectués",
            number_grid_change=grid_changes,
            preproc_filename=preproc_filename,
            func="concat_dataarrays",
        )

        # Maintenant on concatene les differentes steps.
        concat_da = xr.concat(das, dim="valid_time")

        # Faire le postprocessing
        LOGGER.debug(
            f"Element pour le postprocessing : {dict_das['postproc']}",
            preproc_filename=preproc_filename,
            func="concat_dataarrays",
        )

        # Enforcing variable name
        variable_name = dict_das["postproc"].get("param")
        LOGGER.info(
            "Fixing promethee name.",
            old_name=concat_da.name,
            new_name=variable_name,
            preproc_filename=preproc_filename,
            func="concat_dataarrays",
        )
        concat_da.name = variable_name

        da_out = concat_da

        # On regarde si on doit accumuler.
        accum = dict_das["postproc"].get("accum")
        if accum is not None:
            # On fait des choses sur les step units.
            stepUnits = xr.Dataset()
            stepUnits["stepSize"] = ("valid_time", GRIB_StepRange)
            stepUnits.coords["valid_time"] = concat_da.coords["valid_time"]
            concat_da = concat_da.sortby("valid_time")
            stepUnits = stepUnits.sortby("valid_time")
            LOGGER.debug(
                f"stepUnits = {stepUnits}",
                accum=accum,
                preproc_filename=preproc_filename,
                func="concat_dataarrays",
            )
            LOGGER.debug(
                "Doing accumulation",
                preproc_filename=preproc_filename,
                func="concat_dataarrays",
            )
            # On va changer le nom de la variable pour inclure l'accumulation
            l_var = variable_name.split("__")
            l_var[0] = l_var[0] + str(accum)
            concat_da.name = "__".join(l_var)
            LOGGER.debug(
                "Fixing promethee name for accumulation",
                old_name=variable_name,
                new_name=concat_da.name,
                preproc_filename=preproc_filename,
                func="concat_dataarrays",
            )
            da_out = xr_utils.compute_sum_futur(
                concat_da,
                stepout=accum,
                var="valid_time",
                da_step=stepUnits["stepSize"],
            ).sel(valid_time=concat_da.valid_time)

        elif (np.array(source_steps) != dict_das["postproc"]["step"]).any():
            LOGGER.info(
                "source_step != target_step, passage par xr_utils.fill_dataarray",
                source_steps=source_steps,
                target_step=dict_das["postproc"]["step"],
                preproc_filename=preproc_filename,
                dim="valid_time",
            )
            da_out = xr_utils.fill_dataarray(
                da=concat_da,
                source_steps=source_steps,
                target_step=dict_das["postproc"]["step"],
                dim="valid_time",
                freq_base="h",
            )

        LOGGER.debug(
            f"da_out={da_out.load()}",
            preproc_filename=preproc_filename,
            source_steps=source_steps,
            target_step=dict_das["postproc"]["step"],
            start=str(dict_das["postproc"]["start"]),
            stop=str(dict_das["postproc"]["stop"]),
        )
        return xr_utils.slice_dataarray(
            da=da_out,
            start=dict_das["postproc"]["start"],
            stop=dict_das["postproc"]["stop"],
            dim="valid_time",
        )

    def concat_export_dataarrays(self, dataarray_group: Tuple[str, dict]) -> bool:
        """concat_export_dataarrays : Concatenate and export to netcdf a
        group of xarray DataArrays

        Args:
            dataarray_group (tuple) : This tuple has two components :
                * ouput_filename (str) : name of the netcdf file to be exported
                * dict_das (dictionnaire) :

        Returns:
            bool : True if the export went correctly
        """
        preproc_filename, dict_das = dataarray_group
        try:
            concat_da = self.concat_dataarrays(
                dict_das=dict_das, preproc_filename=preproc_filename
            )
        except Exception:
            LOGGER.error(
                f"Failed to concat {preproc_filename}",
                func="concat_export_dataarrays",
                preproc_filename=preproc_filename,
                exc_info=True,
            )
            return False
        try:
            concat_da.to_netcdf(preproc_filename)
        except BaseException:
            LOGGER.error(
                f"Failed to export {preproc_filename}",
                func="concat_export_dataarrays",
                preproc_filename=preproc_filename,
                exc_info=True,
            )
            return False
        return os.path.isfile(preproc_filename)

    def build_stack(self, batch_size: int) -> List[dict]:
        """build_stack : Builds a kind of "task processing stack" in order
        to optimize the use of CPUs with the limitation of available RAM
        (batch_size)

        Args:
            batch_size (int): Maximum number of files that can be opened
                simultaneously (a good approximation seems to be the available
                RAM in GB)

        Returns:
            list : List containing list of dictionnaries. Each list corresponds
                to a batch (to be processed through a Pool.map for parallel
                processing). Each dictionnary is the preprocessing config for
                a speficific file to extract.
        """
        stack = []
        current_batch = []
        # Loop on all the preprocessed files configurations to create
        # a 'raw stack', i.ea list of all the preprocessing config dicts
        for preproc_id, preproc_config in self.preprocessed_config.items():
            preproc_rh = preproc_config["resource_handler"][0]
            preproc_filename = preproc_rh["local"]
            os.makedirs(os.path.dirname(preproc_filename), exist_ok=True)
            root_param = preproc_config["agg"]["param"]
            # Retrieving all useful post-proc information
            preproc_rundate = Datetime(preproc_rh["date"])
            postproc = {
                "step": preproc_rh["step"],
                "start": preproc_rundate + Timedelta(hours=preproc_rh["begintime"]),
                "stop": preproc_rundate + Timedelta(hours=preproc_rh["endtime"]),
            }
            postproc.update(preproc_config["agg"])

            file_conf_list = []
            for source_id, source_info in preproc_config["sources"].items():
                for term in source_info["terms"]:
                    if str(term) not in self.sources_config[source_id]:
                        LOGGER.error(
                            "Inconsistency between term given by preprocessed file "
                            "and available source terms",
                            preproc_id=preproc_id,
                            source_id=source_id,
                            term=term,
                            func="build_stack",
                        )
                        continue
                    if len(self.sources_config[source_id][str(term)]) == 0:
                        LOGGER.error(
                            "Source file configuration empty.",
                            source_id=source_id,
                            term=term,
                            func="build_stack",
                        )
                        continue

                    source_conf = self.sources_config[source_id][str(term)][0]
                    # checking if the source_conf["local"] grib is missing or empty
                    grib_filename = source_conf["local"]
                    if grib_filename in self.missing_gribs:
                        # if grib is already labeled as missing
                        continue
                    else:
                        if not os.path.isfile(grib_filename):
                            # if grib is missing and not already labeled as missing
                            LOGGER.error(
                                "Missing source grib file.",
                                grib_filename=grib_filename,
                                source_id=source_id,
                                term=term,
                                func="build_stack",
                            )
                            self.missing_gribs.append(grib_filename)
                            continue

                        if os.path.getsize(grib_filename) < 1000:
                            LOGGER.error(
                                "Source grib file empty (size = "
                                f"{os.path.getsize(grib_filename)} octets).",
                                grib_filename=grib_filename,
                                source_id=source_id,
                                term=term,
                                func="build_stack",
                            )
                            self.missing_gribs.append(grib_filename)
                            continue

                    try:
                        backend_kwargs = self.get_backend_kwargs(
                            root_param, source_conf["model"]
                        )
                    except BaseException:
                        LOGGER.error(
                            "Failed to retrieve backend_kwargs for (param, model)"
                            f" = ({root_param}, {source_conf['model']}).",
                            grib_filename=grib_filename,
                            source_id=source_id,
                            term=term,
                            func="build_stack",
                            exc_info=True,
                        )
                        continue

                    # Case of a accum param with lengthOfTimeRange
                    if "lengthOfTimeRange" in backend_kwargs["filter_by_keys"]:
                        backend_kwargs["filter_by_keys"]["lengthOfTimeRange"] = int(
                            source_info["step"]
                        )

                    units = backend_kwargs["filter_by_keys"].pop("units", None)

                    file_conf = {
                        "grib_filename": source_conf["local"],
                        "backend_kwargs": backend_kwargs,
                        "preproc_filename": preproc_filename,
                        "grib_attrs": {
                            "PROMETHEE_z_ref": preproc_rh["geometry"],
                            "units": units,
                        },
                        "postproc": postproc,
                        "preproc_attrs": {
                            "source_grid": source_conf["geometry"],
                            "preproc_grid": preproc_rh["geometry"],
                            "source_step": int(source_info["step"]),
                        },
                    }

                    file_conf_list += [file_conf]

            if len(file_conf_list) >= batch_size:
                stack += [file_conf_list]

            elif len(current_batch) + len(file_conf_list) > batch_size:
                stack += [current_batch]
                current_batch = file_conf_list
            else:
                current_batch += file_conf_list

        if len(current_batch) > 0:
            stack += [current_batch]

        return stack

    def preprocess(self, nproc: int, batch_size: int):
        """preprocess : Preprocess all the data config dict in self.data_config

        Args:
            nproc (int): Number of CPUs to be used in parallel
            batch_size (int): Maximum number of files that can be opened
                simultaneously (a good approximation seems to be the available
                RAM in GB)
        """
        # Building the preprocessing stack
        stack = self.build_stack(batch_size)

        # Logging building stack results
        LOGGER.info(
            "Batchs in the preprocessing stack",
            batch_number=len(stack),
            func="preprocess",
        )

        # Opening and extracting by batch
        for batch_index, batch in enumerate(stack):
            LOGGER.info("Starting batch", batch_index=batch_index, func="preprocess")

            # Extracting parameters
            LOGGER.info(
                f"Batch {batch_index} : {len(batch)} dataarrays to extract",
                batch_index=batch_index,
                func="preprocess",
            )
            checkin = time.time()
            if nproc > 1:
                pool = Pool(nproc)
                file_das = pool.map(self.extract_param_from_file, batch)
                pool.close()
                pool.join()
            else:
                file_das = []
                for elt in batch:
                    file_das.append(self.extract_param_from_file(elt))
            checkout = time.time()
            LOGGER.info(
                f"Batch {batch_index} : done in {checkout-checkin:.1f} seconds",
                batch_index=batch_index,
                time_exec=checkout - checkin,
                func="preprocess",
            )

            # Grouping dataarrays by file
            checkin = time.time()
            grouped_das = dict()
            for file_da in file_das:
                if file_da is None or not (
                    isinstance(file_da, tuple) and len(file_da) == 4
                ):
                    continue
                preproc_filename, preproc, postproc, dataarray = file_da
                grouped_das.setdefault(preproc_filename, {}).setdefault(
                    "file", []
                ).append({"da": dataarray, "preproc": preproc})
                # On a un unique dictionnaire de postprocessing par fichier de
                # sortie
                grouped_das[preproc_filename]["postproc"] = postproc
            checkout = time.time()
            LOGGER.info(
                f"Batch {batch_index} : grouped in {checkout-checkin:.1f} seconds",
                batch_index=batch_index,
                time_exec=checkout - checkin,
                func="preprocess",
            )

            # Concat and export
            checkin = time.time()
            if nproc > 1:
                pool = Pool(nproc)
                pool.map(self.concat_export_dataarrays, list(grouped_das.items()))
                pool.close()
                pool.join()
            else:
                for elt in list(grouped_das.items()):
                    LOGGER.info(
                        "Concat and export on element",
                        preproc_filename=elt[0],
                        batch_index=batch_index,
                        func="preprocess",
                    )
                    self.concat_export_dataarrays(elt)
            checkout = time.time()
            LOGGER.info(
                f"Batch {batch_index} : exported in {checkout-checkin:.1f} seconds",
                batch_index=batch_index,
                time_exec=checkout - checkin,
                func="preprocess",
            )
