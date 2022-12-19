import re
from types import SimpleNamespace
from typing import TypedDict


class ParseResult(TypedDict):
    register_office_code: str
    national_num: str
    check_letter: str
    district_code: str


class NationalID:
    """
    Argentina National ID number
    https://www.protecto.ai/argentina-national-identity-number-download-sample-data-for-testing/
    https://en.wikipedia.org/wiki/Documento_Nacional_de_Identidad_(Argentina)
    """
    METADATA = SimpleNamespace(**{
        'iso3166_alpha2': 'AR',
        'min_length': 10,
        'max_length': 10,
        'parsable': False,
        'regexp': re.compile(r'^(?P<first_section>[0-9][0-9])'
                             r'([.])'
                             r'(?P<second_section>[0-9][0-9][0-9])'
                             r'([.])'
                             r'(?P<third_section>[0-9][0-9][0-9])$')
    })

    @staticmethod
    def validate(id_number: str) -> bool:
        """
        Validate the ARG id number
        """
        if not isinstance(id_number, str):
            id_number = repr(id_number)
        return NationalID.METADATA.regexp.search(id_number) is not None