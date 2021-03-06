from multiprocessing import Pool
import subprocess

codes = ['./commands/run_data_visualization.sh', './commands/run_drafter_gui.sh', 'python webapp/app.py']

def run_bash(code:str) -> None:
    subprocess.run(code.split())


if __name__ == '__main__':
    try:
        p = Pool(5)
        p.map(run_bash, codes)
    except KeyboardInterrupt:
        p.close()
