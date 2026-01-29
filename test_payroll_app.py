import unittest
from unittest import mock
from payroll_app import read_csv, calculate_paye, calculate_usc, calculate_overtime
from decimal import Decimal

class TestPayrollApp(unittest.TestCase):

    def test_read_csv_with_string_field(self):
        """Test read_csv function with string field using mock Open"""
        csv_content = """PPSN,name,hours,rate
1234567A,John Doe,40,25.00
8765432B,Siobhan O'Neill,35,30.00"""

        with mock.patch('builtins.open', mock.mock_open(read_data=csv_content)):
            result = {}
            read_csv('dummy.csv', result, ['name', 'hours', 'rate'])
            self.assertEqual(result['1234567A']['name'], 'John Doe')
            self.assertEqual(result['8765432B']['name'], "Siobhan O'Neill")
    
    def test_calculate_paye_below_cutoff(self):
        """Test calculate_paye function for gross income below cutoff"""
        gross = Decimal('800')
        paye = calculate_paye(gross)
        expected_paye = ((gross * 52) * Decimal('0.20') - Decimal('3750'))
        self.assertEqual(paye, expected_paye)
    
    def test_calculate_paye_above_cutoff(self):
        """Test calculate_paye function for gross income above cutoff"""
        gross = Decimal('1000')
        paye = calculate_paye(gross)
        expected_paye = ((Decimal('44000') * Decimal('0.20') + (gross * 52 - Decimal('44000')) * Decimal('0.40') - Decimal('3750')))
        self.assertEqual(paye, expected_paye)

    def test_calculate_usc_tier1(self):
        """Test calculate_usc function for gross income in tier 1"""
        gross = Decimal('200')
        usc = calculate_usc(gross)
        expected_usc = (gross * 52 * Decimal('0.005'))
        self.assertEqual(usc, expected_usc)

    def test_calculate_usc_tier2(self):
        """Test calculate_usc function for gross income in tier 2"""
        gross = Decimal('400')  
        usc = calculate_usc(gross)
        
        tier1 = Decimal('12012')
        t1_tax = tier1 * Decimal('0.005')
        t2_tax = ((gross * 52) - tier1) * Decimal('0.02')
        
        expected_usc = t1_tax + t2_tax
        self.assertEqual(usc, expected_usc)

    def test_calculate_usc_above_tier2(self):
        """Test calculate_usc function for gross income above tier 2"""
        gross = Decimal('1000')
        usc = calculate_usc(gross)
        tier1 = Decimal('12012')
        tier2 = Decimal('28700')
        expected_usc = ((tier1 * Decimal('0.005') + (tier2 - tier1) * Decimal('0.02') + ((gross * 52 - tier2) * Decimal('0.04'))))
        self.assertEqual(usc, expected_usc)

    def test_calculate_overtime(self):
        """Test calculate_overtime function"""
        hours = 50
        hours_scheduled = 40
        rate = Decimal('20.00')
        overtime_pay = calculate_overtime(hours, hours_scheduled, rate)
        expected_overtime_pay = (hours - hours_scheduled) * rate * Decimal('1.5')
        self.assertEqual(overtime_pay, expected_overtime_pay)
    
    if __name__ == '__main__':
        unittest.main()