# gitgood

A Git CLI designed for efficent project management

## 🙋 Why did we make this?

While GitHub CLI is a fantastic developer tool that dramatically simplifies collaboration on a project, it lacks several features. We have to rely on the GUI to use them, such as Github projects and notifications.

The lack of these features was our motivation to build this project so that not only us but thousands of other CLI-loving dev can make there "Git" experience "good".

## 👷 Who are we?

This package was built by [Rohan Rout](https://github.com/routrohan), [Ali Farhan Hassan Kiyani](https://github.com/farhan2742), [Sakshi Rambhia](https://github.com/Sakshi16) and [Ankit Maity](https://github.com/QEDK).

## Getting Started

These instructions will help you get started with using GitGood and making project management on github through cli a breeze.

### Prerequisites

* python 3

### Basic configuration



### Installation
It is recommended you use a virtual environment for building the project (such as Python's `venv` or the `virtualenv` module) to easily manage dependencies.
```bash
$ git clone git@github.com:QEDK/goodbot.git
$ cd goodbot
$ pip3 install -r requirements.txt
```

## User Guide

There are two commands that operate in the app. They are "project" and "notifs".

1. Project Management: The command "project" deals with tasks realted to viewing/managing the projects and their content(columns, cards etc)

Arguments: repo_address : this is the address of the repository in the form of user_name/repository_name. For ex: "QEDK/gitgood"

2. Notification management: The command "notifs" deals with the tasks related to notifications.

Arguments: 1 [LIMIT] (type: int) : This argument is OPTIONAL and prints only [LIMIT] no of notifications
           2 read(type: string) : This is used to mark a specific no. of notifications as READ. Use 'A' for all notifications or any
           3 repo-notif (type: string): This prints all the notifications in the repository mentioned in the argument. 

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

## License
Licensed under either of

 * MIT license ([LICENSE-MIT](LICENSE-MIT) or http://opensource.org/licenses/MIT)
 * Lesser General Public license v3.0 or later ([LICENSE-LGPL](LICENSE-LGPL) or https://www.gnu.org/licenses/lgpl-3.0.html)

at your option.

The documentation is released under the [GFDL license v1.3](https://www.gnu.org/licenses/fdl-1.3.html) or later.

### Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in the work by you, as defined in the LGPL-3.0 license, shall be dual licensed as above, without any
additional terms or conditions.
