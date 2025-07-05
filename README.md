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

**Option 1: Interactive Setup (Recommended)**
```bash
python setup.py
```
This will guide you through the configuration process step by step.

**Option 2: Manual Setup**
1. **Copy the example environment file:**
```bash
cp example.env .env
```

2. **Edit the `.env` file with your Jira configuration:**
   - Open `.env` in your preferred text editor
   - Update the required fields (see below)
   - Save the file

> **⚠️ Security Note**: Never commit your `.env` file to version control as it contains sensitive information like API tokens. The `.env` file is already included in `.gitignore` to prevent accidental commits.

### Required Configuration

You must configure these two fields to connect to your Jira instance:

```env
# Your Jira site URL
# Cloud: https://yourcompany.atlassian.net
# Server/Data Center: https://jira.yourcompany.com or https://yourcompany.com/jira
JIRA_SITE_URL=https://yourcompany.atlassian.net

# Your Jira Personal Access Token (not your password!)
JIRA_API_TOKEN=your_personal_access_token_here
```

### Optional Configuration

You can customize the JQL queries to track different types of issues:

```env
# Query 1: Default project issues
JQL_QUERY_ONE=project = DEMO

# Query 2: Another project or filter
JQL_QUERY_TWO=project = IP

# Query 3: Issues reported by current user
JQL_QUERY_THREE=reporter = currentUser() order by created DESC

# Query 4: Additional project or custom filter
JQL_QUERY_FOUR=project = ITZ

# Server mode (set to TRUE for background service)
JIRA_SERVER=FALSE
```

### Jira Deployment Types

This application works with all Jira deployment types:

| Type | URL Format | Description |
|------|------------|-------------|
| **Jira Cloud** | `https://yourcompany.atlassian.net` | Hosted by Atlassian |
| **Jira Server** | `https://jira.yourcompany.com` | Self-hosted on-premises |
| **Jira Data Center** | `https://yourcompany.com/jira` | Enterprise self-hosted |

### Jira API Token Setup

**For Jira Cloud:**
1. **Go to your Atlassian account:**
   - Visit: https://id.atlassian.com/manage-profile/security/api-tokens
   - Or navigate from your Jira instance: Profile Settings → Security → API tokens

2. **Create a new API token:**
   - Click "Create API token"
   - Give it a descriptive label (e.g., "Jira Issue Tracker Desktop App")
   - Copy the generated token

**For Jira Server/Data Center:**
1. **Go to your Jira instance:**
   - Navigate to Profile Settings → Security → API tokens
   - Or use your admin's preferred method for API access

2. **Create a new API token:**
   - Follow your organization's process for API token creation
   - Copy the generated token

3. **Add to your `.env` file:**
   - Paste the token as the value for `JIRA_API_TOKEN`

> **💡 Tip**: API tokens are more secure than passwords and can be revoked individually if needed.

### JQL Query Examples

Here are some useful JQL patterns you can use:

| Query Type | JQL Example | Description |
|------------|-------------|-------------|
| Project Issues | `project = DEMO` | All issues in a specific project |
| Assigned to Me | `assignee = currentUser()` | Issues assigned to you |
| My Reports | `reporter = currentUser()` | Issues you reported |
| High Priority | `priority = High` | High priority issues |
| Recent Issues | `created >= -7d` | Issues created in last 7 days |
| Open Issues | `status != Done` | Issues not marked as done |
| Combined | `project = DEMO AND priority = High` | Multiple conditions |
| Ordered | `project = DEMO ORDER BY created DESC` | Issues sorted by creation date |

For more JQL help, visit: [Atlassian JQL Documentation](https://support.atlassian.com/jira-software-cloud/docs/use-advanced-search-with-jira-query-language-jql/)

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
├── setup.py                         # Interactive setup script
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

## Troubleshooting

### Common Issues

#### "Key JIRA_SITE_URL not found in .env"
- **Solution**: Make sure you've copied `example.env` to `.env` and updated the values
- **Check**: Verify your `.env` file exists in the project root directory

#### "Unable to connect to Jira"
- **Solution**: Verify your `JIRA_SITE_URL` is correct (include `https://`)
- **Check**: Test the URL in your browser to ensure it's accessible
- **Server/Data Center**: Ensure your Jira instance allows external API access

#### "Authentication failed"
- **Solution**: Regenerate your API token and update the `.env` file
- **Check**: Ensure you're using an API token, not your password

#### "No issues found"
- **Solution**: Check your JQL queries are valid
- **Check**: Test the JQL query directly in your Jira instance

#### "KivyMD version warning"
- **Solution**: This is just a warning and doesn't affect functionality
- **Note**: The app works fine with the current KivyMD version

### Getting Help

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
