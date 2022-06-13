import os
import re

def find_parent_folder(parent: str) -> str:
    current = os.path.abspath(__file__)
    if parent.startswith('/'):
        parent = parent[1:]
    while not current.endswith('/'+parent):
        current = os.path.dirname(current)
    return current


def find_in_data_folder(file_path: str) -> str:
    if file_path != "" and not file_path.startswith('/'):
        file_path = '/'+file_path
    path = find_parent_folder("FantasyFootball")
    return path + f"/backend/data{file_path}"