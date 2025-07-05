#!/usr/bin/env python3
"""
Setup script for Jira Issue Tracker Server
Helps users quickly configure their environment
"""

import os
import shutil
import sys
from pathlib import Path


def main():
    """Main setup function"""
    print("🚀 Jira Issue Tracker - Setup")
    print("=" * 50)

    # Check if .env already exists
    if os.path.exists(".env"):
        print("⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (y/N): ").lower()
        if response != "y":
            print("Setup cancelled.")
            return

    # Copy example.env to .env
    if not os.path.exists("example.env"):
        print("❌ example.env file not found!")
        print(
            "Please make sure you're running this script from the project root directory."
        )
        return

    try:
        shutil.copy("example.env", ".env")
        print("✅ Created .env file from example.env")
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return

    # Interactive configuration
    print("\n📝 Configuration Setup")
    print("-" * 30)

    # Get Jira site URL
    print("\n1. Jira Site URL")
    print("   Cloud: https://yourcompany.atlassian.net")
    print(
        "   Server/Data Center: https://jira.yourcompany.com or https://yourcompany.com/jira"
    )
    jira_url = input("   Enter your Jira site URL: ").strip()

    if jira_url:
        update_env_file("JIRA_SITE_URL", jira_url)
        print("   ✅ Jira site URL configured")

    # Get API token
    print("\n2. Jira API Token")
    print("   Generate at: https://id.atlassian.com/manage-profile/security/api-tokens")
    print("   (This is NOT your password - it's a separate API token)")
    api_token = input("   Enter your Jira API token: ").strip()

    if api_token:
        update_env_file("JIRA_API_TOKEN", api_token)
        print("   ✅ API token configured")

    # Optional: Customize JQL queries
    print("\n3. JQL Queries (Optional)")
    print("   You can customize the JQL queries now or edit .env later")
    customize_queries = input("   Customize JQL queries now? (y/N): ").lower()

    if customize_queries == "y":
        configure_jql_queries()

    print("\n🎉 Setup Complete!")
    print("=" * 50)
    print("Your .env file has been configured.")
    print("You can now run the application with: python main.py")
    print("\nTo customize JQL queries later, edit the .env file directly.")
    print(
        "For help with JQL syntax, see: https://support.atlassian.com/jira-software-cloud/docs/use-advanced-search-with-jira-query-language-jql/"
    )


def update_env_file(key, value):
    """Update a key-value pair in the .env file"""
    try:
        with open(".env", "r") as f:
            lines = f.readlines()

        with open(".env", "w") as f:
            for line in lines:
                if line.startswith(f"{key}="):
                    f.write(f"{key}={value}\n")
                else:
                    f.write(line)
    except Exception as e:
        print(f"   ⚠️  Warning: Could not update {key}: {e}")


def configure_jql_queries():
    """Interactive JQL query configuration"""
    queries = [
        ("JQL_QUERY_ONE", "Query 1 (e.g., 'project = DEMO')"),
        ("JQL_QUERY_TWO", "Query 2 (e.g., 'project = IP')"),
        (
            "JQL_QUERY_THREE",
            "Query 3 (e.g., 'reporter = currentUser() order by created DESC')",
        ),
        ("JQL_QUERY_FOUR", "Query 4 (e.g., 'project = ITZ')"),
    ]

    for key, description in queries:
        print(f"\n   {description}")
        print("   Press Enter to keep default, or enter a new JQL query:")
        query = input(f"   {key}: ").strip()
        if query:
            update_env_file(key, query)
            print(f"   ✅ {key} updated")


if __name__ == "__main__":
    main()
