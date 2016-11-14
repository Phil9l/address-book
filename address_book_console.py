#!/usr/bin/python3

import contextlib
import sys
from argparse import ArgumentParser
from address_book import AddressBook
from friends import Friend, VK_Friend, Twitter_Friend
from utils import get_input, VK_API, Twitter_API
from TwitterAPI import TwitterError


def get_arguments():
    parser = ArgumentParser(description='usage: %prog [options]')
    group = parser.add_argument_group()
    group.add_argument('-v', '--vk', dest='vk_id', type=int,
                       help='vk user ID (e.g. 44232785)', metavar='id')
    group.add_argument('-t', '--twitter', dest='twitter_id', type=int,
                       help='Twitter user ID (e.g. 44)', metavar='id')
    parser.add_argument('--output', dest='output',
                        help='Output file (e.g. tmp.csv)', metavar='FILE')

    args = parser.parse_args()

    if args.twitter_id is None and args.vk_id is None:
        parser.error('At least one social network is required')

    return args


@contextlib.contextmanager
def file_open(filename=None):
    opened_file = open(filename, 'w') if filename else sys.stdout
    try:
        yield opened_file
    finally:
        if opened_file is not sys.stdout:
            opened_file.close()


class MyApp(AddressBook):
    def __init__(self, csv_fields, vk_id=None, twitter_id=None):
        sys.stderr.write('Initializing...\n')
        super(MyApp, self).__init__()
        self.vk_id = vk_id
        self.twitter_id = twitter_id
        self.friend_list = []
        self.csv_fields = csv_fields

    def _wrong_id(self):
        sys.stderr.write('Wrong ID\n'.format())
        if get_input('Do you want to continue?') == 'n':
            exit(1)


    def save_CSV(self, filename=None):
        with file_open(filename) as f:
            f.write(self._generate_CSV(self.csv_fields, self.friend_list))

    def get_friends(self):
        if self.vk_id is not None:
            sys.stderr.write('Getting VK friends...\n')
            self.friend_list = self._get_friends(self.vk_id, VK_API(),
                                                 VK_Friend)
        try:
            if self.twitter_id is not None:
                sys.stderr.write('Getting Twitter friends...\n')
                self.friend_list += self._get_friends(self.twitter_id,
                                                      Twitter_API(),
                                                      Twitter_Friend)
        except TwitterError.TwitterRequestError:
            self._wrong_id()

    def _merge_friends(self, friend1, friend2):
        sys.stderr.write('These friends seem to be equal.\n')
        sys.stdout.write('First friend:\n')
        sys.stdout.write(str(friend1))
        sys.stdout.write('\n__________________\n')
        sys.stdout.write('Second friend:\n')
        sys.stdout.write(str(friend2))
        if get_input('\nDo you want to merge them?') != 'y':
            return None
        sys.stdout.write('\n')

        result = Friend(**vars(friend1))
        for attr in vars(friend1):
            if getattr(friend1, attr) != getattr(friend2, attr):
                if getattr(friend1, attr) == '':
                    setattr(result, attr, getattr(friend2, attr))
                elif getattr(friend2, attr) == '':
                    setattr(result, attr, getattr(friend1, attr))
                else:
                    sys.stdout.write('Difference in {} field:\n'.format(
                        self.csv_fields[attr]))
                    sys.stdout.write(
                        'User1 value: {} | User2 value: {}\n'.format(
                            getattr(friend1, attr), getattr(friend2, attr)))
                    res = get_input('What field is preferable?', ('1', '2'))
                    if res == '2':
                        setattr(result, attr, getattr(friend2, attr))
        sys.stdout.write('____________________')
        return result

    def merge_friend_list(self):
        sys.stderr.write('Merging friends...\n')
        set_percentage = lambda x: sys.stderr.write('{}%\r'.format(int(x)))
        self.friend_list = self._merge_friend_lists(self.friend_list,
                                                    set_percentage)


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
    app = MyApp(csv_fields, vk_id=argsuments.vk_id,
                twitter_id=argsuments.twitter_id)
    app.get_friends()
    app.merge_friend_list()
    app.save_CSV(argsuments.output)
