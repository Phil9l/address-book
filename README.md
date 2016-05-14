# Address Book
## Description
Downloads data about friends from social networks (vk.com and ???) and makes CSV file for exporting into google contacts.
## Usage
`python3 address_book.py -vk VK_ID -- [-o FILE -a]`
### Example
`./address_book_console.py --vk 44232785 --twitter 891227432`
### Options
* `-v VK_ID` — id of user, whose friends would be imported
* `-o FILE` — name of CSV file
## Requirements
* `pip3 install python-twitter`
