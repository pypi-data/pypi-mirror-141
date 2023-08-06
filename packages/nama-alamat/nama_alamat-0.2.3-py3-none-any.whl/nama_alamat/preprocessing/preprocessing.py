"""_summary_.

Returns:
    _type_: _description_
"""

# import library
import os
import re
from functools import reduce

import roman

# membuat dictionary untuk preprocessing nama dan alamat
dict_alamat = {}
dict_nama = {}

here = os.path.dirname(os.path.abspath(__file__))

# menambahkan tiap baris dari file txt ke dictionary
with open(os.path.join(here, 'dict_files', 'dict_alamat.txt'), 'r') as file:
    for line in file:
        key, value = line.replace('\'', '').rstrip('\n').split(':')
        dict_alamat[key] = value

with open(os.path.join(here, 'dict_files', 'dict_nama.txt'), 'r') as file:
    for line in file:
        key, value = line.replace('\'', '').rstrip('\n').split(':')
        dict_nama[key] = value


class Preprocessing:
    """_summary_."""

    def __init__(self, tipe='alamat'):
        """_summary_.

        Args:
            tipe (str, optional): _description_. Defaults to 'alamat'.
        """
        self.tipe = tipe

    # standarisasi penulisan nama dan alamat
    def standardize(self, strings):
        """_summary_.

        Args:
            strings (_type_): _description_

        Returns:
            _type_: _description_
        """
        tipe = self.tipe
        if tipe == 'alamat':
            result = " ".join(dict_alamat.get(ele, ele) for ele in strings.split())
        else:
            result = re.sub(r'\s', '_', strings)
            for i, k in dict_nama.items():
                str_from = '(_|^)' + i + '(_|$)'
                str_to = '_' + k + '_'
                result = re.sub(str_from, str_to, result)
            result = re.sub('_', ' ', result)
        return result

    def preprocessing(self, strings):
        """_summary_.

        Args:
            strings (_type_): _description_

        Returns:
            _type_: _description_
        """
        tipe = self.tipe

        # kata-kata tidak berguna
        stopword = [
            'please specify',
            'hold mail',
            'holdmail',
            'dummy',
            'unknown',
            'middlename',
            'npwp',
            'qq',
            'sp_xplor',
            'null',
            'anonymous',
            'not_associate',
        ]

        if isinstance(strings, str):
            # lowercase
            result = strings.lower()

            # remove non ascii chars
            result = re.sub(r'[^\x00-\x7f]', '', result)

            # remove inside bracket
            result = re.sub(r'\([^)]*\)', '', result)

            # remove stopword
            # for i in stopword:
            #     result = re.sub(i,'',result)
            result = reduce(lambda a, b: a.replace(b, ''), stopword, result)

            if tipe == 'nama':
                # remove number
                result = re.sub(r'\d+', '', result)
            if tipe == 'alamat':
                # remove kodepos
                result = re.sub(r' \d\d\d\d\d', '', result)

            # remove punctuation
            result = re.sub(r'[^\w\s]', ' ', result)

            # remove whitespace
            result = result.strip()

            # remove double space
            result = re.sub(r'\s+', ' ', result)

            # remove old style name 'A L I'
            if re.match(r'^(?:\w ){2,}[A-z]($|\W)', result):
                result = ''.join(result.split())

            # standardize
            result = self.standardize(result)

            # remove whitespace
            result = result.strip()

            # remove double space
            result = re.sub(r'\s+', ' ', result)

            # hapus nama 1 kata diulang
            if tipe == 'nama':
                len_nama = len(result.split())
                if len_nama == 2 and result.split()[0] == result.split()[1]:
                    result = result.split()[0]

            # roman to arabic
            if tipe == 'alamat':
                result = ' '.join(
                    [
                        str(roman.fromRoman(x))
                        if re.match("(^(?=[MDCLXVI])M*(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[XV]|V?I{0,3})$)", x)
                        else x
                        for x in result.upper().split()
                    ]
                ).lower()

            return result
        else:
            return strings
