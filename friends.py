from utils import (extract_phone, extract_date, equal,
                   extract_name_parts, absolutely_equal, Twitter_API)

MINIMUM_SIMILARITY = 0.80


class Friend:
    _fields = (
        ('full_name', (0.5, equal)), ('first_name', (0.03, equal)),
        ('last_name', (0.12, equal)), ('bdate', (0.2, absolutely_equal)),
        ('phone', (0.15, absolutely_equal)),
        ('site', (0, absolutely_equal)),
        ('nickname', (0, absolutely_equal)),
        ('city', (0, absolutely_equal)),
    )
    _field_dict = dict(_fields)

    def __init__(self, **kwargs):
        for field in self._field_dict:
            setattr(self, field, kwargs.get(field, ''))

    def __repr__(self):
        return '<Frined object: {}>'.format(self.full_name)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return ';\n'.join('{} is {}'.format(
            key.replace('_', ' ').title(),
            val
        ) for key, val in vars(self).items())

    @staticmethod
    def _fields_equal(val1, val2, eq_function):
        if val1 == '' or val2 == '' or val1 == [] or val2 == []:
            return 1
        return eq_function(val1, val2)

    def merge(self, other):
        if not self.is_mergeble(other):
            raise ValueError
        result = Friend(**vars(self))
        for attr in vars(self):
            setattr(result, attr, getattr(
                other if getattr(self, attr) == '' else self, attr))
        return result

    def is_mergeble(self, other):
        return self.is_subset(other) or other.is_subset(self)

    def is_similar(self, other):
        similarity = 0
        for key, value in self._field_dict.items():
            coef, eq = value
            similarity += coef * (self._fields_equal(getattr(self, key),
                                                     getattr(other, key), eq))
        return similarity >= MINIMUM_SIMILARITY

    def is_subset(self, other):
        for field in vars(self):
            if getattr(other, field) != '' and \
               getattr(self, field) != getattr(other, field):
                return False
        return True


class VK_Friend(Friend):
    def __init__(self, **kwargs):
        user_data = {
            'full_name': '{} {}'.format(
                kwargs.get('last_name', ''), kwargs.get('first_name', '')
            ),
            'first_name': kwargs.get('first_name', ''),
            'last_name': kwargs.get('last_name', ''),
            'bdate': extract_date(kwargs.get('bdate', '')),
            'phone': extract_phone(kwargs.get('home_phone', '')),
            'nickname': kwargs.get('nickname', ''),
            'site': kwargs.get('site', ''),
        }
        super().__init__(**user_data)


class Twitter_Friend(Friend):
    def __init__(self, grab_friends=False, **kwargs):
        api = Twitter_API()
        user_data = {
            'first_name': extract_name_parts(
                kwargs.get('name', ''))[0],
            'last_name': extract_name_parts(
                kwargs.get('name', ''))[1],
            'friends': api.get_friends(
                kwargs.get('id', ''),
            ) if grab_friends else []
        }
        user_data['full_name'] = '{} {}'.format(
            user_data.get('last_name', ''),
            user_data.get('first_name', '')
        )
        super().__init__(**user_data)
