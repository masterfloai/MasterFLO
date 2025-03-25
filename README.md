# MasterFLO.ai Dashboard - User Guide

## Overview

This Python-based dashboard application is designed specifically for MasterFLO.ai, a digital marketing agency specializing in martial arts clients. The dashboard provides a comprehensive solution for managing clients, tasks, campaigns, and operations in one centralized platform.

## Features

The dashboard is organized into four main sections:

1. **Clients Section**
   - Track client information including services, campaign status, and billing
   - Filter clients by status and billing information
   - View detailed client profiles with notes and contract information

2. **Team Tasks Section**
   - Kanban board for visual task management
   - Task list with filtering capabilities
   - Track task assignments, due dates, and priorities
   - Link tasks to specific clients

3. **Campaign Tracker Section**
   - Monitor Meta Ads and Google Ads performance
   - Track leads, spend, and ROAS for each client
   - Manage GHL automation status
   - Store landing page URLs and campaign notes

4. **Operations Hub**
   - Access SOPs and resources
   - Team directory with contact information
   - Meeting notes with action items
   - Quick links to external tools and resources

## Installation

### Requirements
- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Download the dashboard package**
   - Save the `python_dashboard` folder to your computer

2. **Install dependencies and run the application**
   - Open a terminal/command prompt
   - Navigate to the `python_dashboard` folder
   - Run the following command:
     ```
     ./run.sh
     ```
   - This script will install all required dependencies and start the dashboard

3. **Alternative manual setup**
   - If the script doesn't work, you can manually install dependencies:
     ```
     pip install streamlit pandas matplotlib plotly
     streamlit run app.py
     ```

## Usage Guide

### Dashboard Overview

The main dashboard provides a summary of your agency's performance, including:
- Client statistics (total clients, active campaigns, etc.)
- Task status breakdown
- Campaign performance metrics
- Clients needing attention
- Upcoming tasks

### Managing Clients

1. **View Clients**
   - Navigate to the "Clients" section
   - Use filters to sort by campaign status or billing status
   - Click on a client to view detailed information

2. **Add/Edit Clients**
   - Click the "Add/Edit Client" tab
   - Fill in the client information form
   - Click "Save Client" to store the information

### Managing Tasks

1. **Kanban Board**
   - Drag tasks between columns to update their status
   - Click on a task to view details or edit
   - Use the "Add Task" button to create new tasks

2. **Task List**
   - Filter tasks by status, priority, or assignment
   - Click on a task to view details
   - Use the "Add/Edit Task" tab to create or modify tasks

### Tracking Campaigns

1. **View Campaigns**
   - Navigate to the "Campaign Tracker" section
   - Filter by client or GHL status
   - Click on a campaign to view detailed performance metrics

2. **Add/Edit Campaigns**
   - Use the "Add/Edit Campaign" tab
   - Enter performance data for Meta Ads and Google Ads
   - Add notes and update GHL status

### Using the Operations Hub

1. **SOPs & Resources**
   - Browse standard operating procedures by category
   - View and edit SOPs as needed
   - Add new SOPs for team reference

2. **Team Directory**
   - Access contact information for all team members
   - Add or edit team member profiles

3. **Meeting Notes**
   - Record and access notes from team meetings
   - Track action items and responsibilities

4. **Quick Links**
   - Access frequently used tools and resources
   - Add new links for easy reference

## Data Management

- All data is stored in a local SQLite database (`masterflo_dashboard.db`)
- The database is automatically created when you first run the application
- Sample data is provided to help you get started

## Customization

You can customize the dashboard by:
- Modifying the `app.py` file to add new features
- Editing the database schema to track additional information
- Customizing the UI colors and layout

## Troubleshooting

If you encounter issues:
1. Ensure Python 3.7+ is installed
2. Verify all dependencies are installed
3. Check that the database file is not corrupted
4. Restart the application

## Support

For additional support or customization, please contact the development team.
