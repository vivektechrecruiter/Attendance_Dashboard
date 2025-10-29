import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set the style for better-looking graphs
plt.style.use('seaborn-v0_8')
sns.set_theme(style="whitegrid")
sns.set_palette("husl")

# Read the cleaned data files
attendance_df = pd.read_csv('Employee_Attendance_Clean.csv')
employee_df = pd.read_excel('Employees_Master_Clean.xlsx')

# Convert date to datetime
attendance_df['Date'] = pd.to_datetime(attendance_df['Date'])

# Create directory for saving plots
import os
if not os.path.exists('attendance_plots'):
    os.makedirs('attendance_plots')

def create_department_attendance_plot():
    # Calculate department-wise attendance percentages
    dept_attendance = attendance_df.merge(employee_df[['EmployeeID', 'Department']], on='EmployeeID')
    dept_stats = dept_attendance.groupby('Department')['Status'].value_counts(normalize=True).unstack()
    
    # Create a stacked bar plot
    plt.figure(figsize=(12, 6))
    dept_stats.plot(kind='bar', stacked=True)
    plt.title('Attendance Status Distribution by Department')
    plt.xlabel('Department')
    plt.ylabel('Percentage')
    plt.legend(title='Status', bbox_to_anchor=(1.05, 1))
    plt.tight_layout()
    plt.savefig('attendance_plots/department_attendance.png')
    plt.close()

def create_monthly_trend_plot():
    # Calculate monthly attendance trends
    attendance_df['Month'] = attendance_df['Date'].dt.strftime('%Y-%m')
    monthly_status = attendance_df.groupby(['Month', 'Status']).size().unstack()
    
    plt.figure(figsize=(15, 6))
    monthly_status.plot(kind='line', marker='o')
    plt.title('Monthly Attendance Trends')
    plt.xlabel('Month')
    plt.ylabel('Number of Employees')
    plt.xticks(rotation=45)
    plt.legend(title='Status', bbox_to_anchor=(1.05, 1))
    plt.tight_layout()
    plt.savefig('attendance_plots/monthly_trends.png')
    plt.close()

def create_weekday_pattern_plot():
    # Analyze weekday patterns
    attendance_df['Weekday'] = attendance_df['Date'].dt.day_name()
    weekday_status = attendance_df.groupby(['Weekday', 'Status']).size().unstack()
    
    # Reorder days
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    weekday_status = weekday_status.reindex(weekday_order)
    
    plt.figure(figsize=(12, 6))
    weekday_status.plot(kind='bar', stacked=True)
    plt.title('Attendance Patterns by Weekday')
    plt.xlabel('Day of Week')
    plt.ylabel('Number of Employees')
    plt.legend(title='Status', bbox_to_anchor=(1.05, 1))
    plt.tight_layout()
    plt.savefig('attendance_plots/weekday_patterns.png')
    plt.close()

def create_department_boxplot():
    # Calculate attendance percentage by employee and department
    attendance_metrics = attendance_df.merge(employee_df[['EmployeeID', 'Department']], on='EmployeeID')
    attendance_metrics = attendance_metrics.groupby(['EmployeeID', 'Department'])['Status'].apply(
        lambda x: (x.isin(['Present', 'Wfh']).sum() / len(x)) * 100
    ).reset_index()
    
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='Department', y='Status', data=attendance_metrics)
    plt.title('Attendance Percentage Distribution by Department')
    plt.xlabel('Department')
    plt.ylabel('Attendance Percentage')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('attendance_plots/department_boxplot.png')
    plt.close()

def create_location_attendance_plot():
    # Calculate location-wise attendance
    location_attendance = attendance_df.merge(
        employee_df[['EmployeeID', 'Location']], on='EmployeeID'
    ).dropna(subset=['Location'])
    
    location_stats = location_attendance.groupby('Location')['Status'].value_counts(normalize=True).unstack()
    
    plt.figure(figsize=(12, 6))
    location_stats.plot(kind='bar', stacked=True)
    plt.title('Attendance Status Distribution by Location')
    plt.xlabel('Location')
    plt.ylabel('Percentage')
    plt.legend(title='Status', bbox_to_anchor=(1.05, 1))
    plt.tight_layout()
    plt.savefig('attendance_plots/location_attendance.png')
    plt.close()

def create_wfh_trend_plot():
    # Analyze WFH trends over time
    wfh_trend = attendance_df[attendance_df['Status'] == 'Wfh'].groupby(
        attendance_df['Date'].dt.strftime('%Y-%m')
    ).size()
    
    plt.figure(figsize=(12, 6))
    wfh_trend.plot(kind='line', marker='o')
    plt.title('Work From Home Trends Over Time')
    plt.xlabel('Month')
    plt.ylabel('Number of WFH Instances')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('attendance_plots/wfh_trends.png')
    plt.close()

# Generate all plots
print("Generating attendance visualization plots...")
create_department_attendance_plot()
print("1. Department-wise attendance distribution plot created")
create_monthly_trend_plot()
print("2. Monthly attendance trends plot created")
create_weekday_pattern_plot()
print("3. Weekday patterns plot created")
create_department_boxplot()
print("4. Department-wise attendance distribution boxplot created")
create_location_attendance_plot()
print("5. Location-wise attendance distribution plot created")
create_wfh_trend_plot()
print("6. Work from home trends plot created")

print("\nAll plots have been saved in the 'attendance_plots' directory.")
print("\nPlot descriptions:")
print("1. department_attendance.png: Shows the distribution of attendance status across departments")
print("2. monthly_trends.png: Displays attendance trends over months")
print("3. weekday_patterns.png: Shows attendance patterns for different days of the week")
print("4. department_boxplot.png: Shows the distribution of attendance percentages within each department")
print("5. location_attendance.png: Shows attendance patterns across different office locations")
print("6. wfh_trends.png: Displays the trend of work from home over time")