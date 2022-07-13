from multiprocessing import Pool
import subprocess
import os
path = os.path.abspath(os.getcwd())

codes = ['./commands/run_data_visualization.sh', './commands/run_drafter_gui.sh', 'python webapp/app.py']

def run_bash(code:str) -> None:
    print(code)
    subprocess.run(code.split())


if __name__ == '__main__':
    p = Pool(5)
    p.map(run_bash, codes)
    p.join()