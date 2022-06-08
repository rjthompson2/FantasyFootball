from backend.data_collection.Bootstrap import get_bootstrap, get_cf
import pandas as pd
import logging


LOG = logging.getLogger(__name__)


class TestBootstrap():
    df = pd.DataFrame({'PLAYER': ['Joe', 'Joe', 'Joe'], 'POS':['WR', 'WR', 'WR'], 'FTPS': [323, 400, 22]})
    def test_get_bootstrap(self):
        data = get_bootstrap(self.df)
        
        assert all(i is not None for i in data)

    def test_get_cf(self):
        data = get_bootstrap(self.df)
        cf_df = get_cf(data)

        assert not cf_df.empty