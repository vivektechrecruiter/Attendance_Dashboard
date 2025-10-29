import pandas as pd
import numpy as np
from scripts.clean_data import (
    standardize_date,
    standardize_time,
    clean_department,
    clean_location,
)


def test_standardize_date_various_formats():
    assert standardize_date('01/07/24') == '2024-07-01'
    assert standardize_date('02-07-2024') == '2024-07-02'
    assert standardize_date('2024/07/03') == '2024-07-03'
    assert pd.isna(standardize_date('not a date'))


def test_standardize_time_various_formats():
    assert standardize_time('9.00 AM') == '09:00'
    assert standardize_time('6.00 PM') == '18:00'
    assert standardize_time('09-10') == '09:10'
    assert standardize_time('10:05') == '10:05'
    assert np.isnan(standardize_time(np.nan))


def test_clean_department_variations():
    assert clean_department(' Hr ') == 'HR'
    assert clean_department('i.t') == 'IT'
    assert clean_department('ops') == 'OPERATIONS'
    assert clean_department('Fin') == 'FINANCE'
    assert pd.isna(clean_department(np.nan))


def test_clean_location_variations():
    assert clean_location('blr') == 'Bengaluru'
    assert clean_location('Bom') == 'Mumbai'
    assert clean_location('Hyderabaad') == 'Hyderabad'
    assert pd.isna(clean_location(np.nan))
