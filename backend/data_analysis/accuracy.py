import numpy as np
import pandas as pd
import math
import logging


LOG = logging.getLogger(__name__)


def error_calculator(prediction: pd.DataFrame, actual: pd.DataFrame, on:list, keep:list=None):
    diff_df = {}

    for column in on:
        #subtract all rows, get the absolute value, sums them, then gets the total, and averages it
        difference_num = round(abs(actual[on].sub(prediction[on]))[on].sum().iloc[0]/len(actual[on]) , 2)
        #subtract all rows, get the absolute value, divide by original, multiply by 100, then gets the total, and averages it
        difference_percent = round(abs(actual[on].sub(prediction[on])).div(actual[on]).mul(100)[on].sum().iloc[0]/len(actual[on]), 2)
        
        diff_df["Numeric"] = difference_num
        diff_df["Percentage"] =  difference_percent
        # difference["STD"] = math.sqrt(actual - prediction**2/len(total))

        LOG.warning(diff_df["Numeric"])
        LOG.warning(diff_df["Percentage"])