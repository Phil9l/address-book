import abc
from utils import CSV_Generator


class AddressBook(object):
    def __init__(self):
        pass

    @abc.abstractmethod
    def _wrong_id(self):
        return

    @abc.abstractmethod
    def save_CSV(self, filename=None):
        return

    @abc.abstractmethod
    def get_friends(self):
        return

    @abc.abstractmethod
    def _merge_friends(self, friend1, friend2):
        return

    @abc.abstractmethod
    def merge_friend_list(self):
        return

    def _merge_friend_lists(self, friends, set_percentage=None,
                            is_stopped=None):
        result = []
        init_friends_num = len(friends)

        while friends:
            if is_stopped is not None and is_stopped():
                break
            if set_percentage is not None:
                set_percentage((init_friends_num - len(friends)) * 100 /
                               init_friends_num)
            cur_friend = friends.pop(0)
            is_unique = True
            for friend_index in range(len(friends)):
                other_friend = friends[friend_index]
                if cur_friend.is_mergeble(other_friend):
                    friends[friend_index] = cur_friend.merge(other_friend)
                    is_unique = False
                    continue

                if not cur_friend.is_similar(other_friend):
                    continue

                merge_result = self._merge_friends(cur_friend, other_friend)
                if merge_result is None:
                    continue

                friends[friend_index] = merge_result
                is_unique = False
                break
            if is_unique:
                result.append(cur_friend)
        return result

    def _get_friends(self, user_id, api, friend_class):
        try:
            friend_list = [friend_class(**friend)
                           for friend in api.get_friends(user_id)]
            return friend_list
        except ValueError:
            self._wrong_id()

    @staticmethod
    def _generate_CSV(csv_fields, friend_list):
        csv_file = CSV_Generator(csv_fields)
        csv_file.set_titles(**csv_fields)
        for friend in friend_list:
            csv_file.add_values(**vars(friend))
        return str(csv_file)
