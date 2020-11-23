from logging import exception
import os
import typer
import github
from dotenv import load_dotenv
from pathlib import Path
from github import Github

app = typer.Typer()

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


@app.callback()
def callback():
    """
    Here to help! ✨
    """


@app.command()
def project(repo_address: str, cards: bool = False, project_card: str = ""):
    """This command helps you view details about the projects

    Args:
    repo_address (str): user_name/repository_name\n
    cards (bool, optional): This option lets you view all the cards of all the projects. Defaults to False\n
    project-card (string, optional): This lets you view the card of a particular project. Defaults to "".
    """
    repo = g.get_repo(repo_address)
    project_list = "----------------------------------------\nAll Projects:\n"
    count = 1
    for project in repo.get_projects():
        project_name = project.name
        project_list += f"\n{count}. {project_name}"
        count += 1
    project_list += "\n"

    if cards:
        try:
            show_card(repo_address, project_list)
        except github.GithubException as e:
            typer.echo(e)

    if project_card != "":
        show_card_number(repo_address, project_card)


def show_card(repo_address: str, project_list: str):
    body = project_list
    repo = g.get_repo(repo_address)
    for project in repo.get_projects():
        body += f"\n-----------------------------\nProject Name: {project.name}\n-----------------------------\n\nColumns:\n\n"
        count = 1
        for column in project.get_columns():
            body += f"{count}.{column.name} \t"
            count += 1
        body += "\n"
    typer.echo(body)


def show_card_number(repo_address: str, project_name: str):
    body = ""
    repo = g.get_repo(repo_address)
    for project in repo.get_projects():
        if project.name == project_name:
            body += f"\n-----------------------------\nProject Name: {project.name}\n-----------------------------\n\n"
            count = 1
            for column in project.get_columns():
                body += f"{count}.{column.name} \n-----------------------------\n"
                count += 1
                for card in column.get_cards():
                    flag = 0
                    for ch in card.get_content().body:
                        if ch == "#":
                            flag = 1
                    if flag == 1:
                        body += f"\nPull Request:\n"
                    else:
                        body += f"\nIssue:\n"
                    body += f"\nTitle: {card.get_content().title}"
                    if card.get_content().assignee == None:
                        pass
                    else:
                        body += f"\n\nAssignee: {card.get_content().assignee.login}"
                    body += f"\n\nLabels:"
                    for label in card.get_content().labels:
                        body += f"\n{label.name}"
                    body += f"\n\n{card.get_content().body}\n-----------------------------\n"
    typer.echo(body)


if __name__ == "__main__":
    app()
