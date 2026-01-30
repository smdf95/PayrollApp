# Software Design Document

**Payroll processing app**

Séaghan Fisher

- [Software Design Document](#software-design-document)
  - [Program Overview](#program-overview)
  - [Program Requirements](#program-requirements)
    - [Functional Requirements](#functional-requirements)
    - [Technical Requirements](#technical-requirements)
  - [Input Format](#input-format)
    - [Personal Info](#personal-info)
    - [Timetable](#timetable)
    - [Rate](#rate)
  - [Output Format](#output-format)
    - [Payroll Table](#1-payroll-table)
    - [Payslip](#2-payslip)
  - [Testing Approach](#testing-approach)


## Program Overview

The payroll processing application is a software that assists users in processing multiple CSV files and converting them into a readable table of employee payroll information and creating individual payslips. Users can upload CSV files of employee information (including personal info, timetables, and pay rate) into the program to process the data, perform calculations, and return a structured table in a readable format. The program will also create individual payslips for each employee based on hours worked that week, while automatically calculating the PAYE and USC tax. The software aims to provide a simple and efficient way to process employee payroll information and create a single table with all relevant data. 

The application will be developed using the Python programming language in conjunction with the procedural design philosophy.

## Program Requirements

### Functional Requirements

- Read timetable, rate, and personal info CSV files
- Extract relevant info
- Calculate gross pay
- Calculate overtime pay if applicable
- Calculate tax (PAYE and USC)
- Calculate net pay
- Calculate total gross, net, and tax paid so far this year
- Create payroll report summarising company expenditure
- Create individual payslips for each employee

### Technical Requirements

- Platform: cross-platform (Windows, Linux, MacOS)
- Language: Developed Python, ensuring wide support and maintainability
- Database: CSV files

## Input format

#### Personal Info

```csv
PPSN, Name, EmployeeNo, Dep
1234567A, John Doe, 1, IT
```

#### Timetable

```csv
PPSN, hours, hours_scheduled
1234567A, 36, 35
```

#### Rate

```csv
PPSN, Rate
1234567A, 15
```

## Output format

### 1. Payroll table

| Employee no | Employee | Department | Hours | Overtime Hours | Gross Pay | Overtime Pay | Net Take-Home | Tax Liability |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 001 | John Doe | IT | 40 | 0 | €620.00 | €0.00 | €557.82 | €62.18 |

| Description | Total Amount |
| :--- | :--- |
| **Total Gross Payroll** | **€4,249.75** |
| **Total Net Pay** | **€3,449.09** |
| **Total Tax** | **€800.66** |


### 2. Payslip
| Employee Details | | | | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Payroll Period Info | |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Name:** | Jane Doe | **Emp No:** | 002 | | **Date:** | 30/01/2026 |
| **PPSN:** | 8765432B | **Department:** | IT | | **Pay Week** | 5 |
| **Hours:** | 37.5 | **Overtime Hours:** | 2.5 |

### EARNINGS AND DEDUCTIONS
| Description | Amount | Deductions | Amount |
| :--- | :--- | :--- | :--- |
| **Gross Pay** | **€1,050.00** | PAYE | €220.65 |
| **Overtime** | **€105.00** | USC | €31.70 |
| --- | --- | --- | --- |
| **Total Earnings** | **€1,155.00** | **Total Deductions** | **€252.35** |

### NET PAY: €902.65

## Testing Approach

The approach to testing this application will be multifaceted but primarily focus on the concept of unit testing, where each individual function is tested in isolation with a set of predetermined inputs to verify that the output matches expected results. This will involve:

- Mocking File Systems: Utilising tools like mock_open to simulate reading from CSV files without requiring physical files on disk, ensuring the data is correctly parsed into application dictionaries.

- Progressive Tax Verification: Testing the calculate_paye and calculate_usc functions against various income thresholds to ensure standard rates, marginal rates, and tiered social charges are applied accurately.

- Precision Arithmetic Validation: Using the Decimal library within test cases to confirm that currency calculations for gross pay and overtime are exact and free from floating-point errors.

- Automated Suite Execution: Running a comprehensive suite of seven distinct tests (including test_calculate_overtime and multiple USC tiers) to confirm that recent code changes haven't introduced regressions.

- Result Verification: Comparing functional outputs against manually calculated "Expected Results" to ensure the application "works as intended" before generating final payslips and summary reports.
