import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from io import BytesIO
import os

# For Excel export
import io

# Set page configuration
st.set_page_config(
    page_title="Employee Attendance Dashboard",
    page_icon="📊",
    layout="wide"
)

# Add custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stPlotlyChart {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# Load the data
@st.cache_data
def load_data():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    attendance_df = pd.read_csv(os.path.join(base_path, 'Employee_Attendance_Clean.csv'))
    employee_df = pd.read_excel(os.path.join(base_path, 'Employees_Master_Clean.xlsx'))
    
    # Convert date to datetime
    attendance_df['Date'] = pd.to_datetime(attendance_df['Date'])
    return attendance_df, employee_df

def calculate_metrics(attendance_df, employee_df):
    # Merge data
    merged_df = attendance_df.merge(employee_df[['EmployeeID', 'Department', 'Location']], on='EmployeeID')
    
    # Calculate overall metrics
    total_employees = employee_df.shape[0]
    present_rate = (merged_df['Status'].isin(['Present', 'Wfh']).mean() * 100).round(2)
    leave_rate = (merged_df['Status'] == 'Leave').mean() * 100
    absent_rate = (merged_df['Status'] == 'Absent').mean() * 100
    
    return total_employees, present_rate, leave_rate, absent_rate

def create_department_chart(merged_df):
    dept_stats = merged_df.groupby('Department')['Status'].value_counts(normalize=True).unstack()
    fig = px.bar(dept_stats, 
                 title='Attendance Status by Department',
                 barmode='stack',
                 labels={'value': 'Percentage', 'Status': 'Status'})
    fig.update_layout(height=400)
    return fig

def create_attendance_trend(merged_df):
    daily_status = merged_df.groupby(['Date', 'Status']).size().unstack(fill_value=0)
    fig = px.line(daily_status, 
                  title='Attendance Trends Over Time',
                  labels={'value': 'Number of Employees', 'Date': 'Date'})
    fig.update_layout(height=400)
    return fig

def create_location_chart(merged_df):
    location_stats = merged_df.groupby('Location')['Status'].value_counts(normalize=True).unstack()
    fig = px.bar(location_stats,
                 title='Attendance Status by Location',
                 barmode='stack',
                 labels={'value': 'Percentage', 'Status': 'Status'})
    fig.update_layout(height=400)
    return fig

def create_weekday_chart(merged_df):
    merged_df['Weekday'] = merged_df['Date'].dt.day_name()
    weekday_stats = merged_df.groupby('Weekday')['Status'].value_counts(normalize=True).unstack()
    # Reorder days
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    weekday_stats = weekday_stats.reindex(weekday_order)
    
    fig = px.bar(weekday_stats,
                 title='Attendance Patterns by Weekday',
                 barmode='stack',
                 labels={'value': 'Percentage', 'Status': 'Status'})
    fig.update_layout(height=400)
    return fig

def main():
    # Load data
    attendance_df, employee_df = load_data()
    merged_df = attendance_df.merge(employee_df[['EmployeeID', 'Department', 'Location', 'Name']], on='EmployeeID')
    
    # Title
    st.title("📊 Employee Attendance Dashboard")
    st.markdown("---")
    
    # Calculate metrics
    total_employees, present_rate, leave_rate, absent_rate = calculate_metrics(attendance_df, employee_df)
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Employees", total_employees)
    with col2:
        st.metric("Present + WFH Rate", f"{present_rate:.1f}%")
    with col3:
        st.metric("Leave Rate", f"{leave_rate:.1f}%")
    with col4:
        st.metric("Absent Rate", f"{absent_rate:.1f}%")
    
    st.markdown("---")
    
    # Filters in sidebar
    st.sidebar.header("Filters")
    
    # Date range filter
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(merged_df['Date'].min(), merged_df['Date'].max()),
        min_value=merged_df['Date'].min().date(),
        max_value=merged_df['Date'].max().date()
    )
    
    # Department filter
    departments = merged_df['Department'].dropna().unique()
    selected_departments = st.sidebar.multiselect(
        "Select Departments",
        options=sorted(list(departments)),
        default=sorted(list(departments))
    )
    
    # Location filter
    locations = list(merged_df['Location'].dropna().unique())
    if merged_df['Location'].isna().any():
        locations.append('Unknown')
    selected_locations = st.sidebar.multiselect(
        "Select Locations",
        options=sorted(locations),
        default=sorted(locations)
    )
    
    # Filter data based on selections
    date_mask = (
        (merged_df['Date'].dt.date >= date_range[0]) &
        (merged_df['Date'].dt.date <= date_range[1])
    )
    dept_mask = merged_df['Department'].isin(selected_departments)
    
    # Handle location filtering including NaN values
    if 'Unknown' in selected_locations:
        loc_mask = merged_df['Location'].isin(selected_locations) | merged_df['Location'].isna()
    else:
        loc_mask = merged_df['Location'].isin(selected_locations)
    
    filtered_df = merged_df[date_mask & dept_mask & loc_mask]
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_department_chart(filtered_df), use_container_width=True)
    with col2:
        st.plotly_chart(create_location_chart(filtered_df), use_container_width=True)
        
    col3, col4 = st.columns(2)
    
    with col3:
        st.plotly_chart(create_attendance_trend(filtered_df), use_container_width=True)
    with col4:
        st.plotly_chart(create_weekday_chart(filtered_df), use_container_width=True)
    
    # Detailed Data View
    st.markdown("### Detailed Attendance Data")
    
    # Calculate employee-wise attendance
    employee_stats = filtered_df.groupby(['EmployeeID', 'Name', 'Department', 'Location']).agg({
        'Status': ['count',
                  lambda x: (x == 'Present').sum(),
                  lambda x: (x == 'Wfh').sum(),
                  lambda x: (x == 'Leave').sum(),
                  lambda x: (x == 'Absent').sum()]
    }).reset_index()
    
    employee_stats.columns = ['EmployeeID', 'Name', 'Department', 'Location', 
                            'Total_Days', 'Present_Days', 'WFH_Days', 'Leave_Days', 'Absent_Days']
    
    employee_stats['Present_Rate'] = ((employee_stats['Present_Days'] + employee_stats['WFH_Days']) / 
                                    employee_stats['Total_Days'] * 100).round(2)
    
    # Export buttons for the employee-level stats
    csv_bytes = employee_stats.to_csv(index=False).encode('utf-8')
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        employee_stats.to_excel(writer, index=False, sheet_name='EmployeeMetrics')
    excel_bytes = excel_buffer.getvalue()

    col_export_1, col_export_2 = st.columns([1, 1])
    with col_export_1:
        st.download_button("Download CSV", data=csv_bytes, file_name='employee_metrics.csv', mime='text/csv')
    with col_export_2:
        st.download_button("Download Excel", data=excel_bytes, file_name='employee_metrics.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    st.dataframe(
        employee_stats.style.format({
            'Present_Rate': '{:.1f}%'
        }),
        height=300
    )

    st.markdown("---")
    st.markdown("### Employee Detail Drilldown")
    # Employee selection for drilldown
    employee_list = ['All'] + sorted(employee_df['Name'].dropna().unique().tolist())
    selected_employee = st.selectbox("Select Employee (for detail view)", employee_list)

    if selected_employee and selected_employee != 'All':
        emp_id = employee_df[employee_df['Name'] == selected_employee]['EmployeeID'].iloc[0]
        emp_att = attendance_df[attendance_df['EmployeeID'] == emp_id].copy()
        emp_att['Date'] = pd.to_datetime(emp_att['Date'])
        
        # Apply date filter to employee data
        date_mask = (
            (emp_att['Date'].dt.date >= date_range[0]) &
            (emp_att['Date'].dt.date <= date_range[1])
        )
        emp_att = emp_att[date_mask]
        
        if len(emp_att) == 0:
            st.warning("No data found for the selected date range!")
            return
            
        total_days = len(emp_att)
        present_days = emp_att['Status'].isin(['Present', 'Wfh']).sum()
        wfh_days = (emp_att['Status'] == 'Wfh').sum()
        leave_days = (emp_att['Status'] == 'Leave').sum()
        absent_days = (emp_att['Status'] == 'Absent').sum()
        present_rate_emp = round((present_days / total_days * 100) if total_days else 0, 2)

        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("Total Records", total_days)
        k2.metric("Present + WFH", f"{present_days}")
        k3.metric("WFH", f"{wfh_days}")
        k4.metric("Leave", f"{leave_days}")
        k5.metric("Absent", f"{absent_days}")

        present_rate_emp = round((present_days / total_days * 100) if total_days else 0, 2)
        leave_rate_emp = round((leave_days / total_days * 100) if total_days else 0, 2)
        st.markdown(f"""
        **Present Rate:** {present_rate_emp}% | **Leave Rate:** {leave_rate_emp}%
        """)

        # Prepare calendar-like heatmap (weeks x weekday)
        emp_att['ISO_Year'] = emp_att['Date'].dt.isocalendar().year
        emp_att['ISO_Week'] = emp_att['Date'].dt.isocalendar().week
        emp_att['Week_Label'] = emp_att['ISO_Year'].astype(str) + "-W" + emp_att['ISO_Week'].astype(str)
        emp_att['Weekday_Num'] = emp_att['Date'].dt.weekday  # 0=Monday

        # Map status to numeric values for heatmap
        status_map = {'Present': 1.0, 'Wfh': 1.0, 'Leave': 0.5, 'Absent': 0.0}
        emp_att['Status_Num'] = emp_att['Status'].map(status_map).fillna(0.0)

        pivot = emp_att.pivot_table(index='Week_Label', columns='Weekday_Num', values='Status_Num', aggfunc='mean')
        # Reindex weekdays to 0..6 and fill missing with NaN
        pivot = pivot.reindex(columns=range(0, 7))

        # Plot heatmap
        fig, ax = plt.subplots(figsize=(10, max(2, 0.4 * len(pivot))))
        sns.heatmap(pivot, ax=ax, cmap='YlGnBu', cbar_kws={'label': 'Attendance (1=Present,0=Absent)'} , vmin=0, vmax=1)
        ax.set_ylabel('Week')
        ax.set_xlabel('Weekday (0=Mon)')
        st.pyplot(fig)

        st.markdown("#### Recent Records")
        st.dataframe(emp_att[['Date', 'Status', 'InTime', 'OutTime']].sort_values('Date', ascending=False), height=300)

if __name__ == "__main__":
    main()