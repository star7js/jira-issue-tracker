# Changelog

All notable changes to this project will be documented in this file.

## [0.4.0] - Environment Setup & CI/CD Improvements
- **Project Renaming**: Renamed from `jira-issue-tracker-server` to `jira-issue-tracker` for better clarity
- **Interactive Setup**: Added `setup_interactive.py` script for guided configuration
- **Enhanced Documentation**: Comprehensive setup instructions and troubleshooting guide
- **Multi-Environment Support**: Clear documentation for Jira Cloud, Server, and Data Center
- **CI/CD Fixes**: Fixed Kivy window creation issues in headless environments
- **Environment Configuration**: Enhanced `example.env` with detailed documentation and JQL examples
- **Better User Experience**: Improved onboarding process for new users
- **Code Quality**: Maintained consistent formatting and style across all files

## [0.3.0] - UI/UX Improvements
- **Better Spacing & Layout**: Increased spacing and padding for improved visual hierarchy
- **Loading Indicators**: Added spinners and loading states during API calls
- **Better Error Messages**: User-friendly error messages with specific HTTP status code handling
- **Tooltips**: Added helpful hints for buttons and interactive elements
- **Visual Enhancements**: Improved button colors, error styling, and overall visual appeal
- **Enhanced User Experience**: Better feedback during loading and error states
- **Test Reliability**: Improved test mocking for UI components

## [0.2.0] - Code Quality & Testing Improvements
- **Code Quality**: Applied Black formatting to all files for consistent code style
- **Code Quality**: Removed unused imports and variables, fixed all Flake8 warnings
- **Testing**: Enhanced test suite with comprehensive error handling tests
- **Testing**: Improved test coverage for API error scenarios and UI interactions
- **Testing**: Fixed test reliability issues with proper mocking and KivyMD context handling
- **Project Structure**: Enhanced project configuration with proper development dependencies
- **Documentation**: Updated README with better installation and usage instructions

## [0.1.0] - Initial Release
- First public release of Jira Issue Tracker
- Kivy-based desktop app for tracking Jira issues with custom JQL queries
- Light/dark mode toggle, user settings popup, and secure API integration 