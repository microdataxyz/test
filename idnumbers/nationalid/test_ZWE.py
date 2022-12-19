from unittest import TestCase, main

from idnumbers.nationalid import ZWE


class TestNGAValidation(TestCase):
    def test_normal_case(self):
        self.assertTrue(ZWE.NationalID.validate('75191961R00'))
        self.assertTrue(ZWE.NationalID.validate('751919620S86'))

    def test_error_case(self):
        self.assertFalse(ZWE.NationalID.validate('75191962R00'))
        self.assertFalse(ZWE.NationalID.validate('00191962R58'))
        self.assertFalse(ZWE.NationalID.validate('40191962R75'))

    def test_parse_11_digits(self):
        result = ZWE.NationalID.parse('75191961R00')
        self.assertEqual('75', result['register_office_code'])
        self.assertEqual('191961', result['national_num'])
        self.assertEqual('R', result['check_letter'])
        self.assertEqual('00', result['district_code'])

    def test_parse_12_digits(self):
        result = ZWE.NationalID.parse('751910961R58')
        self.assertEqual('75', result['register_office_code'])
        self.assertEqual('1910961', result['national_num'])
        self.assertEqual('R', result['check_letter'])
        self.assertEqual('58', result['district_code'])


if __name__ == '__main__':
    main()