"""Convert to and from Roman numerals

This program is part of "Dive Into Python", a free Python book for
experienced programmers.  Visit http://diveintopython.org/ for the
latest version.
"""

__author__ = "Mark Pilgrim (mark@diveintopython.org)"
__version__ = "$Revision: 1.2 $"
__date__ = "$Date: 2004/05/05 21:57:20 $"
__copyright__ = "Copyright (c) 2001 Mark Pilgrim"
__license__ = "Python"

import re

#Define exceptions
class RomanError(Exception): pass


class OutOfRangeError(RomanError): pass


class NotIntegerError(RomanError): pass


class InvalidRomanNumeralError(RomanError): pass

roman_numeral_lookup = ((100, 'CM', 'D', 'CD', 'C'),
          (10, 'XC', 'L', 'XL', 'X'),
          (1, 'IX', 'V', 'IV', 'I'))

def toRoman(n):
    """convert integer to Roman numeral"""
    if n >= 4000 or n <= 0:
        raise OutOfRangeError
    elif not isinstance(n, int):
        raise NotIntegerError

    romanNumeral = ''

    romanNumeral += n / 1000 * "M"

    for modulus, nines, fives, fours, ones in roman_numeral_lookup:
        digit = n % (modulus * 10) / modulus
        if digit <= 3:
            romanNumeral += digit * ones
        elif digit == 4:
            romanNumeral += fours
        elif digit == 9:
            romanNumeral += nines
        else:
            romanNumeral += fives + (digit - 5) * ones

    return romanNumeral




def fromRoman(s):
    """convert Roman numeral to integer"""
    if not re.match('^M?M?M?(CM|CD|D?C?C?C?)(XC|XL|L?X?X?X?)(IX|IV|V?I?I?I?)$', s):
        raise InvalidRomanNumeralError, 'Invalid Roman numeral: %s' % s

    number = 0
    thousands = len(re.findall('^M*', s)[0])
    if thousands > 0:
        number += thousands * 1000
        s = s[thousands:]

    for multiplier, nines, fives, fours, ones in roman_numeral_lookup:
        if re.findall('^%s' % nines, s):
            number += (9 * multiplier)
            s = s[2:]

        if re.findall('^%s' % fives, s):
            number += (5 * multiplier)
            s = s[1:]

        if re.findall('^%s' % fours, s):
            number += (4 * multiplier)
            s = s[2:]

        if re.findall('^%s' % ones, s):
            oneses = len(re.findall('^%s*' % ones, s)[0])
            number += (oneses * multiplier)
            s = s[oneses:]

    return number

