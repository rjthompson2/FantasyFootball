from frontend.data_visualizer.utils import find_parent_dir, find_in_data_folder
import logging


LOG = logging.getLogger(__name__)


class TestUtils:
    def test_get_parent_folder(self):
        result = find_parent_dir("FantasyFootball")
        assert result.endswith("/FantasyFootball")
        result = find_parent_dir("/FantasyFootball")
        assert result.endswith("/FantasyFootball")

    
    def test_find_in_data_folder(self):
        result = find_in_data_folder(f"test")
        assert result.endswith("/FantasyFootball/backend/data/test")
        result = find_in_data_folder(f"/test")
        assert result.endswith("/FantasyFootball/backend/data/test")
