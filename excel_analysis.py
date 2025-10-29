import pandas as pd

# Read the Excel files
try:
    attendance_df = pd.read_csv('Employee_Attendance.csv')
    # Read employee master file
    employee_master_df = pd.read_excel('Employees_Master.xlsx')
    
    # Display basic information about the datasets
    print("\nEmployee Attendance Dataset Info:")
    print("--------------------------------")
    print(attendance_df.info())
    print("\nFirst few rows of attendance data:")
    print(attendance_df.head())
    
    print("\nEmployee Master Dataset Info:")
    print("-----------------------------")
    print(employee_master_df.info())
    print("\nFirst few rows of master data:")
    print(employee_master_df.head())
    
except Exception as e:
    print(f"An error occurred: {str(e)}")
    print("Please make sure both files exist in the correct format (CSV/Excel)")