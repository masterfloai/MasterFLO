import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# Set page configuration
st.set_page_config(
    page_title="MasterFLO.ai Dashboard",
    page_icon="🥋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database setup
DB_PATH = "masterflo_dashboard.db"

def init_db():
    """Initialize the database with tables if they don't exist"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create Clients table
    c.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        services TEXT,
        start_date TEXT,
        campaign_status TEXT,
        assigned_team TEXT,
        contract_end_date TEXT,
        billing_status TEXT,
        monthly_budget REAL,
        notes TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create Tasks table
    c.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        related_client TEXT,
        assigned_to TEXT,
        due_date TEXT,
        status TEXT,
        priority TEXT,
        task_type TEXT,
        estimated_hours REAL,
        actual_hours REAL,
        notes TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create Campaigns table
    c.execute('''
    CREATE TABLE IF NOT EXISTS campaigns (
        id INTEGER PRIMARY KEY,
        client_name TEXT NOT NULL,
        campaign_manager TEXT,
        last_review_date TEXT,
        next_review_date TEXT,
        meta_ads_spend REAL,
        meta_ads_roas REAL,
        meta_ads_leads INTEGER,
        meta_ads_notes TEXT,
        google_ads_spend REAL,
        google_ads_roas REAL,
        google_ads_leads INTEGER,
        google_ads_notes TEXT,
        ghl_status TEXT,
        landing_page_url TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create Operations table for SOPs
    c.execute('''
    CREATE TABLE IF NOT EXISTS sops (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT,
        content TEXT,
        last_updated TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create Team Directory table
    c.execute('''
    CREATE TABLE IF NOT EXISTS team_directory (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        role TEXT,
        email TEXT,
        phone TEXT,
        department TEXT,
        skills TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create Meeting Notes table
    c.execute('''
    CREATE TABLE IF NOT EXISTS meeting_notes (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        date TEXT,
        attendees TEXT,
        meeting_type TEXT,
        notes TEXT,
        action_items TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create Quick Links table
    c.execute('''
    CREATE TABLE IF NOT EXISTS quick_links (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT,
        url TEXT,
        description TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    
    # Check if we need to insert sample data (only if tables are empty)
    c.execute("SELECT COUNT(*) FROM clients")
    if c.fetchone()[0] == 0:
        insert_sample_data(conn)
    
    conn.close()

def insert_sample_data(conn):
    """Insert sample data for a martial arts marketing agency"""
    c = conn.cursor()
    
    # Sample Clients
    clients = [
        ("Dragon Martial Arts Academy", "Meta Ads, Google Ads, GHL", "2025-01-15", "Active", "John Smith", 
         "2026-01-15", "Current", 1500, "Client recently expanded to second location. Need to update ad targeting."),
        ("Elite Taekwondo Center", "Meta Ads, SEO", "2025-02-01", "Needs Attention", "Sarah Johnson", 
         "2026-02-01", "Current", 1200, "Website traffic dropping. Need to review SEO strategy."),
        ("Warrior Jiu-Jitsu", "Google Ads, Web", "2024-12-01", "Active", "Michael Brown", 
         "2025-12-01", "Current", 1000, "New landing page performing well. Consider upselling Meta Ads."),
        ("Master Kim's Karate", "Meta Ads, GHL", "2025-03-01", "Paused", "Sarah Johnson", 
         "2026-03-01", "Overdue", 800, "Client requested pause due to renovation. Follow up on 4/15."),
        ("Victory MMA & Fitness", "Meta Ads, Google Ads, SEO, Web, GHL", "2024-11-15", "Active", "John Smith", 
         "2025-11-15", "Current", 2500, "Our highest-value client. Monthly strategy call scheduled for 4/5.")
    ]
    
    c.executemany('''
    INSERT INTO clients (name, services, start_date, campaign_status, assigned_team, 
                        contract_end_date, billing_status, monthly_budget, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', clients)
    
    # Sample Tasks
    tasks = [
        ("Create April Ad Creative for Elite Taekwondo", "Elite Taekwondo Center", "Michael Brown", 
         "2025-04-01", "To Do", "High", "Ad Creation", 3, None, "Focus on summer camp promotion"),
        ("Optimize Google Ads Campaign for Dragon Martial Arts", "Dragon Martial Arts Academy", "John Smith", 
         "2025-03-28", "In Progress", "Medium", "Ad Creation", 2, 1.5, "Targeting new location, adjust geographic settings"),
        ("Monthly Performance Report - Victory MMA", "Victory MMA & Fitness", "Sarah Johnson", 
         "2025-04-05", "To Do", "Medium", "Reporting", 2, None, "Include comparison to previous quarter"),
        ("Update Landing Page for Warrior Jiu-Jitsu", "Warrior Jiu-Jitsu", "Michael Brown", 
         "2025-03-25", "Review", "High", "Website", 4, 5, "Added testimonials section and lead form"),
        ("Follow up with Master Kim about payment", "Master Kim's Karate", "John Smith", 
         "2025-03-30", "To Do", "Urgent", "Client Communication", 0.5, None, "Billing is overdue for March"),
        ("Team Meeting - April Planning", "Internal", "Sarah Johnson", 
         "2025-04-02", "To Do", "Medium", "Internal", 1, None, "Prepare agenda and quarterly goals")
    ]
    
    c.executemany('''
    INSERT INTO tasks (title, related_client, assigned_to, due_date, status, priority, 
                      task_type, estimated_hours, actual_hours, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', tasks)
    
    # Sample Campaigns
    campaigns = [
        ("Dragon Martial Arts Academy", "John Smith", "2025-03-15", "2025-04-15", 
         750, 3.2, 25, "Strong performance on parent-targeted ads. Increase budget for April.",
         650, 2.8, 18, "Keywords performing well, but CTR dropping. Review ad copy.",
         "Active", "https://dragonmartialarts.com/special-offer"),
        ("Elite Taekwondo Center", "Sarah Johnson", "2025-03-10", "2025-04-10", 
         600, 1.8, 12, "Performance declining. Need to refresh creative and targeting.",
         0, 0, 0, "Not currently running Google Ads.",
         "Issues", "https://elitetaekwondo.com/trial"),
        ("Warrior Jiu-Jitsu", "Michael Brown", "2025-03-20", "2025-04-20", 
         0, 0, 0, "Not currently running Meta Ads.",
         450, 3.5, 15, "New landing page conversion rate up 25%. Increase budget.",
         "Active", "https://warriorjiujitsu.com/free-class"),
        ("Master Kim's Karate", "Sarah Johnson", "2025-03-01", "2025-04-15", 
         400, 1.2, 8, "Campaign paused on 3/15 due to client request.",
         0, 0, 0, "Not currently running Google Ads.",
         "Needs Setup", "https://masterkimskarate.com/special"),
        ("Victory MMA & Fitness", "John Smith", "2025-03-25", "2025-04-25", 
         1200, 4.1, 35, "Excellent performance. New creative resonating well with audience.",
         950, 3.8, 28, "Strong performance across all ad groups. Consider expanding keywords.",
         "Active", "https://victorymma.com/membership")
    ]
    
    c.executemany('''
    INSERT INTO campaigns (client_name, campaign_manager, last_review_date, next_review_date,
                          meta_ads_spend, meta_ads_roas, meta_ads_leads, meta_ads_notes,
                          google_ads_spend, google_ads_roas, google_ads_leads, google_ads_notes,
                          ghl_status, landing_page_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', campaigns)
    
    # Sample Team Directory
    team = [
        ("John Smith", "Senior Account Manager", "john@masterflo.ai", "555-123-4567", 
         "Client Services", "Meta Ads, Google Ads, Client Management"),
        ("Sarah Johnson", "Marketing Strategist", "sarah@masterflo.ai", "555-234-5678", 
         "Strategy", "SEO, Content Strategy, Analytics"),
        ("Michael Brown", "Creative Director", "michael@masterflo.ai", "555-345-6789", 
         "Creative", "Ad Design, Web Development, Copywriting"),
        ("Lisa Chen", "Operations Manager", "lisa@masterflo.ai", "555-456-7890", 
         "Operations", "Project Management, Process Optimization"),
        ("David Wilson", "PPC Specialist", "david@masterflo.ai", "555-567-8901", 
         "Paid Media", "Google Ads, Meta Ads, Analytics")
    ]
    
    c.executemany('''
    INSERT INTO team_directory (name, role, email, phone, department, skills)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', team)
    
    # Sample SOPs
    sops = [
        ("Client Onboarding Process", "Onboarding", 
         "1. Initial consultation call\n2. Collect client assets\n3. Set up ad accounts\n4. Create initial campaign strategy\n5. Client approval\n6. Launch campaigns\n7. Schedule first review", 
         "2025-03-01"),
        ("Meta Ads Optimization SOP", "Ads Optimization", 
         "1. Review performance metrics\n2. Analyze audience insights\n3. Check ad creative performance\n4. Adjust budgets based on ROAS\n5. Update targeting if needed\n6. Create new ad variations\n7. Document changes and results", 
         "2025-02-15"),
        ("Google Ads Optimization SOP", "Ads Optimization", 
         "1. Review search terms report\n2. Analyze keyword performance\n3. Check quality scores\n4. Adjust bids based on performance\n5. Update ad copy if needed\n6. Test new extensions\n7. Document changes and results", 
         "2025-02-15"),
        ("Landing Page Optimization Guide", "Ads Optimization", 
         "1. Review current conversion rate\n2. Analyze user behavior with heatmaps\n3. Check mobile responsiveness\n4. Improve page load speed\n5. Clarify call-to-action\n6. Add social proof\n7. A/B test variations", 
         "2025-03-10"),
        ("Client Welcome Email", "Communication Templates", 
         "Subject: Welcome to MasterFLO.ai Marketing Services!\n\nDear [Client Name],\n\nWe're thrilled to welcome you to the MasterFLO.ai family! As martial arts marketing specialists, we understand the unique challenges and opportunities in growing your school...", 
         "2025-01-05"),
        ("Monthly Report Template", "Communication Templates", 
         "# Monthly Marketing Performance Report\n\n## Executive Summary\n[Brief overview of performance]\n\n## Campaign Performance\n### Meta Ads\n- Spend: $X,XXX\n- Leads: XX\n- Cost per Lead: $XX\n- ROAS: X.X\n\n### Google Ads\n[Similar metrics]\n\n## Recommendations\n[List of recommendations]", 
         "2025-03-01")
    ]
    
    c.executemany('''
    INSERT INTO sops (name, category, content, last_updated)
    VALUES (?, ?, ?, ?)
    ''', sops)
    
    # Sample Meeting Notes
    meetings = [
        ("Weekly Team Huddle", "2025-03-21", "All Staff", "Internal", 
         "Discussed current client performance and upcoming deadlines. Sarah raised concerns about Elite Taekwondo's declining performance. Michael presented new creative concepts for April campaigns.", 
         "Update campaign creative for Elite Taekwondo; Review SEO strategy for Dragon Martial Arts"),
        ("Victory MMA Strategy Session", "2025-03-25", "John Smith, Sarah Johnson", "Client", 
         "Met with client to discuss Q2 strategy. Client wants to focus on summer membership promotion. Agreed to increase Meta Ads budget by 20% and develop new creative focusing on family packages.", 
         "Increase Meta Ads budget; Develop summer promotion campaign"),
        ("Q2 Planning Meeting", "2025-03-28", "All Staff", "Internal", 
         "Reviewed Q1 performance and set goals for Q2. Key focus areas: improving client retention, optimizing ad performance, and launching new service offerings for martial arts schools.", 
         "Finalize Q2 goals; Assign new client acquisition targets")
    ]
    
    c.executemany('''
    INSERT INTO meeting_notes (title, date, attendees, meeting_type, notes, action_items)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', meetings)
    
    # Sample Quick Links
    links = [
        ("Meta Ads Manager", "External Tools", "https://business.facebook.com/", 
         "Meta Ads management platform"),
        ("Google Ads Dashboard", "External Tools", "https://ads.google.com/", 
         "Google Ads management platform"),
        ("Google Analytics", "External Tools", "https://analytics.google.com/", 
         "Website analytics platform"),
        ("Go High Level", "External Tools", "https://app.gohighlevel.com/", 
         "Marketing automation platform"),
        ("WordPress Admin", "External Tools", "https://clientwebsite.com/wp-admin/", 
         "Website management platform")
    ]
    
    c.executemany('''
    INSERT INTO quick_links (name, category, url, description)
    VALUES (?, ?, ?, ?)
    ''', links)
    
    conn.commit()

# Database functions
def get_clients():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM clients", conn)
    conn.close()
    return df

def get_tasks():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM tasks", conn)
    conn.close()
    return df

def get_campaigns():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM campaigns", conn)
    conn.close()
    return df

def get_sops():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM sops", conn)
    conn.close()
    return df

def get_team_directory():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM team_directory", conn)
    conn.close()
    return df

def get_meeting_notes():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM meeting_notes", conn)
    conn.close()
    return df

def get_quick_links():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM quick_links", conn)
    conn.close()
    return df

def add_client(name, services, start_date, campaign_status, assigned_team, 
              contract_end_date, billing_status, monthly_budget, notes):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
    INSERT INTO clients (name, services, start_date, campaign_status, assigned_team, 
                        contract_end_date, billing_status, monthly_budget, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, services, start_date, campaign_status, assigned_team, 
          contract_end_date, billing_status, monthly_budget, notes))
    conn.commit()
    conn.close()

def update_client(id, name, services, start_date, campaign_status, assigned_team, 
                 contract_end_date, billing_status, monthly_budget, notes):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
    UPDATE clients
    SET name = ?, services = ?, start_date = ?, campaign_status = ?, assigned_team = ?,
        contract_end_date = ?, billing_status = ?, monthly_budget = ?, notes = ?
    WHERE id = ?
    ''', (name, services, start_date, campaign_status, assigned_team, 
          contract_end_date, billing_status, monthly_budget, notes, id))
    conn.commit()
    conn.close()

def delete_client(id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM clients WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def add_task(title, related_client, assigned_to, due_date, status, priority, 
            task_type, estimated_hours, actual_hours, notes):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
    INSERT INTO tasks (title, related_client, assigned_to, due_date, status, priority, 
                      task_type, estimated_hours, actual_hours, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (title, related_client, assigned_to, due_date, status, priority, 
          task_type, estimated_hours, actual_hours, notes))
    conn.commit()
    conn.close()

def update_task(id, title, related_client, assigned_to, due_date, status, priority, 
               task_type, estimated_hours, actual_hours, notes):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
    UPDATE tasks
    SET title = ?, related_client = ?, assigned_to = ?, due_date = ?, status = ?, priority = ?,
        task_type = ?, estimated_hours = ?, actual_hours = ?, notes = ?
    WHERE id = ?
    ''', (title, related_client, assigned_to, due_date, status, priority, 
          task_type, estimated_hours, actual_hours, notes, id))
    conn.commit()
    conn.close()

def delete_task(id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def add_campaign(client_name, campaign_manager, last_review_date, next_review_date,
                meta_ads_spend, meta_ads_roas, meta_ads_leads, meta_ads_notes,
                google_ads_spend, google_ads_roas, google_ads_leads, google_ads_notes,
                ghl_status, landing_page_url):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
    INSERT INTO campaigns (client_name, campaign_manager, last_review_date, next_review_date,
                          meta_ads_spend, meta_ads_roas, meta_ads_leads, meta_ads_notes,
                          google_ads_spend, google_ads_roas, google_ads_leads, google_ads_notes,
                          ghl_status, landing_page_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (client_name, campaign_manager, last_review_date, next_review_date,
          meta_ads_spend, meta_ads_roas, meta_ads_leads, meta_ads_notes,
          google_ads_spend, google_ads_roas, google_ads_leads, google_ads_notes,
          ghl_status, landing_page_url))
    conn.commit()
    conn.close()

def update_campaign(id, client_name, campaign_manager, last_review_date, next_review_date,
                   meta_ads_spend, meta_ads_roas, meta_ads_leads, meta_ads_notes,
                   google_ads_spend, google_ads_roas, google_ads_leads, google_ads_notes,
                   ghl_status, landing_page_url):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
    UPDATE campaigns
    SET client_name = ?, campaign_manager = ?, last_review_date = ?, next_review_date = ?,
        meta_ads_spend = ?, meta_ads_roas = ?, meta_ads_leads = ?, meta_ads_notes = ?,
        google_ads_spend = ?, google_ads_roas = ?, google_ads_leads = ?, google_ads_notes = ?,
        ghl_status = ?, landing_page_url = ?
    WHERE id = ?
    ''', (client_name, campaign_manager, last_review_date, next_review_date,
          meta_ads_spend, meta_ads_roas, meta_ads_leads, meta_ads_notes,
          google_ads_spend, google_ads_roas, google_ads_leads, google_ads_notes,
          ghl_status, landing_page_url, id))
    conn.commit()
    conn.close()

def delete_campaign(id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM campaigns WHERE id = ?", (id,))
    conn.commit()
    conn.close()

# UI Functions
def show_dashboard():
    st.title("MasterFLO.ai Dashboard")
    st.subheader("Martial Arts Digital Marketing Agency")
    
    # Get data
    clients_df = get_clients()
    tasks_df = get_tasks()
    campaigns_df = get_campaigns()
    
    # Create metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Clients", len(clients_df))
        
    with col2:
        active_clients = len(clients_df[clients_df['campaign_status'] == 'Active'])
        st.metric("Active Campaigns", active_clients)
        
    with col3:
        needs_attention = len(clients_df[clients_df['campaign_status'] == 'Needs Attention'])
        st.metric("Needs Attention", needs_attention)
        
    with col4:
        monthly_revenue = clients_df['monthly_budget'].sum()
        st.metric("Monthly Revenue", f"${monthly_revenue:,.2f}")
    
    # Create two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Campaign Status")
        campaign_status_counts = clients_df['campaign_status'].value_counts().reset_index()
        campaign_status_counts.columns = ['Status', 'Count']
        
        fig = px.pie(campaign_status_counts, values='Count', names='Status', 
                    color='Status', 
                    color_discrete_map={'Active': '#34A853', 
                                        'Paused': '#FBBC05', 
                                        'Needs Attention': '#EA4335'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Task Status")
        task_status_counts = tasks_df['status'].value_counts().reset_index()
        task_status_counts.columns = ['Status', 'Count']
        
        fig = px.pie(task_status_counts, values='Count', names='Status',
                    color='Status',
                    color_discrete_map={'To Do': '#E0E0E0',
                                        'In Progress': '#4285F4',
                                        'Review': '#FBBC05',
                                        'Done': '#34A853'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Create two columns for tables
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Clients Needing Attention")
        needs_attention_df = clients_df[clients_df['campaign_status'] == 'Needs Attention'][['name', 'assigned_team', 'notes']]
        needs_attention_df.columns = ['Client Name', 'Assigned To', 'Issue']
        st.dataframe(needs_attention_df, use_container_width=True)
    
    with col2:
        st.subheader("Upcoming Tasks")
        upcoming_tasks_df = tasks_df[(tasks_df['status'] == 'To Do') | (tasks_df['status'] == 'In Progress')]
        upcoming_tasks_df = upcoming_tasks_df.sort_values('due_date')[['title', 'due_date', 'assigned_to']]
        upcoming_tasks_df.columns = ['Task', 'Due Date', 'Assigned To']
        st.dataframe(upcoming_tasks_df, use_container_width=True)
    
    # Campaign Performance
    st.subheader("Campaign Performance")
    
    # Calculate total leads and spend
    total_meta_leads = campaigns_df['meta_ads_leads'].sum()
    total_google_leads = campaigns_df['google_ads_leads'].sum()
    total_meta_spend = campaigns_df['meta_ads_spend'].sum()
    total_google_spend = campaigns_df['google_ads_spend'].sum()
    
    # Create metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Ad Spend", f"${total_meta_spend + total_google_spend:,.2f}")
        
    with col2:
        st.metric("Total Leads", f"{total_meta_leads + total_google_leads}")
        
    with col3:
        cost_per_lead = (total_meta_spend + total_google_spend) / (total_meta_leads + total_google_leads) if (total_meta_leads + total_google_leads) > 0 else 0
        st.metric("Avg. Cost Per Lead", f"${cost_per_lead:,.2f}")
        
    with col4:
        st.metric("Campaigns", len(campaigns_df))
    
    # Create leads by client chart
    leads_by_client = campaigns_df[['client_name', 'meta_ads_leads', 'google_ads_leads']].copy()
    leads_by_client['total_leads'] = leads_by_client['meta_ads_leads'] + leads_by_client['google_ads_leads']
    leads_by_client = leads_by_client.sort_values('total_leads', ascending=False)
    
    fig = px.bar(leads_by_client, x='client_name', y=['meta_ads_leads', 'google_ads_leads'],
                labels={'value': 'Leads', 'client_name': 'Client', 'variable': 'Source'},
                title='Leads by Client',
                color_discrete_map={'meta_ads_leads': '#4285F4', 'google_ads_leads': '#EA4335'})
    st.plotly_chart(fig, use_container_width=True)

def show_clients():
    st.title("Clients")
    
    # Get data
    clients_df = get_clients()
    
    # Create tabs
    tab1, tab2 = st.tabs(["View Clients", "Add/Edit Client"])
    
    with tab1:
        # Filter options
        st.subheader("Filter Options")
        col1, col2 = st.columns(2)
        
        with col1:
            status_filter = st.multiselect("Campaign Status", 
                                          options=clients_df['campaign_status'].unique(),
                                          default=clients_df['campaign_status'].unique())
        
        with col2:
            billing_filter = st.multiselect("Billing Status",
                                           options=clients_df['billing_status'].unique(),
                                           default=clients_df['billing_status'].unique())
        
        # Apply filters
        filtered_df = clients_df[
            clients_df['campaign_status'].isin(status_filter) &
            clients_df['billing_status'].isin(billing_filter)
        ]
        
        # Display clients table
        st.subheader("Clients List")
        
        # Format the dataframe for display
        display_df = filtered_df.copy()
        display_df['monthly_budget'] = display_df['monthly_budget'].apply(lambda x: f"${x:,.2f}")
        
        # Apply color coding to campaign status
        def color_campaign_status(val):
            if val == 'Active':
                return 'background-color: #34A853; color: white'
            elif val == 'Paused':
                return 'background-color: #FBBC05; color: black'
            elif val == 'Needs Attention':
                return 'background-color: #EA4335; color: white'
            return ''
        
        # Apply color coding to billing status
        def color_billing_status(val):
            if val == 'Current':
                return 'background-color: #34A853; color: white'
            elif val == 'Overdue':
                return 'background-color: #EA4335; color: white'
            elif val == 'Free Trial':
                return 'background-color: #4285F4; color: white'
            elif val == 'Pending':
                return 'background-color: #FBBC05; color: black'
            return ''
        
        # Apply styling
        styled_df = display_df.style.applymap(color_campaign_status, subset=['campaign_status'])\
                                   .applymap(color_billing_status, subset=['billing_status'])
        
        st.dataframe(styled_df, use_container_width=True)
        
        # Client details section
        st.subheader("Client Details")
        selected_client = st.selectbox("Select Client", options=clients_df['name'].tolist())
        
        if selected_client:
            client_data = clients_df[clients_df['name'] == selected_client].iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Client Name:** {client_data['name']}")
                st.markdown(f"**Services:** {client_data['services']}")
                st.markdown(f"**Campaign Status:** {client_data['campaign_status']}")
                st.markdown(f"**Assigned Team:** {client_data['assigned_team']}")
            
            with col2:
                st.markdown(f"**Start Date:** {client_data['start_date']}")
                st.markdown(f"**Contract End Date:** {client_data['contract_end_date']}")
                st.markdown(f"**Billing Status:** {client_data['billing_status']}")
                st.markdown(f"**Monthly Budget:** ${client_data['monthly_budget']:,.2f}")
            
            st.markdown("**Notes/To-Dos:**")
            st.text_area("", value=client_data['notes'], height=100, key="client_notes_view", disabled=True)
            
            # Actions
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Edit Client", key="edit_client_btn"):
                    st.session_state.edit_client_id = client_data['id']
                    st.session_state.active_tab = "Add/Edit Client"
                    st.rerun()
            
            with col2:
                if st.button("Delete Client", key="delete_client_btn"):
                    delete_client(client_data['id'])
                    st.success(f"Client '{selected_client}' deleted successfully!")
                    st.rerun()
    
    with tab2:
        st.subheader("Add/Edit Client")
        
        # Check if we're editing an existing client
        edit_mode = False
        client_data = None
        
        if hasattr(st.session_state, 'edit_client_id') and st.session_state.edit_client_id:
            edit_mode = True
            client_data = clients_df[clients_df['id'] == st.session_state.edit_client_id].iloc[0]
            st.info(f"Editing client: {client_data['name']}")
        
        # Form for adding/editing client
        with st.form("client_form"):
            name = st.text_input("Client Name", value=client_data['name'] if edit_mode else "")
            
            # Services multi-select
            all_services = ["Meta Ads", "Google Ads", "SEO", "Web", "GHL"]
            default_services = client_data['services'].split(", ") if edit_mode and client_data['services'] else []
            services = st.multiselect("Services", options=all_services, default=default_services)
            
            col1, col2 = st.columns(2)
            
            with col1:
                start_date = st.date_input("Start Date", 
                                          value=datetime.strptime(client_data['start_date'], "%Y-%m-%d").date() if edit_mode and client_data['start_date'] else datetime.now())
                
                campaign_status = st.selectbox("Campaign Status", 
                                              options=["Active", "Paused", "Needs Attention"],
                                              index=["Active", "Paused", "Needs Attention"].index(client_data['campaign_status']) if edit_mode else 0)
                
                assigned_team = st.text_input("Assigned Team Member(s)", 
                                             value=client_data['assigned_team'] if edit_mode else "")
            
            with col2:
                contract_end_date = st.date_input("Contract End Date", 
                                                 value=datetime.strptime(client_data['contract_end_date'], "%Y-%m-%d").date() if edit_mode and client_data['contract_end_date'] else (datetime.now() + timedelta(days=365)))
                
                billing_status = st.selectbox("Billing Status", 
                                             options=["Current", "Overdue", "Free Trial", "Pending"],
                                             index=["Current", "Overdue", "Free Trial", "Pending"].index(client_data['billing_status']) if edit_mode else 0)
                
                monthly_budget = st.number_input("Monthly Budget ($)", 
                                               min_value=0.0, 
                                               value=float(client_data['monthly_budget']) if edit_mode else 1000.0,
                                               step=100.0)
            
            notes = st.text_area("Notes/To-Dos", 
                                value=client_data['notes'] if edit_mode else "")
            
            submit_button = st.form_submit_button("Save Client")
        
        if submit_button:
            # Convert services list to string
            services_str = ", ".join(services)
            
            # Format dates
            start_date_str = start_date.strftime("%Y-%m-%d")
            contract_end_date_str = contract_end_date.strftime("%Y-%m-%d")
            
            if edit_mode:
                update_client(
                    st.session_state.edit_client_id, name, services_str, start_date_str, 
                    campaign_status, assigned_team, contract_end_date_str, 
                    billing_status, monthly_budget, notes
                )
                st.success(f"Client '{name}' updated successfully!")
                # Clear edit mode
                st.session_state.edit_client_id = None
            else:
                add_client(
                    name, services_str, start_date_str, campaign_status, 
                    assigned_team, contract_end_date_str, billing_status, 
                    monthly_budget, notes
                )
                st.success(f"Client '{name}' added successfully!")
            
            # Refresh the page
            st.rerun()

def show_tasks():
    st.title("Team Tasks")
    
    # Get data
    tasks_df = get_tasks()
    clients_df = get_clients()
    team_df = get_team_directory()
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Kanban Board", "Task List", "Add/Edit Task"])
    
    with tab1:
        st.subheader("Task Board")
        
        # Create columns for each status
        col1, col2, col3, col4 = st.columns(4)
        
        # To Do column
        with col1:
            st.markdown("### To Do")
            todo_tasks = tasks_df[tasks_df['status'] == 'To Do'].sort_values('due_date')
            
            for _, task in todo_tasks.iterrows():
                with st.container(border=True):
                    st.markdown(f"**{task['title']}**")
                    st.markdown(f"**Client:** {task['related_client']}")
                    st.markdown(f"**Assigned to:** {task['assigned_to']}")
                    st.markdown(f"**Due:** {task['due_date']}")
                    
                    # Priority indicator
                    priority_color = {
                        'Low': '#34A853',
                        'Medium': '#4285F4',
                        'High': '#FBBC05',
                        'Urgent': '#EA4335'
                    }
                    st.markdown(f"<span style='color:{priority_color.get(task['priority'], '#000000')};'>●</span> **{task['priority']}**", unsafe_allow_html=True)
                    
                    # Actions
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Edit", key=f"edit_todo_{task['id']}"):
                            st.session_state.edit_task_id = task['id']
                            st.session_state.active_tab = "Add/Edit Task"
                            st.rerun()
                    
                    with col2:
                        if st.button("→ In Progress", key=f"move_todo_{task['id']}"):
                            update_task(
                                task['id'], task['title'], task['related_client'], 
                                task['assigned_to'], task['due_date'], "In Progress", 
                                task['priority'], task['task_type'], 
                                task['estimated_hours'], task['actual_hours'], 
                                task['notes']
                            )
                            st.rerun()
        
        # In Progress column
        with col2:
            st.markdown("### In Progress")
            in_progress_tasks = tasks_df[tasks_df['status'] == 'In Progress'].sort_values('due_date')
            
            for _, task in in_progress_tasks.iterrows():
                with st.container(border=True):
                    st.markdown(f"**{task['title']}**")
                    st.markdown(f"**Client:** {task['related_client']}")
                    st.markdown(f"**Assigned to:** {task['assigned_to']}")
                    st.markdown(f"**Due:** {task['due_date']}")
                    
                    # Priority indicator
                    priority_color = {
                        'Low': '#34A853',
                        'Medium': '#4285F4',
                        'High': '#FBBC05',
                        'Urgent': '#EA4335'
                    }
                    st.markdown(f"<span style='color:{priority_color.get(task['priority'], '#000000')};'>●</span> **{task['priority']}**", unsafe_allow_html=True)
                    
                    # Actions
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("← To Do", key=f"back_inprogress_{task['id']}"):
                            update_task(
                                task['id'], task['title'], task['related_client'], 
                                task['assigned_to'], task['due_date'], "To Do", 
                                task['priority'], task['task_type'], 
                                task['estimated_hours'], task['actual_hours'], 
                                task['notes']
                            )
                            st.rerun()
                    
                    with col2:
                        if st.button("→ Review", key=f"move_inprogress_{task['id']}"):
                            update_task(
                                task['id'], task['title'], task['related_client'], 
                                task['assigned_to'], task['due_date'], "Review", 
                                task['priority'], task['task_type'], 
                                task['estimated_hours'], task['actual_hours'], 
                                task['notes']
                            )
                            st.rerun()
        
        # Review column
        with col3:
            st.markdown("### Review")
            review_tasks = tasks_df[tasks_df['status'] == 'Review'].sort_values('due_date')
            
            for _, task in review_tasks.iterrows():
                with st.container(border=True):
                    st.markdown(f"**{task['title']}**")
                    st.markdown(f"**Client:** {task['related_client']}")
                    st.markdown(f"**Assigned to:** {task['assigned_to']}")
                    st.markdown(f"**Due:** {task['due_date']}")
                    
                    # Priority indicator
                    priority_color = {
                        'Low': '#34A853',
                        'Medium': '#4285F4',
                        'High': '#FBBC05',
                        'Urgent': '#EA4335'
                    }
                    st.markdown(f"<span style='color:{priority_color.get(task['priority'], '#000000')};'>●</span> **{task['priority']}**", unsafe_allow_html=True)
                    
                    # Actions
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("← In Progress", key=f"back_review_{task['id']}"):
                            update_task(
                                task['id'], task['title'], task['related_client'], 
                                task['assigned_to'], task['due_date'], "In Progress", 
                                task['priority'], task['task_type'], 
                                task['estimated_hours'], task['actual_hours'], 
                                task['notes']
                            )
                            st.rerun()
                    
                    with col2:
                        if st.button("→ Done", key=f"move_review_{task['id']}"):
                            update_task(
                                task['id'], task['title'], task['related_client'], 
                                task['assigned_to'], task['due_date'], "Done", 
                                task['priority'], task['task_type'], 
                                task['estimated_hours'], task['actual_hours'], 
                                task['notes']
                            )
                            st.rerun()
        
        # Done column
        with col4:
            st.markdown("### Done")
            done_tasks = tasks_df[tasks_df['status'] == 'Done'].sort_values('due_date')
            
            for _, task in done_tasks.iterrows():
                with st.container(border=True):
                    st.markdown(f"**{task['title']}**")
                    st.markdown(f"**Client:** {task['related_client']}")
                    st.markdown(f"**Assigned to:** {task['assigned_to']}")
                    st.markdown(f"**Due:** {task['due_date']}")
                    
                    # Priority indicator
                    priority_color = {
                        'Low': '#34A853',
                        'Medium': '#4285F4',
                        'High': '#FBBC05',
                        'Urgent': '#EA4335'
                    }
                    st.markdown(f"<span style='color:{priority_color.get(task['priority'], '#000000')};'>●</span> **{task['priority']}**", unsafe_allow_html=True)
                    
                    # Actions
                    if st.button("← Review", key=f"back_done_{task['id']}"):
                        update_task(
                            task['id'], task['title'], task['related_client'], 
                            task['assigned_to'], task['due_date'], "Review", 
                            task['priority'], task['task_type'], 
                            task['estimated_hours'], task['actual_hours'], 
                            task['notes']
                        )
                        st.rerun()
    
    with tab2:
        st.subheader("Task List")
        
        # Filter options
        st.subheader("Filter Options")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.multiselect("Status", 
                                          options=tasks_df['status'].unique(),
                                          default=tasks_df['status'].unique())
        
        with col2:
            priority_filter = st.multiselect("Priority",
                                           options=tasks_df['priority'].unique(),
                                           default=tasks_df['priority'].unique())
        
        with col3:
            assigned_filter = st.multiselect("Assigned To",
                                           options=tasks_df['assigned_to'].unique(),
                                           default=tasks_df['assigned_to'].unique())
        
        # Apply filters
        filtered_df = tasks_df[
            tasks_df['status'].isin(status_filter) &
            tasks_df['priority'].isin(priority_filter) &
            tasks_df['assigned_to'].isin(assigned_filter)
        ]
        
        # Display tasks table
        st.subheader("Tasks List")
        
        # Format the dataframe for display
        display_df = filtered_df.copy()
        
        # Apply color coding to status
        def color_status(val):
            if val == 'To Do':
                return 'background-color: #E0E0E0; color: black'
            elif val == 'In Progress':
                return 'background-color: #4285F4; color: white'
            elif val == 'Review':
                return 'background-color: #FBBC05; color: black'
            elif val == 'Done':
                return 'background-color: #34A853; color: white'
            return ''
        
        # Apply color coding to priority
        def color_priority(val):
            if val == 'Low':
                return 'color: #34A853'
            elif val == 'Medium':
                return 'color: #4285F4'
            elif val == 'High':
                return 'color: #FBBC05'
            elif val == 'Urgent':
                return 'color: #EA4335'
            return ''
        
        # Apply styling
        styled_df = display_df.style.applymap(color_status, subset=['status'])\
                                   .applymap(color_priority, subset=['priority'])
        
        st.dataframe(styled_df, use_container_width=True)
        
        # Task details section
        st.subheader("Task Details")
        selected_task = st.selectbox("Select Task", options=tasks_df['title'].tolist())
        
        if selected_task:
            task_data = tasks_df[tasks_df['title'] == selected_task].iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Task Title:** {task_data['title']}")
                st.markdown(f"**Related Client:** {task_data['related_client']}")
                st.markdown(f"**Assigned To:** {task_data['assigned_to']}")
                st.markdown(f"**Due Date:** {task_data['due_date']}")
            
            with col2:
                st.markdown(f"**Status:** {task_data['status']}")
                st.markdown(f"**Priority:** {task_data['priority']}")
                st.markdown(f"**Task Type:** {task_data['task_type']}")
                st.markdown(f"**Estimated Hours:** {task_data['estimated_hours']}")
                st.markdown(f"**Actual Hours:** {task_data['actual_hours'] if task_data['actual_hours'] else 'Not recorded'}")
            
            st.markdown("**Notes:**")
            st.text_area("", value=task_data['notes'], height=100, key="task_notes_view", disabled=True)
            
            # Actions
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Edit Task", key="edit_task_btn"):
                    st.session_state.edit_task_id = task_data['id']
                    st.session_state.active_tab = "Add/Edit Task"
                    st.rerun()
            
            with col2:
                if st.button("Delete Task", key="delete_task_btn"):
                    delete_task(task_data['id'])
                    st.success(f"Task '{selected_task}' deleted successfully!")
                    st.rerun()
    
    with tab3:
        st.subheader("Add/Edit Task")
        
        # Check if we're editing an existing task
        edit_mode = False
        task_data = None
        
        if hasattr(st.session_state, 'edit_task_id') and st.session_state.edit_task_id:
            edit_mode = True
            task_data = tasks_df[tasks_df['id'] == st.session_state.edit_task_id].iloc[0]
            st.info(f"Editing task: {task_data['title']}")
        
        # Form for adding/editing task
        with st.form("task_form"):
            title = st.text_input("Task Title", value=task_data['title'] if edit_mode else "")
            
            # Get client list for dropdown
            client_list = clients_df['name'].tolist()
            client_list.append("Internal")  # Add "Internal" option for non-client tasks
            
            # Get team members for dropdown
            team_list = team_df['name'].tolist()
            
            col1, col2 = st.columns(2)
            
            with col1:
                related_client = st.selectbox("Related Client", 
                                             options=client_list,
                                             index=client_list.index(task_data['related_client']) if edit_mode and task_data['related_client'] in client_list else 0)
                
                assigned_to = st.selectbox("Assigned To", 
                                         options=team_list,
                                         index=team_list.index(task_data['assigned_to']) if edit_mode and task_data['assigned_to'] in team_list else 0)
                
                due_date = st.date_input("Due Date", 
                                        value=datetime.strptime(task_data['due_date'], "%Y-%m-%d").date() if edit_mode and task_data['due_date'] else datetime.now())
                
                status = st.selectbox("Status", 
                                     options=["To Do", "In Progress", "Review", "Done"],
                                     index=["To Do", "In Progress", "Review", "Done"].index(task_data['status']) if edit_mode else 0)
            
            with col2:
                priority = st.selectbox("Priority", 
                                       options=["Low", "Medium", "High", "Urgent"],
                                       index=["Low", "Medium", "High", "Urgent"].index(task_data['priority']) if edit_mode else 1)
                
                task_type = st.selectbox("Task Type", 
                                        options=["Ad Creation", "Content", "Website", "Reporting", "Client Communication", "Internal", "GHL"],
                                        index=["Ad Creation", "Content", "Website", "Reporting", "Client Communication", "Internal", "GHL"].index(task_data['task_type']) if edit_mode and task_data['task_type'] in ["Ad Creation", "Content", "Website", "Reporting", "Client Communication", "Internal", "GHL"] else 0)
                
                estimated_hours = st.number_input("Estimated Hours", 
                                                min_value=0.0, 
                                                value=float(task_data['estimated_hours']) if edit_mode and task_data['estimated_hours'] else 1.0,
                                                step=0.5)
                
                actual_hours = st.number_input("Actual Hours", 
                                             min_value=0.0, 
                                             value=float(task_data['actual_hours']) if edit_mode and task_data['actual_hours'] else 0.0,
                                             step=0.5)
            
            notes = st.text_area("Notes", 
                               value=task_data['notes'] if edit_mode else "")
            
            submit_button = st.form_submit_button("Save Task")
        
        if submit_button:
            # Format date
            due_date_str = due_date.strftime("%Y-%m-%d")
            
            if edit_mode:
                update_task(
                    st.session_state.edit_task_id, title, related_client, 
                    assigned_to, due_date_str, status, priority, 
                    task_type, estimated_hours, actual_hours, notes
                )
                st.success(f"Task '{title}' updated successfully!")
                # Clear edit mode
                st.session_state.edit_task_id = None
            else:
                add_task(
                    title, related_client, assigned_to, due_date_str, 
                    status, priority, task_type, estimated_hours, 
                    actual_hours, notes
                )
                st.success(f"Task '{title}' added successfully!")
            
            # Refresh the page
            st.rerun()

def show_campaigns():
    st.title("Campaign Tracker")
    
    # Get data
    campaigns_df = get_campaigns()
    clients_df = get_clients()
    team_df = get_team_directory()
    
    # Create tabs
    tab1, tab2 = st.tabs(["View Campaigns", "Add/Edit Campaign"])
    
    with tab1:
        # Filter options
        st.subheader("Filter Options")
        col1, col2 = st.columns(2)
        
        with col1:
            client_filter = st.multiselect("Client", 
                                          options=campaigns_df['client_name'].unique(),
                                          default=campaigns_df['client_name'].unique())
        
        with col2:
            ghl_filter = st.multiselect("GHL Status",
                                       options=campaigns_df['ghl_status'].unique(),
                                       default=campaigns_df['ghl_status'].unique())
        
        # Apply filters
        filtered_df = campaigns_df[
            campaigns_df['client_name'].isin(client_filter) &
            campaigns_df['ghl_status'].isin(ghl_filter)
        ]
        
        # Display campaigns table
        st.subheader("Campaigns List")
        
        # Format the dataframe for display
        display_df = filtered_df.copy()
        display_df['meta_ads_spend'] = display_df['meta_ads_spend'].apply(lambda x: f"${x:,.2f}" if x > 0 else "N/A")
        display_df['google_ads_spend'] = display_df['google_ads_spend'].apply(lambda x: f"${x:,.2f}" if x > 0 else "N/A")
        
        # Apply color coding to GHL status
        def color_ghl_status(val):
            if val == 'Active':
                return 'background-color: #34A853; color: white'
            elif val == 'Needs Setup':
                return 'background-color: #FBBC05; color: black'
            elif val == 'Issues':
                return 'background-color: #EA4335; color: white'
            elif val == 'Not Applicable':
                return 'background-color: #E0E0E0; color: black'
            return ''
        
        # Apply styling
        styled_df = display_df.style.applymap(color_ghl_status, subset=['ghl_status'])
        
        st.dataframe(styled_df, use_container_width=True)
        
        # Campaign details section
        st.subheader("Campaign Details")
        selected_campaign = st.selectbox("Select Client Campaign", options=campaigns_df['client_name'].tolist())
        
        if selected_campaign:
            campaign_data = campaigns_df[campaigns_df['client_name'] == selected_campaign].iloc[0]
            
            # Create tabs for Meta Ads and Google Ads
            meta_tab, google_tab, ghl_tab = st.tabs(["Meta Ads", "Google Ads", "GHL & Landing Page"])
            
            with meta_tab:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Meta Ads Spend", f"${campaign_data['meta_ads_spend']:,.2f}" if campaign_data['meta_ads_spend'] > 0 else "N/A")
                
                with col2:
                    st.metric("Meta Ads ROAS", f"{campaign_data['meta_ads_roas']:.1f}x" if campaign_data['meta_ads_roas'] > 0 else "N/A")
                
                with col3:
                    st.metric("Meta Ads Leads", f"{campaign_data['meta_ads_leads']}" if campaign_data['meta_ads_leads'] > 0 else "N/A")
                
                st.markdown("**Meta Ads Notes:**")
                st.text_area("", value=campaign_data['meta_ads_notes'], height=100, key="meta_notes_view", disabled=True)
            
            with google_tab:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Google Ads Spend", f"${campaign_data['google_ads_spend']:,.2f}" if campaign_data['google_ads_spend'] > 0 else "N/A")
                
                with col2:
                    st.metric("Google Ads ROAS", f"{campaign_data['google_ads_roas']:.1f}x" if campaign_data['google_ads_roas'] > 0 else "N/A")
                
                with col3:
                    st.metric("Google Ads Leads", f"{campaign_data['google_ads_leads']}" if campaign_data['google_ads_leads'] > 0 else "N/A")
                
                st.markdown("**Google Ads Notes:**")
                st.text_area("", value=campaign_data['google_ads_notes'], height=100, key="google_notes_view", disabled=True)
            
            with ghl_tab:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**GHL Status:** {campaign_data['ghl_status']}")
                
                with col2:
                    st.markdown(f"**Landing Page URL:** [{campaign_data['landing_page_url']}]({campaign_data['landing_page_url']})")
            
            st.markdown(f"**Campaign Manager:** {campaign_data['campaign_manager']}")
            st.markdown(f"**Last Review Date:** {campaign_data['last_review_date']}")
            st.markdown(f"**Next Review Date:** {campaign_data['next_review_date']}")
            
            # Actions
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Edit Campaign", key="edit_campaign_btn"):
                    st.session_state.edit_campaign_id = campaign_data['id']
                    st.session_state.active_tab = "Add/Edit Campaign"
                    st.rerun()
            
            with col2:
                if st.button("Delete Campaign", key="delete_campaign_btn"):
                    delete_campaign(campaign_data['id'])
                    st.success(f"Campaign for '{selected_campaign}' deleted successfully!")
                    st.rerun()
    
    with tab2:
        st.subheader("Add/Edit Campaign")
        
        # Check if we're editing an existing campaign
        edit_mode = False
        campaign_data = None
        
        if hasattr(st.session_state, 'edit_campaign_id') and st.session_state.edit_campaign_id:
            edit_mode = True
            campaign_data = campaigns_df[campaigns_df['id'] == st.session_state.edit_campaign_id].iloc[0]
            st.info(f"Editing campaign for: {campaign_data['client_name']}")
        
        # Form for adding/editing campaign
        with st.form("campaign_form"):
            # Get client list for dropdown
            client_list = clients_df['name'].tolist()
            
            # Get team members for dropdown
            team_list = team_df['name'].tolist()
            
            client_name = st.selectbox("Client Name", 
                                      options=client_list,
                                      index=client_list.index(campaign_data['client_name']) if edit_mode and campaign_data['client_name'] in client_list else 0)
            
            campaign_manager = st.selectbox("Campaign Manager", 
                                          options=team_list,
                                          index=team_list.index(campaign_data['campaign_manager']) if edit_mode and campaign_data['campaign_manager'] in team_list else 0)
            
            col1, col2 = st.columns(2)
            
            with col1:
                last_review_date = st.date_input("Last Review Date", 
                                               value=datetime.strptime(campaign_data['last_review_date'], "%Y-%m-%d").date() if edit_mode and campaign_data['last_review_date'] else datetime.now())
            
            with col2:
                next_review_date = st.date_input("Next Review Date", 
                                               value=datetime.strptime(campaign_data['next_review_date'], "%Y-%m-%d").date() if edit_mode and campaign_data['next_review_date'] else (datetime.now() + timedelta(days=30)))
            
            # Meta Ads section
            st.subheader("Meta Ads")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                meta_ads_spend = st.number_input("Meta Ads Spend ($)", 
                                               min_value=0.0, 
                                               value=float(campaign_data['meta_ads_spend']) if edit_mode else 0.0,
                                               step=50.0)
            
            with col2:
                meta_ads_roas = st.number_input("Meta Ads ROAS", 
                                              min_value=0.0, 
                                              value=float(campaign_data['meta_ads_roas']) if edit_mode else 0.0,
                                              step=0.1)
            
            with col3:
                meta_ads_leads = st.number_input("Meta Ads Leads", 
                                               min_value=0, 
                                               value=int(campaign_data['meta_ads_leads']) if edit_mode else 0,
                                               step=1)
            
            meta_ads_notes = st.text_area("Meta Ads Notes", 
                                         value=campaign_data['meta_ads_notes'] if edit_mode else "")
            
            # Google Ads section
            st.subheader("Google Ads")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                google_ads_spend = st.number_input("Google Ads Spend ($)", 
                                                 min_value=0.0, 
                                                 value=float(campaign_data['google_ads_spend']) if edit_mode else 0.0,
                                                 step=50.0)
            
            with col2:
                google_ads_roas = st.number_input("Google Ads ROAS", 
                                                min_value=0.0, 
                                                value=float(campaign_data['google_ads_roas']) if edit_mode else 0.0,
                                                step=0.1)
            
            with col3:
                google_ads_leads = st.number_input("Google Ads Leads", 
                                                 min_value=0, 
                                                 value=int(campaign_data['google_ads_leads']) if edit_mode else 0,
                                                 step=1)
            
            google_ads_notes = st.text_area("Google Ads Notes", 
                                          value=campaign_data['google_ads_notes'] if edit_mode else "")
            
            # GHL and Landing Page section
            st.subheader("GHL & Landing Page")
            
            col1, col2 = st.columns(2)
            
            with col1:
                ghl_status = st.selectbox("GHL Status", 
                                         options=["Active", "Needs Setup", "Issues", "Not Applicable"],
                                         index=["Active", "Needs Setup", "Issues", "Not Applicable"].index(campaign_data['ghl_status']) if edit_mode else 0)
            
            with col2:
                landing_page_url = st.text_input("Landing Page URL", 
                                               value=campaign_data['landing_page_url'] if edit_mode else "https://")
            
            submit_button = st.form_submit_button("Save Campaign")
        
        if submit_button:
            # Format dates
            last_review_date_str = last_review_date.strftime("%Y-%m-%d")
            next_review_date_str = next_review_date.strftime("%Y-%m-%d")
            
            if edit_mode:
                update_campaign(
                    st.session_state.edit_campaign_id, client_name, campaign_manager, 
                    last_review_date_str, next_review_date_str, meta_ads_spend, 
                    meta_ads_roas, meta_ads_leads, meta_ads_notes, google_ads_spend, 
                    google_ads_roas, google_ads_leads, google_ads_notes, 
                    ghl_status, landing_page_url
                )
                st.success(f"Campaign for '{client_name}' updated successfully!")
                # Clear edit mode
                st.session_state.edit_campaign_id = None
            else:
                add_campaign(
                    client_name, campaign_manager, last_review_date_str, 
                    next_review_date_str, meta_ads_spend, meta_ads_roas, 
                    meta_ads_leads, meta_ads_notes, google_ads_spend, 
                    google_ads_roas, google_ads_leads, google_ads_notes, 
                    ghl_status, landing_page_url
                )
                st.success(f"Campaign for '{client_name}' added successfully!")
            
            # Refresh the page
            st.rerun()

def show_operations():
    st.title("Operations Hub")
    
    # Get data
    sops_df = get_sops()
    team_df = get_team_directory()
    meetings_df = get_meeting_notes()
    links_df = get_quick_links()
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["SOPs & Resources", "Team Directory", "Meeting Notes", "Quick Links"])
    
    with tab1:
        st.subheader("Standard Operating Procedures")
        
        # Filter by category
        categories = sops_df['category'].unique()
        selected_category = st.selectbox("Filter by Category", options=["All"] + list(categories))
        
        if selected_category == "All":
            filtered_sops = sops_df
        else:
            filtered_sops = sops_df[sops_df['category'] == selected_category]
        
        # Display SOPs
        for _, sop in filtered_sops.iterrows():
            with st.expander(f"{sop['name']} (Last Updated: {sop['last_updated']})"):
                st.markdown(sop['content'])
                
                # Edit button
                if st.button("Edit", key=f"edit_sop_{sop['id']}"):
                    st.session_state.edit_sop_id = sop['id']
                    st.session_state.edit_sop_mode = True
                    st.rerun()
        
        # Add new SOP button
        if st.button("Add New SOP"):
            st.session_state.edit_sop_mode = True
            st.session_state.edit_sop_id = None
            st.rerun()
        
        # Edit SOP form
        if hasattr(st.session_state, 'edit_sop_mode') and st.session_state.edit_sop_mode:
            st.subheader("Add/Edit SOP")
            
            # Check if we're editing an existing SOP
            edit_mode = False
            sop_data = None
            
            if hasattr(st.session_state, 'edit_sop_id') and st.session_state.edit_sop_id:
                edit_mode = True
                sop_data = sops_df[sops_df['id'] == st.session_state.edit_sop_id].iloc[0]
                st.info(f"Editing SOP: {sop_data['name']}")
            
            # Form for adding/editing SOP
            with st.form("sop_form"):
                name = st.text_input("SOP Name", value=sop_data['name'] if edit_mode else "")
                
                category = st.selectbox("Category", 
                                       options=["Onboarding", "Ads Optimization", "Communication Templates", "Other"],
                                       index=["Onboarding", "Ads Optimization", "Communication Templates", "Other"].index(sop_data['category']) if edit_mode and sop_data['category'] in ["Onboarding", "Ads Optimization", "Communication Templates", "Other"] else 0)
                
                content = st.text_area("Content", 
                                      value=sop_data['content'] if edit_mode else "",
                                      height=300)
                
                last_updated = st.date_input("Last Updated", 
                                           value=datetime.strptime(sop_data['last_updated'], "%Y-%m-%d").date() if edit_mode and sop_data['last_updated'] else datetime.now())
                
                col1, col2 = st.columns(2)
                
                with col1:
                    submit_button = st.form_submit_button("Save SOP")
                
                with col2:
                    cancel_button = st.form_submit_button("Cancel")
            
            if submit_button:
                # Format date
                last_updated_str = last_updated.strftime("%Y-%m-%d")
                
                # Connect to database
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                
                if edit_mode:
                    c.execute('''
                    UPDATE sops
                    SET name = ?, category = ?, content = ?, last_updated = ?
                    WHERE id = ?
                    ''', (name, category, content, last_updated_str, st.session_state.edit_sop_id))
                    st.success(f"SOP '{name}' updated successfully!")
                else:
                    c.execute('''
                    INSERT INTO sops (name, category, content, last_updated)
                    VALUES (?, ?, ?, ?)
                    ''', (name, category, content, last_updated_str))
                    st.success(f"SOP '{name}' added successfully!")
                
                conn.commit()
                conn.close()
                
                # Clear edit mode
                st.session_state.edit_sop_mode = False
                st.session_state.edit_sop_id = None
                st.rerun()
            
            if cancel_button:
                # Clear edit mode
                st.session_state.edit_sop_mode = False
                st.session_state.edit_sop_id = None
                st.rerun()
    
    with tab2:
        st.subheader("Team Directory")
        
        # Display team members
        for _, member in team_df.iterrows():
            with st.expander(f"{member['name']} - {member['role']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Email:** {member['email']}")
                    st.markdown(f"**Phone:** {member['phone']}")
                
                with col2:
                    st.markdown(f"**Department:** {member['department']}")
                    st.markdown(f"**Skills:** {member['skills']}")
                
                # Edit button
                if st.button("Edit", key=f"edit_member_{member['id']}"):
                    st.session_state.edit_member_id = member['id']
                    st.session_state.edit_member_mode = True
                    st.rerun()
        
        # Add new team member button
        if st.button("Add New Team Member"):
            st.session_state.edit_member_mode = True
            st.session_state.edit_member_id = None
            st.rerun()
        
        # Edit team member form
        if hasattr(st.session_state, 'edit_member_mode') and st.session_state.edit_member_mode:
            st.subheader("Add/Edit Team Member")
            
            # Check if we're editing an existing team member
            edit_mode = False
            member_data = None
            
            if hasattr(st.session_state, 'edit_member_id') and st.session_state.edit_member_id:
                edit_mode = True
                member_data = team_df[team_df['id'] == st.session_state.edit_member_id].iloc[0]
                st.info(f"Editing team member: {member_data['name']}")
            
            # Form for adding/editing team member
            with st.form("member_form"):
                name = st.text_input("Name", value=member_data['name'] if edit_mode else "")
                role = st.text_input("Role", value=member_data['role'] if edit_mode else "")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    email = st.text_input("Email", value=member_data['email'] if edit_mode else "")
                    department = st.text_input("Department", value=member_data['department'] if edit_mode else "")
                
                with col2:
                    phone = st.text_input("Phone", value=member_data['phone'] if edit_mode else "")
                    skills = st.text_input("Skills", value=member_data['skills'] if edit_mode else "")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    submit_button = st.form_submit_button("Save Team Member")
                
                with col2:
                    cancel_button = st.form_submit_button("Cancel")
            
            if submit_button:
                # Connect to database
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                
                if edit_mode:
                    c.execute('''
                    UPDATE team_directory
                    SET name = ?, role = ?, email = ?, phone = ?, department = ?, skills = ?
                    WHERE id = ?
                    ''', (name, role, email, phone, department, skills, st.session_state.edit_member_id))
                    st.success(f"Team member '{name}' updated successfully!")
                else:
                    c.execute('''
                    INSERT INTO team_directory (name, role, email, phone, department, skills)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''', (name, role, email, phone, department, skills))
                    st.success(f"Team member '{name}' added successfully!")
                
                conn.commit()
                conn.close()
                
                # Clear edit mode
                st.session_state.edit_member_mode = False
                st.session_state.edit_member_id = None
                st.rerun()
            
            if cancel_button:
                # Clear edit mode
                st.session_state.edit_member_mode = False
                st.session_state.edit_member_id = None
                st.rerun()
    
    with tab3:
        st.subheader("Meeting Notes")
        
        # Filter by meeting type
        meeting_types = meetings_df['meeting_type'].unique()
        selected_type = st.selectbox("Filter by Meeting Type", options=["All"] + list(meeting_types))
        
        if selected_type == "All":
            filtered_meetings = meetings_df
        else:
            filtered_meetings = meetings_df[meetings_df['meeting_type'] == selected_type]
        
        # Sort by date (most recent first)
        filtered_meetings = filtered_meetings.sort_values('date', ascending=False)
        
        # Display meetings
        for _, meeting in filtered_meetings.iterrows():
            with st.expander(f"{meeting['title']} ({meeting['date']})"):
                st.markdown(f"**Attendees:** {meeting['attendees']}")
                st.markdown(f"**Meeting Type:** {meeting['meeting_type']}")
                
                st.markdown("**Notes:**")
                st.text_area("", value=meeting['notes'], height=150, key=f"notes_{meeting['id']}", disabled=True)
                
                st.markdown("**Action Items:**")
                st.text_area("", value=meeting['action_items'], height=100, key=f"action_{meeting['id']}", disabled=True)
                
                # Edit button
                if st.button("Edit", key=f"edit_meeting_{meeting['id']}"):
                    st.session_state.edit_meeting_id = meeting['id']
                    st.session_state.edit_meeting_mode = True
                    st.rerun()
        
        # Add new meeting button
        if st.button("Add New Meeting"):
            st.session_state.edit_meeting_mode = True
            st.session_state.edit_meeting_id = None
            st.rerun()
        
        # Edit meeting form
        if hasattr(st.session_state, 'edit_meeting_mode') and st.session_state.edit_meeting_mode:
            st.subheader("Add/Edit Meeting")
            
            # Check if we're editing an existing meeting
            edit_mode = False
            meeting_data = None
            
            if hasattr(st.session_state, 'edit_meeting_id') and st.session_state.edit_meeting_id:
                edit_mode = True
                meeting_data = meetings_df[meetings_df['id'] == st.session_state.edit_meeting_id].iloc[0]
                st.info(f"Editing meeting: {meeting_data['title']}")
            
            # Form for adding/editing meeting
            with st.form("meeting_form"):
                title = st.text_input("Meeting Title", value=meeting_data['title'] if edit_mode else "")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    date = st.date_input("Date", 
                                        value=datetime.strptime(meeting_data['date'], "%Y-%m-%d").date() if edit_mode and meeting_data['date'] else datetime.now())
                
                with col2:
                    meeting_type = st.selectbox("Meeting Type", 
                                              options=["Internal", "Client", "Other"],
                                              index=["Internal", "Client", "Other"].index(meeting_data['meeting_type']) if edit_mode and meeting_data['meeting_type'] in ["Internal", "Client", "Other"] else 0)
                
                attendees = st.text_input("Attendees", value=meeting_data['attendees'] if edit_mode else "")
                
                notes = st.text_area("Notes", 
                                    value=meeting_data['notes'] if edit_mode else "",
                                    height=200)
                
                action_items = st.text_area("Action Items", 
                                          value=meeting_data['action_items'] if edit_mode else "",
                                          height=100)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    submit_button = st.form_submit_button("Save Meeting")
                
                with col2:
                    cancel_button = st.form_submit_button("Cancel")
            
            if submit_button:
                # Format date
                date_str = date.strftime("%Y-%m-%d")
                
                # Connect to database
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                
                if edit_mode:
                    c.execute('''
                    UPDATE meeting_notes
                    SET title = ?, date = ?, attendees = ?, meeting_type = ?, notes = ?, action_items = ?
                    WHERE id = ?
                    ''', (title, date_str, attendees, meeting_type, notes, action_items, st.session_state.edit_meeting_id))
                    st.success(f"Meeting '{title}' updated successfully!")
                else:
                    c.execute('''
                    INSERT INTO meeting_notes (title, date, attendees, meeting_type, notes, action_items)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''', (title, date_str, attendees, meeting_type, notes, action_items))
                    st.success(f"Meeting '{title}' added successfully!")
                
                conn.commit()
                conn.close()
                
                # Clear edit mode
                st.session_state.edit_meeting_mode = False
                st.session_state.edit_meeting_id = None
                st.rerun()
            
            if cancel_button:
                # Clear edit mode
                st.session_state.edit_meeting_mode = False
                st.session_state.edit_meeting_id = None
                st.rerun()
    
    with tab4:
        st.subheader("Quick Links")
        
        # Filter by category
        link_categories = links_df['category'].unique()
        selected_category = st.selectbox("Filter by Category", options=["All"] + list(link_categories), key="link_category")
        
        if selected_category == "All":
            filtered_links = links_df
        else:
            filtered_links = links_df[links_df['category'] == selected_category]
        
        # Display links in a grid
        cols = st.columns(3)
        
        for i, (_, link) in enumerate(filtered_links.iterrows()):
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"**[{link['name']}]({link['url']})**")
                    st.caption(f"Category: {link['category']}")
                    st.markdown(link['description'])
                    
                    # Edit button
                    if st.button("Edit", key=f"edit_link_{link['id']}"):
                        st.session_state.edit_link_id = link['id']
                        st.session_state.edit_link_mode = True
                        st.rerun()
        
        # Add new link button
        if st.button("Add New Link"):
            st.session_state.edit_link_mode = True
            st.session_state.edit_link_id = None
            st.rerun()
        
        # Edit link form
        if hasattr(st.session_state, 'edit_link_mode') and st.session_state.edit_link_mode:
            st.subheader("Add/Edit Link")
            
            # Check if we're editing an existing link
            edit_mode = False
            link_data = None
            
            if hasattr(st.session_state, 'edit_link_id') and st.session_state.edit_link_id:
                edit_mode = True
                link_data = links_df[links_df['id'] == st.session_state.edit_link_id].iloc[0]
                st.info(f"Editing link: {link_data['name']}")
            
            # Form for adding/editing link
            with st.form("link_form"):
                name = st.text_input("Link Name", value=link_data['name'] if edit_mode else "")
                
                category = st.selectbox("Category", 
                                       options=["External Tools", "Client Resources", "Internal Resources", "Other"],
                                       index=["External Tools", "Client Resources", "Internal Resources", "Other"].index(link_data['category']) if edit_mode and link_data['category'] in ["External Tools", "Client Resources", "Internal Resources", "Other"] else 0)
                
                url = st.text_input("URL", value=link_data['url'] if edit_mode else "https://")
                
                description = st.text_area("Description", 
                                         value=link_data['description'] if edit_mode else "",
                                         height=100)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    submit_button = st.form_submit_button("Save Link")
                
                with col2:
                    cancel_button = st.form_submit_button("Cancel")
            
            if submit_button:
                # Connect to database
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                
                if edit_mode:
                    c.execute('''
                    UPDATE quick_links
                    SET name = ?, category = ?, url = ?, description = ?
                    WHERE id = ?
                    ''', (name, category, url, description, st.session_state.edit_link_id))
                    st.success(f"Link '{name}' updated successfully!")
                else:
                    c.execute('''
                    INSERT INTO quick_links (name, category, url, description)
                    VALUES (?, ?, ?, ?)
                    ''', (name, category, url, description))
                    st.success(f"Link '{name}' added successfully!")
                
                conn.commit()
                conn.close()
                
                # Clear edit mode
                st.session_state.edit_link_mode = False
                st.session_state.edit_link_id = None
                st.rerun()
            
            if cancel_button:
                # Clear edit mode
                st.session_state.edit_link_mode = False
                st.session_state.edit_link_id = None
                st.rerun()

# Main app
def main():
    # Initialize database
    init_db()
    
    # Set up sidebar
    st.sidebar.title("MasterFLO.ai")
    st.sidebar.image("https://img.icons8.com/color/96/000000/karate.png", width=100)
    st.sidebar.subheader("Martial Arts Marketing Agency")
    
    # Navigation
    page = st.sidebar.radio("Navigation", ["Dashboard", "Clients", "Team Tasks", "Campaign Tracker", "Operations Hub"])
    
    # Display selected page
    if page == "Dashboard":
        show_dashboard()
    elif page == "Clients":
        show_clients()
    elif page == "Team Tasks":
        show_tasks()
    elif page == "Campaign Tracker":
        show_campaigns()
    elif page == "Operations Hub":
        show_operations()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.caption("© 2025 MasterFLO.ai")

if __name__ == "__main__":
    main()
