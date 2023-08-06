from typing import List
import pandas as pd
from pandas.core.frame import DataFrame
from sklearn.preprocessing import MinMaxScaler


def get_low_pearson_r(
    df_well: DataFrame, r_window_size: int, logname: str, col: str, thresh: float
) -> DataFrame:
    """
    Flags samples with low correlation compared to window around it

    Args:
        df_well (DataFrame): data of one well
        r_window_size (int): window size
        logname (str): log being analyzed
        col (str): column being compared to
        thresh (float): threshold for being a bad correlation

    Returns:
        DataFrame: flagged dataframe
    """
    df_interpolated = df_well[[logname, col]].interpolate()
    rolling_r = df_interpolated[logname].rolling(
        window=r_window_size,
        center=True
    ).corr(df_interpolated[col])
    df_well[f"r_{col}"] = rolling_r
    df_well[f"bad_wr_{col}"] = df_well[f"r_{col}"] < thresh
    # Fill the gap between bad samples if two consecutive bad samples are less
    # than "r_window_size" apart
    mask = df_well[f"bad_wr_{col}"].groupby(
        (
            df_well[f"bad_wr_{col}"] != df_well[f"bad_wr_{col}"].shift()
        ).cumsum()
    ).transform("count").lt(r_window_size)
    mask &= df_well[f"bad_wr_{col}"].eq(False)
    df_well[f"bad_wr_{col}"].update(
        df_well[f"bad_wr_{col}"].loc[mask].replace(False, True)
    )
    return df_well


def flag_well(
    df_well: DataFrame, logname: str, cols: List, r_window_size: int, thresh: float
) -> DataFrame:
    """
    Flags samples with anomalous correlations

    Args:
        df_well (DataFrame): data of one well
        logname (str): log being analyzed
        cols (list): list of columns to compare logname to
        r_window_size (int): window size
        thresh (float): window value threshold to which consider sample an anomaly

    Returns:
        DataFrame: flagged dataframe
    """
    df_well_flagged = pd.DataFrame()
    df_well[[logname]] = MinMaxScaler().fit_transform(df_well[[logname]].values)
    df_well["bad_r"] = False
    for col in cols:
        df_well[[col]] = MinMaxScaler().fit_transform(df_well[[logname]].values)
        df_well = get_low_pearson_r(df_well, r_window_size, logname, col, thresh)
        df_well["bad_r"] = df_well[f"bad_wr_{col}"] | df_well["bad_r"]
    df_well_flagged = df_well_flagged.append(df_well)
    return df_well_flagged


def get_corr_anomalies(
    df_well: DataFrame, logname: str, cols: List, r_window_size: int, thresh: float
) -> List:
    """
    Flags correlations anomalies

    Args:
        df_well (DataFrame): data of one well
        logname (str): log being analyzed
        cols (list): list of columns to compare logname to
        r_window_size (int): window size
        thresh ([type]): [description]

    Returns:
        list: list of anomalous indices
    """
    df_well.fillna(method="ffill", inplace=True)
    df_well.fillna(method="bfill", inplace=True)
    df_flagged = flag_well(
        df_well, logname,
        [c for c in cols if c != logname],
        r_window_size,
        thresh
    )
    df_flagged.fillna(False, inplace=True)
    return df_flagged[df_flagged.bad_r == True].index


def flag_correlate(
    df_well: DataFrame, y_pred: DataFrame = None, **kwargs
) -> DataFrame:
    """
    Returns anomalous correlation indices for AC, ACS and DEN

    Args:
        df_well (DataFrame): df with one wells data
        y_pred (DataFrame, optional): df with results of predictions. Defaults to None.
    Returns:
        DataFrame: df with flag columns
    """
    print("Method: correlation...")
    if y_pred is None:
        y_pred = df_well.copy()
    expected_curves = kwargs.get(
        "expected_curves",
        set([
            "DEPTH", "DEN", "DENC", "AC", "ACS", "BS", "CALI",
            "GR", "NEU", "RDEP", "RMED", "RMIC", "GROUP"
        ])
    )
    y_pred.loc[:, [
        "flag_correlation_gen",
        "flag_correlation_ac",
        "flag_correlation_acs",
        "flag_correlation_den"
    ]] = 0, 0, 0, 0
    r_window_size = kwargs.get("r_window_size", 5)
    thresh = kwargs.get("thresh", 1)
    cols = kwargs.get("cols", list(expected_curves))
    ac_corr_anomalies = get_corr_anomalies(
        df_well, "AC", cols, r_window_size, thresh
    )
    acs_corr_anomalies = get_corr_anomalies(
        df_well, "ACS", cols, r_window_size, thresh
    )
    den_corr_anomalies = get_corr_anomalies(
        df_well, "DEN", cols, r_window_size, thresh
    )
    y_pred.loc[
        ac_corr_anomalies, ["flag_correlation_gen", "flag_correlation_ac"]
    ] = 1
    y_pred.loc[
        acs_corr_anomalies, ["flag_correlation_gen", "flag_correlation_acs"]
    ] = 1
    y_pred.loc[
        den_corr_anomalies, ["flag_correlation_gen", "flag_correlation_den"]
    ] = 1
    return y_pred
