from multiprocessing import Pool
from backend.utils import reset_draft_copy
import subprocess

codes = [
    "frontend/commands/run_data_visualization.sh",
    "frontend/commands/run_drafter_gui.sh",
    "python frontend/webapp/app.py",
    "python backend/events/simple_listener.py",
    "python backend/events/sockets.py",
]


def run_bash(code: str) -> None:
    subprocess.run(code.split())


if __name__ == "__main__":
    reset_draft_copy()
    try:
        p = Pool(5)
        p.map(run_bash, codes)
    except KeyboardInterrupt:
        p.close()
