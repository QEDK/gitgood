import base64
from github import Github
from pprint import pprint
from datetime import datetime
from datetime import date
import typer

username = ({username})
g = Github({accesstoken})
user = g.get_user(username)
app = typer.Typer()


@app.command()
def notifs(limit: int):
    today = date.today()
    repos = user.get_repos(type="all", sort="updated", direction="asc")
    max = limit
    for repo in repos:
        notifs = repo.get_notifications(all=False, participating=True, since=datetime(2019, 11, 7),
                                        before=datetime(today.year, today.month, today.day))
        if limit == 0:
            break
        for notif in notifs:
            typer.echo(notif)
            limit -= 1
            if limit == 0:
                break


@app.command()
def getAllNotifs():
    today = date.today()
    for repos in user.get_subscriptions():
        notifs = repos.get_notifications(all=False, participating=True, since=datetime(2019, 11, 7),
                                         before=datetime(2020, 11, 21))
        for notif in notifs:
            typer.echo(notif)


@app.command()
def markAsRead(num: int):
    today = date.today()
    repos = user.get_repos(type="all", sort="updated", direction="asc")
    limit = num
    for repo in repos:
        repo.mark_notifications_as_read()
        limit -= 1
        if limit == 0:
            break


@app.command()
def markRepoAsRead(repo_name):
    repo = g.get_repo(repo_name)
    repo.mark_notifications_as_read()


if __name__ == "__main__":
    app()
