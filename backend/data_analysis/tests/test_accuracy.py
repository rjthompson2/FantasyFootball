from backend.data_analysis.accuracy import error_calculator
import pandas as pd
import pytest


class TestAccuracy:
    prediction = pd.DataFrame({"PLAYER": ["A", "B", "C", "D"], "FPTS": [390, 384, 372, 365]})
    accuracy = pd.DataFrame({"PLAYER": ["A", "B", "C", "D"], "FPTS": [400, 280, 350, 360]})

    def test_error_calculator(self):
        result = error_calculator(self.prediction, self.accuracy, on=["FPTS"])
        assert result != None
