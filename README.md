# Jira Issue Tracker

[![codecov](https://codecov.io/gh/star7js/jira-issue-tracker/branch/main/graph/badge.svg)](https://codecov.io/gh/star7js/jira-issue-tracker)

<img src="https://github.com/star7js/jira-issue-tracker/assets/126814341/6b9d8d3e-f3ce-4d8d-a99d-2be30f33c757.png" width="50%" height="50%">

Desktop application for tracking Jira issues with custom JQL queries. Built with Kivy/KivyMD.

## Features

- Custom JQL query tracking with auto-refresh (1 hour)
- Direct navigation to Jira from issue boxes
- Light/dark mode toggle
- Secure API requests with retry logic
- Supports Jira Cloud, Server, and Data Center

## Installation

Requires Python 3.9+

```bash
# From PyPI
pip install jira-issue-tracker

# From source
git clone https://github.com/star7js/jira-issue-tracker.git
cd jira-issue-tracker
pip install -e .
```

## Configuration

### Quick Setup (Recommended)

```bash
python setup_interactive.py
```

### Manual Setup

1. Copy `example.env` to `.env`
2. Edit `.env` with your Jira configuration:

```env
# Required: Your Jira URL
JIRA_SITE_URL=https://yourcompany.atlassian.net

# Required: Your API token (not password!)
JIRA_API_TOKEN=your_token_here

# Optional: Custom JQL queries
JQL_QUERY_ONE=project = DEMO
JQL_QUERY_TWO=assignee = currentUser()
JQL_QUERY_THREE=reporter = currentUser() ORDER BY created DESC
JQL_QUERY_FOUR=priority = High
```

### Getting Your API Token

**Jira Cloud:**
1. Visit https://id.atlassian.com/manage-profile/security/api-tokens
2. Create a new token and copy it

**Jira Server/Data Center:**
- Follow your organization's API token creation process

### Deployment Types

| Type | URL Format |
|------|------------|
| Jira Cloud | `https://yourcompany.atlassian.net` |
| Jira Server | `https://jira.yourcompany.com` |
| Jira Data Center | `https://yourcompany.com/jira` |

### JQL Query Examples

| Query | JQL |
|-------|-----|
| Project issues | `project = DEMO` |
| Assigned to me | `assignee = currentUser()` |
| My reports | `reporter = currentUser()` |
| High priority | `priority = High` |
| Recent issues | `created >= -7d` |
| Open issues | `status != Done` |

[JQL Documentation](https://support.atlassian.com/jira-software-cloud/docs/use-advanced-search-with-jira-query-language-jql/)

## Usage

```bash
# If installed via pip
jira-tracker

# Or from source
python main.py
```

On first run, configure your Jira connection if `.env` is not set up.

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=. --cov-report=html --cov-report=term-missing

# Format code
black .
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Key JIRA_SITE_URL not found" | Copy `example.env` to `.env` and configure |
| "Unable to connect" | Verify URL includes `https://` and is accessible |
| "Authentication failed" | Regenerate API token (use token, not password) |
| "No issues found" | Test JQL query directly in Jira |
| KivyMD warning | Safe to ignore, doesn't affect functionality |

## License

MIT License

## Built With

- [Kivy](https://kivy.org/) - Cross-platform Python framework
- [KivyMD](https://kivymd.readthedocs.io/) - Material Design components
- [Jira REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/) - Jira integration
