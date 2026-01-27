# Software Design Document

**Payroll processing app**

Séaghan Fisher

- [Software Design Document](#software-design-document)
  - [Program Overview](#program-overview)
  - [Program Requirements](#program-requirements)
    - [Functional Requirements](#functional-requirements)
    - [Technical Requirements](#technical-requirements)
    - [Input format](#input-format)
      - [PPSN](#ppsn)
      - [Timetable](#timetable)
      - [Rate](#rate)
    - [Output format](#output-format)
      - [Payroll table](#payroll-table)
  - [Testing Approach](#testing-approach)

## Program Overview

The payroll processing application is a software that assists users in processing multiple CSV files and converting them into a readable table of employee payroll information. Users can upload CSV files of employee information (including personal info, timetables, pay rate, and bonuses) into the program to process the data, perform calculations, and return a structured table in a readable format. The software aims to provide a simple and efficient way to process employee payroll information and create a single table with all relevant data.

The application will be developed using the Python programming language in conjunction with the procedural design philosophy.

## Program Requirements

### Functional Requirements

- Read timetable, rate, and PPSN from CSV
- Calculate salary
- Calculate tax (PAYE and USC)
- Calculate salary after tax
- Calculate weekly income before and after tax
- Pivot table with all the calculated data
- Payslip for every worker

### Technical Requirements

- Platform: cross-platform (Windows, Linux, MacOS)
- Language: Developed Python, ensuring wide support and maintainability
- Database: CSV files

### Input format

#### PPSN

```csv
PPSN, Name
1234567A, John Doe
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

### Output format

#### Payroll table

| Name | PPSN | Weekly Gross | Weekly PAYE | Weekly USC | Weekly Net | Yearly Gross | Yearly PAYE | Yearly USC | Yearly Net |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| John Doe | 1234567A | €1,000.00 | €25.00 | €5.00 | €970.00 | €52,000.00 | €1,300.00 | €260.00 | €50,440.00 |

## Testing Approach

The approach to testing this application will be multifaceted but primarily focus on the concept of unit testing, where each individual function is tested in isolation with a set of predetermined inputs to verify that the output matches expected results. This will involve:

- Logic Verification: Passing a known annual salary (e.g., €50,000) into calculate_paye() and ensuring the returned number matches a manual calculation based on Irish Revenue thresholds.

- Boundary Testing: Testing the "Cut-off" points (like exactly €44,000) to ensure the if/else logic switches between the 20% and 40% brackets correctly.

- Data Integrity: Verifying that the read_csv() function correctly handles missing values or non-numeric strings by returning a default value (e.g., Decimal('0')) instead of crashing the program.

- Regression Testing: Ensuring that a fix in the USC calculation does not accidentally break the Net Pay calculation by running the full suite of unit tests after every code change.
