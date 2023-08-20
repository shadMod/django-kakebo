def find_indices(list_obj: list, __value):
    return [obj for obj, value in enumerate(list_obj) if value == __value]
