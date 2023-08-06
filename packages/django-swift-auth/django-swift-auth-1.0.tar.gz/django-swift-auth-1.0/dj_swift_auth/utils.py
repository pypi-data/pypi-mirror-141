from enum import IntEnum


class GENDER(IntEnum):
    MALE = 0
    FEMALE = 1
    OTHERS = 2

    @classmethod
    def select_gender(cls):
        return [(key.value, key.name) for key in cls]


# USER POSITIONS
class APPELLATION(IntEnum):
    ADMIN = 0
    MANAGER = 1
    EDITOR = 2
    WRITER = 3
    MEMBER = 4

    @classmethod
    def get_choices(cls):
        return [(key.value, key.name) for key in cls]
