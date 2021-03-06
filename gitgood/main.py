import os
import typer
import github
from dotenv import load_dotenv
from pathlib import Path
from github import Github
from datetime import datetime
from datetime import date
from typing import Optional
import sys

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
    typer.echo((
        "ℹ You can fetch or generate a new token from https://github.com/settings/tokens\n"
        "You will need to grant the repo, notification, user scopes for gitgood to work properly."
    ))
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
def project(
    repo_address: str, columns: bool = False, project_card: str = "", move: int = 0
):
    """This command helps you view details about the projects

    Args:
    repo_address (str): user_name/repository_name\n
    cards (bool, optional): This option lets you view the columns the projects. Defaults to False\n
    project-card (string, optional): This lets you view the cards of a particular project.
    """
    try:
        repo = g.get_repo(repo_address)
    except github.GithubException:
        error_message = "\n------------------------------------------------\n"
        error_message += typer.style(
            "Invalid username or repository name, please try again!!",
            fg=typer.colors.RED,
            bold=True,
        )
        error_message += "\n------------------------------------------------\n"
        typer.echo(error_message, err=True)
        raise typer.Exit(1)
    project_list = "------------------------------------------------"
    project_list += typer.style("\nAll Projects:\n", fg=typer.colors.GREEN, bold=True)
    count = 1
    for project in repo.get_projects():
        project_name = project.name
        project_list += f"\n{count}. {project_name}"
        count += 1
    project_list += "\n"
    if columns is False and project_card == "" and move == 0:
        typer.echo(project_list)

    if columns:
        try:
            show_card(repo_address, project_list)
        except github.GithubException:
            error_message = "\n------------------------------------------------\n"
            error_message += typer.style(
                "Invalid username or repository name, please try again!!",
                fg=typer.colors.RED,
                bold=True,
            )
            error_message += "\n------------------------------------------------\n"
            typer.echo(error_message, err=True)
            raise typer.Exit(1)

    if project_card != "":
        show_card_number(repo_address, project_card, project_list)

    if move != 0:
        move_card(repo_address, move)


def show_card(repo_address: str, project_list: str):
    body = project_list
    repo = g.get_repo(repo_address)
    for project in repo.get_projects():
        body += "\n------------------------------------------------\n"
        body += typer.style("Project Name: ", fg=typer.colors.GREEN, bold=True)
        body += typer.style(f"{project.name}", fg=typer.colors.BRIGHT_RED, bold=True)
        body += "\n------------------------------------------------\n\n"
        body += typer.style("Columns:\n\n", fg=typer.colors.CYAN, bold=True)
        count = 1
        for column in project.get_columns():
            body += f"{count}.{column.name} \t"
            count += 1
        body += "\n"
    typer.echo(body)


def show_card_number(repo_address: str, project_name: str, project_list: str):
    flag = False
    body = ""
    repo = g.get_repo(repo_address)
    for project in repo.get_projects():
        if project.name == project_name:
            flag = True
            body += "\n------------------------------------------------\n"
            body += typer.style("Project Name: ", fg=typer.colors.GREEN, bold=True)
            body += typer.style(project.name, fg=typer.colors.BRIGHT_RED, bold=True)
            body += "\n------------------------------------------------\n"
            count = 1
            for column in project.get_columns():
                body += typer.style(
                    f"\n{count}.{column.name}", fg=typer.colors.CYAN, bold=True
                )
                body += "\n------------------------------------------------\n"
                count += 1
                for card in column.get_cards():
                    flag = 0
                    if card.note:
                        body += typer.style("\nGeneral", fg=typer.colors.BRIGHT_MAGENTA)
                        body += typer.style("\n\nCard ID: ", fg=typer.colors.GREEN)
                        body += typer.style(str(card.id))
                        body += typer.style("\n\nNote: ", fg=typer.colors.GREEN)
                        body += typer.style(f"\n\n{card.note}")
                        body += typer.style("\n\nCreated by: ", fg=typer.colors.GREEN)
                        body += typer.style(f"{card.creator.name}\n")
                        body += "\n------------------------------------------------\n"
                    else:
                        for ch in card.get_content().body:
                            if ch == "#":
                                flag = 1
                        if flag == 1:
                            body += typer.style(
                                "\nPull Request:\n", fg=typer.colors.BRIGHT_MAGENTA
                            )
                        else:
                            body += typer.style(
                                "\nIssue:\n", fg=typer.colors.BRIGHT_MAGENTA, bold=True
                            )
                        body += typer.style("\n\nCard ID: ", fg=typer.colors.GREEN)
                        body += typer.style(str(card.id))
                        body += typer.style("\n\nTitle: ", fg=typer.colors.GREEN)
                        body += typer.style(
                            card.get_content().title, fg=typer.colors.WHITE
                        )
                        if card.get_content().assignee is None:
                            pass
                        else:
                            body += typer.style(
                                "\n\nAssignee: ", fg=typer.colors.GREEN
                            )
                            body += typer.style(
                                card.get_content().assignee.login, fg=typer.colors.WHITE
                            )
                        body += typer.style("\n\nLabels: ", fg=typer.colors.GREEN)
                        for label in card.get_content().labels:
                            body += typer.style(
                                f"{label.name}\t", fg=typer.colors.WHITE
                            )
                        body += typer.style("\n\nBody:", fg=typer.colors.GREEN)
                        body += typer.style(
                            f"\n\n{card.get_content().body}", fg=typer.colors.WHITE
                        )
                        body += "\n\n------------------------------------------------\n"
    if flag:
        pass
    else:
        error_message = "\n------------------------------------------------"
        error_message += typer.style(
            "\nInvalid Project Name!!\nChoose one from the list given below!\n",
            fg=typer.colors.RED,
            bold=True,
        )
        error_message += project_list
        typer.echo(error_message)
        raise typer.Exit(1)
    typer.echo(body)


def move_card(repo_address: str, card_id: int):
    flag = False
    body = ""
    repo = g.get_repo(repo_address)
    for project in repo.get_projects():
        for column in project.get_columns():
            for card in column.get_cards():
                if card.id == card_id:
                    flag = True
                    body += typer.style(
                        "\n\nCurrently the card is located in: ", fg=typer.colors.GREEN
                    )
                    body += typer.style(f"{column.name}")
                    typer.echo(body)
                    prompt_text = (
                        "\n------------------------------------------------\n\n"
                    )
                    prompt_text += typer.style(
                        "Enter the new column name ", fg=typer.colors.GREEN
                    )
                    column_name = typer.prompt(prompt_text)
                    for columnName in project.get_columns():
                        if column_name == columnName.name:
                            card.move("top", columnName.id)
    if flag:
        pass
    else:
        error_message = "\n------------------------------------------------"
        error_message += typer.style(
            "\nInvalid Card ID!!\n\n", fg=typer.colors.RED, bold=True
        )
        project_card_message = typer.style(
            "--project-card", fg=typer.colors.GREEN, bold=True
        )
        error_message += typer.style(
            f"Please use the {project_card_message} option to get the correct Card ID\n"
        )
        error_message += "------------------------------------------------\n"
        typer.echo(error_message)
        raise typer.Exit(1)
    finish_text = typer.style("\nCard Moved Successfully!", fg=typer.colors.YELLOW)
    finish_text += "\n\n------------------------------------------------\n\n"
    typer.echo(finish_text)


user = g.get_user()


@app.command()
def notifs(
    limit: Optional[int] = typer.Argument(sys.maxsize),
    read: str = "",
    repo_notifs: str = "",
):
    """This command deals with the notifications

    Args:
        limit (Optional[int], optional): Number of notifications to be printed.\n
    read (str, optional): Option to mark notifications as read.\n
    repo_notifs (str): Show notifications of a particular repository. Defaults to "".
    """
    today = date.today()
    message = "\n------------------------------------------------\n\n"
    notification = user.get_notifications(
        before=datetime(today.year, today.month, today.day)
    )
    if read == "" and repo_notifs == "":
        if notification.totalCount != 0:
            for notif in notification[:limit]:
                notif_details = typer.style(f"{notif.repository.name}: ", fg=typer.colors.GREEN)
                notif_details += typer.style(f"{notif.subject.type}: ")
                notif_details += typer.style(f"{notif.subject.title}", fg=typer.colors.BRIGHT_CYAN)
                message += notif_details
                message += "\n"
            message += "\n------------------------------------------------\n\n"
            typer.echo(f"{message}")
        else:
            else_message = "\n------------------------------------------------\n\n"
            else_message += typer.style(
                "No new notifications!\n", fg=typer.colors.GREEN, bold=True
            )
            else_message += "\n------------------------------------------------\n\n"
            typer.echo(else_message)
    if read != "":
        read_notif(read)
    if repo_notifs != "":
        reponotifs(repo_notifs)


def read_notif(read: str):
    today = date.today()
    message = "\n------------------------------------------------\n\n"
    unread_notification = user.get_notifications(
        before=datetime(today.year, today.month, today.day)
    )
    if read == "A":
        for notif in unread_notification:
            notif.mark_as_read()
        message += typer.style("Marked as Read. \n", fg=typer.colors.BRIGHT_CYAN)
        message += "\n------------------------------------------------\n\n"
        typer.echo(f"{message}")
    else:
        for notif in unread_notification[: int(read)]:
            notif.mark_as_read()
        message += typer.style("Marked as Read. \n", fg=typer.colors.BRIGHT_CYAN)
        message += "\n------------------------------------------------\n\n"
        typer.echo(f"{message}")


def reponotifs(repo_name: str):
    try:
        repo = g.get_user().get_repo(repo_name)
    except github.GithubException:
        typer.secho("Invalid Repository Name", err=True, fg=typer.colors.RED)
        raise typer.Exit(1)
    message = "\n------------------------------------------------\n\n"
    notification = repo.get_notifications()
    for notif in notification:
        message += typer.style(notif.subject.title, fg=typer.colors.BRIGHT_CYAN)
        message += "\n"
    message += "\n------------------------------------------------\n\n"
    typer.echo(f"{message}")


if __name__ == "__main__":
    app()
