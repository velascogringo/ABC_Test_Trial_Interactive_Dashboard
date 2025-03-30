import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import calendar
import datetime
from datetime import datetime
import matplotlib.pyplot as plt
import plotly.express as px

#######################################################################
# LOGIN PAGE 
# #####################################################################

# Hardcoded credentials (Replace with a database for real-world usage)
USER_CREDENTIALS = {
    "admin": "1234",
    "user1": "securepass"
}

# Function to check login
def check_login(username, password):
    return USER_CREDENTIALS.get(username) == password

# Function to handle logout
def logout():
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.session_state["section"] = "Trial Participants"  # Reset section on logout
    st.rerun()  # Redirect back to login page

# Login page (Centered)
def login():
    st.set_page_config(page_title="ABC Test Trial", layout="centered")  # Ensures login page is centered

    # Centering login form
    st.title("🔑 ABC Test Trial")
   
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if check_login(username, password):
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.success("Login successful!")
            st.rerun()  # Re-run the app to load the dashboard
        else:
            st.error("Invalid credentials. Try again.")


# Display demo credentials below the login button
    st.markdown("""
        **For demo purposes, please enter the following credentials:**  
        **Username:** `admin`  
        **Password:** `1234`
    """)


# Main function
def main():
    section = None
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        login()
    else:
        
        urls = {
            "test_subject_report": "https://raw.githubusercontent.com/velascogringo/ABC_Test_Trial_Interactive_Dashboard/main/TEST_SUBJECT_REPORT.csv",
            "query_management_report": "https://raw.githubusercontent.com/velascogringo/ABC_Test_Trial_Interactive_Dashboard/main/QUERY_MANAGEMENT_REPORT.csv",
            "crf_entry_status_report": "https://raw.githubusercontent.com/velascogringo/ABC_Test_Trial_Interactive_Dashboard/main/CRF_ENTRY_STATUS_REPORT.csv",
            "ae_sae_report": "https://raw.githubusercontent.com/velascogringo/ABC_Test_Trial_Interactive_Dashboard/main/AE_SAE_REPORT.csv",
            "data_cleaning_report": "https://raw.githubusercontent.com/velascogringo/ABC_Test_Trial_Interactive_Dashboard/main/DATA_CLEANING_STATUS.csv",
            }

        # Initialize empty DataFrames
        dataframes = {}

        for key, url in urls.items():
            try:
                df = pd.read_csv(url)
                if df.empty:
                    print(f"Warning: {key} is empty!")
                else:
                    print(f"Loaded {key} successfully. Columns: {df.columns.tolist()}")
                dataframes[key] = df
            except Exception as e:
                print(f"Error loading {key}: {e}")
                dataframes[key] = pd.DataFrame()  # Assign empty DataFrame if loading fails

        # Access loaded data
        test_subject_report = dataframes["test_subject_report"]
        query_management_report = dataframes["query_management_report"]
        crf_entry_status_report = dataframes["crf_entry_status_report"]
        ae_sae_report = dataframes["ae_sae_report"]
        data_cleaning_report = dataframes["data_cleaning_report"]


        # Dashboard Configuration
        st.set_page_config(
            page_title="ABC TEST TRIAL", 
            layout="wide",  # Dashboard layout is wide
            initial_sidebar_state="expanded"
        )

        # Dashboard Title
        col1, col2 = st.columns([9, 1])  # Title on left, logout on right
        with col1:
            st.title("ABC Test Trial")
        with col2:
            if st.button("Logout"):  # Upper right logout button
                logout()

        st.write("A phase III study to evaluate the efficacy and safety of ABC Treatment vs placebo in improving outcomes for patients with Condition X")
        st.markdown("____")

        # Sidebar for navigation
        st.sidebar.title("Navigation")
        section = st.sidebar.radio("", ["Trial Participants", "Query Management", "Safety & SAE", "Data Entry / CRF Status", "Performance Metrics"])


#######################################################################
# Trial Participants Section
#######################################################################

        if section == "Trial Participants":
            st.header("Trial Participants Overview")
            st.markdown("____")
            
            # Calculate KPIs
            total_enrollment = len(test_subject_report)
            total_sites = test_subject_report['Site_Number'].nunique()
            
            st.markdown(
            f"""
            <style>
                .total-enrollment-container {{
                    display: flex;
                    justify-content: space-around;
                    align-items: center;
                    text-align: center;
                    margin-top: 20px;
                }}
                .metric {{
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                }}
                .circle {{
                    width: 140px;
                    height: 140px;
                    background-color: white;
                    color: red;
                    border-radius: 70%;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    font-size: 60px;
                    font-weight: bold;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
                    margin-top: 10px;
                }}
                .title {{
                    font-size: 20px;
                    font-weight: bold;
                    color: white;
                    margin-top: 10px;
                }}
            </style>
            <div class="total-enrollment-container">
                <div class="metric">
                    <div class="title">SUBJECTS ENROLLED</div>
                    <div class="circle">{total_enrollment}</div>
                </div>
                <div class="metric">
                    <div class="title">PARTICIPATING SITES</div>
                    <div class="circle">{total_sites}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
            )
            
################## Enrollment Rate Over Time ##################

            test_subject_report['Enrollment_Date'] = pd.to_datetime(test_subject_report['Enrollment_Date'])
            enrollment_rate = test_subject_report.groupby(test_subject_report['Enrollment_Date'].dt.to_period("M")).size()
            enrollment_rate.index = enrollment_rate.index.astype(str)
            formatted_dates = enrollment_rate.index.to_series().apply(lambda x: pd.to_datetime(x).strftime('%b %Y'))

            trace_enrollment = go.Scatter(
                x=formatted_dates,
                y=enrollment_rate.values,
                mode='lines+markers',
                name='Enrollment Rate',
                marker=dict(size=8),
                line=dict(color='gray')
            )

            layout = go.Layout(
                title='Enrollment Rate Over Time',
                title_font=dict(size=20),
                xaxis=dict(tickvals=formatted_dates, ticktext=formatted_dates, tickangle=-45, tickfont=dict(size=16)),
                yaxis=dict(title='Number of Enrollments', title_font=dict(size=18), tickfont=dict(size=16)),
                autosize=True,
                width=2000,
                height=600,
            )

            fig = go.Figure(data=[trace_enrollment], layout=layout)
            st.plotly_chart(fig)

            # Use columns to push the download button to the right
            col1, col2, col3 = st.columns([0.6, 0.2, 0.2])  # Adjust column width to move button

            with col3:# Download button for Enrollment Rate Data
                csv_data_enrollment_rate = enrollment_rate.reset_index().to_csv(index=False).encode('utf-8')
                st.download_button("Download Enrollment Rate Over Time Data", data=csv_data_enrollment_rate, file_name="enrollment_rate.csv", mime="text/csv")

################## Subjects per Site ##################
       
            site_counts = test_subject_report['Institution'].value_counts().reset_index()
            site_counts.columns = ['Institution', 'Count']


            # Create a bar chart using Plotly
            site_fig = px.bar(
                site_counts, 
                x='Institution', 
                y='Count', 
                title='Subjects Per Site',
                color='Institution',
                text_auto=True  # Show values on bars
            )

            # Set a single bar color (royalblue)
            site_fig.update_traces(marker_color='royalblue')

            # Adjust layout for better visibility
            site_fig.update_layout(
                width=900,   # Set width
                height=550,  # Set height
                xaxis_title="",
                yaxis_title="Count",
                title_font=dict(size=20),
                xaxis_tickangle=-45,  # Rotate x-axis labels for readability
                showlegend=False
            )

            # Display the chart
            st.plotly_chart(site_fig)

            # Create columns to structure layout
            col1, col2, col3 = st.columns([0.6, 0.2, 0.2])  # Adjusting width to push the button to the right

            with col3:
                # Download button for Subjects Per Site Data
                csv_data_site_counts = site_counts.to_csv(index=False).encode('utf-8')
                st.download_button("Download Subjects Per Site Data", data=csv_data_site_counts, file_name="subjects_per_site.csv", mime="text/csv")
           
                
################## Gender Distribution ##################

            gender_counts = test_subject_report['Gender'].value_counts().reset_index()
            gender_counts.columns = ['Gender', 'Count']

            race_counts = test_subject_report['Race'].value_counts().reset_index()
            race_counts.columns = ['Race', 'Count']

            # Prepare CSV for download
            csv_data_gender = gender_counts.to_csv(index=False).encode('utf-8')
            csv_data_race = race_counts.to_csv(index=False).encode('utf-8')


            # Display in two columns
            col1, col2 = st.columns(2)

            # Gender Distribution (Bar Chart)
            with col1:
                gender_fig = px.bar(
                    gender_counts, 
                    x='Gender', 
                    y='Count', 
                    title='Gender Distribution',
                    color='Gender',
                    color_discrete_map={'Male': 'blue', 'Female': 'pink'},
                    hover_data={'Gender': True, 'Count': True}
                )
                gender_fig.update_layout(
                    title_font_size=20, height=500, showlegend=False
                )
                st.plotly_chart(gender_fig, use_container_width=True)

                # Add spacing before download button
                space1, space2, col_download = st.columns([0.5, 0.2, 0.3])
                with col_download:
                    st.download_button("Download Gender Data", data=csv_data_gender, file_name="gender_distribution.csv", mime="text/csv")



################## Race Distribution ##################

            with col2:
                race_fig = px.bar(
                    race_counts, 
                    x='Race', 
                    y='Count', 
                    title='Race Distribution',
                    color='Race',
                    color_discrete_map={'White': 'blue', 'Black or African American': 'green', 'Asian': 'red'},
                    hover_data={'Race': True, 'Count': True}
                )
                race_fig.update_layout(
                    title_font_size=20, height=500, showlegend=False
                )
                st.plotly_chart(race_fig, use_container_width=True)

                space1, space2, col_download = st.columns([0.5, 0.2, 0.3])
                with col_download:
                    st.download_button("Download Race Data", data=csv_data_race, file_name="race_distribution.csv", mime="text/csv")

                st.write("")  # Blank line for spacing

################## Subject Status Distribution & Subject per Region ##################

            col1, col2 = st.columns(2)

            # Prepare data for Subject Status and Region counts
            status_counts = test_subject_report['Subject_Current_Status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']

            region_counts = test_subject_report['Region'].value_counts().reset_index()
            region_counts.columns = ['Region', 'Count']

            # Prepare CSV for download
            csv_data_status = status_counts.to_csv(index=False).encode('utf-8')
            csv_data_region = region_counts.to_csv(index=False).encode('utf-8')

            # Subject Status Distribution (Bar Chart)
            with col1:
                bar_chart = go.Figure(data=[go.Bar(
                    x=status_counts['Status'], 
                    y=status_counts['Count'], 
                    marker=dict(color='royalblue')
                )])

                bar_chart.update_layout(
                    title="Subject Status Distribution",
                    title_font_size=20,
                    showlegend=False,
                    height=500
                )
                
                st.plotly_chart(bar_chart, use_container_width=True)
                space1, space2, col_download = st.columns([0.5, 0.2, 0.3])
                with col_download:
                    st.download_button("Download Subject Status Data", data=csv_data_status, file_name="subject_status_distribution.csv", mime="text/csv")

            # Subjects Per Region (Pie Chart)
            with col2:
                pie_chart = go.Figure(data=[go.Pie(
                    labels=region_counts['Region'], 
                    values=region_counts['Count'], 
                    hole=0.3,
                    marker=dict(colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']),
                    textinfo='label+value+percent',
                    texttemplate='%{label}<br>%{value} (%{percent})',
                    insidetextorientation='horizontal'
                )])

                pie_chart.update_layout(
                    title="Subjects Per Region",
                    height=500,
                    title_font_size=20,
                    margin=dict(t=50, b=50, l=50, r=50),
                    legend_font_size=14
                )

                st.plotly_chart(pie_chart, use_container_width=True)
                space1, space2, col_download = st.columns([0.5, 0.2, 0.3])
                with col_download:
                    st.download_button("Download Region Data", data=csv_data_region, file_name="subjects_per_region.csv", mime="text/csv")


##############################################################################
    # Query Management Section
##############################################################################

    if section == "Query Management":
        st.header("Query Management")
        st.markdown("____")
        
    # Ensure date columns are in datetime format and handle any conversion errors
        query_management_report['Open Date'] = pd.to_datetime(query_management_report['Open Date'], errors='coerce')
        query_management_report['Response Date'] = pd.to_datetime(query_management_report['Response Date'], errors='coerce')
        query_management_report['Query Closed Date'] = pd.to_datetime(query_management_report['Query Closed Date'], errors='coerce')

# --- EXTRA FILTERS FOR SITE AND SUBJECT ---
        col1, col2 = st.columns(2)
        
        with col1:
            selected_subject = st.selectbox(
                "Select Subject",
                options=["All"] + sorted(query_management_report["SubjectName"].dropna().unique().tolist()),
                index=0
            )
            
        with col2:
            selected_site = st.selectbox(
                "Select Site",
                options=["All"] + sorted(query_management_report["Site Number"].dropna().unique().tolist()),
                index=0
            )

        # Apply filters based on selections
        filtered_data_query = query_management_report.copy()

            # Apply site filter if a site is selected
        if selected_site != "All":
            filtered_data_query = filtered_data_query[filtered_data_query["Site Number"] == selected_site]

        # Apply subject filter if a subject is selected
        if selected_subject != "All":
            subject_site_prefix = str(selected_subject)[:3]  # Extract the first 3 digits

            # Only enforce the check if both site and subject are selected
            if selected_site != "All" and subject_site_prefix != str(selected_site):
                st.error("PLEASE SELECT A VALID FILTER")  # Show error only on mismatch
                st.stop()
            
            # Apply the subject filter if no mismatch
            filtered_data_query = filtered_data_query[filtered_data_query["SubjectName"] == selected_subject]


 ################## Query Management KPIs ##################       
         
    # Check if Open Date column contains any non-null dates
        filtered_data_query['Open Date'].notna().any()
        # Calculating KPI values
        total_queries_issued = len(filtered_data_query)  # Total queries

        # Format the total queries issued with commas
        total_queries_issued_formatted = f"{total_queries_issued:,}"

        # Calculate average queries per day
        date_range = (filtered_data_query['Open Date'].max() - filtered_data_query['Open Date'].min()).days
        ave_queries_per_day = total_queries_issued / date_range if date_range > 0 else 0

        # Calculate average site response time
        filtered_data_query['Response Time'] = (filtered_data_query['Response Date'] - filtered_data_query['Open Date']).dt.days
        ave_site_response_time = filtered_data_query['Response Time'].mean()

        # Calculate average query closing time
        filtered_data_query['Closing Time'] = (filtered_data_query['Query Closed Date'] - filtered_data_query['Open Date']).dt.days
        ave_query_closing_time = filtered_data_query['Closing Time'].mean()

            # Display KPIs in Streamlit
        st.markdown(f"""
            <style>
                .kpi-container {{
                    display: flex;
                    justify-content: space-around;
                    text-align: center;
                    color: white;
                    margin-bottom: 30px;  
                    margin-top: 20px;
                }}
                .kpi-box {{
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    width: 140px;
                    height: 140px;
                    background-color: white;
                    color: red;
                    border-radius: 50%;  /* Makes it a circle */
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);  /* Slight shadow */
                    font-size: 35px;
                    font-weight: bold;
                }}
                .kpi-title {{
                    font-size: 16px;
                    color: #B0C4DE;
                    margin-top: 10px;
                }}
            </style>
            <div class="kpi-container">
                <div>
                    <div class="kpi-box">{total_queries_issued_formatted}</div>
                    <div class="kpi-title">TOTAL QUERIES ISSUED</div>
                </div>
                <div>
                    <div class="kpi-box">{ave_queries_per_day:.2f}</div>
                    <div class="kpi-title">AVE QUERIES PER DAY</div>
                </div>
                <div>
                    <div class="kpi-box">{ave_site_response_time:.2f}</div>
                    <div class="kpi-title">AVE SITE RESPONSE TIME (IN DAY/S)</div>
                </div>
                <div>
                    <div class="kpi-box">{ave_query_closing_time:.2f}</div>
                    <div class="kpi-title">AVE QUERY CLOSING TIME (IN DAY/S)</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.write("")  # Blank line for spacing

################## Query Status Distribution ##################
            
        query_status_counts = filtered_data_query['Query Status'].value_counts().reset_index()
        query_status_counts.columns = ['Query Status', 'Count']  # Rename columns properly

        query_status_fig = px.pie(
            names=query_status_counts['Query Status'],  # Use the status values as labels
            values=query_status_counts['Count'],  # Use the count as values
            title='Query Status Distribution',
            color_discrete_sequence=px.colors.qualitative.Set2,
            labels={'names': 'Query Status', 'values': 'Count'},
            hole=0.3  # Optional: Create a donut chart with a hole in the center
        )

        query_status_fig.update_traces(
            textinfo='value',  # Display value inside the pie
            pull=[0.1] * len(query_status_counts),  # Optional: Pull out slices for emphasis
            hovertemplate="<b>Query Status:</b> %{label}<br><b>Count:</b> %{value}<extra></extra>",  # Custom hover template
            rotation=90,
        )

        query_status_fig.update_layout(
            title_font_size=20,
            width=500,  # Updated size
            height=500,  # Updated size
            margin=dict(t=50, b=50, l=50, r=50),
            showlegend=True
        )

################## Query Distribution per Group ##################

        group_name_counts = filtered_data_query['Group Name'].value_counts().reset_index()
        group_name_counts.columns = ['Group Name', 'Count']  # Rename columns properly
        group_name_counts = group_name_counts.sort_values(by='Count', ascending=True)  # Sort values

        group_name_fig = px.bar(
            y=group_name_counts['Group Name'],  # Use sorted values for y-axis
            x=group_name_counts['Count'],
            title='Query Distribution per Group',
            color_discrete_sequence=['royalblue'],  # Set a single color
            labels={'y': 'Group Name', 'x': 'Count'},
            text=group_name_counts['Count']  # Add count values to bars
        )

        group_name_fig.update_traces(
            textposition='inside',  # Place text inside the bar
            textfont_size=14,  # Increase text size
            marker_line_width=1.5,  # Add border around bars for clarity
            hovertemplate="<b>Group Name:</b> %{y}<br><b>Count:</b> %{x}<extra></extra>"  # Custom hover template
        )

        group_name_fig.update_layout(
            title_font_size=20,
            xaxis_title="Number of Queries",
            yaxis_title="",
            width=500,  # Updated size
            height=500,  # Updated size
            margin=dict(t=50, b=50, l=50, r=50),
            showlegend=False
        )

        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(query_status_fig, use_container_width=True)

            # Download button for Query Status Data
            csv_data_query_status = query_status_counts.to_csv(index=False).encode('utf-8')
            space1, space2, col_download = st.columns([0.5, 0.2, 0.3])
            with col_download:
                    st.download_button("Download Query Status Data", data=csv_data_query_status, file_name="query_status_distribution.csv", mime="text/csv")
        

        with col2:
            st.plotly_chart(group_name_fig, use_container_width=True)

            # Download button for Group Name Distribution Data
            csv_data_group_name = group_name_counts.to_csv(index=False).encode('utf-8')
            

            space1, space2, col_download = st.columns([0.5, 0.2, 0.3])
            with col_download:
                st.download_button("Download Query Group Data", data=csv_data_group_name, file_name="query_group_distribution.csv", mime="text/csv")

        st.write("")  # Blank line for spacing
    
################## Top Sites with Open Queries ##################

        open_queries = filtered_data_query[filtered_data_query['Query Status'] == 'Open']
        top_sites_open_queries = (
            open_queries.groupby('Site Name')
            .size()
            .sort_values(ascending=False)
            .head(10)  # Top 10 sites
        )
        top_sites_open_queries_fig = px.bar(
            x=top_sites_open_queries.index,
            y=top_sites_open_queries.values,
            title='Top Sites with Most Number of Open Queries',
            labels={'x': '', 'y': 'Number of Open Queries'},
            color=top_sites_open_queries.index,
            color_discrete_sequence=px.colors.qualitative.Set3,
            text=top_sites_open_queries.values
        )
        top_sites_open_queries_fig.update_traces(
            textposition='outside',
            textfont_size=15,
            marker_line_width=1.5,
            hovertemplate="<b>Site:</b> %{x}<br><b>Open Queries:</b> %{y}<extra></extra>"  # Custom hover template
        )
        top_sites_open_queries_fig.update_layout(
            title_font_size=20,
            xaxis=dict(tickangle=45, tickfont_size=12),  # Rotate x-axis labels for better visibility
            yaxis=dict(showgrid=False),
            height=500,
            margin=dict(t=80, b=100, l=40, r=40),
            showlegend=False
        )

################## Top Sites with Aging Queries (Bubble + Line Chart) ##################
                
        filtered_data_query['Query Age'] = (
            (datetime.now() - filtered_data_query['Open Date']).dt.days
        )
        aging_queries = filtered_data_query[
            filtered_data_query['Query Status'] == 'Open'
        ].groupby('Site Name')['Query Age'].mean().sort_values(ascending=False).head(10)

        # Bubble size based on the number of open queries for each site
        open_queries = filtered_data_query[filtered_data_query['Query Status'] == 'Open']
        site_query_counts = open_queries.groupby('Site Name').size().loc[aging_queries.index]

        # Create a combined Line and Bubble Chart
        combined_fig = px.scatter(
            x=aging_queries.index,
            y=aging_queries.values,
            size=site_query_counts.values,  # Size of the bubble based on the number of open queries
            title='Top Sites with Aging Queries',
            labels={'x': '', 'y': 'Average Query Age (Days)'},
            color=aging_queries.index,
            color_discrete_sequence=px.colors.qualitative.Set3,
            text=aging_queries.values.astype(int)  # Display the average age as text on the bubbles
            
        )

        # Add the line connecting the points
        combined_fig.add_trace(
            go.Scatter(
                x=aging_queries.index,
                y=aging_queries.values,
                mode='lines',
                line=dict(color='white', dash='solid'),
                name='Average Aging Query'
            )
        )

        combined_fig.update_traces(
            textposition='top center',
            hovertemplate="<b>Site:</b> %{x}<br><b>Ave Aging Query:</b> %{y} Days<br><b>Open Queries:</b> %{marker.size}<extra></extra>",
        )

        combined_fig.update_layout(
            title_font_size=20,
            xaxis=dict(tickangle=45, tickfont_size=12),  # Rotate x-axis labels for better visibility
            yaxis=dict(showgrid=False, tickformat=',d'),  # Ensure y-axis shows whole numbers with "Days"
            height=500,
            margin=dict(t=80, b=100, l=40, r=40),
            showlegend=False
        )


        # Display charts side by side
        col1, col2 = st.columns(2)
        with col1:
            with st.container():
                st.plotly_chart(top_sites_open_queries_fig, use_container_width=True)
                
                # Download button for Open Queries Data
                csv_data_open_queries = top_sites_open_queries.reset_index().to_csv(index=False).encode('utf-8')
                
                space1, space2, col_download = st.columns([0.5, 0.2, 0.3])
                with col_download:
                    st.download_button("Download Open Queries Data", data=csv_data_open_queries, file_name="open_queries_distribution.csv", mime="text/csv")

        with col2:
            with st.container():
                st.plotly_chart(combined_fig, use_container_width=True)
                
                # Download button for Aging Queries Data
                csv_data_aging_queries = aging_queries.reset_index().to_csv(index=False).encode('utf-8')
                
                space1, space2, col_download = st.columns([0.5, 0.2, 0.3])
                with col_download:
                        st.download_button("Download Aging Queries Data", data=csv_data_aging_queries, file_name="aging_queries_distribution.csv", mime="text/csv")
    
        # Add spacing before download button
        st.write("")  # Blank line for spacing
        

################## Top 5 Sites with Fastest Average Response Time & Top 5 Queries ##################
     
        # Calculate response time for each query
        filtered_data_query['Response Time (Days)'] = (
            (filtered_data_query['Response Date'] - filtered_data_query['Open Date']).dt.days
        )

        # Filter out queries where Response Time is negative (invalid data)
        response_time_data = filtered_data_query[filtered_data_query['Response Time (Days)'] >= 0]

        # Aggregate response time by site and sort to get top 5 sites with the fastest response time (ascending order)
        top_sites_response_time = response_time_data.groupby('Site Name')['Response Time (Days)'].mean().sort_values(ascending=True).head(5)

        # Create a bar chart for top 5 sites with the fastest response time
        top_sites_response_time_fig = px.bar(
            x=top_sites_response_time.index,
            y=top_sites_response_time.values,
            title='Top 5 Sites with Fastest Average Response Time',
            labels={'x': '', 'y': 'Average Response Time (Days)'},
            color=top_sites_response_time.index,
            color_discrete_sequence=px.colors.qualitative.Set2,
            text=top_sites_response_time.values.round(0).astype(int),  # Display the response time as text on the bars
        )

        top_sites_response_time_fig.update_traces(
            textposition='outside',
            textfont_size=14,
            marker_line_width=1.5,  # Add border around bars for clarity
            hovertemplate="<b>Site:</b> %{x}<br><b>Avg Response Time:</b> %{y} Days<extra></extra>"   # Custom hover template
        )

        top_sites_response_time_fig.update_layout(
            title_font_size=20,
            xaxis=dict(tickangle=45, tickfont_size=12),  # Rotate x-axis labels for better visibility
            yaxis=dict(showgrid=False, tickformat=',d'),  # Ensure y-axis shows whole numbers with "Days"
            height=500,
            margin=dict(t=80, b=100, l=40, r=40),
            showlegend=False
        )

      
        # Count the number of occurrences of each query (assuming we're interested in the frequency of each query)
        top_queries = filtered_data_query['Query Text'].value_counts().head(5)

        top_queries_fig = px.bar(
            y=top_queries.index,  # Query Text (Top 5 most frequent queries)
            x=top_queries.values,  # Frequency of each query
            title='Top 5 Queries',
            labels={'y': 'Query Text', 'x': 'Frequency'},
            color=top_queries.index,  # Color by query text to differentiate them
            color_discrete_sequence=px.colors.qualitative.Plotly,  # Custom color scheme
            text=top_queries.values.astype(int),  # Display frequency on bars
        )

        top_queries_fig.update_traces(
            textposition='inside',  # Position text inside the bar
            textfont_size=14,  # Adjust text font size for the query text
            marker_line_width=1.5,  # Add border around bars for clarity
            hovertemplate="<b>Query:</b> %{y}<br><b>Frequency:</b> %{x}<extra></extra>"  # Custom hover template
        )

        top_queries_fig.update_layout(
            title_font_size=20,
            xaxis=dict(showgrid=False, tickformat=',d', visible=False),  # Remove x-axis label and grid
            yaxis=dict(tickfont_size=12, categoryorder='total ascending'),  # Sort from highest to lowest
            height=500,
            margin=dict(t=80, b=100, l=40, r=40),  # Adjust margins for better padding
            showlegend=False,
            bargap=0.05,  # Decrease this value to make the bars wider (default is 0.15)
            bargroupgap=0.1 
        )

        # Display both charts side by side in columns
        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(top_sites_response_time_fig, use_container_width=True)

            # Download button for Top Sites Response Time Data
            csv_data_top_sites = top_sites_response_time.reset_index().to_csv(index=False).encode('utf-8')
            
            space1, space2, col_download = st.columns([0.5, 0.2, 0.3])
            with col_download:
                    st.download_button("Download Top Sites Response Time", data=csv_data_top_sites, file_name="top_5_sites_response_time.csv", mime="text/csv")

        with col2:
            st.plotly_chart(top_queries_fig, use_container_width=True)

            # Download button for Top Queries Data
            csv_data_top_queries = top_queries.reset_index().to_csv(index=False).encode('utf-8')
            space1, space2, col_download = st.columns([0.5, 0.2, 0.3])
            with col_download:
                    st.download_button("Download Top 5 Queries", data=csv_data_top_queries, file_name="top_5_queries.csv", mime="text/csv")
            
######################################################################
# Safety & Serious Adverse Events Section
######################################################################

    # Safety and SAE Section
    elif section == "Safety & SAE":
        st.header("Safety & Serious Adverse Events")
        st.markdown("____")

        # --- EXTRA FILTERS FOR SITE AND SUBJECT ---
        col1, col2 = st.columns(2)
        
        with col1:
            selected_subject = st.selectbox(
                "Select Subject",
                options=["All"] + sorted(ae_sae_report["SubjectName"].dropna().unique().tolist()),
                index=0
            )

        with col2:
            selected_site = st.selectbox(
                "Select Site",
                options=["All"] + sorted(ae_sae_report["Site Number"].dropna().unique().tolist()),
                index=0
            )

################## Safety and SAE KPIs ##################  

        # Apply filters based on selections
        filtered_data_sae = ae_sae_report.copy()

        # Apply site filter if a site is selected
        if selected_site != "All":
            filtered_data_sae = filtered_data_sae[filtered_data_sae["Site Number"] == selected_site]

        # Apply subject filter if a subject is selected
        if selected_subject != "All":
            subject_site_prefix = str(selected_subject)[:3]  # Extract the first 3 digits

            # Only enforce the check if both site and subject are selected
            if selected_site != "All" and subject_site_prefix != str(selected_site):
                st.error("PLEASE SELECT A VALID FILTER")  # Show error only on mismatch
                st.stop()
            
            # Apply the subject filter if no mismatch
            filtered_data_sae = filtered_data_sae[filtered_data_sae["SubjectName"] == selected_subject]

        # Filter for rows where Seriousness is "YES" (i.e., SAEs)
        saes_data = filtered_data_sae[filtered_data_sae['SERIOUSNESS'].str.upper() == "YES"]

        # KPI Calculations
        total_saes_recorded = len(saes_data)  # Total number of SAEs
        total_saes_reconciled = len(saes_data[saes_data['RECONCILED WITH SAFETY'].str.upper() == "YES"])  # Total reconciled SAEs
        total_open_issues = len(saes_data[saes_data['RECONCILED WITH SAFETY'].str.upper() == "NO"])  # Total open issues

        # Display KPIs in the same circle format
        st.markdown(f"""
            <style>
                .kpi-container {{
                    display: flex;
                    justify-content: space-around;
                    text-align: center;
                    color: white;
                    margin-bottom: 30px;  
                    margin-top: 20px
                }}
                .kpi-box {{
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    width: 140px;
                    height: 140px;
                    background-color: white;
                    color: red;
                    border-radius: 50%;  /* Makes it a circle */
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);  /* Slight shadow */
                    font-size: 40px;
                    font-weight: bold;
                }}
                .kpi-title {{
                    font-size: 16px;
                    color: #B0C4DE;
                    margin-top: 10px;
                }}
            </style>
            <div class="kpi-container">
                <div>
                    <div class="kpi-box">{total_saes_recorded}</div>
                    <div class="kpi-title">TOTAL # OF SAEs RECORDED</div>
                </div>
                <div>
                    <div class="kpi-box">{total_saes_reconciled}</div>
                    <div class="kpi-title">TOTAL # OF RECONCILED SAEs</div>
                </div>
                <div>
                    <div class="kpi-box">{total_open_issues}</div>
                    <div class="kpi-title">TOTAL # OPEN ISSUES</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        
################## Top 10 SAEs ##################

    # Count the occurrences of each SAE term and get the top 10
        top_saes = saes_data[saes_data['SERIOUSNESS'] == 'Yes']['AETERM'].value_counts().head(10)

        # Convert to a DataFrame for compatibility with Plotly
        top_saes_df = top_saes.reset_index()
        top_saes_df.columns = ['SAE Term', 'Frequency']

        # Create a horizontal bar chart
        top_saes_fig = px.bar(
            top_saes_df,
            y='SAE Term',  # SAE terms as y-axis for horizontal orientation
            x='Frequency',  # Frequency as x-axis
            title="Top 10 Recorded SAEs",
            text='Frequency',  # Display frequency count outside the bars
            color='SAE Term',
            color_discrete_sequence=px.colors.qualitative.Plotly,
        )

            # Update trace to display text positions
        top_saes_fig.update_traces(
            textposition='inside',  # Display the SAE term inside the bar
            insidetextanchor='start',  # Align text to the start of the bar
            textfont=dict(size=12, color='white')  # Ensure SAE term inside the bar is visible
        )

        # Add frequency labels outside the bars
        top_saes_fig.update_traces(
            textposition='outside',  # Display frequency count outside the bar
            texttemplate='%{text}',  # Show the frequency number as text
        )

        # Update layout for improved appearance
        top_saes_fig.update_layout(
            xaxis=dict(title="Total Event Recorded", showgrid=False),  # Set meaningful x-axis title
            yaxis=dict(title="SAE Term", categoryorder='total ascending'),  # Set meaningful y-axis title
            showlegend=False,
            height=500,
            title_font_size=20,
            margin=dict(t=100, b=80, l=100, r=20)  # Adjust margins for clarity
        )

 ################## Site Distribution SAE ##################

        # Filter SAE data for Seriousness = 'YES'
        serious_saes = saes_data[saes_data['SERIOUSNESS'] == 'Yes']

        # Count the occurrences of SAEs per site
        site_distribution = serious_saes['Site'].value_counts().reset_index()
        site_distribution.columns = ['Site', 'Count']

        # Create a bar chart for site distribution
        site_distribution_fig = px.bar(
            site_distribution,
            y='Count',  # Site names on the y-axis (for a horizontal bar chart)
            x='Site',  # SAE counts on the x-axis
            title="Site Distribution of SAE Recording",
            text='Count',  # Show counts on the bars
            color='Site',
            color_discrete_sequence=px.colors.qualitative.Set2,
        )

        # Update trace to display text positions
        site_distribution_fig.update_traces(
            textposition='outside',  # Place text (count) outside the bar
        )

        # Update layout for better visuals
        site_distribution_fig.update_layout(
            xaxis=dict(title="", showgrid=False, tickangle=-45),  # Label x-axis as Count
            yaxis=dict(title="Frequency", categoryorder='total ascending'),  # Order sites by total ascending
            showlegend=False,
            height=500,
            title_font_size=20,
            margin=dict(t=100, b=80, l=100, r=20),  # Adjust margins
        )

        # Display both charts side by side in columns
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(top_saes_fig, use_container_width=True)
                # Download button for Top SAEs Data
            csv_data_top_saes = top_saes_df.to_csv(index=False).encode('utf-8')
                   
            space1, space2, col_download = st.columns([0.5, 0.2, 0.3])
            with col_download:
                    st.download_button("Download Top SAEs Data",data=csv_data_top_saes,file_name="top_saes_data.csv", mime="text/csv")    
        
        with col2:
            st.plotly_chart(site_distribution_fig, use_container_width=True)
        # Download button for Site Distribution Data
            csv_data_site_distribution = site_distribution.to_csv(index=False).encode('utf-8')
            
            space1, space2, col_download = st.columns([0.5, 0.2, 0.3])
            with col_download:
                    st.download_button("Download SAE Site Distribution",data=csv_data_site_distribution,file_name="sae_site_distribution.csv",mime="text/csv")
             
        st.write("")  # Blank line for spacing
  

 ################## Fatal SAEs ##################

            # Filter for fatal SAEs
        fatal_saes = serious_saes[serious_saes['OUTCOME'] == 'FATAL']

        # Count occurrences
        fatal_saes_count = fatal_saes['Site'].value_counts()

        # Calculate the total number of Fatal SAEs
        total_fatal_saes = fatal_saes_count.sum()

        # Create a donut chart
        fatal_saes_fig = px.pie(
            names=fatal_saes_count.index,
            values=fatal_saes_count.values,
            title="Fatal SAEs Recorded",
            hole=0.4,  # Creates the donut effect
            labels={'names': 'Site', 'values': 'Number of Fatal SAEs'},
            color_discrete_sequence=px.colors.qualitative.Vivid,
        )

        # Update traces to display site and count only
        fatal_saes_fig.update_traces(
            textinfo='label+value',  # Show site and actual count
            textposition='outside'   # Position text outside the donut chart
        )

        # Update layout to replace the legend with the total count
        fatal_saes_fig.update_layout(
            height = 500,
            showlegend=False,  # Hide the default legend
            title={
                'text': f"Fatal SAEs Recorded<br>Total: {total_fatal_saes}",  # Display total in the title
                'x': 0,  # Center-align title
                'y': 0.95,
                'xanchor': 'left',
                'yanchor': 'top',
                'font': {'size': 20},
            },
            margin=dict(t=80, b=80, l=100, r=100),  # Adjust margins
        )

 ##################  SAE Outcome Distribution ##################

        # Count the occurrences of each SAE outcome
        top_outcomes = saes_data[saes_data['SERIOUSNESS'] == 'Yes']['OUTCOME'].value_counts()

        # Convert to a DataFrame for compatibility with Plotly
        top_outcomes_df = top_outcomes.reset_index()
        top_outcomes_df.columns = ['SAE Outcome', 'Frequency']

        # Create a horizontal bar chart
        top_outcomes_fig = px.bar(
            top_outcomes_df,
            y='SAE Outcome',  # SAE outcomes as y-axis for horizontal orientation
            x='Frequency',  # Frequency as x-axis
            title="SAE Outcome Distribution",
            height=500,
            text='Frequency',  # Display frequency count outside the bars
            color='SAE Outcome',
            color_discrete_sequence=px.colors.qualitative.Plotly,
        )

        # Update traces to display text positions
        top_outcomes_fig.update_traces(
            textposition='inside',  # Display the SAE outcome inside the bar
            insidetextanchor='start',  # Align text to the start of the bar
            textfont=dict(size=12, color='white')  # Ensure SAE outcome inside the bar is visible
        )

        # Add frequency labels outside the bars
        top_outcomes_fig.update_traces(
            textposition='outside',  # Display frequency count outside the bar
            texttemplate='%{text}',  # Show the frequency number as text
        )

        # Update layout for improved appearance
        top_outcomes_fig.update_layout(
            xaxis=dict(title="Total Events Recorded", showgrid=False),  # Set meaningful x-axis title
            yaxis=dict(title="", categoryorder='total ascending'),  # Set meaningful y-axis title
            showlegend=False,
            height=500,
            title_font=dict(size=20),  # Increase title font size
            title_x=0,  
            margin=dict(t=80, b=80, l=100, r=20)  # Adjust margins to accommodate the title
        )


    # Display both charts side by side in columns
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fatal_saes_fig, use_container_width=True)

                # Prepare Fatal SAEs data for download
            csv_data_fatal_saes = fatal_saes[['Site', 'AETERM', 'OUTCOME']].to_csv(index=False).encode('utf-8')
            
            space1, space2, col_download = st.columns([0.5, 0.2, 0.3])
            with col_download:
                st.download_button("Download Fatal SAEs Data",data=csv_data_fatal_saes,file_name="fatal_saes_data.csv",mime="text/csv")
        
        with col2:
            st.plotly_chart(top_outcomes_fig, use_container_width=True)
            # Prepare SAE Outcome Distribution data for download
            csv_data_outcomes = top_outcomes_df.to_csv(index=False).encode('utf-8')
            
            space1, space2, col_download = st.columns([0.5, 0.2, 0.3])
            with col_download:
                    st.download_button("Download SAE Outcome Data", data=csv_data_outcomes,file_name="sae_outcome_distribution.csv",mime="text/csv")          


############################################################################
#Data Entry / CRF Status Section
############################################################################
    elif section == "Data Entry / CRF Status":
        st.header("Data Entry / CRF Status")
        st.markdown("____")
                
               # --- EXTRA FILTERS FOR SITE AND SUBJECT ---
        col1, col2 = st.columns(2)

        with col1:
            selected_subject = st.selectbox(
                "Select Subject",
                options=["All"] + sorted(crf_entry_status_report["SubjectName"].dropna().unique().tolist()),
                index=0
            )

        with col2:
            selected_site = st.selectbox(
                "Select Site",
                options=["All"] + sorted(crf_entry_status_report["Site Number"].dropna().unique().tolist()),
                index=0
            )

        # Apply filters based on selections
        filtered_data_crf = crf_entry_status_report.copy()

        # Apply site filter if a site is selected
        if selected_site != "All":
            filtered_data_crf = filtered_data_crf[filtered_data_crf["Site Number"] == selected_site]

        # Apply subject filter if a subject is selected
        if selected_subject != "All":
            subject_site_prefix = str(selected_subject)[:3]  # Extract the first 3 digits

            # Only enforce the check if both site and subject are selected
            if selected_site != "All" and subject_site_prefix != str(selected_site):
                st.error("PLEASE SELECT A VALID FILTER")  # Show error only on mismatch
                st.stop()
            else:
                filtered_data_crf = filtered_data_crf[filtered_data_crf["SubjectName"] == selected_subject]


################## Data Entry / CRF Status KPIs ##################  

        # KPI Calculations based on the new column structure
        total_crf_expected = filtered_data_crf['Form_Expected'].sum()  # Ensure this is correct column for Expected CRF
        total_crf_completed = filtered_data_crf['Form_Entered'].sum()  # Ensure this is correct column for Entered CRF
        total_crf_incomplete = filtered_data_crf['Missing'].sum()  # Ensure this is correct column for Missing CRFs

        # Format the KPIs with comma separators
        total_crf_expected_formatted = f"{total_crf_expected:,.0f}"
        total_crf_completed_formatted = f"{total_crf_completed:,.0f}"
        total_crf_incomplete_formatted = f"{total_crf_incomplete:,.0f}"

        # Display KPIs in circular format
        st.markdown(f"""
            <style>
                .kpi-container {{
                    display: flex;
                    justify-content: space-around;
                    text-align: center;
                    color: white;
                    margin-bottom: 30px;  
                    margin-top: 20px
                }}
                .kpi-box {{
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    width: 140px;
                    height: 140px;
                    background-color: white;
                    color: red;
                    border-radius: 50%;  /* Makes it a circle */
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);  /* Slight shadow */
                    font-size: 40px;
                    font-weight: bold;
                }}
                .kpi-title {{
                    font-size: 16px;
                    color: #B0C4DE;
                    margin-top: 10px;
                }}
            </style>
            <div class="kpi-container">
                <div>
                    <div class="kpi-box">{total_crf_expected_formatted}</div>
                    <div class="kpi-title">TOTAL CRFs EXPECTED</div>
                </div>
                <div>
                    <div class="kpi-box">{total_crf_completed_formatted}</div>
                    <div class="kpi-title">TOTAL COMPLETED CRFs</div>
                </div>
                <div>
                    <div class="kpi-box">{total_crf_incomplete_formatted}</div>
                    <div class="kpi-title">TOTAL MISSING CRFs</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        

##################  Sites Backlog Trends ##################

    # Aggregate backlog trends per site
        backlog_trends = (
            filtered_data_crf
            .groupby("SiteName")["Missing"]
            .sum()
            .reset_index()
        )

        # Rename columns for clarity
        backlog_trends.columns = ["Site Name", "Total Missing Pages"]

        # Create Line Chart
        fig_backlog_trends = px.line(
            backlog_trends,
            x="Site Name",
            y="Total Missing Pages",
            title="Backlog Trends Across Sites",
            markers=True,  # Add markers to indicate points
            line_shape="spline",  # Smooth curve
        )

        # Update layout
        fig_backlog_trends.update_traces(line=dict(width=2, color="blue"))  # Blue line for better readability
        fig_backlog_trends.update_layout(
            xaxis_title="Site Name",
            yaxis_title="Total Missing Pages",
            xaxis=dict(showgrid=False, tickangle=-45),  # Rotate site names for visibility
            yaxis=dict(showgrid=True),
            height=500,
            title_font=dict(size=18),
        )

        # Display chart in Streamlit
        st.plotly_chart(fig_backlog_trends, use_container_width=True)

            # Use columns to push the download button to the lower right
        col1, col2, col3 = st.columns([0.6, 0.2, 0.2])  # Adjust column width to move button further right

        with col3:
            # Prepare data for download
            csv_data_backlog = backlog_trends.to_csv(index=False).encode('utf-8')

            # Download button for Enrollment Rate Data
            st.download_button(
                "Download Bcklog Trends Across Sites Data",
                data=csv_data_backlog,
                file_name="backlog_trends_sites.csv",
                mime="text/csv"
            )

##################  CRF Completion Status ##################

        # Data for the Pie Chart
        crf_status_data = {
            'CRF Status': ['Completed', 'Missing'],
            'Count': [total_crf_completed, total_crf_incomplete]
        }

        # Create the pie chart using Plotly
        crf_status_fig = px.pie(
            crf_status_data,
            names='CRF Status',  # Use 'CRF Status' as the labels
            values='Count',  # Use 'Count' as the values
            title='CRF Completion Status',
            color='CRF Status',
            color_discrete_sequence=['#4CAF50', '#FF5722'],  # Green for Completed, Red for Missing
            labels={'CRF Status': 'Status', 'Count': 'Count'},
            hole=0.3  # Optional: Create a donut chart
        )

        # Update traces for additional customization
        crf_status_fig.update_traces(
        textinfo='percent',  # Show percentage and value inside the pie
        pull=[0.1, 0],  # Pull out only the "Completed" slice for emphasis
        hovertemplate="<b>Status:</b> %{label}<br><b>Count:</b> %{value}<br><b>Percentage:</b> %{percent}<extra></extra>",
        insidetextfont=dict(
            color=['white', 'black']  # White for "Completed" slice, black for "Missing" slice
        )
    )

        # Update layout for better presentation
        ##Update layout for better presentation with larger fonts
        crf_status_fig.update_layout(
        title_font_size=20,  # Increase the title font size
        height=500,  # Adjust chart size
        margin=dict(t=100, b=40, l=50, r=50),  # Adjust margins
        showlegend=True,  # Show legend
        font=dict(
            size=18  # Increase font size for labels and legend
        ),
        legend=dict(
            font=dict(size=16),  # Increase font size for the legend
            title_font=dict(size=16)  # Increase font size for the legend title
        )
    )

##################  Top 10 Countries with Missing CRFs ##################

            # Filter rows where missing CRFs exist
        missing_crfs_per_country = filtered_data_crf[filtered_data_crf['Missing'] > 0]

        # Group by 'Country' and sum the 'Missing' CRFs
        country_missing_crfs = missing_crfs_per_country.groupby('Country')['Missing'].sum().reset_index()

        # Sort in descending order and keep only the top 10 countries
        top_10_countries = country_missing_crfs.sort_values(by='Missing', ascending=False).head(10)

        # Ensure top_10_countries is not empty
        if not top_10_countries.empty:
            # Create a Bubble + Line Chart
            combined_crf_fig = px.scatter(
                top_10_countries,  # ✅ Pass the entire DataFrame
                x='Country',  # ✅ Pass column name as a string
                y='Missing',
                size='Missing',  # Bubble size based on missing CRFs
                color='Country',  # Color by country
                color_discrete_sequence=px.colors.qualitative.Set3,
                text='Missing',
                title='Top 10 Countries with Most Missing CRFs',
                labels={'Country': '', 'Missing': 'Total Missing CRFs'}
            )

            # Add a line connecting the points
            combined_crf_fig.add_trace(
                go.Scatter(
                    x=top_10_countries['Country'],
                    y=top_10_countries['Missing'],
                    mode='lines+markers',  # ✅ Fixes the line issue
                    line=dict(color='white', dash='solid'),
                    name='Total Missing CRFs'
                )
            )

            # Update trace for better visualization
            combined_crf_fig.update_traces(
                textposition='top center',
                hovertemplate="<b>Country:</b> %{x}<br><b>Missing CRFs:</b> %{y}<extra></extra>"
            )

            # Update layout for better visuals
            combined_crf_fig.update_layout(
                title_font_size=20,
                xaxis=dict(tickangle=45, tickfont_size=12),  # Rotate x-axis labels for readability
                yaxis=dict(showgrid=False, tickformat=',d'),  # Show whole numbers on the y-axis
                height=500,
                margin=dict(t=80, b=100, l=40, r=40),
                showlegend=False
            )

            # Prepare data for download (CRF Completion Status)
            csv_data_crf_status = pd.DataFrame(crf_status_data).to_csv(index=False).encode('utf-8')

            # Prepare data for download (Top 10 Countries with Most Missing CRFs)
            csv_data_top_countries = top_10_countries.to_csv(index=False).encode('utf-8')

        # Create two columns for layout in Streamlit
        col1, col2 = st.columns(2)
        
        # Display the pie chart in the first column
        with col1:
            st.plotly_chart(crf_status_fig, use_container_width=True)

                # Use columns to align the download button to the lower right
            space1, space2, col_download = st.columns([0.4, 0.2, 0.4])

        with col_download:
            st.download_button( "Download CRF Completion Status Data",data=csv_data_crf_status,file_name="crf_completion_status.csv",mime="text/csv")

        # Display the bar chart in the second column
        with col2:
            st.plotly_chart(combined_crf_fig, use_container_width=True)

            # Use columns to align the download button to the lower right
            space1, space2, col_download = st.columns([0.5, 0.2, 0.3])

            with col_download:
                st.download_button(
                    "Download Missing CRFs Data",data=csv_data_top_countries,file_name="missing_crfs_top_10.csv",  mime="text/csv")


################## Total Critical CRFs with Missing pages ##################

            # Filter for Critical Forms using the loaded crf_entry_status_report DataFrame
        critical_crfs = filtered_data_crf[filtered_data_crf["Critical Form"] == 1]

        # Aggregate Missing Pages by FormName, and filter out forms with zero missing pages
        missing_by_form = (
            critical_crfs.groupby("FormName")["Missing"]
            .sum()
            .reset_index()
            .query("Missing > 0")  # Filter out forms with zero missing pages
            .sort_values(by="Missing", ascending=False)  # Sort in descending order
        )

        # Create Horizontal Bar Chart
        fig_critical_crfs = px.bar(
            missing_by_form,
            x="Missing",
            y="FormName",
            orientation="h",  # Horizontal bar chart
            title="Top Critical CRFs with Missing Pages",
            labels={"Missing": "Number of Missing Pages", "FormName": "CRF Name"},
            text="Missing",  # Show numbers on the bars
            color="Missing",
            color_continuous_scale="Reds"
        )

        fig_critical_crfs.update_traces(textposition="outside")
        fig_critical_crfs.update_layout(
            yaxis=dict(title="Critical CRFs", autorange="reversed"),  # Ensure the highest values are at the top
        xaxis=dict(title="Missing Pages Count"),
        height=500,
        title_font=dict(size=20),
        showlegend=False,  # Remove the legend
        coloraxis_showscale=False, 
        font=dict(size=15),  # Increase font size for overall text
        )

   ################## Pending CRF Distribution by Site ##################            

        # Assuming 'Missing' represents the missing CRFs in your dataset
        missing_crfs_per_site = filtered_data_crf[filtered_data_crf['Missing'] > 0]  # Filter rows with missing CRFs

        # Group the data by 'Site Name' and sum the 'Missing' CRFs for each site
        site_pending_crfs = missing_crfs_per_site.groupby('SiteName')['Missing'].sum().reset_index()

        # Sort the values by 'Missing' in descending order (highest to lowest)
        site_pending_crfs = site_pending_crfs.sort_values(by='Missing', ascending=False)
    
        # Assuming 'site_pending_crfs' is your DataFrame containing the 'SiteName' and 'Missing' data

        # Create the bar chart for pending CRF distribution by site
        site_pending_crfs_fig = px.bar(
            site_pending_crfs,
            x='SiteName',  # Site names on the x-axis
            y='Missing',  # Count of missing CRFs on the y-axis
            title='Pending CRF Distribution by Site',
            text='Missing',  # Show counts of missing CRFs on the bars
            color='SiteName',  # Color by site name
            color_discrete_sequence=px.colors.qualitative.Set2,  # Optional color scheme
        )

        # Update trace to display text positions at the top of each bar
        site_pending_crfs_fig.update_traces(
            textposition='outside',  # Place text (count of missing CRFs) outside the bar
        )

        # Update layout for better visuals
        site_pending_crfs_fig.update_layout(
            xaxis=dict(title="", showgrid=False, tickangle=-45),  # Label x-axis as Site Name
            yaxis=dict(title="Count of Missing CRFs", categoryorder='total ascending'),  # Order by missing count
            showlegend=False,
            height=500,
            title_font_size=20,
            margin=dict(t=100, b=80, l=100, r=20),  # Adjust margins for better presentation
        )

                # Prepare data for download (Critical CRFs with Missing Pages)
        csv_data_critical_crfs = missing_by_form.to_csv(index=False).encode('utf-8')

        # Prepare data for download (Pending CRF Distribution by Site)
        csv_data_pending_crfs = site_pending_crfs.to_csv(index=False).encode('utf-8')

        # Create two columns for layout in Streamlit
        col1, col2 = st.columns(2)

        # Display the Critical CRFs chart in the first column
        with col1:
            st.plotly_chart(fig_critical_crfs, use_container_width=True)

            # Use columns to align the download button to the lower right
            space1, space2, col_download = st.columns([0.5, 0.2, 0.3])

            with col_download:
                st.download_button(
                    "Download Critical CRFs Data",data=csv_data_critical_crfs,  file_name="critical_crfs_missing_pages.csv", mime="text/csv")

        # Display the Pending CRF Distribution chart in the second column
        with col2:
            st.plotly_chart(site_pending_crfs_fig, use_container_width=True)

            # Use columns to align the download button to the lower right
            space1, space2, col_download = st.columns([0.5, 0.2, 0.3])

            with col_download:
                st.download_button("Download Pending CRFs Data", data=csv_data_pending_crfs,file_name="pending_crfs_by_site.csv",mime="text/csv")

    
#####################################################################
#Performance Metrics / Data Cleaning Section
#####################################################################

    elif section == "Performance Metrics":
        st.header("Data Cleaning Status")
        st.markdown("____")

        # Filter subjects based on readiness for lock and locked status
        # Filter subjects based on readiness for lock and locked status
        ready_for_lock_df = data_cleaning_report[data_cleaning_report['READY FOR LOCK?'] == 1].copy()
        not_ready_for_lock_df = data_cleaning_report[
            (data_cleaning_report['READY FOR LOCK?'] == 0) & (data_cleaning_report['LOCKED?'] == 0)
        ].copy()  # Exclude locked subjects
        locked_df = data_cleaning_report[data_cleaning_report['LOCKED?'] == 1].copy()

        # Convert binary values to 'YES' or 'NO'
        def convert_to_yes_no(value):
            return "YES" if value == 1 else "NO"

        # Ensure required columns exist before applying functions
        columns_to_check = ['OPEN QUERY', 'MISSING CRF', 'SAE ISSUE', 'TPV RECONCILIATION ISSUE', 'SOURCE DATA VERIFICATION (SDV) COMPLETED?', 'PI SIGNATURE COMPLETE?']

        # Check for missing columns in both dataframes
        missing_columns_not_ready = [col for col in columns_to_check if col not in not_ready_for_lock_df.columns]
        missing_columns_ready = [col for col in columns_to_check if col not in ready_for_lock_df.columns]

        # Display error if any required column is missing
        if missing_columns_not_ready or missing_columns_ready:
            missing_columns_msg = set(missing_columns_not_ready + missing_columns_ready)
            st.error(f"Missing columns in data: {', '.join(missing_columns_msg)}")
        else:
            # Apply conversion to both DataFrames
            for col in columns_to_check:
                ready_for_lock_df[col] = ready_for_lock_df[col].map({1: "YES", 0: "NO"})
                not_ready_for_lock_df[col] = not_ready_for_lock_df[col].map({1: "YES", 0: "NO"})

        # Function to highlight 'YES' values in red
        def highlight_yes(value):
            return "color: red; font-weight: bold;" if value == "YES" else ""


        # Count total subjects
        total_ready_for_lock = ready_for_lock_df.shape[0]
        total_not_ready_for_lock = not_ready_for_lock_df.shape[0]
        total_locked = locked_df.shape[0]

        # Streamlit state variables for toggling visibility
        if "show_ready_list" not in st.session_state:
            st.session_state.show_ready_list = False
        if "show_not_ready_list" not in st.session_state:
            st.session_state.show_not_ready_list = False
        if "show_locked_list" not in st.session_state:
            st.session_state.show_locked_list = False

################## Data Cleaning Status KPIs ##################  

        st.markdown(f"""
            <style>
                .kpi-container {{
                    display: flex;
                    justify-content: space-around;
                    align-items: center;
                    text-align: center;
                    margin-top: 20px;
                }}
                .metric {{
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    margin-bottom: 20px;
                }}
                .circle {{
                    width: 120px;
                    height: 120px;
                    background-color: white;
                    border-radius: 50%;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    font-size: 50px;
                    font-weight: bold;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
                    margin-top: 10px;
                }}
                .ready {{ color: blue; }}
                .not-ready {{ color: red; }}
                .locked {{ color: green; }}
                .title {{
                    font-size: 18px;
                    font-weight: bold;
                    color: white;
                    margin-top: 10px;
                }}
                .not-text {{ color: red; text-decoration: underline; }}
                .locked-text {{ color: red; text-decoration: underline; }}
            </style>
            <div class="kpi-container">
                <div class="metric">
                    <div class="title">SUBJECTS READY FOR LOCK</div>
                    <div class="circle ready">{total_ready_for_lock}</div>
                </div>
                <div class="metric">
                    <div class="title">SUBJECTS <span class="not-text">NOT</span> READY FOR LOCK</div>
                    <div class="circle not-ready">{total_not_ready_for_lock}</div>
                </div>
                <div class="metric">
                    <div class="title">SUBJECTS <span class="locked-text">LOCKED</span></div>
                    <div class="circle locked">{total_locked}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

            # Button Controls
        col1, col2, col3, col4, col5, col6 = st.columns([1, 2, 1, 2, 1, 2])

        with col2:
            if st.button("CLICK TO VIEW_READY FOR LOCK", key="ready_button"):
                st.session_state.show_ready_list = not st.session_state.show_ready_list

        with col4:
            if st.button("CLICK TO VIEW_NOT READY FOR LOCK", key="not_ready_button"):
                st.session_state.show_not_ready_list = not st.session_state.show_not_ready_list

        with col6:
            if st.button("CLICK TO VIEW_LOCKED", key="locked_button"):
                st.session_state.show_locked_list = not st.session_state.show_locked_list

        # Format the Subject ID Number column
        ready_for_lock_df['Subject ID Number'] = ready_for_lock_df['Subject ID Number'].astype(str).str.replace(',', '')
        not_ready_for_lock_df['Subject ID Number'] = not_ready_for_lock_df['Subject ID Number'].astype(str).str.replace(',', '')
        locked_df['Subject ID Number'] = locked_df['Subject ID Number'].astype(str).str.replace(',', '')

        # Display subject lists dynamically
        with col2:
            if st.session_state.show_ready_list:
                styled_df_ready = ready_for_lock_df[['Subject ID Number'] + [col for col in columns_to_check if col in ready_for_lock_df.columns]].style.applymap(highlight_yes, subset=columns_to_check)
                st.dataframe(styled_df_ready, hide_index=True, use_container_width=True)

        with col4:
            if st.session_state.show_not_ready_list:
                styled_df_notready = not_ready_for_lock_df[['Subject ID Number'] + [col for col in columns_to_check if col in not_ready_for_lock_df.columns]].style.applymap(highlight_yes, subset=columns_to_check)
                st.dataframe(styled_df_notready, hide_index=True, use_container_width=True)

        with col6:
            if st.session_state.show_locked_list:
                st.dataframe(locked_df[['Subject ID Number']], hide_index=True)

### Ending code ###
if __name__ == "__main__":
    main()

       
