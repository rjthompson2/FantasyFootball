from backend.data_collection.utils import Positions

class TestUtils():
    def test_positions_has_value(self):
        assert Positions.has_value('rb')
        assert Positions.has_value('qb')
        assert Positions.has_value('te')
        assert Positions.has_value('wr')
        assert Positions.has_value('k')
        assert Positions.has_value('dst')