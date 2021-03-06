#!/usr/bin/python3

import unittest
from datetime import datetime
from utils import (distance, extract_name_parts, extract_phone, extract_date,
                   normalize_name, CSV_Generator, translit)
from friends import Friend


class TestUtlis(unittest.TestCase):
    def test_distance(self):
        self.assertEqual(distance('aaab', 'abab'), 1)
        self.assertEqual(distance('', 'aaa'), 3)
        self.assertEqual(distance('aaa', 'aaa'), 0)
        self.assertEqual(distance('aa', 'aaa'), 1)
        self.assertEqual(distance('aaa', 'aa'), 1)
        self.assertEqual(distance('', ''), 0)
        self.assertEqual(distance('фвы', 'фв'), 1)

    def test_extract_name_parts(self):
        self.assertEqual(extract_name_parts('Павел Дуров'), ('Павел', 'Дуров'))
        self.assertEqual(extract_name_parts(''), ('', ''))
        self.assertEqual(extract_name_parts('Pavel'), ('Pavel', ''))
        self.assertEqual(extract_name_parts('Pa ve l'), ('Pa', 've l'))

    def test_phone_extraction(self):
        self.assertEqual(extract_phone('88005553535'), '88005553535')
        self.assertEqual(extract_phone('Мой номер: 686332'), '686332')
        self.assertEqual(extract_phone('Случайное число 228'), '')
        self.assertEqual(extract_phone(''), '')
        self.assertEqual(extract_phone('8(800)-555-35-35'), '88005553535')

    def test_date_extraction(self):
        self.assertEqual(extract_date('02.01.2010'),
                         datetime(2010, 1, 2).date())
        self.assertEqual(extract_date('2.1.2010'),
                         datetime(2010, 1, 2).date())
        self.assertEqual(extract_date('2.1.20100'), '')
        self.assertEqual(extract_date('2.1.20'), '')
        self.assertEqual(extract_date(''), '')

    def test_name_normalisation(self):
        self.assertEqual(normalize_name('Ivan Petrov'), 'Иван Петров')
        self.assertEqual(normalize_name('ivan petrov'), 'Иван Петров')
        self.assertEqual(normalize_name('iVaN pEtRoV'), 'Иван Петров')
        self.assertEqual(normalize_name('  iVaN pEtRoV  '), 'Иван Петров')

    def test_csv_generator(self):
        csv_fields = {
            'a': 'A',
            'b': 'B',
            'c': 'C',
        }
        csv_file = CSV_Generator(csv_fields)
        csv_file.set_titles(**csv_fields)
        csv_file.add_values(a=1, b=2, c=3)
        csv_file.add_values(a=11, b=12, c=13)
        result = str(csv_file)
        expected_result = 'A,B,C\n1,2,3\n11,12,13\n'

        self.assertEqual(result, expected_result)

    def test_translit(self):
        self.assertEqual(translit('olia'), 'оля')
        self.assertEqual(translit('misha'), 'миша')
        self.assertEqual(translit('lorem ipsum'), 'лорем ипсум')
        self.assertEqual(translit('some string'), 'соме стринг')
        self.assertEqual(translit('fish sticks'), 'фиш стиcкс')


class TestMergerUtils(unittest.TestCase):
    def test_is_mergeble_with_empty(self):
        friend1 = Friend(full_name='Lorem Ipsum', first_name='Lorem',
                         second_name='Ipsum', phone='+7904424242')
        friend2 = Friend()
        self.assertEqual(friend1.is_mergeble(friend2), True)

    def test_is_mergeble_with_subset(self):
        friend1 = Friend(full_name='Lorem Ipsum', first_name='Lorem',
                         second_name='Ipsum', phone='+7904424242')
        friend2 = Friend(full_name='Lorem Ipsum', first_name='Lorem',)
        self.assertEqual(friend1.is_mergeble(friend2), True)

    def test_is_mergeble_with_empty_fields(self):
        friend1 = Friend(full_name='Lorem Ipsum', first_name='Lorem',
                         second_name='Ipsum', phone='+7904424242')
        friend2 = Friend(full_name='', first_name='',)
        self.assertEqual(friend1.is_mergeble(friend2), True)

    def test_is_mergeble_wrong(self):
        friend1 = Friend(full_name='Lorem Ipsum', first_name='Lorem',
                         second_name='Ipsum', phone='+7904424242')
        friend2 = Friend(full_name='1', first_name='Lorem',)
        self.assertEqual(friend1.is_mergeble(friend2), False)

    def test_is_subset(self):
        friend1 = Friend(full_name='Lorem Ipsum', first_name='Lorem',
                         second_name='Ipsum', phone='+7904424242')
        friend2 = Friend(full_name='', first_name='Lorem',)
        self.assertEqual(friend1.is_mergeble(friend2), True)

    def test_is_subset_wrong(self):
        friend1 = Friend(full_name='Lorem Ipsum', first_name='Lorem',
                         second_name='Ipsum', phone='+7904424242')
        friend2 = Friend(full_name='Ipsum', first_name='Lorem',)
        self.assertEqual(friend1.is_mergeble(friend2), False)


class TestMerging(unittest.TestCase):
    def test_auto_merging_with_empty(self):
        friend1 = Friend(full_name='Lorem Ipsum', first_name='Lorem',
                         second_name='Ipsum', phone='+7904424242')
        friend2 = Friend()
        self.assertEqual(friend1.merge(friend2), friend1)

    def test_auto_merging_with_subset(self):
        friend1 = Friend(full_name='Lorem Ipsum', first_name='Lorem',
                         second_name='Ipsum', phone='+7904424242')
        friend2 = Friend(full_name='Lorem Ipsum', first_name='Lorem',)
        self.assertEqual(friend1.merge(friend2), friend1)

    def test_auto_merging_with_empty_fields(self):
        friend1 = Friend(full_name='Lorem Ipsum', first_name='Lorem',
                         second_name='Ipsum', phone='+7904424242')
        friend2 = Friend(full_name='', first_name='',)
        self.assertEqual(friend1.merge(friend2), friend1)

    def test_is_similar1(self):
        friend1 = Friend(full_name='Lorem Ipsum', first_name='Lorem',
                         second_name='Ipsum', phone='+7904424242')
        friend2 = Friend(full_name='Lorem Ipsum', first_name='Lorem',
                         second_name='Ipsum', phone='+7904424242')
        self.assertEqual(friend1.is_similar(friend2), True)

    def test_is_similar2(self):
        friend1 = Friend(full_name='Lorem Ipsum', first_name='Lorem',
                         second_name='Ipsum', phone='+7904424242')
        friend2 = Friend(full_name='Lorem Ipsum', first_name='Lorem',
                         second_name='Ipsum', phone='')
        self.assertEqual(friend1.is_similar(friend2), True)

    def test_is_similar3(self):
        friend1 = Friend(full_name='Lorem Ipsum', first_name='Lorem',
                         second_name='Ipsum', phone='+7904424242')
        friend2 = Friend(full_name='Lorem Ipsum', first_name='Lorem')
        self.assertEqual(friend1.is_similar(friend2), True)

    def test_is_similar4(self):
        friend1 = Friend(full_name='Lore Ipsim', first_name='Lore',
                         second_name='Ipsim')
        friend2 = Friend(full_name='Lorem Ipsum', first_name='Lorem',
                         phone='+7904424242')
        self.assertEqual(friend1.is_similar(friend2), True)

    def test_is_similar5(self):
        friend1 = Friend(full_name='Lora Ipsim', first_name='Lora',
                         second_name='Ipsimasdasdsa', phone='+72283222131')
        friend2 = Friend(full_name='Lorem Ipsum', first_name='Lorem',
                         phone='+7904424242')
        self.assertEqual(friend1.is_similar(friend2), False)


if __name__ == '__main__':
    unittest.main()
