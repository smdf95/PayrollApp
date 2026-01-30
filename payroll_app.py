import os
import csv
from decimal import Decimal
from datetime import datetime

                        ### --- SET FILE PATHS --- ###

# Set CURRENT_DIRECTORY to current folder
CURRENT_DIRECTORY = os.path.dirname(__file__)

# If CURRENT_DIRECTORY is empty, set it to the working directory
if not CURRENT_DIRECTORY:
    CURRENT_DIRECTORY = os.getcwd()

 # Find the output folder 
OUTPUT_FOLDER = os.path.join(CURRENT_DIRECTORY, 'Output') 

# Create Output folder if it doesn't exist
if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

# Create Employee Payslips folder if it doesn't exist
if not os.path.exists(os.path.join(OUTPUT_FOLDER, 'Employee Payslips')):
        os.makedirs(os.path.join(OUTPUT_FOLDER, 'Employee Payslips'))

                        ### --- GLOBAL VARIABLES --- ###
now = datetime.now()
pay_week = now.isocalendar()[1]
date = now.strftime("%d/%m/%Y")

                        ### --- READ INPUT FILES AND POPULATE DICTIONARY --- ###

# Find and import CSV files
INPUT_EMPLOYEE_INFO_CSV_FILENAME = os.path.join(CURRENT_DIRECTORY, 'Input', 'employee_info.csv')
INPUT_RATES_CSV_FILENAME = os.path.join(CURRENT_DIRECTORY, 'Input', 'rate.csv')
INPUT_TIMETABLE_CSV_FILENAME = os.path.join(CURRENT_DIRECTORY, 'Input', 'hours.csv')

# Procedural Function for reading CSV files
def read_csv(filename, dict_to_update, field_names):
    with open(filename, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            ppsn = row['PPSN']
            person_dict = dict_to_update.get(ppsn, {})
            for field in field_names:
                person_dict[field] = row[field]

            dict_to_update[ppsn] = person_dict


salary_dict = {} # Dictionary to congregate and store info from CSV files 

# Input data from CSV file to dictionary
read_csv(INPUT_EMPLOYEE_INFO_CSV_FILENAME, salary_dict, ['Name', 'EmployeeNo', 'Dep'])
read_csv(INPUT_TIMETABLE_CSV_FILENAME, salary_dict, ['Hours', 'Hours_Scheduled'])
read_csv(INPUT_RATES_CSV_FILENAME, salary_dict, ['Rate'])


                                ### --- PAYROLL CALCULATIONS --- ###

# Procedural Function for PAYE
def calculate_paye(gross):
    # Ensure gross_income is a Decimal and annualised
    gross_income = Decimal(str(gross)) * 52

    cutoff = Decimal(44000)
    credits = Decimal(3750)  # Standard Personal + PAYE credit
    
    # Calculate tax based on bands
    if gross_income <= cutoff:
        tax = gross_income * Decimal('0.20')
    else:
        tax = (cutoff * Decimal('0.20')) + ((gross_income - cutoff) * Decimal('0.40'))
    
    # Tax cannot be less than zero
    return max(0, (tax - credits))


# Procedural Function for USC
def calculate_usc(gross):
    # Ensure gross_income is a Decimal and annualised
    gross_income = Decimal(str(gross)) * 52
    
    # Income based tiers
    tier1 = Decimal('12012')
    tier2 = Decimal('28700')
    
    # Calculate USC based on bands
    if gross_income <= tier1:
        return (gross_income * Decimal('0.005'))
    
    elif gross_income <= tier2:
        return ((tier1 * Decimal('0.005')) + \
               ((gross_income - tier1) * Decimal('0.02')))
    
    else:
        # Tier 1 + Tier 2 + the 4% balance
        tier1_tax = tier1 * Decimal('0.005')
        tier2_tax = (tier2 - tier1) * Decimal('0.02')
        balance_tax = (gross_income - tier2) * Decimal('0.04')
        
        return (tier1_tax + tier2_tax + balance_tax)

# Procedural Function for Overtime Calculation    
def calculate_overtime(hours, hours_scheduled, rate):
    overtime_hours = max(0, hours - hours_scheduled)
    overtime_rate = rate * Decimal('1.5')
    return overtime_hours * overtime_rate

                                ### --- GENERATE PAYROLL REPORTS --- ###

# Create output file in the Output folder
OUTPUT_FILE_NAME = os.path.join(OUTPUT_FOLDER, 'PayrollReport.md')

# Create the Payroll Report
with open(OUTPUT_FILE_NAME, "w", encoding='utf-8') as my_file:

    gross_total = Decimal(0)
    overtime_total = Decimal(0)
    net_total = Decimal(0)
    tax_total = Decimal(0)
    employee_total = Decimal(0)
    
    for i in salary_dict:
        employee_total += 1
    
    # Header Section
    my_file.write(f"# FINANCIAL IT SOLUTIONS LTD\n")
    my_file.write("## Company Payroll Summary Report\n")
    my_file.write(f"**Period: Week {pay_week}**\n\n")
    my_file.write(f"**Number of Employees: {employee_total}**\n\n")
    
    # Markdown Table Headers
    cols = ["Employee no", "Employee", "Department", "Hours", "Overtime Hours", "Gross Pay", "Overtime Pay", "Net Take-Home", "Tax Liability"]
    my_file.write("| " + " | ".join(cols) + " |\n")
    my_file.write("| " + " | ".join([":---"] * len(cols)) + " |\n")

    for ppsn in salary_dict:
        employee = salary_dict[ppsn]
        # Base Variables
        rate = Decimal(employee['Rate'])
        hours = Decimal(employee['Hours'])
        overtime_hours = max(0, hours - Decimal(employee['Hours_Scheduled']))
        
        # Weekly Variables
        overtime = calculate_overtime(hours, Decimal(employee['Hours_Scheduled']), rate)
        gross = (rate * hours) + overtime
        paye = calculate_paye(gross) / Decimal('52') # Calculating based on yearly projection
        usc = calculate_usc(gross) / Decimal('52')
        tax = paye + usc
        net = gross - tax

        # Accumulate Totals
        gross_total += gross
        overtime_total += overtime
        net_total += net
        tax_total += tax
        
        # To Date Calculations
        gross_to_date = gross * pay_week
        paye_to_date = paye * pay_week
        usc_to_date = usc * pay_week
        tax_to_date = paye_to_date + usc_to_date
        net_to_date = gross_to_date - tax_to_date

        # Write Employee Row
        row_data = [
            employee['EmployeeNo'],
            employee['Name'],
            employee['Dep'],
            str(hours),
            str(overtime_hours),
            f"€{gross:,.2f}",
            f"€{overtime:,.2f}",
            f"€{net:,.2f}",
            f"€{tax:,.2f}"
        ]
        my_file.write("| " + " | ".join(row_data) + " |\n")

    # Grand Totals Section
    my_file.write("\n---\n")
    my_file.write("## Weekly Financial Summary\n\n")
    my_file.write("| Description | Total Amount |\n")
    my_file.write("| :--- | :--- |\n")
    my_file.write(f"| **Total Gross Payroll** | **€{gross_total:,.2f}** |\n")
    my_file.write(f"| **Total Overtime Paid** | **€{overtime_total:,.2f}** |\n")
    my_file.write(f"| **Total Net Pay** | **€{net_total:,.2f}** |\n")
    my_file.write(f"| **Total Tax to Remit** | **€{tax_total:,.2f}** |\n\n")

    # Footer Note
    my_file.write(f"**Note:** This report summarises the expenditure for Week {pay_week}")


                        ### --- GENERATE INDIVIDUAL PAYSLIPS --- ###

# Loop through each employee and create individual payslips
for i in salary_dict:
    # Get employee data
    employee = salary_dict[i]

    # Create individual payslip file with employee name and pay week as filename
    EMPLOYEE_PAYSLIP = os.path.join(OUTPUT_FOLDER, 'Employee Payslips', f"{employee['Name'].strip()}Week{pay_week}.md")
    
    # Write Payslip Content
    with open(EMPLOYEE_PAYSLIP, "w", encoding='utf-8') as my_file:

        # Base Variables
        rate = Decimal(employee['Rate'])
        hours = Decimal(employee['Hours'])
        overtime_hours = max(0, hours - Decimal(employee['Hours_Scheduled']))
        
        # Weekly Variables
        overtime = calculate_overtime(hours, Decimal(employee['Hours_Scheduled']), rate)
        gross_before_ot = rate * hours
        gross = gross_before_ot + overtime
        paye = calculate_paye(gross) / Decimal('52') # Calculating based on yearly projection
        usc = calculate_usc(gross) / Decimal('52')
        tax = paye + usc
        net = gross - tax
        
        # To Date Calculations
        gross_to_date = gross * pay_week
        paye_to_date = paye * pay_week
        usc_to_date = usc * pay_week
        tax_to_date = paye_to_date + usc_to_date
        net_to_date = gross_to_date - tax_to_date

        # Company Header
        my_file.write(f"# FINANCIAL IT SOLUTIONS LTD\n")
        my_file.write(f"**PAYSLIP: {employee['Name'].upper()}**\n")
        my_file.write(f"---\n\n")

        # Employee Information Block
        my_file.write("| Employee Details | | | | | Payroll Period Info | |\n")
        my_file.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        my_file.write(f"| **Name:** | {employee['Name']} | **Emp No:** | {employee['EmployeeNo']} | | **Date:** | {date} |\n")
        my_file.write(f"| **PPSN:** | {i} | **Department:** | {employee['Dep']} | | **Pay Week** | {pay_week} |\n")
        my_file.write(f"| **Hours:** | {hours} | **Overtime Hours:** | {overtime_hours} |\n\n")

        # Main Financial Table
        my_file.write("### EARNINGS AND DEDUCTIONS\n")
        my_file.write("| Description | Amount | Deductions | Amount |\n")
        my_file.write("| :--- | :--- | :--- | :--- |\n")
        my_file.write(f"| **Gross Pay** | **€{gross_before_ot:,.2f}** | PAYE | €{paye:,.2f} |\n")
        if overtime_hours > 0:
            my_file.write(f"| **Overtime** | **€{overtime:,.2f}** | USC | €{usc:,.2f} |\n")
        else:
            my_file.write(f"| | | USC | €{usc:,.2f} |\n")
        my_file.write("| --- | --- | --- | --- |\n")
        my_file.write(f"| **Total Earnings** | **€{gross:,.2f}** | **Total Deductions** | **€{tax:,.2f}** |\n\n")
        my_file.write(f"### NET PAY: €{net:,.2f}\n")
        my_file.write(f"---\n\n")


        # Year-to-Date Section
        my_file.write("### YEAR-TO-DATE (YTD) PAY\n")
        my_file.write("| Description | Total |\n")
        my_file.write("| :--- | :--- |\n")
        my_file.write(f"| **Gross Pay** | €{gross_to_date:,.2f} |\n")
        my_file.write(f"| **PAYE Tax** | €{paye_to_date:,.2f} |\n")
        my_file.write(f"| **USC Tax** | €{usc_to_date:,.2f} |\n")
        my_file.write(f"| **Total Deductions** | €{tax_to_date:,.2f} |\n")
        my_file.write("| --- | --- | --- |\n")
        my_file.write(f"| **NET PAY** | **€{net_to_date:,.2f}** |\n\n")

        # Footer Note
        my_file.write("---\n*Generated automatically by Payroll Systems - Private & Confidential*\n\n")
        my_file.write("*For further information, contact Séaghan Fisher: seaghan.fisher@gmail.com or +353871691802*")
