import numpy as np
import pandas as pd
import math
import logging


LOG = logging.getLogger(__name__)


def error_calculator(prediction: pd.DataFrame, actual: pd.DataFrame, on:list, keep:list=None):
    diff_df = {}

    for column in on:
        new = pd.merge(actual, prediction, on='PLAYER')
        #subtract all rows, get the absolute value, sums them, then gets the total, and averages it
        difference_df = round(abs(new[on+'_x'].sub(new[on+'_y'])), 2)
        difference_num = round(difference_df.sum()/len(new) , 2)
        #subtract all rows, get the absolute value, divide by original, multiply by 100, then gets the total, and averages it
        accuracy_df = round(100-abs(new[on+'_x'].sub(new[on+'_y'])).div(new[on+'_x']).mul(100), 2)
        accuracy_df = accuracy_df.apply(lambda x: 0 if x < 0 or x > 100 else x)
        avg_accuracy = round(accuracy_df.sum()/len(new), 2)
        print(avg_accuracy)

        diff_df[on+"Numeric"] = difference_df
        diff_df[on+"Accuracy"] =  accuracy_df
        # difference["STD"] = math.sqrt(actual - prediction**2/len(total))
        
        for item in keep:
            if item == on:
                diff_df['Expected'] = new[item+'_y'] #prediction FPTS
                diff_df['Actual'] = new[item+'_x'] #actual FPTS
            else:
                diff_df[item] = new[item]

        return diff_df