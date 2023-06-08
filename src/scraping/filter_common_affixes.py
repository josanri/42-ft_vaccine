import os


def common_suffix(strings: list) -> str:
    suffix = strings[0]
    for next_string in strings[1:]:
        while not next_string.endswith(suffix):
            suffix = suffix[1:]
    return suffix


def filter_common_affixes(names: list) -> list:
    prefix = os.path.commonprefix(names)
    if prefix:
        names = [name.replace(prefix, '') for name in names]
    suffix = common_suffix(names)
    if suffix:
        names = [name.replace(suffix, '') for name in names]
    return names
