import os
import re
import logging


LOG = logging.getLogger(__name__)


def find_parent_dir(parent: str) -> str:
    current = os.getcwd()

    if parent.startswith('/'):
        parent = parent[1:]

    current = re.findall('/.*'+parent, current)[0]
    if current == None:
        raise RuntimeError

    return current


def find_in_data_folder(file_path: str) -> str:
    if file_path != "" and not file_path.startswith('/'):
        file_path = '/'+file_path
    path = find_parent_dir("FantasyFootball")
    return f"{path}/backend/data{file_path}"