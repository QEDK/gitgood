from logging import exception
import os
import github
from dotenv import load_dotenv
from pathlib import Path
from github import Github
from datetime import datetime
from datetime import date
import typer
from typing import Optional
import sys

__version__ = "0.1.0a"

try:
    config_path = Path(os.environ["GG_PATH"])
except Exception:
    config_path = Path.home().joinpath(".gg")
finally:
    if config_path.is_file():
        load_dotenv(config_path)

try:
    access_token = os.environ["GG_PAT"]
except Exception:
    typer.secho(
        "Uh-oh, cannot find your GitHub personal access token to authenticate. 😓",
        err=True,
        fg=typer.colors.RED,
    )
    typer.echo(
        (
            "ℹ You can fetch or generate a new token from https://github.com/settings/tokens\n"
            "You will need to grant the repo, notification, user scopes for gitgood to work properly."
        )
    )
    access_token = typer.prompt(
        "Enter your personal access token to continue (for safety, it won't show)",
        hide_input=True,
    )
    with open(Path.home().joinpath(".gg"), "a+") as file:
        file.write(f"GG_PAT={access_token}")
    typer.secho(
        "Your token has been stored successfully. 🚀", fg=typer.colors.GREEN, bold=True
    )

g = Github(access_token)
user = g.get_user()
app = typer.Typer()


@app.callback()
def callback():
    """
    Here to help! ✨
    """


@app.command()
def notifs(limit: Optional[int] = typer.Argument(sys.maxsize)):
    today = date.today()
    message = ""
    notification = user.get_notifications(participating=True,
                                          before=datetime(today.year, today.month, today.day))
    for notif in notification[:limit]:
        message += notif.subject.title
        message += "\n"
    typer.secho(f"{message}", fg=typer.colors.MAGENTA)


@app.command()
def read(limit: Optional[int] = typer.Argument(sys.maxsize)):
    today = date.today()
    message = ""
    unread_notification = user.get_notifications(participating=True,
                                                 before=datetime(today.year, today.month, today.day))
    for notif in unread_notification[:limit]:
        notif.mark_as_read()
        message += "Marked as Read. \n"
    typer.secho(f"{message}", fg=typer.colors.BRIGHT_CYAN)


if __name__ == "__main__":
    app()
