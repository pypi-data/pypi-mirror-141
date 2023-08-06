from typing import Any, List, Dict
from pandas.core.frame import DataFrame
import os
import joblib
import pandas as pd
import importlib

from akerbp.mlpet import Dataset
from akerbp.models import Model
from akerbp.models import classification_models
from akerbp.models.rule_based_models import helpers


class BadlogModel(Model):
    """
    Badlog model class
    """

    def __init__(self, **kwargs):
        """
        Initializes badlog model
        """
        self.kwargs = kwargs
        for key, val in kwargs.items():
            setattr(self, key, val)

    def _validate_input(self, X: Any, **kwargs):
        """
        Validated input by checking type of X

        Args:
            X (DataFrame or dict): input data to model

        Raises:
            ValueError: if X is a dict and no metadata key
            ValueError: if X is a dict and no data key
            ValueError: if X not dict nor DataFrame
        """
        if isinstance(X, dict):
            if "metadata" not in X.keys():
                raise ValueError("'metadata' key is required")
            if "data" not in X.keys():
                raise ValueError("'data' key is required")
            X_df = pd.DataFrame.from_dict(X["data"])
            self.metadata = X["metadata"]
            self.X_pred, self.num_cols, self.cat_cols = helpers._apply_metadata(
                X_df, **kwargs.get("_metadata", self.metadata)
            )
        elif isinstance(X, pd.core.frame.DataFrame):
            X_df = X.copy()
            self.X_pred, self.num_cols, self.cat_cols = helpers._apply_metadata(
                X_df, **kwargs.get("_metadata", {})
            )
        else:
            raise ValueError("Please pass the data as a dict or a pandas DataFrame")

    def _init_cp_models(
        self,
        cp_names: List[str],
        folder_path: str,
        data_settings: Dict,
        model_settings: Dict,
        mappings: Dict,
    ):
        """
        Instantiate datasets and models for each of the crossplots

        Args:
            cp_names (list): list with crossplot names
            folder_path (str): path to folder with models
            data_settings (dict): settings of preprocessing for using the model
            model_settings (dict): settings of model XGBoost
            mappings (dict): mappings dictionary of cat variables

        Returns:
            tuple: dictionaries with dataset objects, models and key wells
        """
        datasets = dict()
        models = dict()
        folder_paths = dict()
        for cp_name in cp_names:
            print("init ds and model - BadlogModel - {}".format(cp_name))
            folder_paths[cp_name] = os.path.join(folder_path, cp_name)
            # Create dataset but don't load any data into the dataset, because
            # we need to get that from running the find_crossplot_scores
            datasets[cp_name] = Dataset(
                settings=data_settings,
                mappings=mappings,
                folder_path=folder_paths[cp_name],
            )
            models[cp_name] = classification_models.XGBoostClassificationModel(
                model_settings, folder_paths[cp_name]
            )
        return datasets, models

    def _get_cp_params(self, **kwargs):
        """
        Returns necessary variables to generate crossplots predictions

        Returns:
            tuple: path to models folder, settings for data and models,
            mappings dictionary
        """
        settings = kwargs.get("settings", None)
        mappings = kwargs.get("mappings", None)
        folder_path = kwargs.get("folder_path", None)
        # Assuming all cp_names use the same model- and data-settings
        if all([settings, mappings, folder_path]):
            model_settings = settings["models"]
            data_settings = settings["datasets"]
        else:
            raise ValueError(
                "Please provide settings, mappings and folder path for the crossplot method."
            )
        return folder_path, data_settings, model_settings, mappings

    def predict(self, X: Any, methods: List[str], **kwargs):
        """
        Args:
            X (dict or DataFrame): expected features
            methods (list): list of methods to apply on X

        Returns:
            y (DataFrame): including different badlog flags and scores
        """
        self._validate_input(X, **kwargs)
        # Validate feature
        self.X_pred = helpers._create_features(self.X_pred)
        self.X_pred_features = set(self.X_pred.columns)
        self.expected_curves = set(
            [
                "TVDBML",
                "DEPTH",
                "DEN",
                "DENC",
                "AC",
                "ACS",
                "BS",
                "CALI",
                "GR",
                "NEU",
                "RDEP",
                "RMED",
                "RMIC",
                "PEF",
                "GROUP",
            ]
        )
        helpers._validate_features(self.X_pred_features, self.expected_curves)
        self.methods = methods
        self.y = pd.DataFrame()
        for method in self.methods:
            # Evaluate method
            method_helpers = importlib.import_module(
                f"akerbp.models.rule_based_models.{method}_helpers"
            )
            method_evaluator = getattr(method_helpers, f"flag_{method}")
            if method == "crossplot":
                cp_names = kwargs.get("cp_names", ["vp_den", "vp_vs", "ai_vpvs"])
                datasets, models = self._init_cp_models(
                    cp_names, *self._get_cp_params(**kwargs)
                )
                method_flags = method_evaluator(
                    self.X_pred, cp_names, datasets, models
                )
            else:
                method_flags = method_evaluator(self.X_pred, **self.metadata, **kwargs)
            self.y[method_flags.columns] = method_flags
        result_columns = [
            col
            for col in self.y.columns
            if col.split("_")[0] in ["flag", "agg", "score"]
        ]
        return self.y[result_columns]
