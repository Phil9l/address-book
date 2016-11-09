from urllib import request
from json import loads
from datetime import datetime
from TwitterAPI import TwitterAPI


def translit(string):
    '''Translitiration based on Passport (2013), ICAO standart'''
    return string


def distance(a, b):
    '''Calculates the Levenshtein distance between a and b.'''
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = (previous_row[j] + 1, current_row[j - 1] + 1,
                                   previous_row[j - 1])
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


def extract_name_parts(full_name):
    res = full_name.split(' ', 1)
    if len(res) == 1:
        res.append('')
    return res[0], res[1]


def extract_phone(input_string):
    phone_number = ''.join(filter(lambda char: char.isdigit(), input_string))
    return phone_number if len(phone_number) > 4 else ''


def extract_date(input_string):
    try:
        return datetime.strptime(input_string, "%d.%m.%Y").date()
    except ValueError:
        return ''


def normalize_name(input_string):
    return translit(input_string.strip()).title()


def get_input(question, choice=('y', 'n')):
    result = ''
    while result not in choice:
        result = input('{} [{}] '.format(question, '/'.join(choice)))
    return result


def equal(val1, val2):
    if isinstance(val1, str) and isinstance(val2, str):
        return 1 - (distance(val1, val2) / max(len(val1), len(val2)))**(3/5)
    return val1 == val2


def absolutely_equal(val1, val2):
    return val1 == val2


class VK_API:
    API_URL = (
        'https://api.vk.com/method/'
        '{method}?{params}&lang=ru&access_token={token}'
    )

    def __init__(self):
        self.token = ''

    def _get_request_url(self, method, params, token=''):
        params_string = '&'.join((
            '{}={}'.format(*param) for param in params.items()
        ))
        return self.API_URL.format(
            method=method, params=params_string, token=''
        )

    def _send_request(self, method, params, token=''):
        url = self._get_request_url(method, params, token)
        result = loads(request.urlopen(url).read().decode("utf-8"))
        if 'response' in result:
            return result['response']
        raise ValueError

    def get_friends(self, user_id):
        friends = self._send_request('friends.get', {
            'user_id': user_id,
            'fields': 'first_name,second_name,phone,bdate,contacts'
        })
        return friends


class Twitter_API:
    KEY = 'piI38iQP1BzX83FdWC0IAKT1O'
    SECRET = 'jyWtLZvXrjPEfNBrGyQNiOpDIENluoIRceSBSoV0RvmwWlOkdz'

    def __init__(self):
        self.api = TwitterAPI(self.KEY, self.SECRET, auth_type='oAuth2')

    def get_friends(self, user_id):
        req = self.api.request('friends/list', {
            'user_id': user_id, 'count': 200
        })
        return list(req)


class CSV_Generator:
    def __init__(self, field_names):
        self.fields = field_names
        self.titles = dict.fromkeys(field_names, '')
        self.values = []

    def __str__(self):
        return '{}\n{}\n'.format(self.get_title_string(),
                                 '\n'.join(self._get_values()))

    def set_titles(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.titles:
                self.titles[key] = str(value)

    def add_values(self, **kwargs):
        self.values.append(dict.fromkeys(self.fields, ''))
        for key, value in kwargs.items():
            if key in self.values[-1]:
                self.values[-1][key] = value

    def _get_result_fields(self):
        return self.fields

    def get_title_string(self):
        return ','.join([str(self.titles[field]) for field in sorted(
            self._get_result_fields())])

    def _get_values(self):
        for value in self.values:
            yield ','.join([str(value[field]) for field in sorted(
                self._get_result_fields())])
