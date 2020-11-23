from github import Github
from datetime import datetime
from datetime import date
import typer
from typing import Optional
import sys

username = {username}
g = Github({token})
user = g.get_user()
app = typer.Typer()


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
