import os
import re
import logging


LOG = logging.getLogger(__name__)


def find_parent_dir(parent: str) -> str:
    current = os.getcwd()

    if parent.startswith('/'):
        parent = parent[1:]

    while not current.endswith('/'+parent):
        current = os.path.dirname(current)
    return current


def find_in_data_folder(file_path: str) -> str:
    LOG.warning("First")
    if file_path != "" and not file_path.startswith('/'):
        file_path = '/'+file_path
    path = find_parent_dir("FantasyFootball")
    return f"{path}/backend/data{file_path}"