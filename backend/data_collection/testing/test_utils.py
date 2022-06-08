from backend.data_collection.utils import Positions

class TestUtils():
    def test_positions_has_value(self):
        assert Positions.has_value('wr')