# Jira Issue Tracker
<img src="https://github.com/star7js/jira-issue-tracker-server/assets/126814341/6b9d8d3e-f3ce-4d8d-a99d-2be30f33c757.png" width="50%" height="50%">

Jira Issue Tracker is a Kivy-based application designed to provide an overview of Jira issues based on custom JQL (Jira Query
Language) queries. It offers a simple and intuitive interface to track the status of various issues without needing to browse to Jira.

## Features

- Display issues in a grid layout with customizable queries
- Fetch and update issue counts at regular intervals
- Toggle between light and dark mode for user convenience
- Easy access to user settings

## Installation

To set up Jira Issue Tracker, you will need Python and the following libraries:

- Kivy
- KivyMD
- Requests
- python-dotenv

Install the dependencies with:

```bash
pip install kivy kivymd requests python-dotenv
```

## Usage

To run the program:

```bash
python main.py
```


## Configuration

Make sure you have set up the .env file with your JIRA site URL and API token.
If you don't have this set, the program will ask you for it before it will run.
The variables you enter will be saved in a .env file in the same directory as the main.py file.
If you want to change these variables, you can either edit the .env file directly, or you can choose
'Jira Settings' button in the program.
