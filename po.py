import time
from datetime import datetime, timedelta
import argparse
from pathlib import Path
from rich.progress import Progress
from rich.console import Console
from rich.table import Table
from rich import box
from utils import read_json, write_json
from data import base_project
import click

# HOTKEY = 'p'

# running = Event()
# running.set()

# def handle_key_event(event):
#     if event.event_type == 'down':
#         if running.is_set():
#             running.clear()
#         else:
#             running.set()

# keyboard.hook_key(HOTKEY, handle_key_event)


WORK_PERIOD = 4
TIME_FORMAT = "%d-%m-%Y %H-%M-%S"
RUNNING = True
home = Path.home()
po_path = home / ".po"

# parser = argparse.ArgumentParser(description="Pomodoro Timer and Tracker")
# subparsers = parser.add_subparsers(help="stats n projects")

# project_parser = subparsers.add_parser('start', help='start a project timer')
# project_parser.add_argument('project', help='name of project')

# stats_parser = subparsers.add_parser('stats', help='get stats on projects')
# args = parser.parse_args()

@click.group()
def cli():
    pass

def create_profile() -> None:
    po_path.mkdir(exist_ok=True)
    
def project_exists(project_name: str) -> None:
    """ Determines if a project exists already """
    project_path = po_path / f"{project_name}.json"
    if not project_path.exists():
        write_json(project_path, base_project)

def project_update(project_name: str) -> None:
    """ Updates a project with a recently completed work period """
    project_path = po_path / f"{project_name}.json"

    project_data = read_json(project_path)
    project_data["pomos"].append(str(datetime.now().strftime(TIME_FORMAT)))
    write_json(project_path, project_data)

@cli.command()
@click.argument('project_name')
def start(project_name: str):
    project_exists(project_name)
    with Progress() as progress:
        work = progress.add_task("[red]Work!", total=WORK_PERIOD)

        while not progress.finished:
            progress.update(work, advance=1)
            time.sleep(1)

    project_update(project_name)

@cli.command()
def stats():
    table = Table(title="Pomodoro Stats", box=box.MINIMAL_DOUBLE_HEAD)
    table.add_column("Date")
    projects = po_path.glob("*.json")
    dt_now = datetime.now()
    total_time = 0
    for x in projects:
        project_data = read_json(x)
        pomos = project_data["pomos"]
        for pomo in pomos:
            table.add_row(pomo)
            dt_then = datetime.strptime(pomo, TIME_FORMAT)
            days = (dt_now - dt_then).days
            total_time += 20
    

    console = Console()
    console.print(table)
    console.print(f'{total_time / 60} hours focused overall.')

cli.add_command(stats)
cli.add_command(start)
if __name__ == '__main__':
    cli()

# Control Flow for CLI

