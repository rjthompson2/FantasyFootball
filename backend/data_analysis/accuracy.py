import numpy as np
import pandas as pd
import math
import logging


LOG = logging.getLogger(__name__)


def error_calculator(prediction: pd.DataFrame, actual: pd.DataFrame, on:list, keep:list=None):
    diff_df = {}

    for column in on:
        #TODO need ot match points to player name
        print(actual)
        print(prediction)
        new = pd.merge(actual, prediction, on='PLAYER')
        print(new)
        #subtract all rows, get the absolute value, sums them, then gets the total, and averages it
        difference_num_df = round(abs(new[on+'_x'].sub(new[on+'_y'])), 2)
        difference_num = round(difference_num_df.sum()/len(new) , 2)
        #subtract all rows, get the absolute value, divide by original, multiply by 100, then gets the total, and averages it
        accuracy_df = round(100-abs(new[on+'_x'].sub(new[on+'_y'])).div(new[on+'_x']).mul(100), 2)
        avg_accuracy = round(accuracy_df.sum()/len(new), 2)
        print(avg_accuracy)
        
        diff_df["FPTSNumeric"] = difference_num_df
        diff_df["FPTSAccuracy"] =  accuracy_df
        diff_df["PLAYER"] =  new['PLAYER']
        diff_df["POS"] =  new['POS']
        diff_df['Expected'] = new['FPTS_y'] #prediction FPTS
        diff_df['Actual'] = new['FPTS_x'] #actual FPTS
        diff_df["ECR"] = new['ECR']
        diff_df["ADP"] = new['ADPRANK']
        diff_df["ActualRank"] =  new['Rank']
        # difference["STD"] = math.sqrt(actual - prediction**2/len(total))

        # LOG.warning(diff_df["Numeric"])
        # LOG.warning(diff_df["Accuracy"])
        return diff_df