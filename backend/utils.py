import os
import re
import logging
from enum import Enum


LOG = logging.getLogger(__name__)


def find_parent_dir(parent: str) -> str:
    current = os.getcwd()

    if parent.startswith("/"):
        parent = parent[1:]

    current = re.findall("/.*" + parent, current)[0]
    if current == None:
        raise RuntimeError

    return current


def find_in_data_folder(file_path: str) -> str:
    if file_path != "" and not file_path.startswith("/"):
        file_path = "/" + file_path
    path = find_parent_dir("FantasyFootball")
    return f"{path}/backend/data{file_path}"


class Teams(Enum):
    ARI = "ARI"
    ATL = "ATL"
    BAL = "BAL"
    BUF = "BUF"
    CAR = "CAR"
    CHI = "CHI"
    CIN = "CIN"
    CLE = "CLE"
    DAL = "DAL"
    DEN = "DEN"
    DET = "DET"
    GB = "GB"
    HOU = "HOU"
    IND = "IND"
    JAX = "JAX"
    KC = "KC"
    LA = "LA"
    LAC = "LAC"
    LV = "LV"
    MIA = "MIA"
    MIN = "MIN"
    NE = "NE"
    NO = "NO"
    NYG = "NYG"
    NYJ = "NYJ"
    PHI = "PHI"
    PIT = "PIT"
    SEA = "SEA"
    SF = "SF"
    TB = "TB"
    TEN = "TEN"
    WAS = "WAS"

    def __repr__(self):
        return self.value

    @classmethod
    def has_value(cls, value: str):
        return value in cls._value2member_map_

    @classmethod
    def length(cls):
        return len(cls.__members__)
