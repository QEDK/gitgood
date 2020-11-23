import notification as notification
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
    notification = user.get_notifications(participating=True, since=datetime(2019, 11, 7),
                                          before=datetime(today.year, today.month, today.day))
    for notif in notification:
        typer.secho(f"{notif.subject.title}", fg=typer.colors.MAGENTA)
        limit -= 1
        if limit == 0:
            break


@app.command()
def read(limit: Optional[int] = typer.Argument(sys.maxsize)):
    today = date.today()
    unread_notification = user.get_notifications(participating=True, since=datetime(2019, 11, 7),
                                                 before=datetime(today.year, today.month, today.day))
    for notif in unread_notification:
        notif.mark_as_read()
        typer.secho(f"Marked as Read.", fg=typer.colors.MAGENTA)
        limit -= 1
        if limit == 0:
            break


if __name__ == "__main__":
    app()
