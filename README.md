# Jira Issue Tracker

<img src="https://github.com/star7js/jira-issue-tracker-server/assets/126814341/6b9d8d3e-f3ce-4d8d-a99d-2be30f33c757.png" width="50%" height="50%">

Jira Issue Tracker is a Kivy-based desktop application designed to provide an overview of Jira issues based on custom JQL (Jira Query Language) queries. It offers a simple and intuitive interface to track the status of various issues without needing to browse to Jira.

## Features

- **Custom JQL Queries**: Display issues in a grid layout with customizable queries
- **Auto-refresh**: Fetch and update issue counts at regular intervals (default: 1 hour)
- **Direct Navigation**: Clicking on issue boxes directly opens your Jira site with the JQL search performed
- **Theme Support**: Toggle between light and dark mode for user convenience
- **Settings Management**: Easy access to user settings and configuration
- **Secure API Calls**: Built-in security measures for API requests with retry logic

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)

### Install from PyPI

```bash
pip install jira-issue-tracker-server
```

### Install from Source

1. Clone the repository:
```bash
git clone https://github.com/star7js/jira-issue-tracker-server.git
cd jira-issue-tracker-server
```

2. Create a virtual environment (recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

## Configuration

### Environment Setup

1. Copy the example environment file:
```bash
cp example.env .env
```

2. Edit the `.env` file with your Jira configuration:
```env
JQL_QUERY_ONE=project = DEMO
JQL_QUERY_TWO=project = IP
JQL_QUERY_THREE=reporter = currentUser() order by created DESC
JQL_QUERY_FOUR=project = ITZ
JIRA_API_TOKEN=your_api_token_here
JIRA_SITE_URL=https://your-jira-site.com
JIRA_SERVER=TRUE
```

> **⚠️ Security Note**: Never commit your `.env` file to version control as it contains sensitive information like API tokens. The `.env` file is already included in `.gitignore` to prevent accidental commits.

### Jira API Token Setup

1. Go to your Jira instance
2. Navigate to Profile Settings → Security → API tokens
3. Create a new API token
4. Copy the token to your `.env` file

## Usage

### Running the Application

```bash
python main.py
```

Or if installed via pip:
```bash
jira-tracker
```

### First Run

On first run, if the `.env` file is not configured, the application will show a settings popup where you can configure your Jira connection.

### Using the Interface

- **Issue Boxes**: Each box displays the count of issues matching a JQL query
- **Click to Navigate**: Click any issue box to open your Jira site with that specific JQL search
- **Theme Toggle**: Use the "Toggle Light/Dark Mode" button to switch themes
- **Settings**: Access user settings through the "User Settings" button

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black .
```

### Installing Development Dependencies

```bash
pip install -e ".[dev]"
```

## Project Structure

```
jira-issue-tracker-server/
├── main.py                          # Main application entry point
├── jira_issue_tracker.py            # Main application logic
├── api.py                           # Jira API integration
├── issue_box.py                     # Individual issue box component
├── jira_connection_settings_popup.py # Settings popup
├── security.py                      # Secure request handling
├── pyproject.toml                   # Project configuration
├── README.md                        # This file
├── example.env                      # Environment variables template
└── test_*.py                        # Test files
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/star7js/jira-issue-tracker-server/issues) page
2. Create a new issue with detailed information about your problem
3. Include your Python version, operating system, and any error messages

## Roadmap

- [ ] Service Management Projects support
- [ ] Enhanced JQL query builder
- [ ] Export functionality
- [ ] Multiple Jira instance support
- [ ] Advanced filtering options
