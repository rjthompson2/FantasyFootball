from backend.draft import Draft
import pandas as pd
import pytest

class TestDraft:
    def test_draft(self):
        drft = Draft(pd.DataFrame(), 0)
        assert drft != None

    def test_draft_snake_increment(self):
        drft = Draft(pd.DataFrame(), 14)
        value = drft.snake_increment(5)
        assert value > 1
        value = drft.snake_increment(14)
        assert value < 14

    def test_draft_player(self):
        drft = Draft(pd.DataFrame(["Test"], columns=["PLAYER", "POS", "TEAM", ]), 14)
        drft.draft_player("Test")

    def test_draft_player_edge_case(self):
        player = "Test"
        drft = Draft(pd.DataFrame(), 14)
        drft.draft_player(player)
        assert self.draft["PLAYER"] == [player]
        assert self.draft["POS"] == ["?"]
        assert self.draft["TEAM"] == ["?"]
        assert self.draft["ORDER"] == ["?"]
        assert self.draft["VOR"] == ["?"]

        assert self.current_round == 2
        assert self.current_team == 2
