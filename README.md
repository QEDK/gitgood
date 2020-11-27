# gitgood

A Git CLI designed for efficent project management

## 🙋 Why did we make this?

While the vanilla GitHub CLI is a fantastic developer tool that dramatically simplifies collaboration on a project, it lacks several features. We have to rely on the GUI to use some of them, such as Github projects and notifications.

The lack of these features was our motivation to build this project so that not only us but thousands of other CLI-loving devs can make their "Git" experience truly "good".

## 👷 Who are we?

This package was built by [Rohan Rout](https://github.com/routrohan), [Ali Farhan Hassan Kiyani](https://github.com/farhan2742), [Sakshi Rambhia](https://github.com/Sakshi16) and [Ankit Maity](https://github.com/QEDK).

## 👶 Getting Started
### 🧩 Prerequisites
You'll need to have Python (>= 3.7) and `pip` to get started. If you don't have them installed already, see the [official docs](https://www.python.org/downloads/release/python-379)!

Once you're done, move on to the next steps below. ⬇

### 🛠 Installation
```bash
$ pip install gitgood
```
Yep, that's it. ⚡

After installation, check if `gg` is actually up and running like:
```bash
$ gg
Usage: gg [OPTIONS] COMMAND [ARGS]...

  Here to help! ✨

  ...
```
And you're set! 🚀

### ⚙ Basic configuration
You'll need your GitHub personal access token to make use of the CLI. You can make a new token [here](https://github.com/settings/tokens).

If you already have one, you can make a `.gg` file in your home folder like this (recommended):
```INI
GG_PAT=<your super secret token>
```
And the CLI will automatically pick it up, or you can set the `GG_PAT` environment variable yourself.

If this is all too much, don't fret! The first time you run `gg` on the CLI, you'll get instructions on how to make one. Easy-peezy, lemon-squeezy. 🍋

### 🧱 Building from source
It is highly recommended you use Poetry or virtual environments for building the project (such as Python's `venv` or the `virtualenv` module) to easily manage dependencies.
```bash
$ git clone git@github.com:QEDK/gitgood.git
$ cd gitgood
$ pip3 install poetry
$ poetry install
$ poetry shell
```
Or if you prefer it hardball, just do `pip3 install -r requirements.txt`.

You can also use `poetry` to build the binaries:
```bash
$ poetry build
```
You're now ready to work on `gitgood`! 🥳

## User Guide

There are two commands that operate in the app. They are "project" and "notifs".

1. Project Management: The command "project" deals with tasks realted to viewing/managing the projects and their content(columns, cards etc)

Arguments: repo_address : this is the address of the repository in the form of user_name/repository_name. For ex: "QEDK/gitgood"

2. Notification management: The command "notifs" deals with the tasks related to notifications.

Arguments: This command have following arguments.

- [LIMIT] (type: int) : This argument is OPTIONAL and prints only [LIMIT] no of notifications.
- read(type: string) : This is used to mark a specific no. of notifications as READ. Use 'A' for all notifications or any.
- repo-notif (type: string): This prints all the notifications in the repository mentioned in the argument.

### Printing all the projects in the given repository.

```bash
$ gg project <repo_address>
```
Example

```bash
$ gg project QEDK/gitgood
```

### Printing all the columns in all the projects in the given repository.

```bash
$ gg project <repo_address> --columns
```
Example

```bash
$ gg project QEDK/gitgood --columns
```

### Printing all the cards in a particular project.

```bash
$ gg project <repo_address> --project-card <project_name>
```
Example

```bash
$ gg project QEDK/gitgood --project-card App
```

### Moving a card from one column to another.

```bash
$ gg project <repo_address> --move <card_id>
```
Example

```bash
$ gg project QEDK/gitgood --move 1234567
```

### Printing all the notifications of the user.

```bash
$ gg notifs [LIMIT] (type: int)
```
Example

```bash
$ gg notifs 2
```

### Making the notifications as read. Once, marked they won't appear again on notifs command.

```bash
$ gg notifs --read [read]
```
Example

```bash
$ gg notifs --read 2
```

### Printing all the notifications of a particular repository.

```bash
$ gg notifs --repo-notifs <repository_name>
```
Example

```bash
$ gg notifs --repo-notifs gitgood
```

## Built With

* [Python](https://www.python.org/) - Programming Language
* [Typer](https://typer.tiangolo.com/) - Python CLI library
* [Github Api](https://developer.github.com/v3/) - API
* [PyGithub](https://github.com/PyGithub/PyGithub) - Github API Package
* [flask8](https://pypi.org/project/flake8/) - Linting tool
* [Poetry](https://python-poetry.org/) - Packaging and publishing

## 📜 License
This project is released under a free and open-source software license, Apache License 2.0 or later ([LICENSE](LICENSE) or https://www.apache.org/licenses/LICENSE-2.0). The documentation is also released under a free documentation license, namely the [GFDL v1.3](https://www.gnu.org/licenses/fdl-1.3.en.html) license or later.

### 🖊️ Contributions
Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in the work by you, as defined in the Apache-2.0 license, shall be licensed as above, without any additional terms or conditions.
