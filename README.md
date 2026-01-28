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
PPSN, hours
1234567A, 36
```

#### Rate

```csv
PPSN, Rate
1234567A, 15
```

## Output format

### 1. Payroll table

| Employee no | Employee | Department | Hours | Gross Pay | Net Take-Home | Tax Liability |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | John Doe | IT | 40 | €620.00 | €557.82 | €62.18 |

| Description | Total Amount |
| :--- | :--- |
| **Total Gross Payroll** | **€4,249.75** |
| **Total Net Pay** | **€3,449.09** |
| **Total Tax** | **€800.66** |


### 2. Payslip
| Employee Details | | | | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Payroll Period Info | |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Name:** | John Doe | **Emp No:** | 1 | | **Date:** | 28/01/2026 |
| **PPSN:** | 1234567A | **Department:** | IT | | **Pay Week** | 5 |

| Description | Amount | Deductions | Amount |
| :--- | :--- | :--- | :--- |
| **Gross Pay** | **€620.00** | PAYE | €51.88 |
| | | USC | €10.30 |
| --- | --- | --- | --- |
| **Total Earnings** | **€620.00** | **Total Tax** | **€62.18** |
**NET PAY: €557.82**

## Testing Approach

The approach to testing this application will be multifaceted but primarily focus on the concept of unit testing, where each individual function is tested in isolation with a set of predetermined inputs to verify that the output matches expected results. This will involve:

- Logic Verification: Passing a known annual salary (e.g., €50,000) into calculate_paye() and ensuring the returned number matches a manual calculation based on Irish Revenue thresholds.

- Boundary Testing: Testing the "Cut-off" points (like exactly €44,000) to ensure the if/else logic switches between the 20% and 40% brackets correctly.

- Data Integrity: Verifying that the read_csv() function correctly handles missing values or non-numeric strings by returning a default value (e.g., Decimal('0')) instead of crashing the program.

- Regression Testing: Ensuring that a fix in the USC calculation does not accidentally break the Net Pay calculation by running the full suite of unit tests after every code change.
