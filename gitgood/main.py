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
        err=True, fg=typer.colors.RED)
    typer.echo((
        "ℹ You can fetch or generate a new token from https://github.com/settings/tokens\n"
        "You will need to grant the repo, notification, user scopes for gitgood to work properly."
    ))
    access_token = typer.prompt(
        "Enter your personal access token to continue (for safety, it won't show)",
        hide_input=True)
    with open(Path.home().joinpath(".gg"), "a+") as file:
        file.write(f"GG_PAT={access_token}")
    typer.secho("Your token has been stored successfully. 🚀", fg=typer.colors.GREEN, bold=True)

g = Github(access_token)

@app.callback()
def callback():
    """
    Here to help! ✨
    """
@app.command()
def project(repo_address:str, show_projects:bool = False, show_cards: bool = False):
    """This option deals with the repo projects

    Args: repo_address (str): Should be in the form of "Username/Repository name", for ex: QEDK/gitgood
        
        \n\nshow-projects (bool, optional): Enabling this option allows you to view all the projects for the address of the repository provided. \n\nUsage: gg project --show-projects QEDK/gitgood (Defaults to False)
        \n\nshow-cards (bool, optional): Enabling this option allows you to view all the cards for all the projects in the address of the repository provided. \n\nUsage: gg project --show-cards QEDK/gitgood (Defaults to False)
    """
    repo = g.get_repo(repo_address)
    typer.echo("----------------------------------------")
    count = 1
    if show_projects:
        for project in repo.get_projects():
            project_name = project.name
            typer.echo(f"{count}. {project_name}")
            count+=1
    
    if show_cards:
        show_card(repo_address)


def show_card(repo_address:str):
    repo = g.get_repo(repo_address)
    typer.echo("----------------------------------------")
    for project in repo.get_projects():
        typer.echo(project.name)
        typer.echo("------------")
        for column in project.get_columns():
            typer.echo(column.name)
            typer.echo("------------")
            for card in column.get_cards():
                url = card.get_content().url
                slash_count = 0
                for ch in url:
                    if slash_count == 6:
                        break
                    if ch == '/':
                        slash_count += 1
                if ch == 'p':
                    typer.echo("Pull Request:")
                elif ch == 'i':
                    typer.echo("Issue:")
                    if card.get_content().assignee == None:
                        pass
                    else:
                        typer.echo(f"Assignee: {card.get_content().assignee.login}")
                else:
                    typer.echo("Note:")
                typer.echo(card.get_content().title)
                typer.echo("Labels:")
                for label in card.get_content().labels:
                        typer.echo(label.name)
                typer.echo(card.get_content().body)
                typer.echo("------------")
            typer.echo("------------")


if __name__ == "__main__":
    app()