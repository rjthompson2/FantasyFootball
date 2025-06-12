import numpy as np
import pandas as pd
import math
import logging


LOG = logging.getLogger(__name__)


def error_calculator(
    prediction: pd.DataFrame, actual: pd.DataFrame, on: list, keep: list = None
):
    diff_df = {}
    merged_dfs = pd.merge(actual, prediction, on="PLAYER")

    for column in on:
        # subtract all rows, get the absolute value, sums them, then gets the total, and averages it
        difference_df = round(abs(merged_dfs[column + "_x"].sub(merged_dfs[column + "_y"])), 2)
        # subtract all rows, get the absolute value, divide by original, multiply by 100, then gets the total, and averages it
        accuracy_df = round(
            100
            - abs(merged_dfs[column + "_x"].sub(merged_dfs[column + "_y"]))
            .div(merged_dfs[column + "_x"])
            .mul(100),
            2,
        )
        accuracy_df = accuracy_df.apply(lambda x: 0 if x < 0 or x > 100 else x)

        diff_df[column + "Numeric"] = difference_df
        diff_df[column + "Accuracy"] = accuracy_df
        # difference["STD"] = math.sqrt(actual - prediction**2/len(total))

        if keep and len(keep) > 0:
            for item in keep:
                if item not in diff_df:
                    if item == column:
                        diff_df["Expected"] = merged_dfs[item + "_y"]  # prediction FPTS
                        diff_df["Actual"] = merged_dfs[item + "_x"]  # actual FPTS
                    else:
                        diff_df[item] = merged_dfs[item]

    return diff_df
