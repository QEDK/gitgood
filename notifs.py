from github import Github
from datetime import datetime
from datetime import date
import typer

username = {username}
g = Github({accesstoken})
user = g.get_user(username)
app = typer.Typer()


@app.command()
def notifs(limit: int):
    today = date.today()
    repos = user.get_repos(type="all", sort="updated", direction="asc")
    for repo in repos:
        notifs = repo.get_notifications(all=False, participating=True, since=datetime(2019, 11, 7),
                                        before=datetime(today.year, today.month, today.day))
        if limit == 0:
            break
        for notif in notifs:
            typer.secho(f"{notif.subject.title}", fg=typer.colors.MAGENTA)
            limit -= 1
            if limit == 0:
                break


@app.command()
def allnotifs():
    today = date.today()
    for repos in user.get_subscriptions():
        notifs = repos.get_notifications(all=False, participating=True, since=datetime(2019, 11, 7),
                                         before=datetime(today.year, today.month, today.day))
        for notif in notifs:
            typer.secho(f"{notif.subject.title}", fg=typer.colors.BRIGHT_CYAN)


@app.command()
def read(limit: int):
    today = date.today()
    repos = user.get_repos(type="all", sort="updated", direction="asc")
    for repo in repos:
        notifs = repo.get_notifications(all=False, participating=True, since=datetime(2019, 11, 7),
                                        before=datetime(today.year, today.month, today.day))
        if limit == 0:
            break
        for notif in notifs:
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
