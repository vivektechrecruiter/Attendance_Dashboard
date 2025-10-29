import pandas as pd
import numpy as np

# Read the cleaned data files
attendance_df = pd.read_csv('Employee_Attendance_Clean.csv')
employee_df = pd.read_excel('Employees_Master_Clean.xlsx')

def calculate_attendance_metrics():
    # Calculate attendance statistics for each employee
    attendance_stats = attendance_df.groupby('EmployeeID').agg({
        'Status': [
            ('Total_Days', 'count'),
            ('Present_Days', lambda x: (x == 'Present').sum()),
            ('WFH_Days', lambda x: (x == 'Wfh').sum()),
            ('Leave_Days', lambda x: (x == 'Leave').sum()),
            ('Absent_Days', lambda x: (x == 'Absent').sum())
        ]
    })
    
    # Flatten the column names
    attendance_stats.columns = ['Total_Days', 'Present_Days', 'WFH_Days', 'Leave_Days', 'Absent_Days']
    attendance_stats = attendance_stats.reset_index()
    
    # Calculate percentages
    attendance_stats['Present_Percentage'] = ((attendance_stats['Present_Days'] + attendance_stats['WFH_Days']) / 
                                           attendance_stats['Total_Days'] * 100).round(2)
    attendance_stats['Leave_Percentage'] = (attendance_stats['Leave_Days'] / 
                                         attendance_stats['Total_Days'] * 100).round(2)
    attendance_stats['Absent_Percentage'] = (attendance_stats['Absent_Days'] / 
                                          attendance_stats['Total_Days'] * 100).round(2)
    
    # Merge with employee details
    result = pd.merge(attendance_stats, 
                     employee_df[['EmployeeID', 'Name', 'Department', 'Designation', 'Location', 'Status']], 
                     on='EmployeeID', 
                     how='left')
    
    # Reorder columns for better readability
    column_order = ['EmployeeID', 'Name', 'Department', 'Designation', 'Location', 'Status',
                    'Total_Days', 'Present_Days', 'WFH_Days', 'Leave_Days', 'Absent_Days',
                    'Present_Percentage', 'Leave_Percentage', 'Absent_Percentage']
    result = result[column_order]
    
    return result

# Calculate metrics
attendance_metrics = calculate_attendance_metrics()

# Display overall statistics
print("\nOverall Attendance Statistics:")
print("-----------------------------")
print(f"Total Employees: {len(attendance_metrics)}")
print(f"Average Present Percentage: {attendance_metrics['Present_Percentage'].mean():.2f}%")
print(f"Average Leave Percentage: {attendance_metrics['Leave_Percentage'].mean():.2f}%")
print(f"Average Absent Percentage: {attendance_metrics['Absent_Percentage'].mean():.2f}%")

# Display department-wise statistics
print("\nDepartment-wise Average Present Percentage:")
print("----------------------------------------")
dept_stats = attendance_metrics.groupby('Department')['Present_Percentage'].agg(['mean', 'count']).round(2)
dept_stats.columns = ['Avg Present %', 'Employee Count']
print(dept_stats)

# Display top 5 employees with highest attendance
print("\nTop 5 Employees by Attendance:")
print("----------------------------")
top_5 = attendance_metrics[attendance_metrics['Total_Days'] >= 5].nlargest(5, 'Present_Percentage')[
    ['Name', 'Department', 'Present_Percentage', 'Total_Days']
]
print(top_5)

# Display bottom 5 employees with lowest attendance
print("\nBottom 5 Employees by Attendance:")
print("-------------------------------")
bottom_5 = attendance_metrics[attendance_metrics['Total_Days'] >= 5].nsmallest(5, 'Present_Percentage')[
    ['Name', 'Department', 'Present_Percentage', 'Total_Days']
]
print(bottom_5)

# Save detailed results to Excel
output_file = 'Employee_Attendance_Analysis_Report.xlsx'
attendance_metrics.to_excel(output_file, index=False)
print(f"\nDetailed analysis has been saved to '{output_file}'")

# Additional insights
print("\nAdditional Insights:")
print("------------------")
print("1. Employees with 100% Attendance (Present + WFH):", 
      len(attendance_metrics[attendance_metrics['Present_Percentage'] == 100]))
print("2. Employees with more than 20% Absence:", 
      len(attendance_metrics[attendance_metrics['Absent_Percentage'] > 20]))
print("3. Employees with no leaves taken:", 
      len(attendance_metrics[attendance_metrics['Leave_Days'] == 0]))