from backend.draft.Draft import Draft
import pandas as pd
import pytest

class TestDraft:
    def test_draft(self):
        drft = Draft(pd.DataFrame(), 0)
        assert drft != None

    def test_draft_snake_increment(self):
        drft = Draft(pd.DataFrame(), 14)
        value = drft.snake_increment(5)
        for i in range(14):
            value = drft.snake_increment(1)
            assert value > 1
        for i in range(14):
            value = drft.snake_increment(1)
            assert value < 14

    def test_draft_player(self):
        drft = Draft(pd.DataFrame([{"PLAYER":["Test"], "POS":["QB"], "TEAM":["WAS"]}]), 14)
        drft.draft_player("Test")

    def test_draft_player_edge_case(self):
        player = "Test"
        drft = Draft(pd.DataFrame(), 14)
        drft.draft_player(player)
        assert drft.draft["PLAYER"] == [player]
        assert drft.draft["POS"] == ["?"]
        assert drft.draft["TEAM"] == ["?"]
        assert drft.draft["ORDER"] == ["?"]
        assert drft.draft["VOR"] == ["?"]

        assert drft.current_round == 2
        assert drft.current_team == 2
