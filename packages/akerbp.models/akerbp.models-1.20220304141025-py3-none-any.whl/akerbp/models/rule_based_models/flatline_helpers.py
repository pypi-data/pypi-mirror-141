from typing import List
import pandas as pd
from pandas.core.frame import DataFrame, Series
import numpy as np


def keep_n_largest_groups(df_: Series, n: int) -> List:
    """
    Returns flatlines indices for AC, ACS and DEN

    Args:
        df_ (Series): series with flags
        n (int): number of large groups of consecutive anomalies to keep

    Returns:
        List: processed flags
    """
    df = pd.DataFrame(df_.astype(int).values, columns=['flatline'])
    df['groups'] = df['flatline'].ne(df['flatline'].shift()).cumsum()
    count_groups = df[df.flatline == 1].groups.value_counts()
    count_groups = count_groups[:n].index.tolist()
    df['large_group'] = False
    df.loc[df.groups.isin(count_groups), 'large_group'] = True
    return df.large_group.values


def remove_small_groups(df_: Series, n: int) -> Series:
    """
    Remove small groups of consecutive flags.

    Args:
        df (Series): series to be processed
        n (int): number of consecutive flags to be considered a small group

    Returns:
        Series: processed series
    """

    df = pd.DataFrame(df_.astype(int).values, columns=['flatline'])
    df.loc[:, 'groups'] = df['flatline'].ne(df['flatline'].shift()).cumsum()
    count_groups = df[df.flatline == 1].groups.value_counts()
    count_groups = count_groups[count_groups > n].index.tolist()
    df.loc[:, 'large_group'] = False
    df.loc[df.groups.isin(count_groups), 'large_group'] = True
    return df.large_group.values


def get_sampling_rate(df: DataFrame, logname: str) -> float:
    """
    Returns sampling rate of the logname based on the vertical depth.

    Args:
        df (DataFrame): dataframe with depth and log
        logname (str): log to which get sampling rate

    Returns:
        float: sampling rate of log
    """
    vc = df.DEPTH.diff().value_counts(normalize=True)
    sampling_rate = (vc * vc.index).sum()
    return sampling_rate


def get_cte_values(
    df: DataFrame,
    logname: str,
    sampling_rate: float,
    th: float = 0,
    small_groups: int = 2
) -> List:
    """
    Get consecutive same or similar enough values to be considered constant.

    Args:
        df (DataFrame): dataframe containing logname to find flatlines
        logname (str): log to find flatlines
        sampling_rate (float): log sampling rate
        small_groups (int): number of flags in small group to be removed.Defaults to 2.
        th (float, optional): threshold to be considered flatline. Defaults to 0.

    Returns:
        List: list of indices in dataframe that are flagged as flatline
    """
    df.loc[:, 'flatline'] = (
        df[logname].diff().abs() / sampling_rate <= th
    )
    df.loc[:, 'flatline'] = remove_small_groups(df.flatline, small_groups)
    df.loc[:, 'flatline'] = df['flatline'].replace(False, np.nan).fillna(
        method='bfill', limit=1
    ).replace(np.nan, False)
    return df[df['flatline']].index


def get_cte_derivatives(
    df: DataFrame,
    logname: str,
    sampling_rate: float,
    th: float = 0,
    small_groups: int = 2
) -> List:
    """
    Flags flatlines based on the second difference of consecutive values

    Args:
        df (DataFrame): dataframe containing logname to find flatlines
        logname (str): log to find flatlines
        sampling_rate (float): log sampling rate
        small_groups (int): number of flags in small group to be removed.Defaults to 2.
        th (float, optional): threshold to be considered flatline. Defaults to 0.

    Returns:
        List: list of indices in dataframe that are flagged as flatline
    """
    df.loc[:, 'flatline'] = (
        df[logname].diff().diff().abs() / sampling_rate <= th
    )
    df.loc[:, 'flatline'] = remove_small_groups(df.flatline, small_groups)
    df.loc[:, 'flatline'] = df['flatline'].replace(False, np.nan).fillna(
        method='bfill', limit=2
    ).replace(np.nan, False)
    return df[df['flatline']].index


def get_small_changes(
    df: DataFrame,
    logname: str,
    sampling_rate: float,
    th: float = 0,
    window: int = 3,
    small_groups: int = 2
) -> List:
    """
    Flags flatlines based on the second difference of consecutive values
    and mean and standard deviation of the window

    Args:
        df (DataFrame): dataframe containing logname to find flatlines
        logname (str): log to find flatlines
        sampling_rate (float): log sampling rate
        small_groups (int): number of flags in small group to be removed.Defaults to 2.
        th (float, optional): threshold to be considered flatline. Defaults to 0.
        window (int, optional): size of window to get mean and stf. Deafults to 3.

    Returns:
        List: list of indices in dataframe that are flagged as flatline
    """
    df.loc[:, 'd2'] = df[logname].diff().diff() / sampling_rate
    df.loc[:, 'flatline'] = (
        df['d2'].abs() <= th
    ) & (
        df['d2'].rolling(window, center=True).mean() <= th
    ) & (
        df['d2'].rolling(window, center=True).std() <= th
    )
    df.loc[:, 'flatline'] = remove_small_groups(df.flatline, small_groups)
    df.loc[:, 'flatline'] = df['flatline'].replace(False, np.nan).fillna(
        method='bfill', limit=1
    ).replace(np.nan, False)
    return df[df['flatline']].index


def get_interpolated_points(
    df: DataFrame,
    logname: str,
    sampling_rate: float,
    th: float = 0,
    small_groups: int = 2
) -> List:
    """
    Flags flatlines based on constant (or close to) gradients

    Args:
        df (DataFrame): dataframe containing logname to find flatlines
        logname (str): log to find flatlines
        sampling_rate (float): log sampling rate
        small_groups (int): number of flags in small group to be removed.Defaults to 2.
        th (float, optional): threshold to be considered flatline. Defaults to 0.

    Returns:
        List: list of indices in dataframe that are flagged as flatline
    """
    df.loc[:, 'd1'] = np.abs(np.gradient(df[logname])) / sampling_rate
    return get_cte_values(df, 'd1', sampling_rate, th, small_groups)


def detect_flatlines_old(
    df: pd.DataFrame,
    col: str,
    lim: float,
    window: int = 5,
    n_largest_groups: int = 10
) -> List:
    """
    Returns flatlines indices given log

    Args:
        df (DataFrame): dataframe with log to be processed(col) and depth
        col (str): column to which find flags
        lim (float): threshold for consedeiring anomalous derivatives
        window (int): size of window to compared single point to
        n_largest_groups (int): number of large groups of consecutive anomalies to keep

    Returns:
        List: flags flor given column
    """

    # get sampling rate
    vc = df.DEPTH.diff().value_counts(normalize=True)
    sampling_rate = (vc * vc.index).sum()
    # get second derivative
    df['d2'] = df[col].diff().diff().abs() / sampling_rate
    # detect flatlines based on derivative
    df['d2'] = ((df['d2'] < lim).multiply(
        df['d2'].rolling(window, center=True).median().isnull())
    ) | (
        df['d2'].rolling(window, center=True).median() < lim
    )
    # get largest groups to avoid false positives
    df['d2'] = keep_n_largest_groups(df['d2'], n_largest_groups)
    df['d2'] = np.where(df['d2'], 1, 0)
    return df['d2'].values  # which values are correct, d2 or v2? is v2 coming from d2?


def detect_flatlines(df: DataFrame, col: str, th: List, sg: int, w: int) -> List:
    """
    Puts together all methods for detecting flatlines

    Args:
        df (DataFrame): datfarame with log to detect flatlines and depth
        col (str): log name to process
        th (List): list of fours thresholds (one per method)
        sg (int): small groups to remove, if any
        w (int): window size for get small changes method

    Returns:
        List: list of flatline indices detected
    """
    sr = get_sampling_rate(df, col)
    idx = list(get_cte_values(
        df, col, sampling_rate=sr, th=th[0], small_groups=sg
    )) + list(get_small_changes(
        df, col, sampling_rate=sr, th=th[1], small_groups=sg, window=w
    )) + list(get_interpolated_points(
        df, col, sampling_rate=sr, th=th[2], small_groups=sg
    )) + list(get_cte_derivatives(
        df, col, sampling_rate=sr, th=th[3], small_groups=sg
    ))
    return idx


def flag_flatline(
    df_well: DataFrame, y_pred: DataFrame = None, **kwargs
) -> DataFrame:
    """
    Returns flatlines indices for AC, ACS and DEN

    Args:
        df_well (DataFrame): data from one well
        y_pred (DataFrame): results. Defaults to None.

    Returns:
        DataFrame: df with added column of results
    """
    print("Method: flatline...")
    default_kwargs = {
        "n_largest_groups": -1,
        "den_lim": 0.0001,
        "ac_lim": 0.0005,
        "acs_lim": 0.1,
        "small_groups": 2,
        "window": 3
    }
    user_kwargs = kwargs.get("flatline_params", {})
    kwargs = {}
    for k, v in default_kwargs.items():
        kwargs[k] = user_kwargs.get(k, v)

    if y_pred is None:
        y_pred = df_well.copy()

    y_pred.loc[:, [
        "flag_flatline_gen",
        "flag_flatline_ac",
        "flag_flatline_acs",
        "flag_flatline_den"
    ]] = 0, 0, 0, 0

    sg = kwargs["small_groups"]
    if sg == -1:  # if not remove anything
        sg = 0
    w = kwargs["window"]

    # AC flatlines
    col = "AC"
    th = kwargs[f"{col.lower()}_lim"]
    idx = detect_flatlines(df_well, col, [th, th, th, th / 50], sg, w)
    y_pred.loc[:, [f"flag_flatline_{col.lower()}"]] = 0
    if len(idx) > 0:
        y_pred.loc[set(idx), [f"flag_flatline_{col.lower()}"]] = 1

    # DEN flatlines
    col = "DEN"
    th = kwargs[f"{col.lower()}_lim"]
    idx = detect_flatlines(df_well, col, [th, th, th, th], sg, w)
    y_pred.loc[:, [f"flag_flatline_{col.lower()}"]] = 0
    if len(idx) > 0:
        y_pred.loc[set(idx), [f"flag_flatline_{col.lower()}"]] = 1

    # ACS flatlines
    col = "ACS"
    th = kwargs[f"{col.lower()}_lim"]
    idx = detect_flatlines(df_well, col, [th, th, th * 5, th / 2], sg, w)
    y_pred.loc[:, [f"flag_flatline_{col.lower()}"]] = 0
    if len(idx) > 0:
        y_pred.loc[set(idx), [f"flag_flatline_{col.lower()}"]] = 1

    # keep N largest groups, if chosen
    n_largest = kwargs['n_largest_groups']
    if n_largest != -1 and n_largest >= 0:
        for col in ["AC", "ACS", "DEN"]:
            y_pred[f"flag_flatline_{col.lower()}"] = keep_n_largest_groups(
                y_pred[f"flag_flatline_{col.lower()}"],
                n_largest
            )

    for col in ["AC", "ACS", "DEN"]:
        y_pred.loc[:, "flag_flatline_gen"] =\
            y_pred["flag_flatline_gen"] | y_pred[f"flag_flatline_{col.lower()}"]
    return y_pred
