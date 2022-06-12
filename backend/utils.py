import os
import re

def get_parent_folder(parent: str) -> str:
    current = os.path.abspath(__file__)
    while not current.endswith('/'+parent):
        current = os.path.dirname(current)
    return current


def get_from_data_folder(file_path="": str) -> str:
    if file_path != "" and not file_path.startswith('/'):
        file_path = '/'+file_path
    path = get_parent_folder("FantasyFootball")
    return path + f"/backend/data{file_path}"