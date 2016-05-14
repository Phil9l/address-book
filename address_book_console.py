#!/usr/bin/python3

import contextlib
import sys
from argparse import ArgumentParser
from address_book import AddressBook
from friends import Friend, VK_Friend, Twitter_Friend
from utils import get_input
from utils import VK_API, Twitter_API


def get_arguments():
    parser = ArgumentParser(description='usage: %prog [options]')
    parser.add_argument(
        '--vk', dest='vk_id', help='vk user ID (e.g. 44232785)',
        type=int, metavar='id', required=True
    )
    parser.add_argument(
        '--twitter', dest='twitter_id', help='Twitter user ID (e.g. 44)',
        type=int, metavar='id', required=True
    )
    parser.add_argument(
        '--output', dest='output', help='Output file (e.g. tmp.csv)',
        metavar='FILE'
    )
    return parser.parse_args()


@contextlib.contextmanager
def file_open(filename=None):
    opened_file = open(filename, 'w') if filename else sys.stdout
    try:
        yield opened_file
    finally:
        if opened_file is not sys.stdout:
            opened_file.close()


class MyApp(AddressBook):
    def __init__(self, vk_id, twitter_id, csv_fields):
        super(MyApp, self).__init__()
        self.vk_id = vk_id
        self.twitter_id = twitter_id
        self.friend_list = []
        self.csv_fields = csv_fields

    def _wrong_id(self):
        print('Wrong ID')

    def save_CSV(self, filename=None):
        with file_open(filename) as f:
            f.write(self._generate_CSV(self.csv_fields, self.friend_list))

    def get_friends(self):
        self.friend_list = self._get_friends(
            self.vk_id, VK_API(), VK_Friend
        ) + self._get_friends(self.twitter_id, Twitter_API(), Twitter_Friend)

    def _merge_friends(self, friend1, friend2):
        print('These friends seem to be equal.')
        print('First friend:')
        print(friend1)
        print()
        print('Second friend:')
        print(friend2)
        if get_input('Merge them?') != 'y':
            return None
        print()

        result = Friend(**vars(friend1))
        for attr in vars(friend1):
            if getattr(friend1, attr) != getattr(friend2, attr):
                if getattr(friend1, attr) == '':
                    setattr(result, attr, getattr(friend2, attr))
                elif getattr(friend2, attr) == '':
                    setattr(result, attr, getattr(friend1, attr))
                else:
                    print('Difference in {} field:'.format(
                        self.csv_fields[attr])
                    )
                    print('User1 value: {} | User2 value: {}'.format(
                        getattr(friend1, attr), getattr(friend2, attr)
                    ))
                    res = get_input('What field is preferable?', ('1', '2'))
                    if res == '2':
                        setattr(result, attr, getattr(friend2, attr))
        print('____________________')
        return result

    def merge_friend_list(self):
        self.friend_list = self._merge_friend_lists(self.friend_list)


if __name__ == '__main__':
    argsuments = get_arguments()
    csv_fields = {
        'full_name': 'Name',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'bdate': 'Birthday',
        'phone': 'Mobile Phone',
        'email': 'E-mail Address',
    }
    app = MyApp(argsuments.vk_id, argsuments.twitter_id, csv_fields)
    app.get_friends()
    app.merge_friend_list()
    app.save_CSV(argsuments.output)
