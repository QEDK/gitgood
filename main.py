import os
import typer
from dotenv import load_dotenv
load_dotenv()

try:
    access_token = os.environ["GG_PAT"]
except Exception:
    typer.secho(
        "Cannot find GitHub personal access token to authenticate",
        err=True, fg=typer.colors.RED)
    raise typer.Exit(1)


def main():
    typer.echo("Hello World")


if __name__ == "__main__":
    typer.run(main)
