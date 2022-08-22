import numpy as np
import pandas as pd
import math
import logging


LOG = logging.getLogger(__name__)


def error_calculator(prediction: pd.DataFrame, actual: pd.DataFrame, on:list, keep:list=None):
    diff_df = {}

    for column in on:
        #TODO need ot match points to player name
        #subtract all rows, get the absolute value, sums them, then gets the total, and averages it
        difference_num_df = round(abs(actual[on].sub(prediction[on])), 2)
        difference_num = round(difference_num_df.sum()/len(actual) , 2)
        #subtract all rows, get the absolute value, divide by original, multiply by 100, then gets the total, and averages it
        accuracy_df = round(100-abs(actual[on].sub(prediction[on])).div(actual[on]).mul(100), 2)
        avg_accuracy = round(accuracy_df.sum()/len(actual), 2)
        print(avg_accuracy)
        
        diff_df["Numeric"] = difference_num_df
        diff_df["Accuracy"] =  accuracy_df
        # difference["STD"] = math.sqrt(actual - prediction**2/len(total))

        # LOG.warning(diff_df["Numeric"])
        # LOG.warning(diff_df["Accuracy"])
        return diff_df