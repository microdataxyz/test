# idnumbers
National ID verification libs

* [![PyPI version](https://badge.fury.io/py/idnumbers.svg)](https://badge.fury.io/py/idnumbers)
* [![PyPI Stats](https://img.shields.io/pypi/dm/idnumbers)](https://pypistats.org/packages/idnumbers)

This project in early phase. We might change the interface. Please wait our changelogs for more information.

## Verify National IDs

All modules under nationalid package support the `validate` function.

```python
from idnumbers.nationalid import AUS, NGA, ZAF

# verify AUS tax file number (with checksum code)
AUS.TaxFileNumber.validate('32547689')

# verify AUS driver license number
AUS.DriverLicenseNumber.validate('12 345 678')

# verify AUS Medicare number (with checksum code)
AUS.MedicareNumber.validate('2123 45670 1')

# verify NGA national id number
NGA.NationalID.validate('12345678901')

# verify ZAF nation id number
ZAF.NationalID.validate('7605300675088')
```

## Parse National IDs

Some modules whose `METADATA.parsable == true` support the `parse` function. It unpacks the detail data from the
national id.

```python
from idnumbers.nationalid import ZAF

assert ZAF.NationalID.METADATA.parsable == True
# parse the national id
id_data = ZAF.NationalID.parse('7605300675088')
# access the date of birth, gender, and citizenship
print(id_data['yyyymmdd'])
print(id_data['gender'])
print(id_data['citizenship'])
```

# Supported Country List:

* ARE - United Arab Emirates
* ARG - Argentina 
* AUS - Australia
* BEL - Belgium
* BRA - Brazil
* CAN - Canada
* CHE - Switzerland / Swiss
* CHL - Chile
* CHN - China
* ESP - Spain
* FRA - France
* GBR - United Kingdom of Great Britain and Northern Ireland
* HKG - Hong Kong
* IDN - Indonesia
* IND - India
* IRL - Ireland
* JPN - Japan
* KOR - South Korea
* LKA - Sri Lanka
* MEX - Mexico
* MYS - Malaysia
* NGA - Nigeria
* NLD - Netherlands
* NOR - Norway
* NZL - New Zealand
* PHL - Philippine
* SGP - Singapore
* THA - Thailand
* TWN - Taiwan
* UKR - Ukraine
* USA - United States
* VNM - Viet Nam
* ZAF - South Africa
* ZWE - Zimbabwe
