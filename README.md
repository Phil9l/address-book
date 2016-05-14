# Address Book
## Description
Downloads data about friends from social networks (vk.com and twitter) and makes CSV file for exporting into google contacts.

## Usage
`./address_book_console.py --vk VK_ID --twitter Twitter_ID [--output FILE]`

### Example
`./address_book_console.py --vk 44232785 --twitter 891227432`

### Options
* `-v VK_ID` — id of user, whose friends would be imported
* `-o FILE` — name of CSV file

## Requirements
* `pip3 install Twitter_API`

