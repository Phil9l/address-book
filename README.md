# Address Book
## Description
Downloads data about friends from social networks (vk.com and twitter) and makes CSV file for exporting into google contacts.

## Usage
`./address_book_console.py --vk VK_ID --twitter Twitter_ID [--output FILE]`
or
`./address_book_gui.py` and then add `VK` and `Twitter` friends. Then click `merge`. And, finally, `save` button.

### Example
`./address_book_console.py --vk 44232785 --twitter 891227432`

### Options
* `--vk id` — id of vk.com user, whose friends would be imported
* `--twitter id` — id of twitter user, whose friends would be imported
* `--output filename` — name of CSV file

## Requirements
* `pip3 install TwitterAPI`

## Structure
### tests.py
Test for this project
### utils.py
Subsidiary functions.
* `translit(string)` — translitirates `string` from English to Russian
* `distance(a, b)` — Calculates the Levenshtein distance between a and b
* `extract_name_parts(fullname)` — splits `fullname` into first name and last name
* `extract_phone(input_string)` — extracts phone number from `input_string`
* `extract_date(input_string)` — extracts datetime from `input_string`
* `normalize_name(input_string)` — extracts datetime from `input_string`
* `get_input(question, choice=('y', 'n'))` — prints `question` into console until the answer isn't in `choice`
* `equal(val1, val2)` — returns similarity coefficient of `val1` and `val2`
* `absolutely_equal(val1, val2)` — return 1 if `val1` is equal to `val2` and 0 otherwise
* `VK_API` — class for getting friends from vk.com:
    * `get_friends(user_id)` returns friend list of user with `user_id`
* `Twitter_API` — class for getting friends from twitter.com:
    * `get_friends(user_id)` returns friend list of user with `user_id`
* `CSV_Generator` — class for generating CSV-data
### friends.py
Describes classes for handling friend info.
* Friend — general friend class
    * `__init__(**kwargs)` — accepts userdata as `**kwargs` dict
    * `merge(other)` — merges `self` and `other` or raises `ValueError`
    * `is_mergeble(other)` — checks if it is possible to merge `self` and `other` automatically
    * `is_similar(other)` — checks if `self` and `other` look similar (may be need to be merged)
* VK_Friend(Friend) — vk friend class inherited from `Friend`.
    * `__init__(**kwargs)` — accepts data in format of VK API.
* Twitter_Friend(Friend) — twitter friend class inherited from `Friend`.
    * `__init__(**kwargs)` — accepts data in format of Twitter API.
### address_book.py
Describes AddressBook main class (implementation should be inherited from this one).
* `AddressBook` — main class
    * `_wrong_id()` — abstract method, describes program behavior if either twitter or vk id is wrong
    * `save_CSV(filename=None)` — abstract method, saves result CSV file
    * `get_friends()` — abstract method, gets user id and returns friend list
    * `_merge_friends(friend1, friend2)` — abstract method, returns Friend object, merged from `friend1`  and `friend2`
    * `merge_friend_list()` — abstract method, merges all friends in self friend list
    * `_merge_friend_lists(friends, set_percentage=None)` — merges friends in `friends` list. Calls `set_percentage(percentage)` on each step.
