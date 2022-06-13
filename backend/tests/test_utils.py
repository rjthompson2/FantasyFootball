from backend.utils import find_parent_folder, find_in_data_folder

class TestUtils:
    def test_get_parent_folder(self):
        result = find_parent_folder("FantasyFootball")
        assert result.endswith("/FantasyFootball")
        result = find_parent_folder("/FantasyFootball")
        assert result.endswith("/FantasyFootball")

    
    def test_find_in_data_folder(self):
        result = find_in_data_folder(f"test")
        assert result.endswith("/FantasyFootball/backend/data/test")
        result = find_in_data_folder(f"/test")
        assert result.endswith("/FantasyFootball/backend/data/test")

