import base64
from github import Github
from pprint import pprint
from datetime import datetime
import typer

username = {username}
g = Github({token})
user = g.get_user(username)


def notifs(limit: int):
    today = date.today()
    repos = user.get_repos(type="all", sort="updated", direction="asc")
    max = limit
    for repo in repos:
        notifs = repo.get_notifications(all=False, participating=True, since=datetime(
            2019, 11, 7), before=datetime(today.year, today.month, today.day))
        if limit == 0:
            break
        for notif in notifs:
            print(notif)
            limit -= 1
            if limit == 0:
                break


def getAllNotifs():
    today = date.today()
    for repos in user.get_subscriptions():
        notifs = repos.get_notifications(all=False, participating=True, since=datetime(
            2019, 11, 7), before=datetime(2020, 11, 21))
        for notif in notifs:
            print(notif)


def markAsRead(num: int):
    today = date.today()
    repos = user.get_repos(type="all", sort="updated", direction="asc")
    limit = num
    for repo in repos:
        repo.mark_notifications_as_read()
        limit -= 1
        if limit == 0:
            break


def markRepoAsRead(repo_name):
    repo = g.get_repo(repo_name)
    repo.mark_notifications_as_read()

# app = typer.Typer()


# @app.command()
# def getNotifs():
#     for repos in user.get_subscriptions():
#         notifs = repos.get_notifications(all= False, participating= True, since = datetime(2019,11,7), before= datetime(2020,11,21))
#     for notif in notifs[:10]:
#         print(notif)
#         typer.secho(notif, fg=typer.colors.MAGENTA)


# if __name__ == "__main__":
#     app()
