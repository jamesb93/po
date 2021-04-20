import time
from datetime import datetime, timedelta
from pathlib import Path
from rich.progress import Progress, BarColumn, TimeRemainingColumn
from rich.console import Console
from rich.table import Table
from rich import box
from po.utils import read_json, write_json
from po.data import base_project
import click


WORK_PERIOD = 1200
REST_PERIOD = 300
TIME_FORMAT = "%d-%m-%Y %H-%M-%S"
home = Path.home()
po_path = home / ".po"

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
def stats():
    table = Table(title="Pomodoro Stats", box=box.MINIMAL_DOUBLE_HEAD)
    table.add_column("Name")
    table.add_column("Today")
    table.add_column("Week")
    table.add_column("Month")
    table.add_column("Forever")

    projects = po_path.glob("*.json")
    dt_now = datetime.now()
    for x in projects:
        total_time = 0
        today_time = 0
        weekly_time = 0
        monthly_time = 0
        # Inside Project
        project_data = read_json(x)
        pomos = project_data["pomos"]
        for pomo in pomos:
            dt_then = datetime.strptime(pomo, TIME_FORMAT)
            days = (dt_now - dt_then).days
            if days <= 0:
                today_time += WORK_PERIOD
            if days <= 30:
                monthly_time += WORK_PERIOD
            if days <= 7:
                weekly_time += WORK_PERIOD
            total_time += WORK_PERIOD
        table.add_row(
            str(x.stem),
            f'{round(today_time / 60 / 60, 2)}', 
            f'{round(weekly_time / 60 / 60, 2)}', 
            f'{round(monthly_time / 60 / 60, 2)}',
            f'{round(total_time / 60 / 60, 2)}'
        )
    Console().print(table)

cli.add_command(stats)

if __name__ == '__main__':
    cli()
