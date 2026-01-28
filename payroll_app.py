import os
import csv
from decimal import Decimal

CURRENT_DIRECTORY = os.path.dirname(__file__) # Set CURRENT_DIRECTORY to current folder

# Find and import CSV files
INPUT_PPSN_CSV_FILENAME = os.path.join(CURRENT_DIRECTORY, 'Input', 'PPSN.csv')
INPUT_RATES_CSV_FILENAME = os.path.join(CURRENT_DIRECTORY, 'Input', 'rate.csv')
INPUT_TIMETABLE_CSV_FILENAME = os.path.join(CURRENT_DIRECTORY, 'Input', 'hours.csv')

# Procedural Function for reading CSV files
def read_csv(filename, dict_to_update, field_name):
    with open(filename, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ppsn = row['PPSN']
            field = row[field_name]
            person_dict = dict_to_update.get(row['PPSN'], {})
            person_dict[field_name] = field
            dict_to_update[ppsn] = person_dict


salary_dict = {} # Dictionary to congregate and store info from CSV files 

# Input data from CSV file to dictionary
read_csv(INPUT_PPSN_CSV_FILENAME, salary_dict, 'Name')
read_csv(INPUT_TIMETABLE_CSV_FILENAME, salary_dict, 'Hours')
read_csv(INPUT_RATES_CSV_FILENAME, salary_dict, 'Rate')

# Procedural Function for PAYE
def calculate_paye(gross_income):
    cutoff = Decimal(44000)
    credits = Decimal(3750)  # Standard Personal + PAYE credit
    
    if gross_income <= cutoff:
        tax = gross_income * Decimal('0.20')
    else:
        tax = (cutoff * Decimal('0.20')) + ((gross_income - cutoff) * Decimal('0.40'))
    
    # Tax cannot be less than zero
    return max(0, (tax - credits))


# Procedural Function for USC
def calculate_usc(gross_income):
    # Ensure gross_income is a Decimal
    gross_income = Decimal(str(gross_income))
    
    # Income based tiers
    t1_limit = Decimal('12012')
    t2_limit = Decimal('28700')
    
    if gross_income <= t1_limit:
        return gross_income * Decimal('0.005')
    
    elif gross_income <= t2_limit:
        return (t1_limit * Decimal('0.005')) + \
               ((gross_income - t1_limit) * Decimal('0.02'))
    
    else:
        # Tier 1 + Tier 2 + the 4% balance
        t1_tax = t1_limit * Decimal('0.005')
        t2_tax = (t2_limit - t1_limit) * Decimal('0.02')
        balance_tax = (gross_income - t2_limit) * Decimal('0.04')
        
        return t1_tax + t2_tax + balance_tax
    

    
# Create output file in the Output folder
OUTPUT_FILE_NAME = os.path.join(CURRENT_DIRECTORY, 'Output', 'output.txt')

# Table padding
bw = 20 
w = 15 
sw = 10  
    
with open(OUTPUT_FILE_NAME, "w", encoding='utf-8') as my_file:
    # Table Header
    header = f"{'Name':<{bw}} {'PPSN':<{w}} {'Rate':<{sw}} {'Hours':<{sw}} {'Gross Weekly':<{w}} {'Net Weekly':<{w}} {'PAYE Weekly':<{w}} {'USC Weekly':<{w}} {'Weekly Tax':<{w}} {'Gross Yearly':<{w}} {'Net Yearly':<{w}} {'PAYE':<{w}} {'USC':<{w}} {'Yearly Tax':<{w}}\n"
    my_file.write(header)
    my_file.write("-" * (w * 14) + "\n")

    # Retrieve relevant data
    for ppsn in salary_dict:
        data = salary_dict[ppsn]
        rate = Decimal(salary_dict[ppsn]['Rate'])
        hours = Decimal(salary_dict[ppsn]['Hours'])
        gross = rate * hours * 52
        gross_weekly = rate * hours
        paye = calculate_paye(gross)
        paye_weekly = paye / Decimal(52)
        usc = calculate_usc(gross)
        usc_weekly = usc / Decimal(52)
        total_yearly_tax = paye + usc
        total_weekly_tax = paye_weekly + usc_weekly
        net = gross - total_yearly_tax
        net_weekly = gross_weekly - total_weekly_tax

        # Populate row with formatted data
        row = (f"{data['Name']:<{bw}} "
            f"{ppsn:<{w}} "
            f"€{rate:<{sw}}"
            f"{hours:<{sw}} "
            f"€{gross_weekly:<{w}.2f}"
            f"€{net_weekly:<{w}.2f}"
            f"€{paye_weekly:<{w}.2f}"
            f"€{usc_weekly:<{w}.2f}"
            f"€{total_weekly_tax:<{w}.2f}"
            f"€{gross:<{w}.2f}"
            f"€{net:<{w}.2f}"
            f"€{paye:<{w}.2f}"
            f"€{usc:<{w}.2f}"
            f"€{total_yearly_tax:<{w}.2f} "
            "\n")
  
        my_file.write(row) # Write output file

            