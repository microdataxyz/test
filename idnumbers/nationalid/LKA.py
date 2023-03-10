import re
from datetime import date, timedelta
from types import SimpleNamespace
from typing import Literal, Optional, TypedDict
from .util import modulus_check, modulus_overflow_mod10, validate_regexp
from .constant import Citizenship, Gender


class ParseResult(TypedDict):
    yyyymmdd: date
    gender: Gender
    sn: str
    checksum: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


class OldIDParseResult(ParseResult):
    citizenship: Citizenship


class NationalID:
    """
    LKA National ID number format
    # https://en.wikipedia.org/wiki/National_identification_number#Sri_Lanka
    # https://lk.linkedin.com/posts/nuwansenaratna_srilanka-activity-6926883712584335360-E_69
    # https://drp.gov.lk/Templates/Artical%20-%20English%20new%20number.html
    """
    METADATA = SimpleNamespace(**{
        'iso3166_alpha2': 'LK',
        'min_length': 12,
        'max_length': 12,
        'parsable': True,
        'checksum': True,
        'regexp': re.compile(r'^(?P<year>\d{4})'
                             r'(?P<days>\d{3})'
                             r'(?P<sn>\d{4})'
                             r'(?P<checksum>\d)$')
    })

    MAGIC_MULTIPLIER = [8, 4, 3, 2, 7, 6, 5, 7, 4, 3, 2]

    @staticmethod
    def validate(id_number: str) -> bool:
        """
        Validate the LKA id number
        """
        if not validate_regexp(id_number, NationalID.METADATA.regexp):
            return False
        return NationalID.parse(id_number) is not None

    @staticmethod
    def parse(id_number: str) -> Optional[ParseResult]:
        match_obj = NationalID.METADATA.regexp.match(id_number)
        if not match_obj:
            return None
        year = int(match_obj.group('year'))
        days = int(match_obj.group('days'))
        sn = match_obj.group('sn')
        checksum = NationalID.checksum(id_number)
        if not checksum:
            return None
        else:
            yyyymmdd = date(year, 1, 1) + timedelta(days - 501 if days > 500 else days - 1)
            return {
                'yyyymmdd': yyyymmdd,
                'gender': Gender.MALE if days < 500 else Gender.FEMALE,
                'sn': sn,
                'checksum': int(match_obj.group('checksum'))
            }

    @staticmethod
    def checksum(id_number) -> bool:
        if not validate_regexp(id_number, NationalID.METADATA.regexp):
            return False
        # it uses modulus 11 algorithm with magic numbers
        numbers = [int(char) for char in id_number]
        modulus = modulus_overflow_mod10(modulus_check(numbers[:-1], NationalID.MAGIC_MULTIPLIER, 11))
        return modulus == numbers[-1]


class OldNationalID:
    """
    LKA old National ID number format which is phased out on 2016
    # https://en.wikipedia.org/wiki/National_identification_number#Sri_Lanka
    # https://drp.gov.lk/Templates/Artical%20-%20English%20new%20number.html
    """
    METADATA = SimpleNamespace(**{
        'iso3166_alpha2': 'LK',
        'min_length': 10,
        'max_length': 10,
        'parsable': True,
        'checksum': True,
        'regexp': re.compile(r'^(?P<year>\d{2})'
                             r'(?P<days>\d{3})'
                             r'(?P<sn>\d{3})'
                             r'(?P<checksum>\d)'
                             r'(?P<citizenship>[XxVv])$')
    })

    @staticmethod
    def to_new(id_number: str) -> Optional[str]:
        match_obj = OldNationalID.METADATA.regexp.match(id_number)
        if not match_obj:
            return None
        year = match_obj.group('year')
        days = match_obj.group('days')
        sn = match_obj.group('sn')
        checksum = match_obj.group('checksum')
        return f'19{year}{days}0{sn}{checksum}'

    @staticmethod
    def validate(id_number: str) -> bool:
        """
        Validate the TWN id number
        """
        if not id_number:
            return False

        if not isinstance(id_number, str):
            id_number = repr(id_number)
        return OldNationalID.parse(id_number) is not None

    @staticmethod
    def parse(id_number: str) -> Optional[OldIDParseResult]:
        new_id_num = OldNationalID.to_new(id_number)
        if not new_id_num:
            return None
        result = NationalID.parse(new_id_num)
        if not result:
            return None
        citizenship = Citizenship.CITIZEN if id_number[-1].upper() == 'V' else Citizenship.RESIDENT
        return {
            **result,
            'citizenship': citizenship
        }

    @staticmethod
    def checksum(id_number) -> bool:
        new_id_num = OldNationalID.to_new(id_number)
        if not new_id_num:
            return False
        return NationalID.checksum(new_id_num)
