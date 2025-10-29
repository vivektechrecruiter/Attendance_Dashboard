import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path


def standardize_date(date_str):
    """Convert various date formats to YYYY-MM-DD"""
    try:
        # Try different date formats
        for fmt in ['%d/%m/%y', '%d-%m-%Y', '%Y/%m/%d', '%d-%m-%Y', '%d.%m.%Y']:
            try:
                return pd.to_datetime(date_str, format=fmt).strftime('%Y-%m-%d')
            except:
                continue
        return pd.to_datetime(date_str).strftime('%Y-%m-%d')
    except:
        return pd.NaT

def standardize_time(time_str):
    """Convert various time formats to 24-hour HH:MM format"""
    if pd.isna(time_str):
        return np.nan
    
    try:
        # Remove any spaces in the time string
        time_str = str(time_str).strip()
        
        # Handle different time formats
        if 'AM' in time_str.upper() or 'PM' in time_str.upper():
            # Convert 12-hour format to 24-hour
            return datetime.strptime(time_str, '%I.%M %p').strftime('%H:%M')
        elif '-' in time_str:
            # Handle format like '09-10'
            return time_str.replace('-', ':')
        elif '.' in time_str:
            # Handle format with dots
            return time_str.replace('.', ':')
        
        # If already in HH:MM format
        return datetime.strptime(time_str, '%H:%M').strftime('%H:%M')
    except:
        return np.nan

def clean_department(dept):
    """Standardize department names"""
    if pd.isna(dept):
        return np.nan
    # Convert to uppercase and strip whitespace
    dept = dept.strip().upper()
    # Standard department mapping
    dept_mapping = {
        'HR': 'HR',
        'H R': 'HR',
        'IT': 'IT',
        'I.T': 'IT',
        'OPS': 'OPERATIONS',
        'OPERATION': 'OPERATIONS',
        'FIN': 'FINANCE',
        'SALES': 'SALES',
        'SALE': 'SALES',
        'S A L E S': 'SALES'
    }
    return dept_mapping.get(dept, dept)

def clean_location(location):
    """Standardize location names"""
    if pd.isna(location):
        return np.nan
    # Convert to title case and strip whitespace
    location = location.strip().title()
    # Standard location mapping
    location_mapping = {
        'Pune': 'Pune',
        'Pun': 'Pune',
        'Mumbai': 'Mumbai',
        'Bom': 'Mumbai',
        'Bengaluru': 'Bengaluru',
        'Bangalore': 'Bengaluru',
        'Blr': 'Bengaluru',
        'Hyderabad': 'Hyderabad',
        'Hyderabaad': 'Hyderabad',
        'Hyd': 'Hyderabad',
        'Delhi': 'Delhi',
        'Ncr-Delhi': 'Delhi'
    }
    return location_mapping.get(location, location)
def _get_paths():
    """Return project root and data paths (works when module is imported from anywhere)."""
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / 'data'
    return base_dir, data_dir


def clean_and_save(attendance_path: str | Path, master_path: str | Path, out_attendance: str | Path, out_master: str | Path):
    """Run cleaning pipeline using provided paths and save outputs."""
    attendance_df = pd.read_csv(attendance_path)
    employee_master_df = pd.read_excel(master_path)

    # Clean attendance data
    attendance_clean = attendance_df.copy()
    attendance_clean['Date'] = attendance_clean['Date'].apply(standardize_date)
    attendance_clean['InTime'] = attendance_clean['InTime'].apply(standardize_time)
    attendance_clean['OutTime'] = attendance_clean['OutTime'].apply(standardize_time)
    attendance_clean['Status'] = attendance_clean['Status'].str.title()

    # Clean employee master data
    master_clean = employee_master_df.copy()
    master_clean['DateOfJoining'] = master_clean['DateOfJoining'].apply(standardize_date)
    master_clean['Department'] = master_clean['Department'].apply(clean_department)
    master_clean['Location'] = master_clean['Location'].apply(clean_location)
    master_clean['Status'] = master_clean['Status'].str.title()

    # Save cleaned data
    attendance_clean.to_csv(out_attendance, index=False)
    master_clean.to_excel(out_master, index=False)

    return attendance_clean, master_clean


def main():
    base_dir, data_dir = _get_paths()
    attendance_in = data_dir / 'Employee_Attendance.csv'
    master_in = data_dir / 'Employees_Master.xlsx'
    attendance_out = base_dir / 'Employee_Attendance_Clean.csv'
    master_out = base_dir / 'Employees_Master_Clean.xlsx'

    print("Cleaning attendance data...")
    attendance_clean, master_clean = clean_and_save(attendance_in, master_in, attendance_out, master_out)

    # Display summary of changes
    print("\nCleaned Data Summary:")
    print("\nEmployee Attendance Dataset:")
    print("------------------------")
    print(attendance_clean.head())
    print("\nNull values in Attendance:")
    print(attendance_clean.isnull().sum())

    print("\nEmployee Master Dataset:")
    print("----------------------")
    print(master_clean.head())
    print("\nNull values in Master:")
    print(master_clean.isnull().sum())

    # Display unique values in key columns to verify standardization
    print("\nUnique Departments:", sorted(master_clean['Department'].unique()))
    print("Unique Locations:", sorted(master_clean['Location'].dropna().unique()))
    print("Unique Status Values (Master):", sorted(master_clean['Status'].unique()))
    print("Unique Status Values (Attendance):", sorted(attendance_clean['Status'].unique()))


if __name__ == '__main__':
    main()