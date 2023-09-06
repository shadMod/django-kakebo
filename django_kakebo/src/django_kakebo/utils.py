from django.conf import settings


def find_indices(list_obj: list, __value):
    return [obj for obj, value in enumerate(list_obj) if value == __value]


class KeyKakebo:
    field_list = ["username", "month", "year"]

    def __init__(self):
        self.kwargs = None
        self.request = None

    @property
    def get_key_kakebo(self) -> str:
        field_user = getattr(settings, "USER_FIELD_KAKEBO", self.field_list[0])
        username = getattr(self.request.user, field_user)
        return f'{username}-{self.kwargs[self.field_list[1]]}-{self.kwargs[self.field_list[2]]}'
