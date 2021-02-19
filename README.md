# Metrics Dashboard
A tool to calculate metrics on GitHub repositories.

## Table of Contents
- [Metrics Dashboard](#metrics-dashboard)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
  - [Developing for Metrics Dashboard](#developing-for-metrics-dashboard)
    - [Steps to start developing for Metrics Dashboard in VS Code](#steps-to-start-developing-for-metrics-dashboard-in-vs-code)
    - [Software needed to develop for Metrics Dashboard WITHOUT VS Code](#software-needed-to-develop-for-metrics-dashboard-without-vs-code)
  - [Running Metrics Dashboard](#running-metrics-dashboard)

## About
Metrics Dashboard is an open source project created by the [Loyola University Chicago Software and Systems Laboratory](https://ssl.cs.luc.edu).

For a full project abstract as well as academic papers written on this project, see this [project page](https://ssl.cs.luc.edu/research/in-progress/metrics-dashboard.html)

## Developing for Metrics Dashboard

### Steps to start developing for Metrics Dashboard in VS Code
**NOTE**: The steps listed here assume that you have VS Code installed. If not, scroll down to the next section to see a list of software that needs to be installed to develop for this project.

Requirements for developing Metrics Dashboard in VS Code:
- Docker
- [Remote Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) extension from Microsoft

Steps:
1. Fork this project
2. Open the Metrics Dashboard project
3. When prompted, open the project within the Development Container

### Software needed to develop for Metrics Dashboard WITHOUT VS Code
Requirements for developing Metrics Dashboard:
- Python 3.9+
- Pip
- The contents of [`.devcontainer/requirements.txt`](.devcontainer/requirements.txt)
    - black
    - colorama
    - flask
    - isort
    - pandas
    - requests
    - sphinx
    - sphinx-rtd-theme
    - travis-sphinx
    - tqdm

Steps:
0: Fork this project
1. Open this project in your favorite text editor or IDE

## Running Metrics Dashboard
**NOTE**: At this point, Metrics Dashboard is entirely written in Python 3.9+ compatible code.
**NOTE**: At this point, Metrics Dashboard is only capable of downloading and storing data from a repository.

Requirements for running Metrics Dashboard:
- Python 3.9+
- Pip
- The contents of [`.devcontainer/requirements.txt`](.devcontainer/requirements.txt)
    - black
    - colorama
    - flask
    - isort
    - pandas
    - requests
    - sphinx
    - sphinx-rtd-theme
    - travis-sphinx
    - tqdm
- [GitHub Personal Access Token](https://github.com/settings/tokens/) with *repo* scopes at the minimum

Steps:
0. Fork this project
1. Open this project in a terminal or command line interface
2. Change directory to `Data-Collection`
3. Run `python dataCollection.py -u URL -t GITHUB_TOKEN -o DATABASE.db`
    - `URL` is the GitHub URL of the project formatted like: `https://github.com/USERNAME/REPOSITORY`
    - `GITHUB_TOKEN` is the GitHub Personal Access Token
    - `DATABASE` is the filename of the database file.
      - **NOTE**: The database file needs to end in .db otherwise the program **WILL NOTE WORK**
