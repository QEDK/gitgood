from github import Github
from datetime import datetime
from datetime import date
import typer
from typing import Optional
import sys

username = {username}
g = Github({accesstoken})
user = g.get_user(username)
app = typer.Typer()


@app.command()
def notifs(limit: Optional[int] = typer.Argument(sys.maxsize)):
    today = date.today()
    repos = user.get_repos(type="all", sort="updated", direction="asc")
    for repo in repos:
        notifications = repo.get_notifications(all=False, participating=True, since=datetime(2019, 11, 7),
                                               before=datetime(today.year, today.month, today.day))
        if limit == 0:
            break
        for notif in notifications:
            typer.secho(f"{notif.subject.title}", fg=typer.colors.MAGENTA)
            limit -= 1
            if limit == 0:
                break


@app.command()
def read(limit: int):
    today = date.today()
    repos = user.get_repos(type="all", sort="updated", direction="asc")
    for repo in repos:
        notifications = repo.get_notifications(all=False, participating=True, since=datetime(2019, 11, 7),
                                               before=datetime(today.year, today.month, today.day))
        if limit == 0:
            break
        for notif in notifications:
            if notif.unread is False:
                notif.mark_as_read()
            typer.secho(f"Done", fg=typer.colors.BRIGHT_YELLOW)
            limit -= 1
            if limit == 0:
                break


@app.command()
def markrepoasread(repo_name: str):
    repo = g.get_repo(repo_name)
    repo.mark_notifications_as_read()


if __name__ == "__main__":
    app()
