import pytest
import logging
import pandas as pd
from backend.data_collection.utils import get_season_year
from backend.data_collection.Connectors import DraftConnector


LOG = logging.getLogger(__name__)


class TestDraftConnector(DraftConnector):
    def load(self, df:pd.DataFrame) -> None:
        return

class TestConnectors():
    def test_draft_connector(self):
        TestDraftConnector(get_season_year()).run()